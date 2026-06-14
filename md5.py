"""A byte-oriented MD5 implementation of RFC 1321.

The compression function is implemented here, not delegated to hashlib.
"""

import struct

_MASK = 0xFFFFFFFF
_IV = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)
_SHIFTS = (
    (7, 12, 17, 22) * 4 + (5, 9, 14, 20) * 4
    + (4, 11, 16, 23) * 4 + (6, 10, 15, 21) * 4
)
_K = (
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
)


def _rol(word, shift):
    word &= _MASK
    return ((word << shift) | (word >> (32 - shift))) & _MASK


def _compress(state, block):
    words = struct.unpack('<16I', block)
    a, b, c, d = state
    for step in range(64):
        if step < 16:
            function, index = (b & c) | (~b & d), step
        elif step < 32:
            function, index = (d & b) | (~d & c), (5 * step + 1) % 16
        elif step < 48:
            function, index = b ^ c ^ d, (3 * step + 5) % 16
        else:
            function, index = c ^ (b | ~d), (7 * step) % 16
        mixed = a + function + _K[step] + words[index]
        a, d, c, b = d, c, b, (b + _rol(mixed, _SHIFTS[step])) & _MASK
    return [(old + new) & _MASK for old, new in zip(state, (a, b, c, d))]


class MD5:
    """Incremental hash: update(), digest(), hexdigest(), and independent copy()."""

    name = 'md5'
    block_size = 64
    digest_size = 16

    def __init__(self, data=b''):
        self._state = list(_IV)
        self._buffer = b''
        self._count = 0
        self.update(data)

    def update(self, data):
        """Consume bytes, bytearray or memoryview; text needs explicit encoding."""
        data = bytes(data)
        self._count += len(data)
        data = self._buffer + data
        end = len(data) - len(data) % self.block_size
        for offset in range(0, end, self.block_size):
            self._state = _compress(self._state, data[offset:offset + self.block_size])
        self._buffer = data[end:]

    def copy(self):
        clone = object.__new__(type(self))
        clone._state = self._state.copy()
        clone._buffer = self._buffer
        clone._count = self._count
        return clone

    def digest(self):
        """Return 16 bytes without changing this object; further updates work."""
        clone = self.copy()
        padding = b'\x80' + b'\x00' * ((55 - self._count) % 64)
        length = struct.pack('<Q', (self._count * 8) & 0xFFFFFFFFFFFFFFFF)
        clone.update(padding + length)
        return struct.pack('<4I', *clone._state)

    def hexdigest(self):
        return self.digest().hex()


def md5(data=b''):
    return MD5(data)


def digest(data):
    """One-shot byte digest, retained from the original API."""
    return MD5(data).digest()


def hexdigest(data):
    return digest(data).hex()


def main(argv=None):
    """Print checksums for binary files, or stdin when no file is given."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', help='Files to hash; - reads stdin')
    args = parser.parse_args(argv)
    failed = False
    for filename in args.files or ['-']:
        try:
            value = MD5()
            if filename == '-':
                for chunk in iter(lambda: sys.stdin.buffer.read(65536), b''):
                    value.update(chunk)
            else:
                with open(filename, 'rb') as stream:
                    for chunk in iter(lambda: stream.read(65536), b''):
                        value.update(chunk)
            print(f'{value.hexdigest()}  {filename}')
        except OSError as error:
            print(f'md5: {filename}: {error.strerror}', file=sys.stderr)
            failed = True
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
