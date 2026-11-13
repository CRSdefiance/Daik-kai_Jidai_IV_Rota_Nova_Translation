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
    # V782: exact2661 selections1007-3667;50 complete shared paragraphs.
    "c24544e754a2c1b381e64895f56fa646affd414dbcf555bb6fe938ee860a9e0b",
    # V780: exact2336 selections933-3268;31 complete barmaid paragraphs.
    "aae0dd8240e52e3de1ec94a6f3da5d6fef324714c15e6290a5fcf09ccc64439c",
    # V778: exact2697 selections164-2860;25 follow-up paragraphs.
    "e63495c202bc60958373a51d59df4036605b49fc485cf8a82f530ad3b90f292f",
    # V776: exact2697 selections164-2860;56 complete scheme paragraphs.
    "b4dff11ec2c855458be38255d11ff5b387be7431e6d609f78e25378861c0cf74",
    # V773: exact2151 selections164-2314;25 recruitment/condition entries.
    "504e4dfdd30fff39be5393bc43ad029092659d2ea4a43ff2f89962e7b63c6bb9",
    # V770: exact2151 selections164-2314;32 Tavern continuation entries.
    "ba196ea167c33feb8d2b7341024b2c8befa7bf7e640413505810efec24097b27",
    # V767: exact1813 selections164-1976;two opaque copy spans preserved.
    "df162ac3e064871eaaf2defdabbbbe81e39ff00f56547d028f5bdecf17015cc8",
    # V762: exact1549 selections164-1712;18 reviewed Port/service replies.
    "fe3af5a3a2b97e32d5980786b825e33686fffd3906f59fdb364bf7c4bf39f5a0",
    # V760: exact1549 complete selections164-1712 in existing blocks2-18.
    # Every unselected text byte and packed payload block remains preserved.
    "7e2fc3325ac41442354ecb8547c6cf85a74bd14d05bd19ff39ec93d18c78cfd5",
    # V758: exact1369 complete selections344-1712 in blocks5-18.
    "daa82ab9ba0f0df082939785923c98279cc546dce2b5faa2edfc5825fe2c9a47",
    # V756 Market stock/letters: exact946 complete selections in blocks10-18.
    # Every unselected visible byte and every other block remains unchanged.
    "9cde16387f9932ad0d566212537b6387f502c4dd6e6005308427f1708dfe825c",
    # V753 Market reply whole-selection map across blocks7-10. No arbitrary
    # directory bypass: exact310-message map and complete native copy checks.
    "f57f08bd6869b3927d8e6be154f6d9eb90147f7b28e97c4afc3bebc32aa40e25",
    # V708 adds Cabin recovery1247 to the complete31-help family. All7336
    # warm/cold native copies pass; all3637 other message text bytes stay exact.
    "3d4d4ef8d37f87916522193b53bd4027d3d53ea11a3d1b5400b882e797c77555",
    # V707: exact three-block Refit help map. All3668 original native warm/cold
    # copies pass; all3638 unselected text byte strings and allocator stay exact.
    "99bbbb79a856466f52e89081c0bdf70189b3209bf7b041eae5b0f9f4d16a3d72",
    # V276 six-message name migration: all3668 selections and18 native copies
    # proved; V299 replays the identical COMMON bytes/directory on V298.
    "65c9b7ebe64615e5ab83a3ba06b344954fb492b5fc03e8a95118664882fa0b2c",
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
