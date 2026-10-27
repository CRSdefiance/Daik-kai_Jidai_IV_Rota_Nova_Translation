"""Eleven actual faction/Data Guide pages, original links and history return."""

from pathlib import Path
from unittest.mock import patch

from scripts import verify_trade_help_live_v430 as live


def main():
    capture = Path('work/emulation_v193/faction_help_v440')
    frames = {143: (capture, 21600), 181: (capture, 22000), 184: (capture, 22400),
              182: (capture, 23000), 183: (capture, 23400), 190: (capture, 24200),
              185: (capture, 24800), 188: (capture, 25200), 186: (capture, 25800),
              187: (capture, 26400), 189: (capture, 27000)}
    with patch.object(live, 'ROOT', Path('work/analysis/faction_help_release_v440')), \
            patch.object(live, 'ROM', Path('out/all_routes_combined_v440_candidate.nds')), \
            patch.object(live, 'FIRST', capture), patch.object(live, 'HISTORY', capture), \
            patch.object(live, 'PLAN', Path('work/analysis/faction_help_v439/page_proposal.json')), \
            patch.object(live, 'FRAMES', frames), patch.object(live, 'HISTORY_FRAMES', (27000, 27400)):
        live.main()


if __name__ == '__main__':
    main()
