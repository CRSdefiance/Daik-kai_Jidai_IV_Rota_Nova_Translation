"""Use the already validated exact2b6 oracle; leave the historical old-hash oracle untouched."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_target_name_tools_v8210c')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Gerhard_target_name_v8210b.py','scripts/prove_Gerhard_target_name_v8210c.py',{
        'Gerhard_target_name_v8210b':'Gerhard_target_name_v8210c',
        'from scripts.shady_man_font_oracles_v6263 import expected_pixels':'from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels',
        "preserved_failure='scripts/prove_Gerhard_target_name_v8210.py compiled method shadowed its underlying imported machine;TypeError before research overlay/getters/no ROM changes',":
        "preserved_failures=['scripts/prove_Gerhard_target_name_v8210.py method binding TypeError before input/getters','scripts/prove_Gerhard_target_name_v8210b.py all8 getters passed;older4f4 oracle correctly rejected current2b6 before plane output;no ROM changes'],",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared exact-current2b6 independent font oracle binding;all native guards preserved.')
