"""Bind all B230 bodies, original event prerequisites and distinct effect/end on own V7418 input."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_consumer_tools_v7429')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B229':'B230','source_v7381/seventeen_clean_current_giant_tortoise_callback_source_references':'source_v7428/seventeen_clean_current_phoenix_bascinet_callback_source_references'}
    consumers={**common,'v7382':'v7429','current_V7371_native_v7376':'current_V7418_native_v7423'}
    entry={**common,'v7383':'v7430','current_V7371_native_v7376':'current_V7418_native_v7423','in [229]':'in [230]'}
    controls={**common,'v7384':'v7431','blocks[229]':'blocks[230]','len(block)==944':'len(block)==988',"struct.unpack_from('<H',block,4)[0]==944":"struct.unpack_from('<H',block,4)[0]==988",'block[940:]==bytes(4)':'block[984:]==bytes(4)',"[(932,'00a0ffff35000110',8),(940,'00000000',4)]":"[(976,'00a0ffff34000110',8),(984,'00000000',4)]",'original_offset=932':'original_offset=976','arm,block,940,previous,seed':'arm,block,984,previous,seed','source_stored944_logical944_tail0_complete_end940_preserved':'source_stored988_logical988_tail0_complete_end984_preserved','Original944-byte storage/no tail':'Original988-byte storage/no tail','no_confirmed_shield_discovery_ownership_location_or_gameplay_result_inferred':'no_confirmed_helmet_discovery_ownership_location_or_gameplay_result_inferred'}
    jobs=[('scripts/prove_lil_B229_consumers_v7382.py','scripts/prove_lil_B230_consumers_v7429.py',consumers),('scripts/prove_lil_B229_entry_v7383.py','scripts/prove_lil_B230_entry_v7430.py',entry),('scripts/prove_lil_B229_controls_v7384.py','scripts/prove_lil_B230_controls_v7431.py',controls)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_consumer_entry_control_tools.json',dict(tools=rows,all17_new_bodies34_dispatches_on_own_current_input=True,source_event230_prerequisites_not_assumed_from229=True,A000976_end984_source988_no_tail_bound=True,all_native_high_integer_constants_preserved=True,new_credit=0,full_goal_complete=False))
