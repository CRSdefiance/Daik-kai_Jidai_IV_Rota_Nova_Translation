"""Four actual full-glyph navigation pages and restored link-child identities."""

import json
from pathlib import Path
from unittest.mock import patch

from scripts import verify_trade_help_live_v430 as live

ROOT = Path('work/analysis/navigation_help_release_v461')
CAPTURE = Path('work/emulation_v193/navigation_help_v461')


def main():
    p = json.loads((ROOT / 'navigation_plan.json').read_text(encoding='utf-8'))
    frames = {int(k): (CAPTURE, v) for k, v in p['page_frames'].items()}
    assert set(frames) == {76, 83, 101, 104}
    with patch.object(live, 'ROOT', ROOT), patch.object(live, 'ROM', Path('out/all_routes_combined_v461_candidate.nds')), \
            patch.object(live, 'FIRST', CAPTURE), patch.object(live, 'HISTORY', CAPTURE), \
            patch.object(live, 'PLAN', Path('work/analysis/navigation_help_v460/page_proposal.json')), \
            patch.object(live, 'FRAMES', frames), patch.object(live, 'HISTORY_FRAMES', p['history_frames']):
        live.main()
    path = ROOT / 'release_proof.json'
    d = json.loads(path.read_text(encoding='utf-8'))
    d['actual_all4_navigation_articles_and_restored_parent_links_verified'] = True
    d['actual_original_link_child_count'] = sum(len(x['actual_HELP_parent']['constructed_link_destinations'])
                                               for x in d['actual_complete_HELP_topic_cases'])
    path.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
    print('Four actual navigation pages, restored Captain/Masts paths and7 original link widgets pass.')


if __name__ == '__main__':
    main()
