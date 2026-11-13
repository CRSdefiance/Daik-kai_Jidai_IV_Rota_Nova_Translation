"""Source-reviewed no-growth Tavern announcement research and native printf ABI."""

import json
from pathlib import Path

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path('work/analysis/tavern_round_v382')
ROM = Path('out/all_routes_combined_v378_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    manuscript = Path('translations/tavern_round_announcement_manuscript_v1.json')
    document = json.loads(manuscript.read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    row = document['records'][0]
    clean, parent = NdsImage.open('work/clean.nds'), NdsImage.open(ROM)
    arm = parent.read_file('/__arm9__.bin')
    common = parent.read_file('/COMMON/MESFILE.DK4')
    original = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    before = common_message_entries(common, arm, clean=False)
    assert bytes.fromhex(row['source_hex']) == original[872].text
    assert len(document['records']) == 1 and row['message_id'] == 872
    assert (row['block'], row['record']) == (original[872].block, original[872].record_index)
    audit = audit_native_common_entry(before[872].text, row['english'])
    assert not [issue for issue in audit['issues'] if issue['severity'] in ('warning', 'error')], audit['issues']
    raw = row['english'].removesuffix('{PAD}').encode('cp932')
    assert raw == b"This round's on %s. Enjoy!" and raw.count(b'%s') == 1
    container = IlnkContainer.parse(common)
    block = bytearray(container.blocks[before[872].block])
    start = before[872].block_offset
    block[start:start + len(before[872].text)] = raw.ljust(len(before[872].text), b' ')
    container.blocks[before[872].block] = bytes(block)
    target = container.to_bytes()
    assert len(target) == len(common)
    after = common_message_entries(target, arm, clean=False)
    assert [i for i in range(3668) if before[i].text != after[i].text] == [872]
    assert all((a.block, a.start, a.end, a.copy_end) == (b.block, b.start, b.end, b.copy_end)
               for a, b in zip(before, after))
    u = machine(arm)
    output, fmt, name_at, address_at = STACK + 0x1000, STACK + 0x2000, STACK + 0x2100, STACK + 0x2200
    cases = []
    for name in ('Bergstrom', 'Argot Co.', 'Castor Co.', 'Li Co.', 'Custom Trading Company'):
        for address in ('旦那', '姉さん'):
            u.mem_write(output - 16, b'\xA5' * 288)
            u.mem_write(fmt, raw + b'\0')
            u.mem_write(name_at, name.encode() + b'\0')
            u.mem_write(address_at, address.encode('cp932') + b'\0')
            call(u, 0xD7720, (output, fmt, name_at, address_at))
            expected = raw.replace(b'%s', name.encode()) + b'\0'
            assert bytes(u.mem_read(output, len(expected))) == expected
            assert bytes(u.mem_read(output - 16, 16)) == b'\xA5' * 16
            assert bytes(u.mem_read(output + len(expected), 272 - len(expected))) == b'\xA5' * (272 - len(expected))
            assert bytes(u.mem_read(name_at, len(name) + 1)) == name.encode() + b'\0'
            assert bytes(u.mem_read(address_at, len(address.encode('cp932')) + 1)) == address.encode('cp932') + b'\0'
            cases.append({'name': name, 'original_address': address, 'complete_native_output': expected[:-1].decode(),
                          'unused_original_second_argument_safe': True})
    (ROOT / 'target_common.bin').write_bytes(target)
    parent.replace_file('/COMMON/MESFILE.DK4', target)
    parent.save(ROOT / 'research_only_tavern.nds')
    proof = {'source_common_sha256': sha(common), 'target_common_sha256': sha(target),
             'arm9_sha256': sha(arm), 'changed_message_IDs': [872],
             'all3668_offsets_bounds_copy_extents_and_other_messages_exact': True,
             'no_growth_no_runtime_code_or_address_table_changes': True,
             'native_printf_cases': cases, 'source_japanese_hex': row['source_hex'],
             'natural_dialogue_QA': audit, 'research_only_actual_render_pending': True}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    replay = json.loads(Path('work/emulation_v193/weapon_acquisition_v381/capture_report.json').read_text(encoding='utf-8'))
    (ROOT / 'inputs.json').write_text(json.dumps(replay['scripted_input_schedule'], indent=2) + '\n', encoding='utf-8')
    print('Tavern872: natural QA, all3668 ownership/bounds and10 actual native printf cases pass.')


if __name__ == '__main__':
    main()
