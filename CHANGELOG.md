# Changes

## 0.2.0 — 2026-07-19

- Added the incremental `MD5` object and `copy()`.
- Fixed `digest()` consuming the buffered input. Calling it twice now works.
- File arguments and binary stdin, plus an installable `md5-py` command.
- Reject integers instead of silently treating them as a count of zero bytes.

## 0.1.0 — 2026-05-20

First usable one-shot version. Includes the fix for messages with 56–63 bytes
left over: the length field needs another block there.
