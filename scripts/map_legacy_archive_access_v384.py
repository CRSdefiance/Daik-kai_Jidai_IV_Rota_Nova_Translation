"""Map current native archive/file-open references without claiming unused data."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, Cs
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROM = Path('out/all_routes_combined_v383_candidate.nds')
ROOT = Path('work/analysis/legacy_archive_access_v384')
TARGETS = {0x020D2018: 'ILNK archive open', 0x020D1EF0: 'ILNK block read',
           0x020DED50: 'SDK filesystem open'}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    units = [(f'ARM9 section {i}', s.ramAddress, bytes(s.data))
             for i, s in enumerate(MainCodeFile(rom.read_file('/__arm9__.bin'), 0x02000000).sections)]
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid])
    units += [(f'ARM9 overlay {i}', s.ramAddress, bytes(s.data)) for i, s in overlays.items()]
    arm, thumb = Cs(CS_ARCH_ARM, CS_MODE_ARM), Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    calls, pointers, stems = [], [], []
    for label, base, data in units:
        for offset in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, offset)[0]
            if word & ~1 in TARGETS:
                pointers.append({'unit': label, 'address': base + offset, 'target': word})
            if word & 0x0F000000 != 0x0B000000:
                continue
            delta = word & 0xFFFFFF
            if delta & 0x800000:
                delta -= 0x1000000
            target = base + offset + 8 + delta * 4
            if target not in TARGETS:
                continue
            lo, hi = max(0, offset - 64), min(len(data), offset + 12)
            context = [{'address': i.address, 'instruction': i.mnemonic + ' ' + i.op_str}
                       for i in arm.disasm(data[lo:hi], base + lo)]
            literals = []
            for i in arm.disasm(data[lo:offset], base + lo):
                if i.mnemonic == 'ldr' and i.op_str.startswith('r1, [pc, #'):
                    displacement = int(i.op_str.split('#')[1].split(']')[0], 0)
                    location = i.address + 8 + displacement
                    if base <= location <= base + len(data) - 4:
                        value = struct.unpack_from('<I', data, location - base)[0]
                        for _, other_base, other in units:
                            if other_base <= value < other_base + len(other):
                                raw = other[value - other_base:].split(b'\0', 1)[0]
                                if raw and len(raw) < 128 and all(32 <= b < 127 for b in raw):
                                    literals.append({'load': i.address, 'literal': location,
                                                     'pointer': value, 'ASCII': raw.decode('ascii'),
                                                     'argument_dataflow_not_proven': True})
            calls.append({'unit': label, 'address': base + offset, 'target': target,
                          'operation': TARGETS[target], 'mode': 'ARM', 'context': context,
                          'nearby_r1_string_literals': literals})
        for offset in range(0, len(data) - 3, 2):
            first, second = struct.unpack_from('<2H', data, offset)
            if first & 0xF800 != 0xF000 or second & 0xF800 not in (0xE800, 0xF800):
                continue
            for i in thumb.disasm(data[offset:offset + 4], base + offset, count=1):
                if i.mnemonic in ('bl', 'blx') and i.op_str.startswith('#0x'):
                    target = int(i.op_str[1:], 16)
                    if target in TARGETS:
                        calls.append({'unit': label, 'address': i.address, 'target': target,
                                      'operation': TARGETS[target], 'mode': 'Thumb'})
        for stem in (b'CMMNIMG', b'SLACKIMG', b'WINFRAME'):
            start = 0
            while (offset := data.upper().find(stem, start)) >= 0:
                lo = data.rfind(b'\0', max(0, offset - 128), offset) + 1
                hi = data.find(b'\0', offset)
                address = base + lo
                refs = [{'unit': n, 'address': b + p}
                        for n, b, d in units for p in range(0, len(d) - 3, 4)
                        if struct.unpack_from('<I', d, p)[0] in (address, base + offset)]
                stems.append({'unit': label, 'address': address, 'string_hex': data[lo:hi].hex(),
                              'ASCII': data[lo:hi].decode('ascii'), 'aligned_literal_references': refs})
                start = offset + len(stem)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'units': [{'unit': n, 'base': b, 'bytes': len(d), 'sha256': sha(d)} for n, b, d in units],
             'targets': {hex(k): v for k, v in TARGETS.items()}, 'direct_calls': calls,
             'aligned_function_pointer_candidates': pointers, 'resource_stems': stems,
             'available_save_exports_hidden_gallery_flags': {
                 name: struct.unpack_from('<H', (Path('work/emulation_v193') / name / 'final_arm9_ram.bin').read_bytes(), 0x27985C)[0]
                 for name in ('plaque_voyage_v379', 'crew_voyage_v380', 'weapon_acquisition_v381')},
             'scope': 'Direct aligned ARM BL, direct Thumb BL/BLX, aligned function pointers and ASCII resource stems in all current main-code sections and declared ARM9 overlays. Context/literal candidates require dataflow review. Computed filenames, numeric file IDs, indirect calls and runtime reachability are not excluded.',
             'unused_resource_claim': False, 'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'access_census.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Native access census:', len(calls), 'direct calls;', len(pointers), 'pointer candidates;', len(stems), 'resource stems.')
    for c in calls:
        print(hex(c['address']), c['operation'], [r['ASCII'] for r in c.get('nearby_r1_string_literals', [])])


if __name__ == '__main__':
    main()
