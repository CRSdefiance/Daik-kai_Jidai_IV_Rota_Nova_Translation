"""Earlier whole native outputs and actual company-leader argument combinations."""

import struct
from itertools import product
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE

from dk4tool.patch import tavern_editorial_runtime as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_common import compile_text
from dk4tool.patch.shipyard_editorial import BANKS as OLD_BANKS
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
import scripts.probe_shipyard_runtime_v759 as yard
import scripts.probe_tavern_conversations_v764 as tavern
import scripts.verify_market_balanced_owners_v757 as old_scope
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_storage_v764')


def main():
    arm = NdsImage.open(tavern.CURRENT).read_file('/__arm9__.bin')
    proof = read(ROOT / 'owned_storage_and_native_research.json')
    assert proof['source_ARM9_sha256'] == sha(arm)
    assert proof['module_sha256'] == sha(Path(owned.__file__).read_bytes())
    writes = []
    def loaded(changed=True):
        u = tavern.loaded(arm, False)
        if changed:
            for patch in proof['patches']:
                before, after = bytes.fromhex(patch['source_hex']), bytes.fromhex(patch['target_hex'])
                assert bytes(u.mem_read(patch['address'], len(before))) == before
                u.mem_write(patch['address'], after)
        def watch(cpu, kind, at, size, value, unused):
            if any(at < hi and at + size > lo for lo, hi in (*OLD_BANKS, *owned.BANKS)):
                writes.append([at, size, value]); raise AssertionError('Native write into immutable source bank')
        u.hook_add(UC_HOOK_MEM_WRITE, watch)
        return u
    yard.call = call; old_scope.call = call
    yard.YESNO = (*yard.YESNO, 1246)
    old_cases = read('work/analysis/shipyard_editorial_v759/typed_literal_runtime_RESEARCH/native_layout_matrix.json')['cases']
    paragraphs = {r['message_id']: compile_text(r) for r in read('translations/shipyard_editorial_manuscript_v3.json')['records']}
    yard_results = []
    for i, old in enumerate(old_cases):
        if i % 64 == 0: u = loaded()
        result = yard.layout(u, paragraphs[old['id']], old['id'], tuple(bytes.fromhex(v) for v in old['values_hex']))
        assert (result['formatted_hex'], result['lines']) == (old['formatted_hex'], old['lines'])
        yard_results.append(result)
    assert len(yard_results) == 1124
    port = []
    for old in read('work/analysis/port_services_v762/native_owned/verification.json')['complete_native_font_cases']:
        if old['id'] == 267:
            port.append({'id': 267, 'unchanged_system_template_hex': old['template_hex'], 'new_runtime_does_not_touch_system_consumer': True})
            continue
        result = yard.layout(loaded(), bytes.fromhex(old['template_hex']), old['id'], tuple(bytes.fromhex(v) for v in old['values_hex']))
        assert (result['formatted_hex'], result['lines']) == (old['formatted_hex'], old['lines'])
        port.append(result)
    controls = []
    for parent, n, text in product((0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8),
            (676, 677, 761, 767, 768, 769, 770, 388, 1000),
            ('A clear sentence.', 'An ordinary paragraph with several words to check wrapping and complete letters.',
             "A longer ordinary sentence needs a natural ending, so let's check every line and the final words.",
             'Here is one more ordinary paragraph. It has a few short words and a longer final sentence.')):
        values = []
        for changed in (False, True):
            cpu = loaded(changed)
            cpu.mem_write(STACK + 0x270, bytes(4)); cpu.mem_write(STACK + 0x27C, struct.pack('<I', 0x021184C0))
            values.append(old_scope.scope_output(cpu, text.encode('ascii'), n, (), parent))
        assert values[0] == values[1]
        controls.append({'parent': parent, 'id': n, 'input': text, 'complete_native_output_equal': True})
    save(ROOT / 'inherited_outputs.json', {'source_ARM9_sha256': sha(arm), 'all1124_Yard_outputs': yard_results,
        'all40_Port_cases': port, 'all180_earlier_parent_output_controls': controls,
        'native_bank_writes': writes, 'producer_sha256': sha(Path(__file__).read_bytes())})
    print('1124 Yard,40 Port cases and180 full earlier output controls pass.', flush=True)
    # Source59B38..59BDC enumerates20 companies. Resolve the actual leader name,
    # including the current-admiral special object, rather than assuming a full name.
    inventory = read(ROOT / 'actual_native_person_arguments.json')
    people = [bytes.fromhex(r['name_hex']) for r in inventory['actual20_company_leader_resolutions'] if r['status'] == 'actual-native-leader-name']
    towns = [bytes.fromhex(r['name_hex']) for r in read('work/analysis/tavern_conversations_v763/native_context.json')['actual90_town_names']]
    manuscript = read(tavern.MANUSCRIPT)
    cases, findings = [], []
    for row in (r for r in manuscript['records'] if r['message_id'] in (820, 821)):
        for i, args in enumerate(product(people, towns, owned.PROFESSIONS)):
            if i % 64 == 0: u = loaded()
            result = tavern.format_case(u, row, args)
            cases.append(result)
            if result['findings']: findings.append(result)
            if i and i % 2048 == 0: print(f'Actual leader ID{row["message_id"]}: {i} cases.', flush=True)
    save(ROOT / 'actual_leader_layout_matrix.json', {'count': len(cases), 'findings': findings, 'cases': cases,
        'source_name_inventory_sha256': sha((ROOT / 'actual_native_person_arguments.json').read_bytes()),
        'native_bank_writes': writes, 'scope': 'All current20 company-leader names x90 towns x4 professions x2 paragraphs; supplied combinations are not all claimed earned or legal world states.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    assert not findings and not writes
    print(f'{len(cases)} actual leader-name layouts pass; earlier outputs preserved. Research only.', flush=True)


if __name__ == '__main__': main()
