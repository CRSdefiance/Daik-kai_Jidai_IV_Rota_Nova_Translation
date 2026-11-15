"""Preserve the original seal andadd exact current predecessor compatibility bindings."""
from scripts.Hodram_B49_release_paths_v8447 import *
CONFIG=Path('translations/hodram_B49_editorial_release_v2.json')
PROOFS={**PROOFS,'predecessor_compatibility_current':'work/analysis/Hodram_B49_predecessor_binding_v8454/semantic_binding.json'}
def proofs():return {k:str(Path(v)) for k,v in PROOFS.items()}
