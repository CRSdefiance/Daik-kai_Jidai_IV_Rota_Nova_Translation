"""Trace real town draw entries without filtering pointer values or dimensions."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path('work/analysis/town_call_trace_v498')
ENTRY, TRACE = 0x01FFC504, 0x01FFC5C0


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = Path('out/all_routes_combined_v484_candidate.nds')
    rom = NdsImage.open(parent)
    source = rom.read_file('/__arm9__.bin')
    assert sha(source) == 'b03327187284a6ac560bf76ff442d75f9caa34c6b130438b582a44f2baf37c5b'
    code = MainCodeFile(source, 0x02000000)
    section = code.sections[4]
    assert section.data[ENTRY - 0x01FFC000:0x600] == bytes(0x600 - (ENTRY - 0x01FFC000))
    sites = []
    for i, (name, offset, expected) in enumerate((('town_draw', 0xB5B14, 0xE92D4FF0),
                                                ('descriptor_compose', 0xD470C, 0xE92D40F0),
                                                ('styled_draw', 0xD135C, 0xE92D40F0))):
        assert struct.unpack_from('<I', source, offset)[0] == expected
        entry = ENTRY + i * 40
        buffer = TRACE + i * 20
        text = f'''push {{r0-r3,ip,lr}}
ldr ip,record
stm ip,{{r0-r3}}
ldr r0,[ip,#16]
add r0,r0,#1
str r0,[ip,#16]
pop {{r0-r3,ip,lr}}
.word {expected}
b {0x02000000 + offset + 4}
record: .word {buffer}
'''
        blob = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(text, entry)[0])
        assert len(blob) == 40
        start = entry - section.ramAddress
        section.data[start:start + len(blob)] = blob
        struct.pack_into('<I', code.sections[0].data, offset,
                         0xEA000000 | (branch_link(0x02000000 + offset, entry) & 0xFFFFFF))
        (ROOT / f'{name}.asm').write_text(text)
        sites.append({'name': name, 'offset': offset, 'entry': entry, 'trace': buffer,
                      'continuation': 0x02000000 + offset + 4, 'prefix': expected})
    arm = bytes(code.save())
    assert len(arm) == len(source)
    rom.replace_file('/__arm9__.bin', arm)
    path = ROOT / 'research_only_town_call_trace.nds'
    rom.save(path)
    (ROOT / 'research_arm9.bin').write_bytes(arm)
    report = {'research_only': True, 'parent': str(parent), 'parent_sha256': sha(parent.read_bytes()),
              'research_ROM': str(path), 'research_ROM_sha256': sha(path.read_bytes()), 'sites': sites,
              'every_call_records_original_R0_R3': True, 'original_function_prologues_replayed': True,
              'no_added_allocation_or_free': True, 'not_for_handoff': True}
    (ROOT / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Prepared unfiltered town/descriptor/style entry traces; original execution retained.')


if __name__ == '__main__':
    main()
