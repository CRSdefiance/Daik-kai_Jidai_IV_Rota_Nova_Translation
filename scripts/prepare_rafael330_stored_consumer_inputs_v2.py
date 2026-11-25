"""Bind final327 physical commands after the one-paragraph successor."""
from pathlib import Path
from scripts import prepare_rafael330_stored_consumer_inputs_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path(previous.__file__).read_text(encoding='utf-8'),{
    'Rafael_B81_B84_rebuilt_20261105/reconstruction.json':'Rafael_B81_B84_rebuilt_v2_20261105/reconstruction.json',
    'Rafael330_stored_consumer_inputs_20261105':'Rafael330_stored_consumer_inputs_v2_20261105',
    "native,plans=[load(FORMAT/p) for p in ['combined_native_v5.json','automatic_subset_v5/automatic_plans.json']]":
        "native,plans=[load(Path('work/analysis/Rafael330_Emilio_composite_v2_20261105')/p) for p in ['native323.json','plans323.json']]",
    "str(FORMAT/'combined_native_v5.json')":"str(Path('work/analysis/Rafael330_Emilio_composite_v2_20261105/native323.json'))",
})
exec(compile(source,__file__+'::same-final-offset-andFE-child-binding-one-prose-successor','exec'),globals())
