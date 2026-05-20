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


def digest(data):
    data = bytes(data)
    size = len(data)
    zeros = (55 - size) % 64
    padded = data + b'\x80' + b'\x00' * zeros + struct.pack('<Q', size * 8)
    state = list(_IV)
    for offset in range(0, len(padded), 64):
        state = _compress(state, padded[offset:offset + 64])
    return struct.pack('<4I', *state)


def hexdigest(data):
    return digest(data).hex()
