"""Pack newly reviewed item categories into their owned paragraph span and resident tail."""

from hashlib import sha256
from struct import pack_into, unpack_from
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch.utility_weapon_item_cards_v1 import BASE, POOL, STAGE, cache_plan, compile_item as original_format
from scripts.checkpoint_sailing_alert_review_v1 import branch_target
from scripts.review_source_item_cards_and_coin_v1 import GETTER, LOOKUP, PAINT, PAINTER, item_paragraph

RESIDENT_BASE = 0x01FFD000
CATALOGUE_START = RESIDENT_BASE + 4412
TABLE_SIZE = 218
ARMOR_FIRST = 49
ARMOR_END = 74
ARMOR_PHRASES = (
    'small, round shield', 'harder than iron', 'silver leaf', 'bird in flight', 'face of death',
    'giant tortoise shell', 'the spirits', "attacker's blade", 'central Africa', 'dreadful taste',
    'a little heavy', 'Timurid Empire', '14th century', 'peacock feathers', 'warriors of Tula',
    'yellow sheen', 'Jaguar God', 'sold his soul', 'to the devil', 'Taira commander',
    'goddess of war', 'Sturdy and handsome', 'fine protection', 'No one knows', "Medusa's hair", 'Charles Martel', 'Battle of Tours-Poitiers', 'fit for a king',
)
compile_armor = FunctionType(original_format.__code__, original_format.__globals__ | {
    'PROTECTED_PHRASES': original_format.__globals__['PROTECTED_PHRASES'] + ARMOR_PHRASES,
})


def item_table(arm):
    sections = MainCodeFile(arm, BASE).sections
    assert len(sections) == 6 and sections[3].ramAddress == STAGE
    resident = sections[5]
    assert resident.ramAddress == RESIDENT_BASE and resident.bssSize == 0
    assert CATALOGUE_START <= RESIDENT_BASE + len(resident.data) <= BASE
    payload = bytes(sections[3].data[:-48])
    assert len(payload) == 123264
    assert all(branch_target(arm, pc) == GETTER for pc in LOOKUP)
    assert all(branch_target(arm, pc) == PAINTER for pc in PAINT)
    getter = GETTER - POOL
    assert unpack_from('<I', payload, getter + 20)[0] == 0xE35400DA
    table = unpack_from('<I', payload, getter + 44)[0]
    assert table == 0x0238C6C4
    pointers = unpack_from(f'<{TABLE_SIZE}I', payload, table - POOL)
    assert all(POOL <= pointer < POOL + len(payload) - 64 or
               CATALOGUE_START <= pointer < RESIDENT_BASE + len(resident.data) for pointer in pointers)
    return payload, table, pointers


def replace_category(source, records, table, pointers, payload, *, first, end, compile_paragraph):
    assert tuple(row['item_ID'] for row in records) == tuple(range(first, end))
    assert 0 < first < end < TABLE_SIZE
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 6
    main, resident = code.sections[3], code.sections[5]
    previous_main, previous_resident = bytes(main.data), bytes(resident.data)
    assert main.ramAddress == STAGE and previous_main[:-48] == payload
    assert resident.ramAddress == RESIDENT_BASE and resident.bssSize == 0
    cache = cache_plan(source)
    assert cache['payload_bytes'] == len(payload) == 123264

    start, limit = pointers[first] - POOL, pointers[end] - POOL
    first_field = table - POOL + 4 * first
    field_limit = first_field + 4 * len(records)
    assert 0 <= start < limit < first_field < field_limit <= len(payload)
    for ident, pointer in enumerate(pointers):
        if first <= ident < end:
            continue
        if pointer >= POOL:
            old, _ = item_paragraph(payload, pointer)
            beginning = pointer - POOL
            assert beginning + len(old) <= start or beginning >= limit
        else:
            assert CATALOGUE_START <= pointer < RESIDENT_BASE + len(previous_resident)
            previous_resident.index(b'\0\0', pointer - RESIDENT_BASE)
    for ident, row in enumerate(records, first):
        offset = pointers[ident] - POOL
        assert start <= offset < pointers[ident + 1] - POOL <= limit
        assert pointers[ident] == row['prior_private_pointer']
        assert payload[offset:pointers[ident + 1] - POOL] == bytes.fromhex(row['prior_private_hex'])
        assert row['private_pointer_field'] == table + 4 * ident

    edited_main, edited_resident = bytearray(payload), bytearray(previous_resident)
    cursor = start
    decisions = []
    for ident, row in enumerate(records, first):
        lines, compiled = compile_paragraph(row['english'])
        if cursor + len(compiled) <= limit:
            pointer = POOL + cursor
            edited_main[cursor:cursor + len(compiled)] = compiled
            cursor += len(compiled)
            storage = 'copied catalogue'
        else:
            pointer = RESIDENT_BASE + len(edited_resident)
            edited_resident.extend(compiled)
            storage = 'resident read-only catalogue'
        field = table - POOL + 4 * ident
        pack_into('<I', edited_main, field, pointer)
        decisions.append(dict(item_ID=ident, message_ID=row['message_ID'], field=POOL + field,
            old_pointer=pointers[ident], new_pointer=pointer, compiled_rows=lines,
            compiled_hex=compiled.hex(), storage=storage))
    edited_main[cursor:limit] = bytes(limit - cursor)
    edited_resident.extend(bytes(-len(edited_resident) % 4))
    assert RESIDENT_BASE + len(edited_resident) <= BASE
    main.data = edited_main + previous_main[-48:]
    resident.data = edited_resident
    target = bytes(code.save())
    restored = MainCodeFile(target, BASE)
    assert bytes(restored.save()) == target and cache_plan(target) == cache
    assert len(restored.sections[3].data) == len(previous_main)
    assert bytes(restored.sections[5].data[:len(previous_resident)]) == previous_resident
    for lo, hi in ((start, limit), (first_field, field_limit)):
        restored.sections[3].data[lo:hi] = previous_main[lo:hi]
    restored.sections[5].data = bytearray(previous_resident)
    assert bytes(restored.save()) == source
    return target, dict(
        old_payload_bytes=len(payload), new_payload_bytes=len(payload), new_cache_plan=cache,
        item_paragraphs=decisions, exact_parent_ARM9_inverse=True,
        main_pool_geometry_and_startup_exact=True,
        selected_original_text_span=[POOL + start, POOL + limit],
        appended_resident_text_span=[RESIDENT_BASE + len(previous_resident),
                                     RESIDENT_BASE + len(edited_resident)],
        appended_resident_text_sha256=sha256(edited_resident[len(previous_resident):]).hexdigest(),
        active_pointer_fields=len(decisions),
    )


def transform(source, records, table, pointers, payload):
    return replace_category(source, records, table, pointers, payload,
                            first=ARMOR_FIRST, end=ARMOR_END, compile_paragraph=compile_armor)
