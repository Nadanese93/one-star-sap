"""One Star, Written in Sap — Make.fun entry.

Writes a single one-line 1-star review, in the voice of a houseplant,
about its human owner, to $MAKEFUN_OUTPUT_DIR/entry.txt.
"""

import os
import tempfile

ENTRY = (
    "One star. He waters me with his leftover cold coffee, so now I'm "
    "jittery, wide awake at 3 a.m., and still somehow dying of thirst."
)


def main() -> None:
    if not ENTRY.strip():
        raise ValueError("entry fails the gate: entry is blank or whitespace-only")
    if not 1 <= len(ENTRY) <= 279:
        raise ValueError(
            f"entry fails the gate: {len(ENTRY)} chars, must be 1-279"
        )
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("entry fails the gate: entry must be a single line")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    with open(target, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise IOError("read-back verification failed: entry.txt bytes differ")


if __name__ == "__main__":
    main()
