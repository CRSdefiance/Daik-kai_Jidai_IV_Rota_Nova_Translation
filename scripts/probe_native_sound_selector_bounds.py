"""Execute BGM selector bounds/COMMON lookups; distinguish adjacent SFX path."""

import argparse
import json
import struct
from pathlib import Path

from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.execute_map_entity_tooltip_copy import BASE, machine_for
from scripts.probe_common_copy_arm946_alignment import arm946_machine

OBJECT = 0x02430000


def update(source, index, delta):
    machine = machine_for(source)
    machine.mem_write(OBJECT + 0x108, struct.pack('<I', index))
    machine.reg_write(UC_ARM_REG_R4, OBJECT)
    machine.reg_write(UC_ARM_REG_R1, delta & 0xFFFFFFFF)
    machine.emu_start(BASE + 0x108FC0, BASE + 0x108FE0, count=100)
    result = struct.unpack('<I', machine.mem_read(OBJECT + 0x108, 4))[0]
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x108FE0 or not 2 <= result <= 39:
        raise ValueError('Actual BGM selector update escapes native range 2 through 39')
    return {'index': index, 'delta': delta, 'result': result}


def select(source, common, index):
    machine = arm946_machine(source)
    owner = struct.unpack_from('<I', source, 0x552A0)[0]
    block_id = common_message_entries(common, source, clean=False)[3249 + index].block
    block = bytes(IlnkContainer.parse(common).blocks[block_id])
    machine.mem_write(owner + 0x2C, bytes((block_id, 255, 0, 1)))
    machine.mem_write(owner + 0x30, block)
    machine.mem_write(OBJECT + 0x108, struct.pack('<I', index))
    machine.reg_write(UC_ARM_REG_R5, OBJECT)
    machine.emu_start(BASE + 0x109268, BASE + 0x109278, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x109278:
        raise ValueError('Native BGM lookup fails to reach drawing setup')
    raw = bytes(machine.mem_read(machine.reg_read(UC_ARM_REG_R0), 256)).split(b'\0', 1)[0]
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-v155', action='store_true')
    args = parser.parse_args()
    clean_path = Path('work/clean.nds')
    candidate_path = Path('out/all_routes_combined_v155_candidate.nds' if args.current_v155
                          else 'out/all_routes_combined_v143_candidate.nds')
    if sha(clean_path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Exact clean source required')
    expected = ('d704b60955db30d27b3d48858107096934fd2af08ecd1f3bf3fc2ba4dd884b11' if args.current_v155
                else '2c4cf489bfaaff8b187744e085a0ee8314dc10e4054048f60e9156cf5d786984')
    if sha(candidate_path.read_bytes()) != expected:
        raise ValueError('Exact complete source candidate required')
    clean, candidate = NdsImage.open(clean_path), NdsImage.open(candidate_path)
    source = clean.read_file('/__arm9__.bin')
    arm9, common = candidate.read_file('/__arm9__.bin'), candidate.read_file('/COMMON/MESFILE.DK4')
    spans = ((0x108FC0, 0x108FE0), (0x1090D0, 0x1090D8), (0x109268, 0x109278), (0x109308, 0x10930C))
    if any(source[a:b] != arm9[a:b] for a, b in spans):
        raise ValueError('BGM selector code/base changes from clean source')
    updates = [update(arm9, i, d) for i in range(2, 40) for d in (-1, 1, -100, 100)]
    machine = machine_for(arm9)
    machine.reg_write(UC_ARM_REG_R5, OBJECT)
    machine.emu_start(BASE + 0x1090D0, BASE + 0x1090D8, count=10)
    if struct.unpack('<I', machine.mem_read(OBJECT + 0x108, 4))[0] != 2:
        raise ValueError('Native BGM initialization differs from index two')
    entries = common_message_entries(common, arm9, clean=False)
    cases = []
    for index in range(2, 40):
        raw = select(arm9, common, index)
        entry = entries[3249 + index]
        if raw != entry.text or not raw or any(c > 127 for c in raw):
            raise ValueError('Native BGM selector loses complete English title or selects wrong message')
        cases.append({'index': index, 'native_id': entry.message_id, 'english': raw.decode('ascii'),
                      'complete_native_lookup_matches_saved_selection': True})
    table = struct.unpack_from('<I', source, 0x108CB4)[0]
    sfx_audio = list(source[table - BASE:table - BASE + 59])
    report = {'status': 'pass-bgm-local-selector-bounds-and-native-common-lookups',
              'candidate_sha256': sha(candidate_path.read_bytes()), 'source_arm9_sha256': sha(source),
              'candidate_arm9_sha256': sha(arm9), 'ARM946_copy_alignment_explicitly_modeled': True,
              'code_spans': [{'start': BASE + a, 'end': BASE + b, 'sha256': sha(source[a:b])} for a, b in spans],
              'updates': updates, 'native_title_cases': cases, 'native_id_range': [3251, 3288],
              'native_initial_index': 2,
              'sfx_audio_lookup_table': {'address': table, 'values': sfx_audio,
                  'classification': 'Adjacent SFX path uses +10C to select a separate pointer title table at 02108EC0; its +108 audio IDs must not be combined with the BGM native-ID base.'},
              'limitations': 'Proves reviewed BGM initialization/update/lookup paths, not exclusive global writers or gameplay reachability. Other constructors, SFX pointer-table bounds, complete title rendering, physical audio/input and remaining promotional consumers need separate verification.'}
    output = ('work/analysis/native_sound_selector_bounds_v155_proof.json' if args.current_v155
              else 'work/analysis/native_sound_selector_bounds_proof.json')
    Path(output).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(updates)} native BGM updates and {len(cases)} complete English lookups pass; reviewed range excludes promotional IDs.')


if __name__ == '__main__':
    main()
