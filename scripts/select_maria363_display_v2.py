"""Include William's complete handover and second two-page report within the measured QA budget."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/select_maria363_display_v1.py').read_text(encoding='utf8'),{
    "ROOT/'display_selection_v1.json'":"ROOT/'display_selection_v2.json'",
    '[229,230,231,232,233,234,235,236,240,241,242]':'[229,230,231,232,233,234,235,236,240,241,242,246,247,248]',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-control-geometry-andinput-contract-added-William-sample','exec'),globals())
