"""Bind the exact original paired-opaque receipt field before running production reader."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    derive('dk4tool/patch/hodram_B49_controls_v1.py','dk4tool/patch/hodram_B49_controls_v2.py',{
        "source['isolated_opaque_effect_structural_pairs']":"source['paired_opaque_structural_decodes']",
    })
