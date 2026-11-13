"""Keep twenty promotional fragments bound to one reviewed native description."""

from hashlib import sha256
from struct import pack_into
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch.figurehead_navigation_gift_cards_v1 import replace_prefix
from dk4tool.patch import reviewed_item_cards as storage
from dk4tool.patch.utility_weapon_item_cards_v1 import compile_item as previous_format

FIRST, FRAGMENT, END = 188, 198, 218
item_table = storage.item_table
PHRASES = (
    'ancient writing', 'ward off evil', 'rites of exorcism', 'carved in relief',
    'Rose quartz', 'six-rayed star', 'phantom crystal', 'island nation',
    'without touching', 'No one knows', 'every illness', 'good-luck charm', 'Legend says', 'improve concentration', "It's said",
)
compile_item = FunctionType(previous_format.__code__, previous_format.__globals__ | {
    'PROTECTED_PHRASES': previous_format.__globals__['PROTECTED_PHRASES'] + PHRASES,
})


def transform(source, records, table, pointers, payload):
    assert tuple(row['item_ID'] for row in records) == tuple(range(FIRST, END))
    assert len(set(pointers[FRAGMENT:])) == 1
    previous = MainCodeFile(source, storage.BASE)
    previous_resident = bytes(previous.sections[5].data)
    previous_cache = storage.cache_plan(source)
    mid, first = replace_prefix(source, records[:10], table, pointers, payload,
        first=FIRST, end=FRAGMENT, compile_paragraph=compile_item)
    mid_payload, mid_table, mid_pointers = item_table(mid)
    assert table == mid_table and mid_pointers[FRAGMENT:] == pointers[FRAGMENT:]

    code = MainCodeFile(mid, storage.BASE)
    copied, resident = code.sections[3], code.sections[5]
    edits = bytearray(mid_payload)
    lines, compiled = compile_item(records[10]['english'])
    old, _ = storage.item_paragraph(payload, pointers[FRAGMENT])
    address = storage.RESIDENT_BASE + len(resident.data)
    resident.data.extend(compiled)
    resident.data.extend(bytes(-len(resident.data) % 4))
    assert storage.RESIDENT_BASE + len(resident.data) <= storage.BASE
    changes = []
    for ident, row in enumerate(records[10:], FRAGMENT):
        field = table + 4 * ident
        assert row['prior_private_pointer'] == pointers[ident] and row['private_pointer_field'] == field
        assert bytes.fromhex(row['prior_private_hex']) == old and row['english'] == records[10]['english']
        pack_into('<I', edits, field - storage.POOL, address)
        changes.append(dict(item_ID=ident, message_ID=row['message_ID'], field=field,
            old_pointer=pointers[ident], new_pointer=address, compiled_rows=lines,
            compiled_hex=compiled.hex(), storage='shared resident fragment paragraph'))
    copied.data = edits + copied.data[-48:]
    target = bytes(code.save())
    new_payload, new_table, new_pointers = item_table(target)
    assert new_table == table and new_pointers[FRAGMENT:] == (address,) * 20
    assert new_payload[:table - storage.POOL + 4 * FRAGMENT] == mid_payload[:table - storage.POOL + 4 * FRAGMENT]
    assert storage.cache_plan(target) == previous_cache
    restored = MainCodeFile(target, storage.BASE)
    resident_bytes = bytes(restored.sections[5].data)
    assert resident_bytes[:len(previous_resident)] == previous_resident
    for lo, hi in (first['selected_original_text_span'], (table + FIRST * 4, table + END * 4)):
        start, end = lo - storage.POOL, hi - storage.POOL
        restored.sections[3].data[start:end] = previous.sections[3].data[start:end]
    restored.sections[5].data = bytearray(previous_resident)
    assert bytes(restored.save()) == source
    return target, dict(
        old_payload_bytes=len(payload), new_payload_bytes=len(payload), new_cache_plan=previous_cache,
        item_paragraphs=first['item_paragraphs'] + changes, exact_parent_ARM9_inverse=True,
        main_pool_geometry_and_startup_exact=True,
        selected_original_text_span=first['selected_original_text_span'], active_pointer_fields=len(records),
        shared_fragment_pointer=address, retired_fragment_pointer=pointers[FRAGMENT],
        shared_fragment_alias_count=len(changes),
        appended_resident_text_span=[storage.RESIDENT_BASE + len(previous_resident),
                                     storage.RESIDENT_BASE + len(resident_bytes)],
        appended_resident_text_sha256=sha256(resident_bytes[len(previous_resident):]).hexdigest(),
    )
