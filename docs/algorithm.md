# Implementation notes

MD5 reads sixteen little-endian words from each 64-byte block. Each of
the four rounds selects its own Boolean function, word order and rotations.
Python integers do not overflow, so additions and rotations must explicitly
retain the low 32 bits.

Padding starts with 0x80. Zero bytes bring the length to 56 modulo 64, then the
original bit length is appended as a little-endian 64-bit integer. The modulo
operation matters at lengths 56 through 63: those inputs need an extra block.
The digest consists of four little-endian state words.

The streaming object retains only the chaining state, total byte count and
at most 63 trailing bytes between updates. Finalization operates on a copy.
The format stores the bit length modulo 2**64, as described in RFC 1321.
