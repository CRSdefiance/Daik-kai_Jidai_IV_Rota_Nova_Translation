"""Use the exact clean B53 indices in the representative display selection."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/select_maria310_display_v1.py').read_text(encoding='utf-8'),{
    'display_selection_v1.json':'display_selection_v2.json',
    '[113,117,121,124,127,130]':'[113,117,120,123,127,130]',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-targeted-cases-exact-clean-indices','exec'),globals())
