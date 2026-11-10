"""Inventory the clean event-linked surrounding conversations; context only, no new credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_context_tools_v8795');assert not root.exists()
    receipt=derive('scripts/inventory_Hodram_next_clean_v8785.py','scripts/inventory_Hodram_B54_B60_context_v8795.py',{
        'Hodram_next_clean_v8785':'Hodram_B54_B60_clean_context_v8795',
        'editorial_handoff_verification_v8775':'editorial_handoff_verification_v8790',
        '==7234':'==7237',"=='all-routes-unified-v8704'":"=='all-routes-unified-v8778'",
        'for number in [54,55,56,57,58,59,60]':'for number in [15,37,65,128,142]',
        "g['block'] in [54,55,56,57,58,59,60]":"g['block'] in [15,37,65,128,142]",
        'complete_clean_SC1_B54_B60_EV1_andcoverage_before_current_English.json':'complete_clean_linked_15_37_65_128_142_context_before_B54_B60_English.json',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_original_complete_clean_blocks_EV1_reference_decode_andcoverage_guards_preserved=True,
        additional_source_context_not_added_to82candidate_orcredited_asreviewed=True,
        source_event_links_not_original_location_earned_progress_orchronological_proximity=True,
        no_current_dialogue_ROM_orcounter_change=True,full_goal_complete=False))
