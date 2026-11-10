"""Finish only the approval receipt after the writer's path-type serialization error.

The already written manuscript/names are complete and immutable. Revalidate them
against the predecessor and original proofs; do not rewrite or rerun native work.
"""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_Hodram_B31_B53_format_v8745 import OLD,DOC,OLD_NAMES,NAMES,REVIEW,PROOFS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_format_v8745b')
FAILED=Path('scripts/approve_Hodram_B31_B53_format_v8745.py')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/Hodram_B31_B53_format_v8745/formatting_approval.json').exists()
    old,doc,oldnames,names,review=map(read,[OLD,DOC,OLD_NAMES,NAMES,REVIEW]);data={k:read(p) for k,p in PROOFS.items()}
    validate_natural_dialogue_batch(doc)
    assert doc['encoder']=='dialogue-relocatable-v1' and doc['predecessor_manuscript_sha256']==sha(OLD.read_bytes()) and doc['names_packet_sha256']==sha(NAMES.read_bytes())
    assert names['predecessor_review_sha256']==sha(OLD_NAMES.read_bytes()) and names['all_individual_scoped_five_gates_true']
    assert doc['actual_review_sha256']==sha(REVIEW.read_bytes()) and (review['total_runs'],review['total_frames'],review['total_holds'])==(4,24004,76)
    assert review['offline_only_text_IDs']==['DK4_MES_B31_R0013'] and review['all_four_sheets_directly_viewed']
    assert len(doc['records'])==3 and not doc['typed_choice_records']
    refs={r['id']:r for r in data['stored']['records']}
    for before,row in zip(old['records'],doc['records'],strict=True):
        for key in ['id','english','logical_English','compiled_hex','source_hex','source_reference','current_hex','current_reference','decision','finding','localization_note']:assert before[key]==row[key]
        assert all(v is True for v in row['review'].values()) and before['review']['formatting'] is False
        ref=refs[row['id']];assert row['final_reference']==row['stored_final_reference']==ref['final_reference'] and row['final_hex']==row['stored_hex']==ref['stored_hex']
        assert row['compiler_owned_parity_space']==ref['parity_space_added']==False and row['qa_waivers']==row['qa_waiver_scope']==[]
        assert row['formatting_approval_reason'] and row['formatting_registered_release_pending']
    assert all(not r['base_QA']['issues'] for r in data['plan']['records']) and not data['plan']['failures']
    for before,row in zip(oldnames['records'],names['records'],strict=True):
        assert before['actor_ID']==row['actor_ID'] and before['speaker']==row['speaker'] and before['reason']==row['reason']
        assert before['review']['formatting'] is False and all(v is True for v in row['review'].values())
    assert names['full_name_resolution']['actual_B31_progressive_header_verified'] and names['full_name_resolution']['full_catalogue_UI_still_unobserved']
    assert names['new_name_asset_changes']==0 and names['wider_catalogue_UI_all207_names_roles_aliases_customnames_andother_contexts_still_open']
    for packet in [doc,names,review]:assert packet['new_credit']==0 and not packet['full_goal_complete']
    paths=[OLD,DOC,OLD_NAMES,NAMES,REVIEW,*map(Path,PROOFS.values()),FAILED,Path(__file__)]
    ROOT.mkdir(parents=True);save(ROOT/'formatting_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        speech_approvals=3,scoped_progressive_name_approvals=2,all3_five_gates_true=True,standard_natural_dialogue_v2_validation_pass=True,
        all_source_current_final_references_words_compiledbytes_andindividual_prose_reasons_preserved=True,
        original_infos=0,warnings=0,waivers=0,offline_only_text_IDs=['DK4_MES_B31_R0013'],actual_unique_text_IDs=review['actual_unique_text_IDs'],measured_limits=review,
        source_name_fullgetter_composition_andretention_not_fullcatalogue_UI_approval=True,
        preserved_partial_complete_manuscript_andnames_generated_before_receipt_only_failure=True,stopped_writer=str(FAILED),stopped_writer_sha256=sha(FAILED.read_bytes()),
        qualification='The writer completed validated manuscript and name outputs before its receipt comprehension called read_bytes on a string path. This reader revalidates those exact complete outputs and writes only the missing receipt with Path-normalized evidence. No approval,prose,bytes orQA gate is weakened andno old output is overwritten.',
        frozen_policy_production_atomic_registered_patch_startup_andcredit_pending=True,new_native_runs=0,new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in paths}))
    print('Qualified existing completev4manuscript/v3names;standardv2 andall3formatting gates pass. Missingreceipt repaired separately;failedwriter andall outputs preserved. Formal integration pending,zero credit.',flush=True)
