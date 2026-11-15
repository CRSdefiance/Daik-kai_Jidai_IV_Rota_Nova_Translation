"""Reuse exact menu aliases and interval guards for Lil's no-battery fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/check_reviewed_maria_actual_menus_v1.py').read_text(encoding='utf-8'), {
    'scripts.analyze_maria390_menu_actual_v1': 'scripts.analyze_rafael_B201_B220_menu_actual_v1',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-menu-guards-with-original-no-battery-contract', 'exec'), globals())
