"""Prepare a clean-only next-exchange inventory without touching protected integration inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B47_clean_tools_v8310')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/inventory_Hodram_next_clean_v8178.py','scripts/inventory_Hodram_B47_clean_v8310.py',{
        'Hodram_next_clean_v8178':'Hodram_B47_clean_v8310',
        'editorial_handoff_verification_v8166':'editorial_handoff_verification_v8292',
        '7143':'7171','for number in [45]:':'for number in [47]:','B45':'B47','if g[\'block\']==45:':'if g[\'block\']==47:',
    })
    ROOT.mkdir(parents=True);save(ROOT/'clean_only_inventory_successor.json',dict(derivation=result,
        source_only_no_current_English_compared_no_translation_orcompletion_credit=True,
        registry_ledger_pins_andall_atomic_test_inputs_unchanged=True,full_goal_complete=False))
