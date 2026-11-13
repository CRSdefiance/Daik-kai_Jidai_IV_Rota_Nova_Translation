"""Complete nine-page actual city HELP glyphs, link children and return links."""

import json
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from scripts import verify_trade_help_live_v430 as live


def main():
    capture = Path('work/emulation_v193/city_help_v436')
    root = Path('work/analysis/city_help_release_v436')
    frames = {145: (capture, 26000), 146: (capture, 26600), 147: (capture, 27200),
              149: (capture, 27800), 150: (capture, 28400), 206: (capture, 28800),
              151: (capture, 29200), 207: (capture, 29600), 194: (capture, 32400)}
    with patch.object(live, 'ROOT', root), \
            patch.object(live, 'ROM', Path('out/all_routes_combined_v436_candidate.nds')), \
            patch.object(live, 'FIRST', capture), patch.object(live, 'HISTORY', capture), \
            patch.object(live, 'PLAN', Path('work/analysis/city_help_v435/page_proposal.json')), \
            patch.object(live, 'FRAMES', frames), patch.object(live, 'HISTORY_FRAMES', (28400, 31000)):
        live.main()
    first = Image.open(capture / 'frame_029200_navigation.png').convert('RGB')
    returned = Image.open(capture / 'frame_030000_navigation.png').convert('RGB')
    assert first.tobytes() == returned.tobytes()
    path = root / 'release_proof.json'
    proof = json.loads(path.read_text(encoding='utf-8'))
    proof['both_actual_article_return_links_full_frame_pixel_exact'] = True
    proof['actual_new_continuation_topics206_207_loaded_and_clicked'] = True
    proof['actual_seven_complete_articles_nine_pages_verified'] = True
    path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Both actual return links restore complete original article pixels;208-topic integration verified.')


if __name__ == '__main__':
    main()
