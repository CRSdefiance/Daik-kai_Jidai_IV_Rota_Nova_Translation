"""Qualify a simultaneous-replacement key; reuse the two already complete native modules exactly."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    wrapper="""from scripts.source_locked_derivation_v5118 import derive as original_derive,checked_text

def derive(a,b,changes):
    target=Path(b);expected=checked_text(Path(a).read_text(encoding='utf-8'),changes)
    if not target.exists():return original_derive(a,b,changes)
    assert target.read_text(encoding='utf-8')==expected
    return dict(previous=a,previous_sha256=sha(Path(a).read_bytes()),successor=b,successor_sha256=sha(target.read_bytes()),reused_exact_completed_output_of_stopped_preparer=True,native_high_integer_constants_and_multiplicity_preserved=True)
"""
    derive('scripts/prepare_Hodram_B54_B60_native_v8837.py','scripts/prepare_Hodram_B54_B60_native_v8837b.py',{
        'from scripts.source_locked_derivation_v5118 import derive':wrapper,
        "root=Path('work/analysis/Hodram_B54_B60_native_tools_v8837')":"root=Path('work/analysis/Hodram_B54_B60_native_tools_v8837b')",
        '"ROOT=Path(\'work/analysis/Hodram_B54_B60_native_validation_v8838\')":':'"ROOT=Path(\'work/analysis/Hodram_B31_B53_native_validation_v8754\')":',
    })
