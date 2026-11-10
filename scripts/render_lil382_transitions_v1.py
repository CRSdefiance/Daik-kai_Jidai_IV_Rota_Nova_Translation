"""Bind intact Lil host exits to resupply and the following native steering tutorial."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(Path('scripts/render_maria_reviewed_transitions_v1.py').read_text(encoding='utf-8'), {
    'display_run_menu': 'display_run',
    'display_pixels_menu': 'display_pixels',
    ' Want to resupply for ６００ gold?': ' Want to resupply for １００ gold?',
    "'Departed Hangzhou.' in r['text_CP932']": "r['text_CP932'].startswith(\"We're finally at sea!\")",
    "('departure', departure)": "('following native tutorial', departure)",
    "kind='final sailing'": "kind='final captured tutorial state'",
    'initialized_QA_hosts_reach_resupply_departure_andfinal_sailing=True':
        'initialized_QA_hosts_reach_resupply_andfollowing_native_tutorial=True, free_sailing_not_claimed=True',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-observer-hashes-exact-events-andcomplete-capture-binding','exec'),globals())
