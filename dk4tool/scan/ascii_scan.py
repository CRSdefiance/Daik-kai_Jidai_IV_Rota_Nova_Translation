from __future__ import annotations

import re
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AsciiHit:
    offset: int
    length: int
    decoded: str
    encoding: str = "ascii"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def scan_ascii(data: bytes, min_chars: int = 4) -> list[AsciiHit]:
    pattern = re.compile(rb"[\x20-\x7E]{%d,}" % min_chars)
    return [
        AsciiHit(match.start(), len(match.group()), match.group().decode("ascii"))
        for match in pattern.finditer(data)
    ]

