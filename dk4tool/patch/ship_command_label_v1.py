"""Localize the exact raw Assign Sailors command without touching its menu code."""

import struct

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_goods_info_terminator_v1 import FIELDS as MARKET_FIELDS
from dk4tool.patch.market_goods_info_terminator_v1 import NEW_FORMAT, PAYLOAD as MARKET_PAYLOAD


BASE = 0x02000000
SOURCE_ARM_SHA256 = 'dae19a97e1496d4a698c0b06161006dec7f4fe0123192a3129da795e6682d797'
TABLE = 0x1150B0
FIELD = TABLE + 4
OLD_OFFSET = 0x134E54
OLD_POINTER = BASE + OLD_OFFSET
OLD_TEXT = '船を捨てる'.encode('cp932') + b'\0'
NEW_POINTER = NEW_FORMAT + len(MARKET_PAYLOAD)
TEXT = b'Abandon Ship\0'
ALLOCATION = TEXT + bytes(-len(TEXT) % 4)


def transform(source):
    if sha(source) != SOURCE_ARM_SHA256:
        raise ValueError('Exact registered Lil261 ARM9 required')
    code = MainCodeFile(source, BASE)
    if bytes(code.save()) != source:
        raise ValueError('Predecessor ARM9 serialization differs')
    section = code.sections[-1]
    if (len(code.sections), section.ramAddress, bytes(section.data), section.bssSize) != (
            6, NEW_FORMAT, MARKET_PAYLOAD, 0):
        raise ValueError('Expected exact registered read-only Market literal section')
    if any(struct.unpack_from('<I', source, field)[0] != NEW_FORMAT for field in MARKET_FIELDS):
        raise ValueError('Market pointers differ')
    if source[OLD_OFFSET:OLD_OFFSET + len(OLD_TEXT)] != OLD_TEXT:
        raise ValueError('Clean-matched raw ship label differs')
    if [i for i in range(0, len(source) - 3, 4) if source[i:i + 4] == struct.pack('<I', OLD_POINTER)] != [FIELD]:
        raise ValueError('Expected one owned aligned menu pointer')
    if any(not (s.ramAddress + len(s.data) + s.bssSize <= NEW_POINTER
                or NEW_POINTER + len(ALLOCATION) <= s.ramAddress) for s in code.sections):
        raise ValueError('Declared label allocation overlaps existing section or BSS')
    if NEW_POINTER + len(ALLOCATION) > BASE:
        raise ValueError('Label exceeds the initialized ITCM address range')

    struct.pack_into('<I', code.sections[0].data, FIELD, NEW_POINTER)
    section.data.extend(ALLOCATION)
    target = bytes(code.save())
    parsed = MainCodeFile(target, BASE)
    literal = parsed.sections[-1]
    if (len(parsed.sections), literal.ramAddress, bytes(literal.data), literal.bssSize) != (
            6, NEW_FORMAT, MARKET_PAYLOAD + ALLOCATION, 0):
        raise ValueError('Serialized literal allocation differs')
    if any(struct.unpack_from('<I', target, field)[0] != NEW_FORMAT for field in MARKET_FIELDS):
        raise ValueError('Market pointer changed')
    if target[OLD_OFFSET:OLD_OFFSET + len(OLD_TEXT)] != OLD_TEXT:
        raise ValueError('Original label storage changed')

    struct.pack_into('<I', parsed.sections[0].data, FIELD, OLD_POINTER)
    del literal.data[len(MARKET_PAYLOAD):]
    if bytes(parsed.save()) != source:
        raise ValueError('Complete predecessor ARM9 inverse failed')
    return target, dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        pointer_field=FIELD, original_pointer=OLD_POINTER, target_pointer=NEW_POINTER,
        source_terminated_hex=OLD_TEXT.hex(), target_terminated_hex=TEXT.hex(),
        appended_readonly_allocation_hex=ALLOCATION.hex(), preserved_market_literal_address=NEW_FORMAT,
        preserved_market_pointer_fields=list(MARKET_FIELDS), unchanged_native_code_andother_existing_data=True,
        whole_serialized_ARM9_inverse_exact=True, release_or_review_credit=False)
