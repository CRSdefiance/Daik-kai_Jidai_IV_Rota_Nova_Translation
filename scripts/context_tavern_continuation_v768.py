"""Original851-882 providers,role queues and vocative/target distinctions."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1,
    UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R11, UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_continuation_v768')
CURRENT = Path('out/all_routes_combined_v767_candidate.nds')
RAM_REPORT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/tavern_editorial_v767_final_v767/capture_report.json')
REGIONS = ('the North Sea', 'the Mediterranean', 'Africa', 'the Indian Ocean', 'Southeast Asia', 'East Asia', 'the New World')


def main():
    rom = NdsImage.open(CURRENT); arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    source_spans = ((0x57A5C, 0x58834), (0x59880, 0x599DC), (0x53CB0, 0x53F9C))
    for lo, hi in source_spans: assert arm[lo:hi] == clean[lo:hi], hex(lo)
    u = machine(arm); u.mem_write(BASE, snapshot(read(RAM_REPORT), 3200))
    def get(fn, args=()): call(u, fn, args); return u.reg_read(UC_ARM_REG_R0)
    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def string(at): return bytes(u.mem_read(at, 256)).split(b'\0')[0]
    def name(obj): return string(get(ptr(ptr(obj) + 8) - BASE, (obj,)))
    officers, force_root, town_root, item_root = [get(fn) for fn in (0xCB184, 0xCB160, 0xCB178, 0xCB190)]
    town = get(0xB6618); npc = get(0xB2CD8, (town, 13)); captain = officers + 0x19E4
    force_names = [{'index': i, 'object': force_root + 4 + i * 0x4C, 'name_hex': name(force_root + 4 + i * 0x4C).hex()} for i in range(20)]
    towns = [{'index': i, 'object': town_root + 4 + i * 108, 'name_hex': name(town_root + 4 + i * 108).hex()} for i in range(90)]
    items = [{'index': i, 'object': item_root + 4 + i * 20, 'name_hex': name(item_root + 4 + i * 20).hex(),
              'original_region_index': get(0x4A3F0, (item_root + 4 + i * 20,))} for i in range(218)]
    region_rows = []
    clean_cpu = machine(clean)
    for i, english in enumerate(REGIONS):
        record = get(0x945B4, (i,)); field = ptr(record)
        call(clean_cpu, 0x945B4, (i,)); src_record = clean_cpu.reg_read(UC_ARM_REG_R0)
        src_pointer = struct.unpack('<I', clean_cpu.mem_read(src_record, 4))[0]
        source = bytes(clean_cpu.mem_read(src_pointer, 80)).split(b'\0')[0]
        region_rows.append({'index': i, 'record': record, 'native_name_pointer': field,
            'source_Japanese': source.decode('cp932'), 'current_UI_name': string(field).decode('cp932'),
            'proposed_dialogue_region_phrase': english, 'global_UI_data_unchanged': True})
    assert tuple(struct.unpack_from('<8i', arm, 0x118400)) == (852, -1, 853, 854, 855, 856, 857, 858)
    roles = []
    for i in range(40):
        obj = officers + 4 + i * 32; voice = get(0x7E988, (obj,)); chosen = get(0x53F4C, (obj, 0x02118400))
        assert 0 <= voice < 8 and chosen == (852 if voice in (0, 1) else 851 + voice)
        roles.append({'actor_index': i, 'voice': voice, 'selected_cost_ID': chosen,
            'given_name': string(get(0x7EB0C, (obj,))).decode('cp932')})
    assert get(0x53F4C, (0, 0x02118400)) == 852
    route_field = struct.unpack_from('<I', arm, 0x5B0A0)[0] + 0x48
    original_route = bytes(u.mem_read(route_field, 4)); voices = []
    for table, ids in ((0x021166F0, tuple(range(859, 863))), (0x02116810, tuple(range(864, 868)))):
        assert struct.unpack('<4I', u.mem_read(table, 16)) == ids
        for route in range(4):
            u.mem_write(route_field, struct.pack('<I', route))
            chosen = get(0x53C6C, (table,)); assert chosen == ids[route]
            voices.append({'table': table, 'route': route, 'selected_ID': chosen})
    u.mem_write(route_field, original_route)
    counts = {851: 2, 863: 2, 868: 0, 869: 1, 870: 3, 871: 2, 872: 2, 873: 1, 874: 0,
              875: 1, 876: 1, 877: 1, 878: 2, 879: 2, 880: 2, 881: 2, 882: 2}
    events, cases = [], []
    def observe(cpu, pc, size, unused):
        n = cpu.reg_read(UC_ARM_REG_R1); assert n in counts, n
        pointers = [cpu.reg_read(UC_ARM_REG_R2), cpu.reg_read(UC_ARM_REG_R3)]
        pointers += list(struct.unpack('<I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP), 4)))
        events.append({'id': n, 'arguments_hex': [string(p).hex() for p in pointers[:counts[n]]]})
        cpu.emu_stop()
    handle = u.hook_add(UC_HOOK_CODE, observe, begin=BASE + 0x53FE4, end=BASE + 0x53FE4)
    def fragment(lo, hi, registers, stack=()):
        events.clear(); u.reg_write(UC_ARM_REG_SP, STACK)
        for reg, value in registers: u.reg_write(reg, value)
        for off, value in stack: u.mem_write(STACK + off, struct.pack('<I', value))
        u.emu_start(BASE + lo, BASE + hi, count=10000)
        assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x53FE4 and len(events) == 1, (hex(lo), events)
        return dict(events[0])
    def add(event, expected, **extra):
        assert event['arguments_hex'] == [v.hex() for v in expected], (event, expected)
        cases.append({**event, **extra})
    try:
        # Actual virtual company/town getters,not surnames or guessed countries.
        for company in force_names:
            for place in towns:
                event = fragment(0x587A4, 0x5880C, ((UC_ARM_REG_R4, company['index']), (UC_ARM_REG_R5, place['object'])), ((4, npc),))
                assert event['id'] == 851
                add(event, [bytes.fromhex(company['name_hex']), bytes.fromhex(place['name_hex'])])
        for item in items:
            region = item['original_region_index']
            if not 0 <= region < 7: continue
            event = fragment(0x59950, 0x59994, ((UC_ARM_REG_R5, region), (UC_ARM_REG_R6, item['object'])))
            assert event['id'] == 863
            add(event, [bytes.fromhex(item['name_hex']), region_rows[region]['current_UI_name'].encode('cp932')],
                item_ID=item['index'], region_index=region, actual_original_item_region_provider=True)
        for route in range(4):
            u.mem_write(route_field, struct.pack('<I', route))
            surname = string(get(ptr(ptr(captain) + 0x24) - BASE, (captain,)))
            sex = get(0x7E9B8, (captain,))
            address = b'Sir' if sex == 0 else b"Ma'am"
            event = fragment(0x57FDC, 0x58000, ((UC_ARM_REG_R5, npc),))
            assert event['id'] == 875; add(event, [surname], supplied_route=route)
            event = fragment(0x5802C, 0x58058, ((UC_ARM_REG_R5, npc),))
            assert event['id'] == 877; add(event, [address], supplied_route=route, argument_is_vocative_not_subject=True)
            for company in force_names:
                current_company_name = name(company['object'])
                event = fragment(0x58008, 0x58028, ((UC_ARM_REG_R4, company['object']), (UC_ARM_REG_R5, npc)))
                assert event['id'] == 876; add(event, [current_company_name], supplied_route=route, company_index=company['index'], runtime_company_name_may_depend_on_route=True)
                u.mem_write(0x02470000, address + b'\0')
                event = fragment(0x58060, 0x58084, ((UC_ARM_REG_R4, company['object']), (UC_ARM_REG_R5, npc), (UC_ARM_REG_R6, 0x02470000)))
                assert event['id'] == 878
                add(event, [current_company_name, address], supplied_route=route, company_index=company['index'], second_argument_addresses_player=True)
            # Round acknowledgement/name and gender address remain distinct fields.
            get(0x7E9B8, (captain,)); u.mem_write(0x02470100, surname + b'\0')
            event = fragment(0x5845C, 0x5846C, ((UC_ARM_REG_R7, npc), (UC_ARM_REG_R11, 0x02470100)))
            assert event['id'] == 869; add(event, [surname], supplied_route=route)
            for lo, hi, n in ((0x58480, 0x5849C, 871), (0x584CC, 0x584E8, 872)):
                event = fragment(lo, hi, ((UC_ARM_REG_R4, sex), (UC_ARM_REG_R6, npc), (UC_ARM_REG_R7, npc), (UC_ARM_REG_R11, 0x02470100)))
                assert event['id'] == n
                add(event, [surname, address], supplied_route=route, second_field_is_gendered_address_not_name_or_rank=True)
            for item in items:
                region = item['original_region_index']
                if not 0 <= region < 7: continue
                event = fragment(0x5829C, 0x582F0, ((UC_ARM_REG_R4, item['object']), (UC_ARM_REG_R5, npc), (UC_ARM_REG_R9, region)))
                assert event['id'] == 870
                add(event, [address, bytes.fromhex(item['name_hex']), region_rows[region]['current_UI_name'].encode('cp932')], supplied_route=route, item_ID=item['index'], region_index=region)
            u.mem_write(0x02470000, address + b'\0')
            event = fragment(0x58308, 0x58318, ((UC_ARM_REG_R5, npc), (UC_ARM_REG_R6, 0x02470000)))
            assert event['id'] == 873; add(event, [address], supplied_route=route)
        u.mem_write(route_field, original_route)
        for lo, hi, n in ((0x599BC, 0x599C8, 868), (0x584FC, 0x58508, 874)):
            event = fragment(lo, hi, ((UC_ARM_REG_R4, npc), (UC_ARM_REG_R6, npc)))
            assert event['id'] == n; add(event, [])
    finally:
        u.hook_del(handle); u.mem_write(route_field, original_route)
    save(ROOT / 'native_context_partial.json', {'source_ARM9_sha256': sha(clean), 'current_ARM9_sha256': sha(arm),
        'source_spans_identical': source_spans, 'real_company_names': force_names, 'real_town_names': towns,
        'real_item_names_and_native_regions': items, 'seven_region_labels_and_proposed_private_dialogue_phrases': region_rows,
        '40_actual_actor_voice_selector_cases': roles, 'eight_four_captain_round_selections': voices,
        'original_provider_fragments': cases,
        '877_vocative_and878_player_target_confirmed': True,
        '871_872_existing_honorific_omission_preserves_original_two_caller_arguments': True,
        'remaining_context_gates': ['Price wrapper/core argument binding', '879-882 destination versus docked getters and mode selectors'],
        'scope': 'Supplied native fragments only,no earned events,actual new scenes or ROM edits. Remaining gates prevent context approval.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(cases)} original provider fragments;40 voice cases;8 captain selections. Price/core and fleet-state gates still pending.', flush=True)


if __name__ == '__main__': main()
