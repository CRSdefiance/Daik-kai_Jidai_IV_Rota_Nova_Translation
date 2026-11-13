"""Reconstruct the same330 objects with the single fresh Emilio paragraph."""
from pathlib import Path
from scripts import rebuild_rafael_B81_B84_with_FE_pages_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path(previous.__file__).read_text(encoding='utf-8'),{
    "ROOT=Path('work/analysis/Rafael_B81_B84_rebuilt_20261105')":
        "ROOT=Path('work/analysis/Rafael_B81_B84_rebuilt_v2_20261105')",
    'translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json':
        'translations/rafael_B81_B84_contextual_editorial_manuscript_v2.json',
    "FORMAT/'combined_native_v5.json'":"Path('work/analysis/Rafael330_Emilio_composite_v2_20261105/native323.json')",
    "FORMAT/'automatic_subset_v5/automatic_plans.json'":"Path('work/analysis/Rafael330_Emilio_composite_v2_20261105/plans323.json')",
    'rom_retention_pins.Rafael330_research.pending.json':'rom_retention_pins.Rafael330_research_v2.pending.json',
})
exec(compile(source,__file__+'::same-complete-reconstruction-one-contextual-paragraph-successor','exec'),globals())
