"""Prepare clean-only neighboring event inventories while the independent registered build runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_next_clean_tools_v8785');assert not root.exists()
    receipt=derive('scripts/inventory_Hodram_B53_clean_v8711.py','scripts/inventory_Hodram_next_clean_v8785.py',{
        'Hodram_B53_clean_v8711':'Hodram_next_clean_v8785',
        'editorial_handoff_verification_v8710':'editorial_handoff_verification_v8775',
        '==7229':'==7234',"=='all-routes-unified-v8609'":"=='all-routes-unified-v8704'",
        'for number in [53]':'for number in [54,55,56,57,58,59,60]',
        'complete_clean_SC1_B53_EV1_andcoverage_before_current_English.json':'complete_clean_SC1_B54_B60_EV1_andcoverage_before_current_English.json',
        "if g['block']==53:":"if g['block'] in [54,55,56,57,58,59,60]:",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_original_clean_ROM_full_block_native_inventory_EV1_source_reference_coverage_anddecode_guards_preserved=True,
        only_clean_Japanese_andcoverage_keys_no_current_English_read=True,
        seven_numbered_blocks_are_candidate_source_context_not_proven_chronological_conversation=True,
        source_meaning_names_native_controls_choices_actual_policy_andrelease_reviews_still_pending=True,
        B31_B53_registered_builder_not_restarted_orinterfered_with=True,new_credit=0,full_goal_complete=False))
