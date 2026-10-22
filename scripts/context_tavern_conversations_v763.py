"""Original Tavern argument providers, including qualitative two-axis hints."""

import struct
from itertools import product
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_conversations_v763')
CURRENT = Path('out/all_routes_combined_v762_candidate.nds')
RAM_REPORT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/port_services_v762_copy_no_funds_762/capture_report.json')
PRIVATE = 0x02470000
NORTH_SOUTH = (b'north', b'south')
EAST_WEST = (b'east', b'west')
DISTANCE = (b'a little', b'far', b'very far')
SOURCE_DISTANCE = tuple(s.encode('cp932') for s in ('ちょっ', 'ずっ', 'ずーっ'))


def private_directions(u):
    cursor = PRIVATE + 0x100
    for table, values in ((PRIVATE, NORTH_SOUTH), (PRIVATE + 8, EAST_WEST), (PRIVATE + 16, DISTANCE)):
        for index, value in enumerate(values):
            u.mem_write(cursor, value + b'\0'); u.mem_write(table + index * 4, struct.pack('<I', cursor)); cursor += len(value) + 1
    for at, pointer in ((0x58F08, PRIVATE), (0x58F0C, PRIVATE + 16), (0x58F10, PRIVATE + 8)):
        u.mem_write(BASE + at, struct.pack('<I', pointer))
    return {'tables': [PRIVATE, PRIVATE + 8, PRIVATE + 16], 'string_bytes': cursor - PRIVATE - 0x100,
        'three_function_local_literal_patches_only': [0x02058F08, 0x02058F0C, 0x02058F10],
        'source_shared_cardinal_labels_and_tables_preserved': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, rom = [NdsImage.open(p) for p in ('work/clean.nds', CURRENT)]
    ca, arm = [r.read_file('/__arm9__.bin') for r in (clean, rom)]
    original_spans = ((0x58C64, 0x58EE8), (0x59C9C, 0x59CE4), (0x59288, 0x592D0),
        (0x53BD8, 0x53CB0), (0x58990, 0x589D4), (0x58A70, 0x58A98), (0x59EDC, 0x59F30))
    for lo, hi in original_spans: assert ca[lo:hi] == arm[lo:hi], hex(lo)
    raw = snapshot(read(RAM_REPORT), 3200); u = machine(arm); u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args); return u.reg_read(UC_ARM_REG_R0)
    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def string(at): return bytes(u.mem_read(at, 256)).split(b'\0')[0]
    item_root, officer_root, town_root, good_root = [get(fn) for fn in (0xCB190, 0xCB184, 0xCB178, 0xCB124)]
    company_root = get(0xCB160); force = company_root + 4 + get(0x397D8, (company_root,)) * 0x4C
    town = get(0xB6618); admiral = get(0x7F244)
    actor = officer_root + 4 + admiral * 32
    names = []
    for index in range(218):
        obj = item_root + 4 + index * 20; fn = ptr(ptr(obj) + 8); name = string(get(fn - BASE, (obj,)))
        names.append({'item_ID': index, 'object': obj, 'name_hex': name.hex(), 'name': name.decode('cp932')})
    assert len(names) == 218 and max(len(bytes.fromhex(r['name_hex'])) for r in names) == 23
    goods, towns = [], []
    # Slot124 is an initialized base-class placeholder with a null name member,
    # distinct from the124 named commodity objects. Do not call its virtual
    # name entry as though it were a normal product.
    reserved_good = good_root + 4 + 124 * 16
    assert ptr(reserved_good) == 0x0215B650 and ptr(reserved_good + 4) == 0
    for kind, root, stride, count, result in (('good', good_root, 16, 124, goods), ('town', town_root, 108, 90, towns)):
        for index in range(count):
            obj = root + 4 + index * stride
            try:
                name = string(get(ptr(ptr(obj) + 8) - BASE, (obj,)))
            except Exception as error:
                raise RuntimeError(f'{kind} index{index} object{obj:#x} vtable{ptr(obj):#x} getter{ptr(ptr(obj) + 8):#x}') from error
            result.append({'index': index, 'object': obj, 'name_hex': name.hex(), 'name': name.decode('cp932')})
    ns_table, distance_table, ew_table = [struct.unpack_from('<I', arm, at)[0] for at in (0x58F08, 0x58F0C, 0x58F10)]
    assert (ns_table, distance_table, ew_table) == (0x02118B40, 0x02118B58, 0x02118B48)
    current_values = {'north_south': [string(ptr(ns_table + 4 * i)) for i in range(2)],
        'east_west': [string(ptr(ew_table + 4 * i)) for i in range(2)],
        'distance': [string(ptr(distance_table + 4 * i)) for i in range(3)]}
    assert current_values == {'north_south': [b'N', b'S'], 'east_west': [b'E', b'W'], 'distance': list(SOURCE_DISTANCE)}
    events = []
    counts = {820: 3, 821: 3, 843: 5, 844: 3, 845: 3, 846: 1, 847: 1, 848: 1, 849: 2, 850: 2}
    def observe(cpu, pc, size, unused):
        if pc != BASE + 0x53FE4: return
        n = cpu.reg_read(UC_ARM_REG_R1); assert n in counts, n
        pointers = [cpu.reg_read(UC_ARM_REG_R2), cpu.reg_read(UC_ARM_REG_R3)]
        pointers += list(struct.unpack('<3I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP), 12)))
        events.append({'id': n, 'arguments_hex': [string(p).hex() for p in pointers[:counts[n]]], 'parent': 0x02054014})
        cpu.emu_stop()
    h = u.hook_add(UC_HOOK_CODE, observe)
    cases = []
    item = names[60]['object']; item_name = bytes.fromhex(names[60]['name_hex'])
    def fragment(start, end):
        events.clear(); u.reg_write(UC_ARM_REG_SP, STACK); u.emu_start(BASE + start, BASE + end, count=10000)
        assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x53FE4 and len(events) == 1
        return events[0]
    try:
        for english in (False, True):
            if english: resource = private_directions(u)
            ns = NORTH_SOUTH if english else (b'N', b'S')
            ew = EAST_WEST if english else (b'E', b'W')
            degree = DISTANCE if english else SOURCE_DISTANCE
            for dx, dy, xdir, ydir in product((149, 150, 499, 500, 1999, 2000, 2001), (149, 150, 499, 500, 1999, 2000, 2001), range(2), range(2)):
                for off, value in ((0x10, actor), (0x18, ydir), (0x24, dx), (0x28, dy)):
                    u.mem_write(STACK + off, struct.pack('<I', value))
                u.reg_write(UC_ARM_REG_R4, item); u.reg_write(UC_ARM_REG_R9, xdir)
                event = fragment(0x58D4C, 0x58EA4)
                xlevel = 2 if dx >= 2000 else 1 if dx >= 500 else 0
                ylevel = 2 if dy >= 2000 else 1 if dy >= 500 else 0
                if dx >= 150 and dy >= 150:
                    n, expected = 843, [item_name, degree[ylevel], ns[ydir], degree[xlevel], ew[xdir]]
                elif dx >= 150:
                    n, expected = 844, [item_name, degree[xlevel], ew[xdir]]
                elif dy >= 150:
                    n, expected = 845, [item_name, degree[ylevel], ns[ydir]]
                else:
                    n, expected = 846, [item_name]
                assert event['id'] == n and event['arguments_hex'] == [v.hex() for v in expected], (dx, dy, xdir, ydir, event)
                cases.append({'supplied_internal_axis_distances': [dx, dy], 'supplied_direction_indices': [xdir, ydir],
                    'private_English_provider': english, **event})
        profession = string(get(0x3CF70, (force,)))
        for n in (820, 821):
            u.reg_write(UC_ARM_REG_R7, actor); u.reg_write(UC_ARM_REG_R5, town)
            u.reg_write(UC_ARM_REG_R6, force); u.reg_write(UC_ARM_REG_R4, actor); u.reg_write(UC_ARM_REG_R8, n)
            event = fragment(0x59C9C, 0x59CE4)
            full_name = string(get(ptr(ptr(actor) + 0x24) - BASE, (actor,)))
            town_name = string(get(ptr(ptr(town) + 8) - BASE, (town,)))
            assert event['arguments_hex'] == [v.hex() for v in (full_name, town_name, profession)]
            cases.append({'actual_native_person_town_force_objects': True, **event})
        # Source threshold49/50 is the native current/prospective trend selector.
        # The original virtual getters supply town first, commodity second.
        for level in (49, 50):
            u.mem_write(STACK + 4, struct.pack('<I', actor))
            u.reg_write(UC_ARM_REG_R4, town); u.reg_write(UC_ARM_REG_R5, good_root + 4)
            u.reg_write(UC_ARM_REG_R6, level)
            event = fragment(0x58990, 0x589D4)
            assert event['id'] == (849 if level < 50 else 850)
            assert event['arguments_hex'] == [towns[next(i for i, r in enumerate(towns) if r['object'] == town)]['name_hex'], goods[0]['name_hex']]
            cases.append({'supplied_native_trend_selector_value': level, **event})
            u.reg_write(UC_ARM_REG_R0, good_root + 4); u.reg_write(UC_ARM_REG_R4, actor); u.reg_write(UC_ARM_REG_R7, level)
            event = fragment(0x58A70, 0x58A98)
            assert event['id'] == (847 if level < 50 else 848) and event['arguments_hex'] == [goods[0]['name_hex']]
            cases.append({'supplied_native_trend_selector_value': level, **event})
    finally:
        u.hook_del(h)
    route_field = struct.unpack_from('<I', arm, 0x5B0A0)[0] + 0x48
    queued = []
    for literal, expected in ((0x59344, (830, 831, 832, 833)), (0x5934C, (835, 836, 837, 838))):
        table = struct.unpack_from('<I', arm, literal)[0]
        assert ca[literal:literal + 4] == arm[literal:literal + 4]
        assert struct.unpack('<4I', u.mem_read(table, 16)) == expected
        for index in range(4):
            u.mem_write(route_field, struct.pack('<I', index)); chosen = get(0x53C6C, (table,))
            assert chosen == expected[index]
            queued.append({'original_table': table, 'supplied_route_index': index, 'selected_ID': chosen})
    coordinate_cases = []
    for row in names:
        obj = row['object']; get(ptr(ptr(obj) + 0x20) - BASE, (0x02450000, obj))
        position = bytes(u.mem_read(0x02450000, 8))
        if position == b'\xff' * 8: continue
        value = string(get(0x51580, (0x02450000,)))
        assert value.startswith(b'\n ') and all(c < 128 for c in value)
        coordinate_cases.append({'item_ID': row['item_ID'], 'original_position_hex': position.hex(), 'argument_hex': value.hex(),
            'decoded': value.decode('ascii'), 'coordinate_text_not_region_or_city_name': True})
    assert coordinate_cases
    save(ROOT / 'native_context.json', {'source_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(CURRENT.read_bytes()),
        'original_provider_spans_clean_current_identical': [{'lo': lo, 'hi': hi, 'sha256': sha(arm[lo:hi])} for lo, hi in original_spans],
        'current_source_provider_tables': {k: [v.hex() for v in values] for k, values in current_values.items()},
        '392_hint_provider_cases_and6_person_trend_fragments': cases, 'eight_original_four_captain_gift_voice_selections': queued,
        'actual218_item_names': names, 'actual124_named_commodity_objects': goods, 'actual90_town_names': towns,
        'reserved_commodity124_base_class_null_name_not_treated_as_named_product': {'object': reserved_good, 'bytes_hex': bytes(u.mem_read(reserved_good, 16)).hex()},
        'actual_coordinate_formatter_arguments_for842': coordinate_cases,
        '843_roles': ['item_name', 'NS_distance_qualifier', 'NS_direction', 'EW_distance_qualifier', 'EW_direction'],
        '844_845_roles': ['item_name', 'distance_qualifier', 'direction'],
        '820_821_roles': ['person_full_name', 'town_name', 'force_profession'],
        '847_848_roles': ['commodity_name'], '849_850_roles': ['town_name', 'commodity_name'],
        'source_500_2000_qualitative_thresholds_not_miles_days_or_degrees': True,
        'private_English_resource_RESEARCH_only': resource,
        'untranslated_Japanese_distance_fragments_confirmed': True,
        'COMMON842_argument_contains_provider_LF_and_spacing_to_normalize': True,
        'all_UI_calls_stopped_at_original_boundary_no_eligibility_earned_scene_or_ROM_change_claim': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(cases)} original person/trend/hint fragments;8 gift voice selections;218 item/124 named good/90 town names;{len(coordinate_cases)} real coordinate strings. Private English provider is CPU-only research.', flush=True)


if __name__ == '__main__': main()
