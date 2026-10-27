"""Verify source-faithful Rotate and register all inherited V322 layers."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sail_rotation_caption import transform
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/sail_rotation_v324')
CONFIG = Path('translations/sail_rotation_caption_release_v1.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (
        'out/all_routes_combined_v322_candidate.nds', 'work/clean.nds',
        'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(*arms)
    cases = []
    for table in (0x119134, 0x11914C):
        for mode in (4, 16):
            before = execute(arms[0], 'unused', footer_table=table, mode=mode)
            after = execute(target, 'unused', footer_table=table, mode=mode)
            texts = [row['text'] for row in after['footer_draws']]
            assert after['pixels'] == expected_pixels(target, ''.join(texts), 0, 0, mode, advance=6)
            assert after['footer_metadata'] == before['footer_metadata']
            if table == 0x119134:
                assert texts.count('Rotate') == 1 and texts.count('Sails') == 1
            else:
                assert after == before
            assert texts.count('Inspect') == 1
            cases.append({'table': table, 'mode': mode, 'labels': texts,
                          'native_raster_sha256': sha(after['pixels']),
                          'all_original_footer_positions_and_widths_exact': True,
                          'all_complete_ink_blank_cells_and_native_returns_pass': True})
    proof = {'transform': plan, 'native_cases': cases,
             'source_review': '帆回転 means sail rotation. Restore canonical Rotate to distinguish L/R angle control from A Sails open/close; complete natural action verb, no abbreviation.',
             'old_generic_object_label_superseded_without_rewriting_historical_release': True,
             'goal_complete': False}
    evidence = ROOT / 'native_proof.json'
    evidence.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'research_arm9.bin').write_bytes(target)
    config = {'format': 'dk4-sail-rotation-caption-release-v1', 'target_arm9_sha256': sha(target),
              'source_review': proof['source_review'],
              'verification_evidence_sha256': {str(evidence): sha(evidence.read_bytes())},
              'status': 'experimental-native-verified-live-pending'}
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v322'])
    profile['sail_rotation_caption_release'] = str(CONFIG)
    profile['note'] = 'Full V322 stack plus restoration of source-faithful Rotate verb; distinct Sails open/close and Inspect retained. All graphics and equipment obligations remain open.'
    prior = registry['profiles'].get('all-routes-unified-v324')
    assert prior is None or prior == profile
    registry['profiles']['all-routes-unified-v324'] = profile
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Four native footer cases pass; complete V324 profile registered.')


if __name__ == '__main__':
    main()
