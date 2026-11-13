"""Preserve stoppedv2;use its exact existing source path with trusted source digest."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    derive('dk4tool/patch/hodram_B49_controls_v2.py','dk4tool/patch/hodram_B49_controls_v3.py',{
        'import trusted_adapter,CONTROLS,TRUSTED':'import trusted_adapter,TRUSTED',
        "INPUT=Path('work/analysis/current_V8377_Hodram_native_v8380/current_native_input.json')":"CONTROLS=SOURCE\nINPUT=Path('work/analysis/current_V8377_Hodram_native_v8380/current_native_input.json')",
    })
    derive('scripts/validate_Hodram_B49_controls_v8441.py','scripts/validate_Hodram_B49_controls_v8441b.py',{
        'hodram_B49_controls_v2':'hodram_B49_controls_v3','Hodram_B49_independent_controls_v8441':'Hodram_B49_independent_controls_v8441b',
    })
