"""Add the required gate declaration to the scoped-name output; keep every v1 check."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/finalize_rafael255_research_v1.py').read_text(encoding='utf-8'), {
    "ROOT = Path('work/analysis/Rafael255_checked_v1_20261105')":
        "ROOT = Path('work/analysis/Rafael255_checked_v2_20261105')",
    "    validate_natural_dialogue_batch(name_doc)":
        "    name_doc['review_gates'] = ['source', 'context', 'localization', 'naturalness', 'formatting']\n    validate_natural_dialogue_batch(name_doc)",
})
exec(compile(source, __file__+'::required-scoped-name-review-gate-declaration', 'exec'), globals())
