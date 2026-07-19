# md5

I wanted to work through MD5 without hiding the compression step behind
`hashlib`. This is the result: one Python file, including a small checksum CLI.
Useful for reading the algorithm and checking old file digests. MD5 is broken
for collision resistance; don't use it for new signatures or passwords.

Python 3.10+, standard library only. No installation needed:

```sh
printf abc | python3 md5.py
# 900150983cd24fb0d6963f7d28e17f72  -
python3 md5.py README.md
```

From the same directory:

```python
from md5 import MD5, hexdigest

assert hexdigest(b"abc") == "900150983cd24fb0d6963f7d28e17f72"
h = MD5(b"a")
h.update(b"bc")
print(h.hexdigest())
```

`digest(data)` returns 16 raw bytes; `md5(data)` is a shorthand for `MD5(data)`.
The object also has `copy()`. Reading a digest doesn't consume the state, so
you can keep adding data afterwards. Inputs are bytes, bytearray or memoryview;
encode strings yourself. `update()` returns `None`.

The CLI accepts several filenames and `-` for stdin. It keeps going after a
missing file and exits with status 1 if any file failed. It doesn't read checksum
lists (`md5sum -c` is outside the scope of this script).

Optional: `python3 -m pip install .` adds the `md5-py` command.
Padding and word-order notes are in [docs/algorithm.md](docs/algorithm.md).
