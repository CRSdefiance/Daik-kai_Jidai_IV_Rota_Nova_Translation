"""Reuse exact per-record comparison bindings for the complete 373-object batch."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/save_hodram_B171_B190_comparisons.py').read_text(encoding='utf-8'), {
    'from scripts.save_hodram_B171_B190_drafts import ROOT': 'from scripts.save_hodram_B191_B210_drafts import ROOT',
    'Hodram_B171_B190_current_20261102': 'Hodram_B191_B210_current_20261104',
    'Hodram_B171_B190_current_objects_20261102': 'Hodram_B191_B210_current_objects_20261104',
    'all435_clean_English_drafts_v2.json': 'complete_clean_English_drafts_v1.json',
})
exec(compile(source, __file__ + '::same-source-current-draft-whole-exchange-comparison', 'exec'), globals())
