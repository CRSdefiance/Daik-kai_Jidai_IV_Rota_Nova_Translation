"""Verify both native footer owners and register the full inherited candidate."""

import copy
import json
from itertools import pairwise
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sea_inspect_caption import transform
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/sea_inspect_v322')
CONFIG = Path('translations/sea_inspect_caption_release_v1.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (
        'out/all_routes_combined_v318_candidate.nds', 'work/clean.nds',
        'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(*arms)
    cases = []
    for table in (0x119134, 0x11914C):
        for mode in (4, 16):
            result = execute(target, 'unused', footer_table=table, mode=mode)
            texts = [row['text'] for row in result['footer_draws']]
            assert texts.count('Inspect') == 1 and 'Sea Map' not in texts
            assert result['pixels'] == expected_pixels(target, ''.join(texts), 0, 0, mode, advance=6)
            positions = []
            for slot in range(6):
                left, width, source_x = result['footer_metadata'][slot * 3:slot * 3 + 3]
                if left != -1:
                    assert 0 <= left <= left + width <= 256
                    positions.append({'slot': slot, 'left': left, 'width': width, 'source_x': source_x})
            ordered = sorted(positions, key=lambda row: row['left'])
            assert all(a['left'] + a['width'] <= b['left'] for a, b in pairwise(ordered))
            cases.append({'table': table, 'mode': mode, 'labels': texts,
                          'positions': positions, 'complete_native_raster_sha256': sha(result['pixels']),
                          'all_complete_letters_and_original_footer_bounds': True})
    capture = Path('work/emulation_v193/ordinary_voyage_v321/capture_report.json')
    report = json.loads(capture.read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == sha(Path('out/all_routes_combined_v318_candidate.nds').read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 16800
    proof = {'source_review': '洋上 means at sea. Actual action enters Info Mode and selects cities/ships for information. Inspect is a complete natural functional localization, not a map command.',
             'native_cases': cases, 'transform': plan,
             'observed_parent_capture': str(capture), 'observed_parent_capture_sha256': sha(capture.read_bytes()),
             'unsuccessful_voyage_food_exhausted_no_port_or_equipment_credit': True,
             'goal_complete': False}
    proof_path = ROOT / 'native_proof.json'
    proof_path.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'research_arm9.bin').write_bytes(target)
    config = {'format': 'dk4-sea-inspect-caption-release-v1',
              'target_arm9_sha256': sha(target), 'source_review': proof['source_review'],
              'verification_evidence_sha256': {str(proof_path): sha(proof_path.read_bytes())},
              'status': 'experimental-native-verified-live-pending'}
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v318'])
    profile['sea_inspect_caption_release'] = str(CONFIG)
    profile['note'] = 'Full V318 stack plus contextual Inspect caption for both original at-sea footer owners. All graphics/equipment audit obligations retained.'
    previous = registry['profiles'].get('all-routes-unified-v322')
    assert previous is None or previous == profile
    registry['profiles']['all-routes-unified-v322'] = profile
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Four native footer cases pass; complete V318 profile inherited for V322.')


if __name__ == '__main__':
    main()
