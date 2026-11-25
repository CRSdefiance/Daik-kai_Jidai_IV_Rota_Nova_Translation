"""Fit the revised paragraphs inside the existing deployed allocation."""

from struct import pack, pack_into, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.source_item_cards_and_coin_v1 import BASE, POOL, cache_plan, coin_wrapper, compile_item
from dk4tool.patch.source_item_cards_and_coin_v1 import DYNAMIC, HOOK, PARAGRAPH, PRIOR


RETIRED_TABLE = 0x0238C2AC
RETIRED_COUNT = 198


def extend_item_payload(source, records, table, pointers, payload):
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 6
    section = code.sections[3]
    original = bytes(section.data)
    assert original[:-48] == payload
    parent_cache = cache_plan(source)
    assert parent_cache['payload_bytes'] == len(payload)

    # The generated-map extension replaced this table with an active 218-entry
    # table. No ARM9 literal points at the retired table.
    assert source.find(pack('<I', RETIRED_TABLE)) == -1
    inactive = RETIRED_TABLE - POOL
    historical = unpack_from(f'<{RETIRED_COUNT}I', payload, inactive)
    assert [i for i, (before, now) in enumerate(zip(historical, pointers)) if before != now] == [116]
    count = len(records)
    start, end = pointers[0] - POOL, pointers[count] - POOL
    retired_end = inactive + RETIRED_COUNT * 4
    assert 0 <= start < end < inactive < retired_end < table - POOL
    assert not any(start <= p - POOL < end or inactive <= p - POOL < retired_end for p in pointers[count:])
    assert all(pointers[i] < pointers[i + 1] for i in range(count))

    edited = bytearray(payload)
    cursor, spill = start, inactive
    changes = []
    for ident, row in enumerate(records):
        assert ident == row['item_ID']
        field = table - POOL + 4 * ident
        assert row['private_pointer_field'] == POOL + field and pointers[ident] == row['prior_private_pointer']
        assert payload[pointers[ident] - POOL:pointers[ident + 1] - POOL] == bytes.fromhex(row['prior_private_hex'])
        lines, compiled = compile_item(row['english'])
        if spill == inactive and cursor + len(compiled) <= end:
            offset = cursor
            cursor += len(compiled)
        else:
            offset = spill
            spill += len(compiled)
            assert spill <= retired_end
        edited[offset:offset + len(compiled)] = compiled
        pack_into('<I', edited, field, POOL + offset)
        changes.append(dict(item_ID=ident, message_ID=row['message_ID'], field=POOL + field,
            old_pointer=pointers[ident], new_pointer=POOL + offset, compiled_rows=lines, compiled_hex=compiled.hex()))
    edited[cursor:end] = bytes(end - cursor)
    section.data = edited + original[-48:]
    target = bytes(code.save())
    reloaded = MainCodeFile(target, BASE)
    assert cache_plan(target) == parent_cache
    assert len(reloaded.sections[3].data) == len(original)
    assert all((a.ramAddress, a.bssSize) == (b.ramAddress, b.bssSize)
               for a, b in zip(code.sections, reloaded.sections, strict=True))
    original_regions = ((start, end), (inactive, spill), (table - POOL, table - POOL + 4 * count))
    for lo, hi in original_regions:
        reloaded.sections[3].data[lo:hi] = original[lo:hi]
    assert bytes(reloaded.save()) == source
    return target, dict(old_payload_bytes=len(payload), new_payload_bytes=len(payload), new_cache_plan=parent_cache,
        item_paragraphs=changes, exact_parent_ARM9_inverse=True, main_pool_geometry_and_startup_exact=True,
        selected_original_text_span=[POOL + start, POOL + end],
        unreferenced_retired_table_span=[RETIRED_TABLE, POOL + retired_end],
        retired_bytes_reused=spill - inactive, active_pointer_fields=count,
        previous_payload_except_selected_text_inactive_table_and_selected_live_pointers_preserved=True)

