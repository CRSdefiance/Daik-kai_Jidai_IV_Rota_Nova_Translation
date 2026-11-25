"""Preserve passing v1; add explicit summary/scope/ROM-ownership consistency to v2."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_atomic_tools_v8296b')
if __name__=='__main__':
    assert not ROOT.exists()
    stage=derive('dk4tool/patch/hodram_three_blocks_editorial_v1.py','dk4tool/patch/hodram_three_blocks_editorial_v2.py',{
        'from dk4tool.patch.hodram_three_blocks_controls_v1 import':'from dk4tool.patch.hodram_three_blocks_controls_v2 import',
        'translations/hodram_three_blocks_editorial_release_v1.json':'translations/hodram_three_blocks_editorial_release_v2.json',
    })
    pin=derive('scripts/pin_Hodram_production_v8296.py','scripts/pin_Hodram_production_v8296b.py',{
        'from dk4tool.patch.hodram_three_blocks_editorial_v1 import':'from dk4tool.patch.hodram_three_blocks_editorial_v2 import',
        'Hodram_production_tools_v8296':'Hodram_production_tools_v8296b',
        "    save(config,dict(":"    deps|={Path('dk4tool/patch/hodram_three_blocks_editorial_v2.py'),Path('dk4tool/patch/hodram_three_blocks_controls_v2.py')}\n    save(config,dict(",
    })
    positive=derive('scripts/validate_Hodram_atomic_positive_v8297.py','scripts/validate_Hodram_atomic_positive_v8297b.py',{
        'hodram_three_blocks_editorial_v1':'hodram_three_blocks_editorial_v2',
        'Hodram_atomic_positive_v8297':'Hodram_atomic_positive_v8297b',
    })
    ROOT.mkdir(parents=True);save(ROOT/'summary_ownership_consistency_successor.json',dict(stage=stage,pin=pin,positive=positive,
        earlier_v1_positive_andall_native_actual_checks_preserved=True,
        reason='Detailed entries already validate;reject contradictory declared guard/scope flags andwrong wrapper ROM ownership aswell.',
        no_original_native_oractual_check_removed_orweakened=True,new_credit=0,full_goal_complete=False))
