from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise


class IlnkError(ValueError):
    pass


@dataclass
class IlnkContainer:
    blocks: list[bytes]

    @classmethod
    def parse(cls, data: bytes) -> IlnkContainer:
        if len(data) < 12 or data[:4] != b"ILNK":
            raise IlnkError("not an ILNK container")
        count = int.from_bytes(data[4:8], "little")
        header_size = 8 + (count + 1) * 4
        if count <= 0 or header_size > len(data):
            raise IlnkError("invalid ILNK block count")
        offsets = [
            int.from_bytes(data[8 + index * 4 : 12 + index * 4], "little")
            for index in range(count + 1)
        ]
        if offsets[0] != header_size:
            raise IlnkError(
                f"ILNK first block starts at 0x{offsets[0]:X}; expected 0x{header_size:X}"
            )
        if offsets[-1] != len(data):
            raise IlnkError(
                f"ILNK end offset is 0x{offsets[-1]:X}; file size is 0x{len(data):X}"
            )
        if any(left > right for left, right in pairwise(offsets)):
            raise IlnkError("ILNK offsets are not monotonic")
        return cls([data[offsets[index] : offsets[index + 1]] for index in range(count)])

    def to_bytes(self) -> bytes:
        header_size = 8 + (len(self.blocks) + 1) * 4
        offsets = [header_size]
        for block in self.blocks:
            offsets.append(offsets[-1] + len(block))
        header = bytearray(b"ILNK" + len(self.blocks).to_bytes(4, "little"))
        for offset in offsets:
            header.extend(offset.to_bytes(4, "little"))
        return bytes(header) + b"".join(self.blocks)
