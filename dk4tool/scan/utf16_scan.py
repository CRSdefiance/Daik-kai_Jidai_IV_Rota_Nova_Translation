from __future__ import annotations

from dataclasses import asdict, dataclass

from .sjis_scan import contains_japanese


@dataclass(frozen=True)
class Utf16Hit:
    offset: int
    length: int
    decoded: str
    score: float
    terminator: str | None
    encoding: str = "utf-16le"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def scan_utf16le(data: bytes, min_chars: int = 4, aggressive: bool = False) -> list[Utf16Hit]:
    hits: list[Utf16Hit] = []
    minimum = 2 if aggressive else min_chars
    for alignment in (0, 1):
        start = alignment
        while start + 1 < len(data):
            first = int.from_bytes(data[start : start + 2], "little")
            if not contains_japanese(chr(first)):
                start += 2
                continue
            end = start
            while end + 1 < len(data) and data[end : end + 2] not in (b"\0\0",):
                end += 2
            raw = data[start:end]
            if raw:
                try:
                    decoded = raw.decode("utf-16le")
                except UnicodeDecodeError:
                    decoded = ""
                if len(decoded) >= minimum and contains_japanese(decoded):
                    hits.append(
                        Utf16Hit(
                            start,
                            len(raw),
                            decoded,
                            0.9 if end + 1 < len(data) else 0.8,
                            "0000" if end + 1 < len(data) else None,
                        )
                    )
            start = max(end + 2, start + 2)
    unique = {(hit.offset, hit.length, hit.decoded): hit for hit in hits}
    return sorted(unique.values(), key=lambda hit: (hit.offset, hit.length))
