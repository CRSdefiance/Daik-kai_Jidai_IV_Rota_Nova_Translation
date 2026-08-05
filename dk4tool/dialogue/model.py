from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DialogueToken:
    """One lossless unit in a standard-dialogue byte stream."""

    kind: str
    value: str
    raw: bytes

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "value": self.value, "raw_hex": self.raw.hex().upper()}
