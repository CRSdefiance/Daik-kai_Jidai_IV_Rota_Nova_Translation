"""Execute all planned race UI lines through the native ASCII request loop."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import SLOTS, sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_ascii_requests import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE, CANDIDATE_SHA


def main():
    if sha(CANDIDATE.read_bytes()) != CANDIDATE_SHA:
        raise ValueError('Combined source candidate differs')
    source = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if source[0xD1604:0xD16B4] != clean[0xD1604:0xD16B4]:
        raise ValueError('Native ASCII loop differs from clean source')
    allocation_path = Path('work/analysis/grand_race_ui_allocation_v136/report.json')
    plan = json.loads(allocation_path.read_text())
    if plan['candidate_sha256'] != CANDIDATE_SHA or len(plan['selections']) != 60:
        raise ValueError('Current complete allocation proof differs')
    proofs = []
    menu_names = {name.removeprefix('GRAND_RACE_UI_') for name in SLOTS}
    for row in plan['selections']:
        if row['message'] in menu_names:
            continue
        proof = execute(source, row['line'], 0, 0, 15)
        proofs.append({'key': row['key'], 'line': row['line'], **proof})
    layout_path = Path('work/qa/grand_race_region_player_layout_v136/report.json')
    layout = json.loads(layout_path.read_text())
    if layout['candidate_sha256'] != CANDIDATE_SHA or not layout['preview_reviewed']:
        raise ValueError('Current region/player layout proof is not reviewed')
    positioned = [{'id': row['id'], **execute(source, row['english'], *row['position'])}
                  for row in layout['selections']]
    report = {'status': 'pass-native-ascii-requests', 'rom_written': False, 'runtime_verified': False,
              'candidate_sha256': CANDIDATE_SHA, 'renderer_span': [0xD1604, 0xD16B4],
              'renderer_sha256': sha(source[0xD1604:0xD16B4]),
              'allocation_report_sha256': sha(allocation_path.read_bytes()),
              'layout_report_sha256': sha(layout_path.read_bytes()),
              'complete_allocation_strings': proofs, 'positioned_region_role_player_requests': positioned,
              'string_count': len(proofs), 'separate_menu_raster_labels': len(menu_names), 'glyph_request_count': sum(len(p['requests']) for p in proofs),
              'limitations': ['All planned lines executed at synthetic origin for text/advance proof; those origins are not screen layouts.',
                              'Ten region/role/player cases separately use mapped native coordinates.',
                              'Glyph requests captured at D16B4; glyph pixel painting, frame graphics and physical screen routing not executed.',
                              'Menu rasterization uses a separate path and retains its separate proof; no generalized renderer claim.',
                              'Allocated remaining English is research input, not yet integrated into a playable ROM.']}
    Path('work/analysis/grand_race_native_ascii_v136_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f"{len(proofs)} complete strings / {report['glyph_request_count']} native glyph requests pass; ten mapped-coordinate cases pass.")


if __name__ == '__main__':
    main()
