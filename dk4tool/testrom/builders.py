from __future__ import annotations

from dk4tool.scan.compression_probe import compress_lz10_literals


def japanese_text_blob() -> bytes:
    return b"\x01\x02" + "出航しますか？".encode("cp932") + b"\0\x03"


def lz10_japanese_blob() -> bytes:
    return compress_lz10_literals(japanese_text_blob())

