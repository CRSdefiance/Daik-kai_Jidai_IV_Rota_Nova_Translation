"""Map four-route ID selector callers, preserving unresolved branch alternatives."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.inventory_native_common_extended_calls import joined_context_argument
from scripts.inventory_remaining_common_numeric_references import CLEAN, IDS


def native_select(arm9, table, route):
    if not 0 <= route < 4 or table % 4 or not BASE <= table <= BASE + len(arm9) - 16:
        raise ValueError('Four-route table fixture outside mapped source')
    values = struct.unpack_from('<4I', arm9, table - BASE)
    expected = values[route]
    if expected == 0xFFFFFFFF:
        expected = next((v for v in values if v != 0xFFFFFFFF), 0xFFFFFFFF)
    machine = machine_for(arm9)
    state = struct.unpack_from('<I', arm9, 0x7F250)[0]
    machine.mem_write(state + 0x48, struct.pack('<I', route))
    machine.reg_write(UC_ARM_REG_R0, table)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.emu_start(BASE + 0x53C6C, STOP, count=150)
    if (machine.reg_read(UC_ARM_REG_PC) != STOP or
            machine.reg_read(UC_ARM_REG_SP) != STACK or
            machine.reg_read(UC_ARM_REG_R0) != expected):
        raise ValueError('Actual native current-route selector disagrees')
    return {'route_fixture': route, 'selected_id': expected, 'stack_return_verified': True}


def indexed_tables(arm9, entries):
    """Review adjacent static regions; do not infer the live virtual return range."""
    specs = (
        (0x12720, 0x1278C, '9bae2c6fc3a175a9dcee2eb3a269102e95546ab167c92bcda261f9c4726d332b',
         0x12764, 0x12770, 0x12788, 0x130BDC, 0x130C30,
         'd40f99bd78a083fdaa2af07636d194551554f861ee44192236176e95c7cc4955'),
        (0x128B4, 0x12920, '7c480e7b445651cbccf6073340f20102edb5af5919fa289db905434908c227b7',
         0x128F8, 0x12904, 0x1291C, 0x130B88, 0x130BDC,
         '243c4b11353451b7eaf2135b41012b62b35268c578cf38648c8dca1f94c59943'),
    )
    rows = []
    for lo, hi, digest, start, stop, literal, array_lo, array_hi, array_digest in specs:
        if sha(arm9[lo:hi]) != digest or sha(arm9[array_lo:array_hi]) != array_digest:
            raise ValueError('Indexed COMMON producer/array region differs')
        if struct.unpack_from('<I', arm9, literal)[0] != BASE + array_lo:
            raise ValueError('Indexed COMMON array literal differs')
        slots = []
        for index, table in enumerate(struct.unpack_from('<21I', arm9, array_lo)):
            slot = {'index': index, 'table_address': table, 'cases': []}
            if table:
                if not BASE <= table <= BASE + len(arm9) - 16 or table % 4:
                    raise ValueError('Indexed table pointer outside source')
                values = list(struct.unpack_from('<4I', arm9, table - BASE))
                if any(v != 0xFFFFFFFF and v >= len(entries) for v in values):
                    raise ValueError('Indexed table contains invalid message ID')
                slot.update({'four_slots': values, 'remaining_id_overlap': any(v in IDS for v in values),
                             'source_text': [None if v == 0xFFFFFFFF else entries[v].text.decode('cp932') for v in values]})
                for route in range(4):
                    expected = native_select(arm9, table, route)['selected_id']
                    machine = machine_for(arm9)
                    state = struct.unpack_from('<I', arm9, 0x7F250)[0]
                    machine.mem_write(state + 0x48, struct.pack('<I', route))
                    machine.reg_write(UC_ARM_REG_R0, index)
                    machine.reg_write(UC_ARM_REG_SP, STACK)
                    machine.reg_write(UC_ARM_REG_LR, STOP)
                    machine.emu_start(BASE + start, BASE + stop, count=160)
                    if (machine.reg_read(UC_ARM_REG_R0) != expected or
                            machine.reg_read(UC_ARM_REG_PC) != BASE + stop or
                            machine.reg_read(UC_ARM_REG_SP) != STACK):
                        raise ValueError('Actual indexed COMMON selection differs')
                    slot['cases'].append({'route_fixture': route, 'selected_id': expected,
                                          'caller_array_and_native_selector_executed': True})
            else:
                slot['classification'] = ('caller-special-path' if index in (12, 16) else
                                          'null-slot-live-index-exclusion-unproven')
            slots.append(slot)
        rows.append({'caller_segment': [BASE + start, BASE + stop],
                     'producer_span_sha256': digest,
                     'array_region': [BASE + array_lo, BASE + array_hi],
                     'array_region_sha256': array_digest, 'slots': slots,
                     'region_extent_basis': '21 adjacent words ending at the next static pointer group; not a live bounds proof',
                     'upstream': '02081F54 searches 31 bytes through 020820DC, then dispatches object vtable+18; no-match and null-object return 24',
                     'limitations': 'Virtual method, object initialization, live role indexes and exclusion of null slots 9-11 remain unproved. Caller handles 12/16 separately and returns early for 24.'})
    return rows


def main():
    path = Path('work/clean.nds')
    if sha(path.read_bytes()) != CLEAN:
        raise ValueError('Exact clean ROM required')
    image = NdsImage.open(path)
    arm9 = image.read_file('/__arm9__.bin')
    for lo, hi, digest in (
            (0x53BD8, 0x53C24, '7a5d7e7bec7d01c3751cd8a4edcb76e1f3ade0d360d85c1fc8279821ca800075'),
            (0x53C6C, 0x53CB0, '3b7d87fb6d300e920646d37ecc693cdf295bbb4cccb0e3671513eca002184485')):
        if sha(arm9[lo:hi]) != digest:
            raise ValueError('Native four-route wrapper/selector differs')
    entries = common_message_entries(image.read_file('/COMMON/MESFILE.DK4'), arm9)
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    alternatives = {
        0x02012478: (0x1242C, 0x12494, 'fcdf933ac4157eedadd23907d9d0d693ef71c2214ec488f1fbaac731aae6dc00',
                     (0x12488, 0x1248C, 0x12490)),
        0x020125E0: (0x12574, 0x12604, '538d25991565b1915be9777d7019a16dd80ba94cec3a5edd8ec630a6cd42106e',
                     (0x125F0, 0x125F4, 0x125F8, 0x125FC)),
        0x020DB080: (0xDB024, 0xDB084, '67dc2271c7c31e82cb24e3af4857107e05db2ea44925f9667a461940d4f9d959',
                     (0xDB124,)),
    }
    for lo, hi, digest, _ in alternatives.values():
        if sha(arm9[lo:hi]) != digest:
            raise ValueError('Reviewed current-route branch producer differs')
    calls = []
    for offset in range(0, len(arm9) - 3, 4):
        word = struct.unpack_from('<I', arm9, offset)[0]
        target = direct_bl_target(word, BASE + offset)
        if target not in (BASE + 0x53C6C, BASE + 0x53BD8):
            continue
        lo = max(0, offset - 128)
        context = list(cs.disasm(arm9[lo:offset], BASE + lo))
        table = joined_context_argument(context, arm9, BASE, 'r0')
        values = None
        cases = []
        if table is not None and table % 4 == 0 and BASE <= table <= BASE + len(arm9) - 16:
            proposed = struct.unpack_from('<4I', arm9, table - BASE)
            if all(v == 0xFFFFFFFF or v < len(entries) for v in proposed):
                values = list(proposed)
                cases = [native_select(arm9, table, route) for route in range(4)]
        branches = []
        if BASE + offset in alternatives:
            lo_review, hi_review, digest, literals = alternatives[BASE + offset]
            for literal in literals:
                pointer = struct.unpack_from('<I', arm9, literal)[0]
                slots = list(struct.unpack_from('<4I', arm9, pointer - BASE))
                if any(v != 0xFFFFFFFF and v >= len(entries) for v in slots):
                    raise ValueError('Reviewed branch table is not native message IDs')
                branches.append({'literal_address': BASE + literal, 'table_address': pointer,
                                 'four_slots': slots,
                                 'native_route_fixture_cases': [native_select(arm9, pointer, route) for route in range(4)],
                                 'remaining_id_overlap': any(v in IDS for v in slots),
                                 'source_text': [None if v == 0xFFFFFFFF else entries[v].text.decode('cp932') for v in slots],
                                 'producer_span': [BASE + lo_review, BASE + hi_review],
                                 'producer_span_sha256': digest})
        calls.append({'call_address': BASE + offset, 'target': target, 'table_address': table,
                      'four_slots': values, 'native_route_fixture_cases': cases,
                      'reviewed_branch_alternatives': branches,
                      'remaining_id_overlap': None if values is None else any(v in IDS for v in values),
                      'source_text': None if values is None else [None if v == 0xFFFFFFFF else entries[v].text.decode('cp932') for v in values],
                      'context_span_sha256': sha(arm9[lo:offset + 4]),
                      'context': [f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in context],
                      'classification': ('locally-resolved-table' if values is not None else
                                         'reviewed-long-span-alternatives' if branches else
                                         'incoming-or-branch-alternative-table-unresolved')})
    report = {'status': 'four-route-selector-inventory-not-global-bounds-proof',
              'source_rom_sha256': CLEAN,
              'selector_span_sha256': sha(arm9[0x53C6C:0x53CB0]),
              'calls': calls,
              'indexed_table_regions': indexed_tables(arm9, entries),
              'additional_wrapper': {'entry': BASE + 0x53BD8,
                                     'argument': 'incoming r0 saved at sp+8 after two pushes',
                                     'forwarded_selector': BASE + 0x53C6C,
                                     'following_common_accessor': BASE + 0x5528C,
                                     'span_sha256': sha(arm9[0x53BD8:0x53C24])},
              'limitations': ['Primary route values 0 through 3 are fixtures; live writers remain unbounded.',
                              'The native fallback loop reads four slots; no primary-index clamp exists here.',
                              'Only direct ARM BL sites in the main serialized ARM9 are scanned.',
                              'Local resolution does not prove function boundaries or gameplay reachability.',
                              'Branch alternatives and incoming pointers require separate mapping.']}
    altered = bytearray(arm9)
    altered[0x12768] ^= 1
    try:
        indexed_tables(altered, entries)
    except ValueError:
        report['changed_indexed_load_rejected'] = True
    else:
        raise ValueError('Changed indexed load was incorrectly accepted')
    Path('work/analysis/current_route_common_tables_clean.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'calls': len(calls), 'resolved_tables': sum(c['four_slots'] is not None for c in calls),
                      'reviewed_branch_tables': sum(len(c['reviewed_branch_alternatives']) for c in calls),
                      'native_cases': sum(len(c['native_route_fixture_cases']) + sum(len(b['native_route_fixture_cases']) for b in c['reviewed_branch_alternatives']) for c in calls)}))
    print(json.dumps({'indexed_caller_cases': sum(len(s['cases']) for r in report['indexed_table_regions'] for s in r['slots']),
                      'indexed_nonnull_tables': sum(bool(s['table_address']) for r in report['indexed_table_regions'] for s in r['slots'])}))
    for call in calls:
        print(hex(call['call_address']), call['table_address'], call['four_slots'])


if __name__ == '__main__':
    main()
