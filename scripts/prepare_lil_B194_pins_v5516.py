"""Prepare audited preservation pins for both complete conditional B194 fixtures."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/pin_lil_B193_display_v5470.py', 'scripts/pin_lil_B194_display_v5516.py', {
        'B193': 'B194', 'display_tools_v5470': 'display_tools_v5516',
        'display_fixture_v5469': 'display_fixture_v5514',
        'source_speeches=15,progressive=14': 'source_speeches=11,progressive=10',
        'source_commands=18,stored_fixture_commands=27': 'source_commands=21,stored_fixture_commands=30',
        'All15 panels and original A000/C200/end retained;actual observation pending.':
        'All11 stored objects and original availability,FI,resource42,two C200 and end retained;actual selection pending.',
    }))
