"""Map real barmaids,original dialogue branches and exact first-name providers."""

import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
                               UC_ARM_REG_LR, UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/barmaid_editorial_v779')
CURRENT = Path('out/all_routes_combined_v778_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    report_path = Path('E:/Rota Nova translations/Generated/work/emulation_v193/followup_v778_bribe_live/capture_report.json')
    report = read(report_path)
    snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == 3200)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256'] and report['ROM_sha256'] == sha(CURRENT.read_bytes())
    spans = [(0x79D8, 0x7A28), (0x58F4C, 0x59138), (0x59358, 0x5950C),
             (0x5950C, 0x59784), (0x59F38, 0x59FA0), (0x1371C, 0x13724)]
    for a, b in spans:
        assert arm[a:b] == clean[a:b]
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)
    def ptr(p): return struct.unpack('<I', u.mem_read(p, 4))[0]
    def text(p): return bytes(u.mem_read(p, 160)).split(b'\0')[0]
    def name(obj, method=8): return text(get(ptr(ptr(obj)+method)-BASE, (obj,)))
    officers, towns = get(0xCB184), get(0xCB178)
    first_owner = officers+struct.unpack_from('<I', arm, 0x59774)[0]
    first_name = name(first_owner, 0x20)
    assert first_name == b'Hodram' and ptr(ptr(first_owner)+0x20) == BASE+0x1371C
    assert get(0x1371C, (first_owner,)) == first_owner+0x20
    catalog = []
    all_lookup = []
    for town_id in range(114):
        row = get(0x79D8, (town_id,))
        all_lookup.append({'town_ID': town_id, 'information_row': row})
        if not row:
            continue
        info = bytes(u.mem_read(row, 3))
        assert info[1] == town_id and info[0] < 207
        obj = officers+4+32*info[0]
        catalog.append({'town_ID': town_id, 'information_row': row, 'information_hex': info.hex(),
                        'town_name_hex': name(towns+4+108*town_id).hex(), 'actor_index': info[0],
                        'object': obj, 'name_hex': name(obj).hex(), 'name': name(obj).decode('cp932')})
    assert len(catalog) == 21 and len({r['object'] for r in catalog}) == 21
    captain = {'object': first_owner, 'first_name_hex': first_name.hex(),
               'name_getter': BASE+0x1371C, 'field_offset': 0x20,
               'current_snapshot_name_not_a_new_glossary_choice': True}
    observed, cases = [], []
    def observe(c, pc, size, unused):
        n = c.reg_read(UC_ARM_REG_R1)
        argc = 2 if n in (989, 990) else 1 if n == 999 else 0
        observed.append({'id': n, 'speaker_object': c.reg_read(UC_ARM_REG_R0),
                         'arguments_hex': [text(c.reg_read(r)).hex() for r in (UC_ARM_REG_R2, UC_ARM_REG_R3)[:argc]]})
        c.emu_stop()
    hook = u.hook_add(UC_HOOK_CODE, observe, begin=BASE+0x53FE4, end=BASE+0x53FE4)
    try:
        def run(start, end, regs):
            observed.clear()
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            for reg, value in regs:
                u.reg_write(reg, value)
            u.emu_start(BASE+start, BASE+end if end else STOP, count=10000)
            assert len(observed) == 1
            return dict(observed[0])
        for row in catalog:
            obj, town_id = row['object'], row['town_ID']
            intro = run(0x5964C, None, ((UC_ARM_REG_R0, 0), (UC_ARM_REG_R1, town_id), (UC_ARM_REG_R2, obj)))
            expected = 989 if town_id in (5, 13, 25) else 990 if town_id in (34, 38, 47) else 827
            assert intro['id'] == expected and intro['speaker_object'] == obj
            want = [bytes.fromhex(row['name_hex']), first_name] if expected == 989 else [first_name, bytes.fromhex(row['name_hex'])] if expected == 990 else []
            assert intro['arguments_hex'] == [s.hex() for s in want]
            cases.append({'kind': 'first-introduction', 'town_ID': town_id, **intro})
            casual = run(0x58F4C, None, ((UC_ARM_REG_R0, 0), (UC_ARM_REG_R1, town_id), (UC_ARM_REG_R2, obj)))
            assert casual['speaker_object'] == obj and casual['id'] in {*range(1003, 1020), 998}
            cases.append({'kind': 'city-specific-casual-chat', 'town_ID': town_id, **casual})
            gift = run(0x5950C, None, ((UC_ARM_REG_R0, 0), (UC_ARM_REG_R1, town_id), (UC_ARM_REG_R2, obj), (UC_ARM_REG_R3, 0)))
            assert gift['speaker_object'] == obj
            assert gift['id'] in (999, 1000, 1001, 1002, 840)
            assert gift['arguments_hex'] == ([first_name.hex()] if gift['id'] == 999 else [])
            cases.append({'kind': 'city-specific-special-gift-response', 'town_ID': town_id, **gift})
            # Begin after the original one-in-three branch is selected;leave its
            # randomness untouched and make no probabilistic gameplay claim.
            ordinary = run(0x59378, 0x59490, ((UC_ARM_REG_R6, town_id), (UC_ARM_REG_R5, obj)))
            assert ordinary['speaker_object'] == obj and 991 <= ordinary['id'] <= 998
            cases.append({'kind': 'original-selected-ordinary-chat-branch', 'town_ID': town_id, **ordinary})
        catalog_IDs = {r['id'] for r in cases}
        assert set(range(989, 1020))-catalog_IDs == {996}
        osaka = next(r for r in catalog if r['town_ID'] == 59)
        assert get(0x79D8, (58,)) == 0
        latent = run(0x59378, 0x59490, ((UC_ARM_REG_R6, 58), (UC_ARM_REG_R5, osaka['object'])))
        assert latent['id'] == 996 and latent['speaker_object'] == osaka['object']
    finally:
        u.hook_del(hook)
    missing = sorted(set(range(989, 1020)) - {r['id'] for r in cases})
    save(ROOT/'city_branch_research.json', {'catalog': catalog, 'cases': cases, 'unobserved_IDs': missing,
                                           'not_complete_context_proof': bool(missing)})
    assert missing == [996]
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    disassembly = [{'span': [a, b], 'sha256': sha(clean[a:b]),
                    'instructions': [{'address': x.address, 'mnemonic': x.mnemonic, 'operands': x.op_str}
                                     for x in cs.disasm(clean[a:b], BASE+a)]} for a, b in spans]
    save(ROOT/'native_context.json', {'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
                                      'source_ARM9_sha256': sha(clean), 'current_ARM9_sha256': sha(arm),
                                      'capture_report': str(report_path), 'pre_fixture_snapshot': snapshot,
                                      'all114_native_city_information_lookups': all_lookup, 'all21_original_barmaids': catalog,
                                      'original_mutable_captain_first_name': captain,
                                      'all84_original_city_and_name_provider_cases': cases,
                                      'all30_catalog_selected_IDs': sorted({r['id'] for r in cases if 989 <= r['id'] <= 1019}),
                                      'latent996_source_branch': {**latent, 'supplied_city_ID': 58,
                                          'supplied_actor_from_city_ID': 59,
                                          'not_a_valid_current_catalog_city_actor_pair': True,
                                          'source_lookup58_is_null': True,
                                          'normal_reachability_not_yet_closed': True},
                                      'source_current_context_spans': disassembly,
                                      'intro989_argument_order': ['barmaid', 'captain_first_name'],
                                      'intro990_argument_order': ['captain_first_name', 'barmaid'],
                                      '999_argument': 'captain_first_name',
                                      'source_branches_not_inferred_from_message_adjacency': True,
                                      'no_actual_gameplay_or_gift_acquisition_claim': True,
                                      'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('21 actual barmaids,114 lookups and84 original callers cover30 entries;996 has a separate latent source branch,normal reachability open.', flush=True)


if __name__ == '__main__':
    main()
