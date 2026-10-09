"""Conservative preexisting pointer/branch inventory for the ITCM extension."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_monthly_word_wrap_hook import prepare


def references(raw, base, lo, hi):
    found = []
    for offset in range(0, len(raw) - 3, 4):
        value = struct.unpack_from('<I', raw, offset)[0]
        if lo <= value < hi:
            found.append({'address': base + offset, 'kind': 'aligned-pointer', 'target': value})
        if value & 0x0E000000 == 0x0A000000 and value >> 28 != 15:
            displacement = (value & 0xFFFFFF) << 2
            if displacement & (1 << 25):
                displacement -= 1 << 26
            target = base + offset + 8 + displacement
            if lo <= target < hi:
                found.append({'address': base + offset, 'kind': 'arm-branch-candidate', 'target': target})
    for offset in range(0, len(raw) - 3, 2):
        first, second = struct.unpack_from('<2H', raw, offset)
        if first & 0xF800 == 0xF000 and second & 0xF800 in (0xF800, 0xE800):
            displacement = ((first & 0x7FF) << 12) | ((second & 0x7FF) << 1)
            if displacement & (1 << 22):
                displacement -= 1 << 23
            target = base + offset + 4 + displacement
            if second & 0xF800 == 0xE800:
                target &= ~3
            if lo <= target < hi:
                found.append({'address': base + offset, 'kind': 'thumb-branch-pair-candidate', 'target': target})
    return found


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source = rom.read_file('/__arm9__.bin')
    proposed, placement = prepare(source)
    lo, hi = 0x01FF9B20, 0x01FF9B20 + placement['total_payload_bytes']
    sections = MainCodeFile(source, 0x02000000).sections
    components = [(f'section_{index}', section.ramAddress, bytes(section.data))
                  for index, section in enumerate(sections)]
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid])
    components += [(f'overlay_{index}', overlay.ramAddress, bytes(overlay.data))
                   for index, overlay in overlays.items()]
    checks = [{'component': name, 'base': base, 'bytes': len(raw), 'sha256': sha(raw),
               'references': references(raw, base, lo, hi)} for name, base, raw in components]
    count = sum(len(check['references']) for check in checks)
    for check in checks:
        for reference in check['references']:
            if reference == {'address': 0x020E45E4, 'kind': 'aligned-pointer', 'target': lo}:
                reference['review'] = 'Native SDK arena 3 initial low boundary; proposed ARM9 advances it past complete aligned resident extent.'
    unresolved = sum('review' not in reference for check in checks for reference in check['references'])
    report = {'status': ('no-static-reference-candidates' if count == 0 else
                         'static-candidates-classified' if unresolved == 0 else 'static-candidates-need-review'),
              'source_arm9_sha256': sha(source), 'proposed_arm9_sha256': sha(proposed),
              'extension': {'lo': lo, 'hi': hi}, 'components': checks,
              'unclassified_candidates': unresolved,
              'reserved_arena_low': placement['reserved_arena_low'],
              'limitations': 'Scans every aligned word and Thumb branch pair conservatively, including data. Does not prove absence of computed addresses, indirect writes or external hardware ownership. Declared section/overlay bounds and actual native autoload proof provide separate evidence.'}
    Path('work/analysis/common_word_wrap_itcm_refs.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(checks)} resident/DTCM/static/overlay components scanned; {count} preexisting reference candidates into added ITCM interval.')


if __name__ == '__main__':
    main()
