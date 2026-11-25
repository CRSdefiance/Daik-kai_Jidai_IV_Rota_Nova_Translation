"""Prepare a history-preserving checkpoint for22 uncredited native-approved drafts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/checkpoint_lil_B202_native_v5980.py').read_text(encoding='utf-8')
    names_line=next(s for s in old.splitlines() if "inventory['B202_names_and_spoken_title_context_v5980']" in s)
    move_line=next(s for s in old.splitlines() if "move=read('work/analysis/storage_recovery_v5974" in s)
    move_inventory=next(s for s in old.splitlines() if "inventory['dependency_storage_recovery_v5980']" in s)
    proof=derive('scripts/checkpoint_lil_B202_native_v5980.py','scripts/checkpoint_lil_B203_native_v6032.py',{
        'nineteen uncredited':'twenty-two uncredited','B202':'B203','native_checkpoint_text_v5980':'native_checkpoint_text_v6032',
        'native_checkpoint_v5980':'native_checkpoint_v6032','verification_v5981':'verification_v6033','verification_v5958':'verification_v6009',
        'native_approval_v5979':'native_approval_v6031','all19_source_prose_current_native_approval':'all22_source_prose_current_native_approval',
        'native_approved_v5980':'native_approved_v6032','unfinished_editorial_scope_v5980':'unfinished_editorial_scope_v6032',
        'all19_five_gates':'all22_five_gates',"len(doc['records'])==19":"len(doc['records'])==22",
        "len(approval['formatter_negatives'])==14":"len(approval['formatter_negatives'])==28",
        "approval['source_consumer_negatives']==21":"approval['source_consumer_negatives']==22",
        "approval['covered_native_alignment_cases']==152":"approval['covered_native_alignment_cases']==176",
        'all19_objects':'all22_objects','all_routes_unified_v5947':'all_routes_unified_v5998',
        "len(manifest['batches'])==589":"len(manifest['batches'])==590",move_line:'',move_inventory:'',
        "old['unfinished_editorial_scope_v5957']":"old['unfinished_editorial_scope_v6008']",
        'historical_B202_clean_only_before_v5980':'historical_B203_clean_only_before_v6032',
        'Lil_B202_clean_only_uncredited_v5957':'Lil_B203_clean_only_uncredited_v6008',
        'Lil_B202_native_review_v5980':'Lil_B203_native_review_v6032',
        'reviewed_uncredited_objects=19,revisions=6':'reviewed_uncredited_objects=22,revisions=9',
        'native_covered_alignments=152,source_consumer_negatives=21,formatter_negatives=14,actual_source_speeches=19':'native_covered_alignments=176,source_consumer_negatives=22,formatter_negatives=28,actual_source_speeches=22',
        names_line:"        inventory['B203_names_and_unspoken_item_title_context_v6032']=dict(proof=doc['contextual_reconciliation'],source_defined_Mysterious_Old_Man_retained_no_doctor_or_nationality_invented=True,Mikhail_full_middle_name_and_progressive_omission_preserved=True,item18_card_bound_without_inserting_an_unspoken_title=True,no_global_name_or_item_widget_completion_credit=True)",
        'following_B43_source_item_term_observed_v5980':'following_B43_source_item_term_observed_v6032','frame=7690':'frame=8410',
        "Path('scripts/lil_B202_native_checkpoint_text_v5980.py')":"Path('scripts/lil_B203_native_checkpoint_text_v6032.py')",
        ",Path('work/analysis/storage_recovery_v5974/verified_dependency_move.json')":'',
        'B202_uncredited_objects=19':'B203_uncredited_objects=22',
        'reviewed_uncredited_objects=19,revised=6':'reviewed_uncredited_objects=22,revised=9',
        '## V5980: B202 native-reviewed19 objects await integration;V5947 preserved':'## V6032: B203 native-reviewed22 objects await integration;V5998 preserved',
        '# Current editorial handoff - V5980':'# Current editorial handoff - V6032',
        '19 native-reviewed B202 drafts remain uncredited,V5947 unchanged':'22 native-reviewed B203 drafts remain uncredited,V5998 unchanged',
        "new['records_editorially_completed']==6308 and new['records_with_source_and_prose_pass']==6311":"new['records_editorially_completed']==6327 and new['records_with_source_and_prose_pass']==6330",
        'six targets,19 five-gate drafts':'six targets,22 five-gate drafts',
        "'B202_clean_source_glosses':19,'B202_native_approved_uncredited_objects':19":"'B203_clean_source_glosses':22,'B203_native_approved_uncredited_objects':22",
        "'B202_actual_source_speeches':19":"'B203_actual_source_speeches':22",
        'Verified V5980:B20219 native-approved uncredited drafts,V5947/6308':'Verified V6032:B20322 native-approved uncredited drafts,V5998/6327',
    })
    root=Path('work/analysis/lil_B203_native_checkpoint_tools_v6032');root.mkdir(parents=True);save(root/'derivation.json',proof)
