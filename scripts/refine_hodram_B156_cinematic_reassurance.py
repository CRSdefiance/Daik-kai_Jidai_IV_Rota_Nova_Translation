"""Keep the entire We shall meet phrase; preserve every earlier probe and panel."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/refine_hodram_B156_cinematic_English.py').read_text(encoding='utf-8'),{
    'Hodram_B156_cinematic_English_v3_20261102':'Hodram_B156_cinematic_English_v4_20261102',
    "or (words[stop-1],words[stop])==('shall','meet')":"or (words[stop-1],words[stop]) in {('We','shall'),('shall','meet')}",
    '"for p in [PRIOR,original,INPUT,GEOMETRY,",':'"for p in [PRIOR,Path(\'scripts/check_hodram_B156_cinematic_English.py\'),INPUT,GEOMETRY,",',
})
exec(compile(source,__file__+'::complete-reassurance-clause','exec'),globals())
