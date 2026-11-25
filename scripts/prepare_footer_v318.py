"""Register the complete inherited footer fix after native family checks."""

import copy
import json
from pathlib import Path

from dk4tool.patch.footer_measurement import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/footer_measurement_v318')
CONFIG = Path('translations/footer_measurement_release_v1.json')


def main():
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in
            ('out/all_routes_combined_v316_candidate.nds', 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(*arms)
    proposed = Path('work/analysis/auto_move_contexts_v317/proposed_arm9.bin')
    assert target == proposed.read_bytes()
    proof_paths = [Path('work/analysis/auto_move_contexts_v317/proof.json'), Path('work/analysis/auto_move_contexts_v317/families_proof.json')]
    native, families = [json.loads(p.read_text(encoding='utf-8')) for p in proof_paths]
    assert len(native['native_measurement_cases']) == 129 and len(families['cases']) == 10
    assert families['target_sha256'] == sha(target)
    assert all(row['unchanged_vs_current'] for row in families['cases'] if row['table'] in (0x12EC10, 0x12EC28, 0x12EC3C))
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / 'research_arm9.bin').write_bytes(target)
    config = {'format': 'dk4-footer-measurement-release-v1', 'target_arm9_sha256': sha(target),
              'source_arm9_sha256': sha(arms[0]), 'verification_evidence_sha256': {str(p): sha(p.read_bytes()) for p in proof_paths},
              'source_review': '自動移動停止 means Stop Auto Move; complete wording fits original16-byte slot.',
              'status': 'experimental-native-verified-live-sailing-footer-pending'}
    CONFIG.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    path = Path('translations/release_stack.json')
    stack = json.loads(path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v316'])
    profile['footer_measurement_release'] = str(CONFIG)
    profile['status'] = 'experimental'
    profile['note'] = ('Complete V316 stack plus footer-wide exact ASCII widths and full Stop Auto Move caption. '
                       '129 native length cases and10 footer family rasters verified; physical sailing footer pending. '
                       'All18 plaques and broader graphics gates remain open; Online low resolution images exempt.')
    prior = stack['profiles'].get('all-routes-unified-v318')
    assert prior is None or prior == profile
    stack['profiles']['all-routes-unified-v318'] = profile
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'preparation.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    print('V318 complete470-batch profile registered; two width instructions and original16-byte Stop caption only.')


if __name__ == '__main__':
    main()
