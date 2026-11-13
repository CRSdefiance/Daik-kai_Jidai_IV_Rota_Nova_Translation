"""Correct the absent derivation key; simultaneous source substitutions use original4001."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_initializer_preparer_v7701b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prepare_Maria_B207_initializer_v7701.py','scripts/prepare_Maria_B207_initializer_v7701b_generated.py',{
        'maria_B207_initializer_tools_v7701':'maria_B207_initializer_tools_v7701b',
        '"assert r[\'frames\']==6001 and':'"assert r[\'frames\']==4001 and',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_original_derivation_key.json',dict(derivation=result,failed_original_preparer_preserved=True,new_credit=0,full_goal_complete=False))
