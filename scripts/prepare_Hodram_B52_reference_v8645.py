"""Derive a pinned B52 research image from whole registered V8609, with exact scope labels."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_reference_tools_v8645');assert not root.exists()
    result=derive('scripts/create_Hodram_B51_reference_v8570.py','scripts/create_Hodram_B52_reference_v8645.py',{
        'Hodram_B51_reference_v8570':'Hodram_B52_reference_v8645','all_routes_combined_v8543_candidate':'all_routes_combined_v8609_candidate',
        'Hodram_B51_relocation_v8565':'Hodram_B52_relocation_v8642','Hodram_B51_independent_v8569':'Hodram_B52_independent_v8644','Hodram_B51_stored_v8566':'Hodram_B52_stored_v8643','hodram_B51_editorial_manuscript_v2':'hodram_B52_editorial_manuscript_v3',
        'all-routes-unified-v8543':'all-routes-unified-v8609',"len(manifest['batches'])==644":"len(manifest['batches'])==645",
        'all5_full_first_internal_final_glyphs_bounds_consumption_single_page_andviewed_ink_checks_pass':'all3_speech_full_first_internal_final_glyphs_bounds_consumption_single_page_andviewed_ink_checks_pass',
        "len(controls['stored_dispatches'])==5 and len(controls['normal_seeded_ends'])==25 and len(stored['records'])==5":"len(controls['stored_dispatches'])==3 and len(controls['distinct_seeded_ends'])==50 and len(stored['records'])==3 and len(stored['typed_choice_records'])==2",
        'if a!=b]==[51]':'if a!=b]==[52]',
        'only_changed_blocks=[50]':'only_changed_blocks=[52]',
        'B51 five-speech research reference from completeV8543;onlySC1B51':'B52 three-speech/two-choice research reference from completeV8609;onlySC1B52',
        'B51 research reference from full registered V8543':'B52 research reference from full registered V8609',
        'Pinned B51researchreference fromfullV8543;onlySC1B51':'Pinned B52researchreference fromfullV8609;onlySC1B52',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,correct_B52_scope_label_andthree_speech_two_choice_fifty_end_counts=True,all_registered_manifest_accepted_main4701_wholeROM_inverse_andprior_pin_guards_preserved=True,research_only_no_handoff_promotion_orcredit=True,new_credit=0,full_goal_complete=False))
