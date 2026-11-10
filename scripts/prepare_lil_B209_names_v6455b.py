"""Use the captain2 identity already proven by strict CurrentContext; add no native getter address."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_names_tools_v6455b')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/bind_lil_B209_names_v6455.py','scripts/bind_lil_B209_names_v6455b.py',{
        'names_v6455\')':'names_v6455b\')',
        'ident==get(0x7F244)':'ident==2',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',dict(tool=r,prior_failure='Source-locked adapter rejected an added7F244 native getter constant before any context/output mutation. Strict CurrentContext already asserts captain2;the special captain object is now selected by that proven identity. All inherited getter addresses and multiplicities remain exact.',full_goal_complete=False))
