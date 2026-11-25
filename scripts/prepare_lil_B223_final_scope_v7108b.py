"""Retain naturally different final captain getters; preserve the failed fixed-ID audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_final_scope_tools_v7108b')
if __name__=='__main__':
    assert not ROOT.exists()
    a='scripts/audit_lil_B223_English_v7108.py';b='scripts/audit_lil_B223_English_v7108b.py'
    c={
      "ROOT=Path('work/analysis/lil_B223_English_actual_v7108')":"ROOT=Path('work/analysis/lil_B223_English_actual_v7108b')",
      'root=get(0xCB184);assert get(0x7F244)==2;':'root=get(0xCB184);captain=get(0x7F244);assert captain in range(4);',
      'captain_ID=2,seed=':'captain_ID=captain,seed=',
      "whole_actor_and_captain_equal=final[0]['whole_actor_hex']==final[1]['whole_actor_hex']":"whole_actor_bytes_equal=final[0]['whole_actor_hex']==final[1]['whole_actor_hex'],captain_IDs=[v['captain_ID'] for v in final],captain_IDs_equal=final[0]['captain_ID']==final[1]['captain_ID'],whole_actor_and_captain_equal=final[0]['whole_actor_hex']==final[1]['whole_actor_hex'] and final[0]['captain_ID']==final[1]['captain_ID']",
    }
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_final_scope_correction.json',dict(tool=row,failed_fixed_captain2_assertion_preserved=True,both_final_snapshot_hashes_verified_before_change=True,original_native_getter_and_actor_root_extent_unchanged=True,no_RAM_role_roster_RNG_result_or_input_retiming=True,no_whole_RAM_future_sequence_equivalence_or_causal_claim=True,new_boots=0,new_credit=0,full_goal_complete=False))
