"""Twenty-nine actual Help pages, original widgets and continuation/history return."""

import json
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from scripts import verify_trade_help_live_v430 as live

ROOT = Path('work/analysis/sailor_data_help_release_v447')
CAPTURE = Path('work/emulation_v193/sailor_data_help_fixed_v447')


def main():
    plan = json.loads((ROOT / 'navigation_plan.json').read_text(encoding='utf-8'))
    frames = {int(topic): (CAPTURE, frame) for topic, frame in plan['page_frames'].items()}
    assert len(frames) == 29
    with patch.object(live, 'ROOT', ROOT), \
            patch.object(live, 'ROM', Path('out/all_routes_combined_v447_candidate.nds')), \
            patch.object(live, 'FIRST', CAPTURE), patch.object(live, 'HISTORY', CAPTURE), \
            patch.object(live, 'PLAN', Path('work/analysis/sailor_data_help_v446/page_proposal.json')), \
            patch.object(live, 'FRAMES', frames), patch.object(live, 'HISTORY_FRAMES', plan['history_frames']):
        live.main()
    first, returned = [Image.open(CAPTURE / f'frame_{f:06d}_navigation.png') for f in plan['HP_return_frames']]
    assert first.tobytes() == returned.tobytes()
    proof_path = ROOT / 'release_proof.json'
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    proof['actual_HP_continuation_and_return_link_restore_full_page_exactly'] = True
    proof['actual_all28_articles_29_complete_pages_verified'] = True
    proof['actual_original_link_child_count'] = sum(len(r['actual_HELP_parent']['constructed_link_destinations'])
                                                   for r in proof['actual_complete_HELP_topic_cases'])
    proof_path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('All29 actual complete pages and HP continuation/return pass; original widgets and L/R history verified.')


if __name__ == '__main__':
    main()
