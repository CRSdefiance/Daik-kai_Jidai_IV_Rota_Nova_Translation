"""Verify complete result rows through native frame and text-request code."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_grand_race_result_frame import execute


def main():
    proposal = Path('work/analysis/grand_race_complete_ui_proposal_v136')
    source = (proposal / 'proposed_arm9.bin').read_bytes()
    proposal_report = json.loads((proposal / 'report.json').read_text())
    printf_path = Path('work/analysis/grand_race_native_printf_v136_proof.json')
    printf = json.loads(printf_path.read_text())
    if sha(source) != proposal_report['proposed_arm9_sha256'] or sha(source) != printf['proposed_arm9_sha256']:
        raise ValueError('Native format/frame proposal lineage differs')
    cases = []
    for case in printf['cases']:
        for selected in (False, True):
            proof = execute(source, bytes.fromhex(case['full_row_hex'])[:-1], case['place'] - 1, selected)
            proof.update({'place': case['place'], 'player': case['player'], 'name_hex': case['name_hex']})
            cases.append(proof)
    output = {'status': 'pass-native-result-frame-geometry-and-full-glyph-dispatch-with-draw-contracts',
              'proposed_arm9_sha256': sha(source), 'printf_proof_sha256': sha(printf_path.read_bytes()),
              'rom_written': False, 'runtime_verified': False, 'case_count': len(cases), 'cases': cases,
              'limitations': ['Actual native centering, row placement, FB004 virtual setter, FB324 frame geometry and D1604 ASCII/CP932 dispatch execute.',
                              'Background/border strip coordinates and complete frame extents remain on the 256x192 screen.',
                              'Image/resource lookup, edge artwork painting and glyph pixel painters use explicit external contracts.',
                              'Native text pixels separately verified in earlier synthetic-context probes; complete artwork/frame pixels and gameplay remain pending.',
                              'No registered release batch, ROM, runtime acceptance or automatic editorial-gate promotion.']}
    Path('work/analysis/grand_race_native_frame_v136_proof.json').write_text(json.dumps(output, indent=2) + '\n')
    print(f'{len(cases)} native frame/text cases pass; complete frame stays on screen and complete glyph sequence is intact.')


if __name__ == '__main__':
    main()
