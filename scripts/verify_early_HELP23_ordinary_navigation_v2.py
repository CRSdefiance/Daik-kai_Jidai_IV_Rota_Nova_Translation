"""Same complete planes/native target/history checks on corrected ordinary control schedule."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/verify_early_HELP23_ordinary_navigation.py').read_text(encoding='utf-8'),{
    'ordinary_navigation_v1':'ordinary_navigation_v2',
    'ordinary_navigation_checked_v1':'ordinary_navigation_checked_v2',
    'ordinary_navigation_plan_v1':'ordinary_navigation_plan_v2',
})
exec(compile(source,__file__+'::same-complete-actual-pixel-andwidget-verification','exec'),globals())
