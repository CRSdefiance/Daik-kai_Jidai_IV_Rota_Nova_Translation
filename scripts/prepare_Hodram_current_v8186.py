"""Prepare ordinary own-V8172 Hodram New Game capture before native source/control comparison."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_current_tools_v8186')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/capture_Rafael_B50_context_v8174.py','scripts/capture_Hodram_current_v8186.py',{
        'Rafael_B50_context_runs_v8174':'Hodram_B137_B45_B46_context_runs_v8186',
        'Rafael_B50_route{route}_v8174_V8172':'Hodram_B137_B45_B46_route{route}_v8186_V8172',
        'choices=[0]':'choices=[1]',
        'Capture own-current Rafael New Game through original ordinary inputs;not B50 activation.':'Capture own-current Hodram New Game through original ordinary inputs;not B137/B45/B46 activation.',
        'ordinary_route_selection_not_optional_B50_activation':'ordinary_route_selection_not_optional_B137_B45_B46_activation',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared ordinary own-V8172 Hodram startup;no optional scene activation ornew editorial credit.')
