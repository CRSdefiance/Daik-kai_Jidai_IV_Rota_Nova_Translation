"""Verify eight actual HELP pages using the existing exact glyph/widget checks."""

from pathlib import Path
from unittest.mock import patch

from scripts import verify_trade_help_live_v430 as live


def main():
    capture = Path('work/emulation_v193/general_help_v434')
    frames = {11: (capture, 21600), 21: (capture, 22000), 23: (capture, 22400),
              103: (capture, 23200), 105: (capture, 23600), 127: (capture, 24000),
              134: (capture, 24800), 144: (capture, 25600)}
    with patch.object(live, 'ROOT', Path('work/analysis/general_help_release_v434')), \
            patch.object(live, 'ROM', Path('out/all_routes_combined_v434_candidate.nds')), \
            patch.object(live, 'FIRST', capture), patch.object(live, 'HISTORY', capture), \
            patch.object(live, 'PLAN', Path('work/analysis/help_navigation_v433/page_proposal.json')), \
            patch.object(live, 'FRAMES', frames), patch.object(live, 'HISTORY_FRAMES', (25600, 26000)):
        live.main()


if __name__ == '__main__':
    main()
