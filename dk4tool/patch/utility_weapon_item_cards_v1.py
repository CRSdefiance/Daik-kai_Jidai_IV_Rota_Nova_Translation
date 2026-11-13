"""Store reviewed item paragraphs without enlarging the main RAM cache copy."""

from hashlib import sha256
from struct import pack, pack_into
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch.source_item_cards_and_coin_v1 import BASE, POOL, STAGE, cache_plan, compile_item as previous_format
from dk4tool.patch.source_item_cards_and_coin_v2 import RETIRED_COUNT, RETIRED_TABLE


FIRST_ITEM = 20
AFTER_LAST_ITEM = 49
FIRST_WEAPON = 24
PROTECTED = ('Hua Tuo', 'Three Kingdoms era', 'crescent moon', 'Kublai Khan', 'King Arthur',
             'cure any contagious disease', 'the twelve Olympians', 'on the spot')
compile_item = FunctionType(previous_format.__code__, previous_format.__globals__ | {
    'PROTECTED_PHRASES': previous_format.__globals__['PROTECTED_PHRASES'] + PROTECTED,
})


def transform(source, records, table, pointers, payload):
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 6
    main, resident = code.sections[3], code.sections[5]
    original_main, original_resident = bytes(main.data), bytes(resident.data)
    assert main.ramAddress == STAGE and original_main[:-48] == payload
    assert resident.ramAddress == 0x01FFD000 and resident.bssSize == 0
    cache = cache_plan(source)
    assert cache['payload_bytes'] == len(payload) == 123264

    local = pointers[FIRST_ITEM] - POOL
    local_end = pointers[AFTER_LAST_ITEM] - POOL
    inactive, retired_end = RETIRED_TABLE - POOL, RETIRED_TABLE - POOL + RETIRED_COUNT * 4
    # The table base is now also the start of item 15's reviewed paragraph.
    # Its only stored reference must be that description's live pointer field.
    literal = pack('<I', RETIRED_TABLE)
    first_spilled_field = source.index(payload) + table - POOL + 4 * 15
    assert source.count(literal) == 1 and source.index(literal) == first_spilled_field
    assert all(inactive <= pointer - POOL < retired_end for pointer in pointers[15:FIRST_ITEM])
    assert all(pointer - POOL < inactive for pointer in pointers[:15])
    prior_ending = payload.index(b'\0\0', pointers[FIRST_ITEM - 1] - POOL) + 2
    assert inactive < prior_ending < retired_end < table - POOL
    assert 0 < local < local_end < inactive
    protected = pointers[:FIRST_ITEM] + pointers[AFTER_LAST_ITEM:]
    for pointer in protected:
        beginning = pointer - POOL
        ending = payload.index(b'\0\0', beginning) + 2
        assert ending <= local or beginning >= local_end
        assert ending <= prior_ending or beginning >= retired_end

    selected_fields = table - POOL + 4 * FIRST_ITEM
    main_bytes, resident_bytes = bytearray(payload), bytearray(original_resident)
    cursor, spill = local, prior_ending
    changes = []
    for index, row in zip(range(FIRST_ITEM, AFTER_LAST_ITEM), records, strict=True):
        offset = pointers[index] - POOL
        assert row['item_ID'] == index and row['prior_private_pointer'] == POOL + offset
        assert payload[offset:pointers[index + 1] - POOL] == bytes.fromhex(row['prior_private_hex'])
        field = table - POOL + 4 * index
        assert row['private_pointer_field'] == POOL + field
        lines, compiled = compile_item(row['english'])
        # Exercise the resident storage with the first weapon in the regular Items replay.
        if index != FIRST_WEAPON and cursor + len(compiled) <= local_end:
            pointer = POOL + cursor
            main_bytes[cursor:cursor + len(compiled)] = compiled
            cursor += len(compiled)
            storage = 'copied catalogue'
        elif index != FIRST_WEAPON and spill + len(compiled) <= retired_end:
            pointer = POOL + spill
            main_bytes[spill:spill + len(compiled)] = compiled
            spill += len(compiled)
            storage = 'retired table'
        else:
            pointer = resident.ramAddress + len(resident_bytes)
            resident_bytes.extend(compiled)
            storage = 'resident read-only catalogue'
        pack_into('<I', main_bytes, field, pointer)
        changes.append(dict(item_ID=index, message_ID=row['message_ID'], field=POOL + field,
                            old_pointer=pointers[index], new_pointer=pointer, compiled_rows=lines,
                            compiled_hex=compiled.hex(), storage=storage))
    main_bytes[cursor:local_end] = bytes(local_end - cursor)
    resident_bytes.extend(bytes(-len(resident_bytes) % 4))
    assert resident.ramAddress + len(resident_bytes) <= BASE
    assert resident_bytes[:len(original_resident)] == original_resident
    main.data = main_bytes + original_main[-48:]
    resident.data = resident_bytes
    target = bytes(code.save())
    parsed = MainCodeFile(target, BASE)
    assert bytes(parsed.save()) == target and cache_plan(target) == cache
    assert parsed.sections[3].ramAddress == STAGE and len(parsed.sections[3].data) == len(original_main)
    assert parsed.sections[5].ramAddress == resident.ramAddress
    assert bytes(parsed.sections[5].data) == resident_bytes
    for lo, hi in ((local, local_end), (prior_ending, spill),
                   (selected_fields, selected_fields + 4 * len(changes))):
        parsed.sections[3].data[lo:hi] = original_main[lo:hi]
    parsed.sections[5].data = bytearray(original_resident)
    assert bytes(parsed.save()) == source
    return target, dict(
        old_payload_bytes=len(payload), new_payload_bytes=len(payload), new_cache_plan=cache,
        item_paragraphs=changes, exact_parent_ARM9_inverse=True,
        main_pool_geometry_and_startup_exact=True,
        selected_original_text_span=[POOL + local, POOL + local_end],
        unreferenced_retired_table_span=[POOL + prior_ending, POOL + retired_end],
        retired_bytes_reused=spill - prior_ending,
        appended_resident_text_span=[resident.ramAddress + len(original_resident),
                                     resident.ramAddress + len(resident_bytes)],
        appended_resident_text_sha256=sha256(resident_bytes[len(original_resident):]).hexdigest(),
        active_pointer_fields=len(changes),
    )
