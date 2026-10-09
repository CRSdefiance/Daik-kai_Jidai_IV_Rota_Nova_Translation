"""COMMON global message boundaries proven by the ARM9 message loader."""
from __future__ import annotations

import struct
from dataclasses import dataclass
from hashlib import sha256

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_entry_tables import CLEAN_COMMON_SHA256

DIRECTORY_OFFSET = 0x14186C
TABLE_OFFSET = 0x141910
MESSAGE_COUNT = 3668
TABLE_END = 0x1435BA
DIRECTORY_HASH = "774d5730d2b39844f55a0ecebb3eaf2575150adf524e33f9a93b6486a03898b6"
TABLE_HASH = "305f075a25a7476b0099895bbb21e6fdea6f56e7f0ae24ec5b80aead8bafc1c8"
# Exact whole-record map verified against all 3,668 messages. Clean mode
# continues to require the original directory. No arbitrary directory bypass.
RELOCATED_DIRECTORY_HASHES = frozenset({
    "b12f4aa9d84cdf9e3fbf40bf49ca175c2fe98ce2ec5f4fc9161622cb28e566a3",
    "e00046fc75fe92f69ec5f484efe5307e6275cca9276def974bb15aeddddd5ee5",
    "e44ff559788ea5e72feccc219aa74b4d764d880b8074d433d05c12077b691042",
    "8b6d75ad611d4158fddd80af1e8c83a3113a3005d777c0b52df9a8fc87a38184",
    "434050668966812204dd657e9b22e6fccfbbd9d33744be0cbc31479e669b5750",
    "2d49bf06c24eebb1f22f3e59d7ca8adf60f45ba0638bc3987d43971feabd326a",
    "c7735c4532192e4b274ac5e6f9d510ee1515c3d490edb8502265fb1a6474dd78",
    "d878a6c87827099e490ddc72a115efe69f1eef1983660be285a68f8032abafeb",
    "a0124b582150fcedd91da12cae0d7fd61bcb6959e6ad5fa830173dbca29c4f45",
    "62032b4da461fdc31fe4ae67c476b33a5f5c48a218666da3ee3aada77356f0b3",
    "218e40c7e4b7859c71415002695c8a50e24ec43e2ba5ac0134059416cf52b0b4",
    "84337bd2b161b7ef886d68209849f1fa5f2c7ff7f215e5857952f68e5e030305",
    "bc904d394a86e2573d02b115033416556c26841d249456dc843800bcbb114c86",
})
CODE_LOCKS = (
    (0x534F4, 0x535E0, "b5ea4399280057428c40d78ebcf959597a94278304df6135d95355cc8355e724"),
    (0x53628, 0x53660, "c77430052d65fc5e6eb998c8d87cb0ebb6aaf12d4298280812508effc87ffb91"),
)


@dataclass(frozen=True)
class CommonMessageEntry:
    message_id: int
    block: int
    table_offset: int
    block_offset: int
    copy_end: int
    record_index: int
    start: int
    end: int
    text: bytes


def common_message_entries(common: bytes, arm9: bytes, *, clean: bool = True) -> list[CommonMessageEntry]:
    """Read clean or current native offsets without substituting guessed starts.

    Current mode retains the verified directory and executable loader, but reads
    the candidate's own offset table (accepted BGM entries were repacked).
    The visible span stops at NUL; copy_end retains the engine's full copy span.
    """
    locks = list(CODE_LOCKS)
    directory_hash = sha256(arm9[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    allowed_directories = {DIRECTORY_HASH} if clean else {DIRECTORY_HASH, *RELOCATED_DIRECTORY_HASHES}
    if directory_hash not in allowed_directories:
        raise ValueError(f"COMMON loader/table evidence mismatch at {DIRECTORY_OFFSET:#x}")
    if clean:
        locks.append((TABLE_OFFSET, TABLE_END, TABLE_HASH))
        if sha256(common).hexdigest() != CLEAN_COMMON_SHA256:
            raise ValueError("COMMON source hash does not match the verified clean image")
    for lo, hi, expected in locks:
        if sha256(arm9[lo:hi]).hexdigest() != expected:
            raise ValueError(f"COMMON loader/table evidence mismatch at {lo:#x}")
    blocks = IlnkContainer.parse(common).blocks
    if len(blocks) != 41:
        raise ValueError("COMMON requires exactly 41 native blocks")
    directory = [struct.unpack_from("<HH", arm9, DIRECTORY_OFFSET + i * 4) for i in range(41)]
    first_ids = [row[0] for row in directory]
    if first_ids[0] != 0 or first_ids != sorted(set(first_ids)) or first_ids[-1] >= MESSAGE_COUNT:
        raise ValueError("Invalid COMMON global message directory")
    offsets = struct.unpack_from(f"<{MESSAGE_COUNT + 1}H", arm9, TABLE_OFFSET)
    if offsets[-1] != 0:
        raise ValueError("COMMON final message sentinel changed")
    entries = []
    for block_index, (first, size) in enumerate(directory):
        block = blocks[block_index]
        if len(block) != size or size > 4096:
            raise ValueError(f"COMMON B{block_index}: native cache size mismatch")
        last = first_ids[block_index + 1] if block_index < 40 else MESSAGE_COUNT
        starts = offsets[first:last]
        if starts != tuple(sorted(set(starts))):
            raise ValueError(f"COMMON B{block_index}: native starts are not strictly increasing")
        records = []
        position = 0
        for index, raw in enumerate(block.split(b"\0")):
            if raw:
                records.append((index, position, position + len(raw)))
            position += len(raw) + 1
        for message_id in range(first, last):
            start, following = offsets[message_id:message_id + 2]
            copy_end = following if following >= start else size
            owners = [(index, lo, hi) for index, lo, hi in records if lo <= start < hi]
            if (clean and start % 2) or not start < copy_end <= size or len(owners) != 1:
                raise ValueError(f"COMMON message {message_id}: invalid native copy span")
            record, lo, hi = owners[0]
            end = min(copy_end, hi)
            text = block[start:end]
            text.decode("cp932")
            entries.append(CommonMessageEntry(message_id, block_index, TABLE_OFFSET + message_id * 2,
                                              start, copy_end, record, start - lo, end - lo, text))
    return entries
