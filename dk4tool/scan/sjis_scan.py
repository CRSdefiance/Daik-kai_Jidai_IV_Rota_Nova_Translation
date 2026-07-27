from __future__ import annotations

from dataclasses import asdict, dataclass


def contains_japanese(text: str) -> bool:
    return any(
        "\u3040" <= char <= "\u30ff" or "\u3400" <= char <= "\u9fff" for char in text
    )


@dataclass(frozen=True)
class TextHit:
    offset: int
    length: int
    decoded: str
    score: float
    terminator: str | None
    context_before_hex: str
    context_after_hex: str
    encoding: str = "shift_jis"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _score(text: str, terminated: bool) -> float:
    japanese = sum(
        "\u3040" <= char <= "\u30ff" or "\u3400" <= char <= "\u9fff" for char in text
    )
    ratio = japanese / max(len(text), 1)
    return round(min(1.0, 0.45 + ratio * 0.45 + (0.1 if terminated else 0.0)), 3)


def scan_sjis(data: bytes, min_chars: int = 4, aggressive: bool = False) -> list[TextHit]:
    """Find non-overlapping CP932 runs containing Japanese characters.

    Runs are bounded by common binary control bytes. Strict decoding prevents replacement
    characters from being mistaken for text.
    """
    hits: list[TextHit] = []
    start = 0
    minimum = 2 if aggressive else min_chars
    while start < len(data):
        while start < len(data) and (data[start] < 0x20 or data[start] == 0x7F):
            start += 1
        end = start
        while end < len(data) and data[end] >= 0x20 and data[end] != 0x7F:
            end += 1
        if end > start:
            raw = data[start:end]
            try:
                decoded = raw.decode("cp932")
            except UnicodeDecodeError:
                decoded = ""
            if len(decoded) >= minimum and contains_japanese(decoded):
                terminated = end < len(data) and data[end] == 0
                hits.append(
                    TextHit(
                        offset=start,
                        length=len(raw),
                        decoded=decoded,
                        score=_score(decoded, terminated),
                        terminator="00" if terminated else None,
                        context_before_hex=data[max(0, start - 8) : start].hex().upper(),
                        context_after_hex=data[end : min(len(data), end + 8)].hex().upper(),
                    )
                )
        start = max(end + 1, start + 1)
    return hits

