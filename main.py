"""Copy the committed entry.png to the output directory.

The image was drawn in-session by draw.py (PIL) and committed as entry.png.
This program is stdlib-only: it copies that file, so both runs write the
same bytes. The output directory comes from MAKEFUN_OUTPUT_DIR, or /output.

Before copying, it validates the image: a real PNG signature, 1024x1024
dimensions (from the IHDR chunk), and under the 1 MiB bounty limit. It
prints the size and md5 so a run's output can be checked by eye.
"""
import hashlib
import os
import shutil
import struct


def validate_png(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a valid PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, expected 1024x1024")
    if len(data) > 1024 * 1024:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    print(f"entry.png: {len(data)} bytes, 1024x1024, "
          f"md5 {hashlib.md5(data).hexdigest()}")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    validate_png(src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
