"""Preserve failed six-word assertion; check the original complete native result contract."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_control_tools_v7686b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Maria_B207_controls_v7686.py','scripts/prove_Maria_B207_controls_v7686b.py',{
        'maria_B207_controls_v7686':'maria_B207_controls_v7686b',
        "case['native_result']==[0,case['initial_value_word']]":"case['native_result']==[0,case['initial_value_word'],0,0,0,0]",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_six_word_native_result_assertion.json',dict(derivation=result,failed_original_preserved=True,no_native_expectation_orseed_change=True,full_goal_complete=False))
