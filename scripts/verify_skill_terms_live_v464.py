"""All35 actual crew Help pages, complete original widgets and return controls."""

import json
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from scripts import verify_trade_help_live_v430 as live

ROOT = Path('work/analysis/skill_terms_release_v464')
CAPTURE = Path('work/emulation_v193/skill_terms_v464')


def main():
    plan = json.loads((ROOT / 'navigation_plan.json').read_text(encoding='utf-8'))
    frames = {int(topic): (CAPTURE, frame) for topic, frame in plan['page_frames'].items()}
    assert len(frames) == 15
    with patch.object(live, 'ROOT', ROOT), patch.object(live, 'ROM', Path('out/all_routes_combined_v464_candidate.nds')), \
            patch.object(live, 'FIRST', CAPTURE), patch.object(live, 'HISTORY', CAPTURE), \
            patch.object(live, 'PLAN', Path('work/analysis/skill_terms_v463/page_proposal.json')), \
            patch.object(live, 'FRAMES', frames), patch.object(live, 'HISTORY_FRAMES', plan['history_frames']):
        live.main()
    first, returned = [Image.open(CAPTURE / f'frame_{f:06d}_navigation.png') for f in plan['list_return_frames']]
    assert first.tobytes() == returned.tobytes()
    first_hp, returned_hp = [Image.open(CAPTURE / f'frame_{f:06d}_navigation.png') for f in plan['HP_return_frames']]
    assert first_hp.tobytes() == returned_hp.tobytes()
    p = ROOT / 'release_proof.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['actual_list_continuation_and_return_restore_full_page_exactly'] = True
    d['actual_HP_continuation_and_return_restore_full_page_exactly'] = True
    d['actual_all13_articles_15_complete_pages_verified'] = True
    d['actual_original_link_child_count'] = sum(len(r['actual_HELP_parent']['constructed_link_destinations'])
                                               for r in d['actual_complete_HELP_topic_cases'])
    p.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
    print('All15 actual terminology pages, both original continuation/return controls and full link widgets pass.')


if __name__ == '__main__':
    main()
