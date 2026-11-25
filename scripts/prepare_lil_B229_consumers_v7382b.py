"""Bind seventeen new speech bodies and the distinct event/effect controls on own V7371 input."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_consumer_tools_v7382b')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B228':'B229','source_v7334/thirteen_clean_current_armadillo_shield_rumor_source_references':'source_v7381/seventeen_clean_current_giant_tortoise_callback_source_references','current_V7324_native_v7329':'current_V7371_native_v7376'}
    consumers={**common,'v7335':'v7382','all13_clean_glosses_precede_old_English':'all17_clean_glosses_precede_old_English','len(cases)==26':'len(cases)==34','len(effective)==13':'len(effective)==17','all26_source_current_dispatches':'all34_source_current_dispatches','all13_current_templates':'all17_current_templates','thirteen_effective_bodies26_dispatches_two_actors_four_name_consumers':'seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers','two actors,four original name consumers and thirteen':'two actors,four original name consumers and seventeen','bodies=13,dispatches=26':'bodies=17,dispatches=34'}
    entry={**common,'v7336':'v7383','in [228]':'in [229]'}
    controls={**common,'v7337':'v7384','blocks[228]':'blocks[229]','len(block)==760':'len(block)==944',"struct.unpack_from('<H',block,4)[0]==758":"struct.unpack_from('<H',block,4)[0]==944",'block[754:]==bytes(6)':'block[940:]==bytes(4)','len(commands)==15':'len(commands)==19',"[(746,'00a0ffff32000110',8),(754,'00000000',4)]":"[(932,'00a0ffff35000110',8),(940,'00000000',4)]",'original_offset=746':'original_offset=932','arm,block,754,previous,seed':'arm,block,940,previous,seed','source_stored760_logical758_tail2_complete_end754_preserved':'source_stored944_logical944_tail0_complete_end940_preserved','Original760-byte storage/tail2':'Original944-byte storage/no tail'}
    controls.pop('current_V7324_native_v7329')
    jobs=[('scripts/prove_lil_B228_consumers_v7335.py','scripts/prove_lil_B229_consumers_v7382.py',consumers),('scripts/prove_lil_B228_entry_v7336.py','scripts/prove_lil_B229_entry_v7383.py',entry),('scripts/prove_lil_B228_controls_v7337.py','scripts/prove_lil_B229_controls_v7384.py',controls)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_consumer_entry_control_tools.json',dict(tools=rows,all17_new_bodies34_dispatches_same_two_actors_on_new_current_input=True,event229_A000932_andend940_not_reused_fromB228=True,source944_logical944_no_tail=True,all_native_high_integer_constants_preserved=True,new_credit=0,full_goal_complete=False))
