"""Preserve the import-time adapter failure;bind the exact frozen inherited QA source."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_QA_adapter_tools_v7984b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/plan_Rafael_B47_layout_v7984.py','scripts/plan_Rafael_B47_layout_v7984b.py',{
        'Rafael_B47_layout_v7984':'Rafael_B47_layout_v7984b',
        'inspect.getsource(previous.base_qa)':'previous.qa_adapter',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        prior_failure='V7984 import-time source derivation rejected absent Rafael-B46-native-QA in inspect.getsource of the inherited dynamic function.',
        correction='Use previous.qa_adapter, the exact already frozen B46 QA adapter source, and change only its local diagnostic name.',
        no_native_numeric_constant_guard_profile_font_prose_orROM_change=True,new_credit=0,full_goal_complete=False))
    print('Prepared source-locked B47 planner successor fromthe exact stored QA adapter;failed producer preserved.')
