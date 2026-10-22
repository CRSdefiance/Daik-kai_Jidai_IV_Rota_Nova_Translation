"""All378 restored actors, complete body words and original native VM cursor."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.message_actor_integrity import repair
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine

ROOT = Path('work/analysis/message_actor_integrity_v296')


def execute(arm, data, at):
    cpu = machine(arm)
    obj, counter = 0x02460000, 0x0245F000
    source = data[at - 5:]
    cpu.mem_write(obj, source)
    cpu.mem_write(counter, struct.pack('<I', 100))
    cpu.reg_write(UC_ARM_REG_R4, counter)
    cpu.reg_write(UC_ARM_REG_R5, obj)
    sp = cpu.reg_read(UC_ARM_REG_SP)
    draws = []

    def observe(uc, address, size, _):
        if address == 0x0202425C:
            pointer = uc.reg_read(UC_ARM_REG_R1)
            body = bytes(uc.mem_read(pointer, 512)).split(b'\0', 1)[0]
            draws.append((uc.reg_read(UC_ARM_REG_R0), body))
            # External display call is a contract; native byte scan and cursor
            # rounding after its return execute original instructions.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    cpu.hook_add(UC_HOOK_CODE, observe)
    cpu.emu_start(0x02029B18, 0x02029BC0, count=10000)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x02029BC0
    assert cpu.reg_read(UC_ARM_REG_SP) == sp and cpu.reg_read(UC_ARM_REG_R5) == obj
    assert bytes(cpu.mem_read(obj, len(source))) == source
    assert len(draws) == 1
    cursor = struct.unpack('<I', cpu.mem_read(counter, 4))[0]
    return draws[0], cursor


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    image = NdsImage.open('out/all_routes_combined_v275_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    census_path = Path('work/analysis/held_actor_v295/current_actor_preservation_census.json')
    census = json.loads(census_path.read_text(encoding='utf-8'))
    paths = sorted({row['file_path'] for row in census['mismatches']})
    sources = {path: image.read_file(path) for path in paths}
    target, report = repair(sources, {path: clean.read_file(path) for path in paths}, census)
    arm = image.read_file('/__arm9__.bin')
    parsed = {path: IlnkContainer.parse(raw).blocks for path, raw in target.items()}
    before = {path: IlnkContainer.parse(raw).blocks for path, raw in sources.items()}
    cases = []
    for row in report['records']:
        path, block, at = [row[k] for k in ('file_path', 'block', 'actor_offset')]
        old_draw, old_cursor = execute(arm, before[path][block], at)
        new_draw, new_cursor = execute(arm, parsed[path][block], at)
        assert old_draw[0] != row['actor'] and new_draw[0] == row['actor']
        assert new_draw[1].decode('cp932').split() == bytes.fromhex(row['old_hex']).decode('cp932').split()
        assert old_cursor == new_cursor
        cases.append({'file_path': path, 'id': row['id'], 'actor': new_draw[0],
                      'complete_native_body_hex': new_draw[1].hex(),
                      'all_original_visible_words_and_macros_preserved': True,
                      'native_VM_cursor_same': new_cursor, 'method': row['method']})
    assert len(cases) == 378
    config = {'format': 'dk4-message-actor-integrity-release-v1',
              'census': str(census_path), 'census_sha256': sha(census_path.read_bytes()),
              'source_file_sha256': report['source_file_sha256'],
              'target_file_sha256': report['target_file_sha256'],
              'status': 'research-native-control-proof-complete-actual-release-display-pending'}
    Path('translations/message_actor_integrity_release_v1.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    proof = {'format': 'dk4-native-message-actor-integrity-v296', 'cases': cases,
             'all378_native_actors_bodies_and_VM_cursors_verified': True,
             'all_words_macros_block_archive_and_following_command_addresses_preserved': True,
             'native_display_call_is_explicit_bridge': True,
             'native_graphics_fonts_code_and_arm7_unchanged': True,
             'actual_full_registered_ROM_release_display_pending': True,
             'all18_plaque_hint_entries_and_variants_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'transform_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('378 native actor/body cases and378 unchanged VM cursors pass; no prose or macro discarded.')


if __name__ == '__main__':
    main()
