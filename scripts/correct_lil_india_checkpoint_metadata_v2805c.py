"""Correct inherited chapter/scope labels; preserve119-credit receipt andcounts."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_India_Polder_checkpoint_v2805c')
PRIOR=Path('work/analysis/lil_India_Polder_checkpoint_v2805b/checkpoint_receipt.json')
OLD_TITLE='## V2805:119 post-Seville and Egypt-warning reviews; reference and release pending'
NEW_TITLE='## V2805:119 India, Camille, polder and gift reviews; release pending'
if __name__=='__main__':
    assert not ROOT.exists();receipt=read(PRIOR)
    for p,digest in receipt['updated_files'].items():assert sha(Path(p).read_bytes())==digest,p
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    family=ledger['contextual_story_natural_dialogue_pass_v1871']['latest_pending_contextual_family']
    pending='Complete193-command references,all40relative spans/200relocated branch cases,tenrelocated predicates,119finalparity targets/476macroalignments,336wholeblock loaders/two parentmodes/fullentrycensus,representative sharedrules andguarded cumulativeV2783integration/exactcleanpatch/required currentstartup.'
    ledger['active_source_prose_drafts']['status']='3-reviewed-COMMON-incomplete;119-India-Camille-polder-gift-native-reviewed-pending-release'
    for item in ledger['contextual_story_natural_dialogue_pass_v1871']['pending_contextual_families']:item['pending']=pending
    ledger['lil_India_Polder_source_prose_native_v2805']['pending']=pending
    for item in ledger['coverage_units']:
        if item['id']==family:item['pending']=pending
        if item['id']=='all-route-scenes':item['next']='Integrate119 reviewed India/Camille/polder/gift speeches after reference,representative andregistered-release gates;continue every untouched storyline/shared shop-town/random/player prose family.'
    docs=[Path(p) for p in receipt['updated_files'] if Path(p).parent==Path('docs')]
    assert len(docs)==5 and all(p.read_text(encoding='utf8').count(OLD_TITLE)==1 for p in docs)
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    for p in docs:p.write_text(p.read_text(encoding='utf8').replace(OLD_TITLE,NEW_TITLE,1),encoding='utf8',newline='\n')
    for k in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file','completed_editorial_families','current_integrated_candidate','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:assert ledger[k]==before[k]
    for k in ['record_keys','integrated_record_keys','pending_record_keys','fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release']:assert ledger['contextual_story_natural_dialogue_pass_v1871'][k]==before['contextual_story_natural_dialogue_pass_v1871'][k]
    save(lp,ledger)
    correction=ROOT/'heading_and_scope_metadata_correction.json'
    save(correction,dict(prior_receipt=str(PRIOR),prior_receipt_sha256=sha(PRIOR.read_bytes()),before_files=receipt['updated_files'],after_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},old_title=OLD_TITLE,new_title=NEW_TITLE,only_human_scope_labels_changed=True,coverage_keys_counts_and_all_completed_records_unchanged=True,this_operation_adds_source_prose_orcompletion_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    combined=deepcopy(receipt);combined.update(updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},baseline_checkpoint_root='work/analysis/lil_India_Polder_checkpoint_v2805b',metadata_correction=str(correction),metadata_correction_sha256=sha(correction.read_bytes()),this_operation_adds_source_prose_orcompletion_credit=0,producer_sha256=sha(Path(__file__).read_bytes()))
    combined['evidence'].update({str(PRIOR):sha(PRIOR.read_bytes()),str(correction):sha(correction.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())})
    save(ROOT/'checkpoint_receipt.json',combined)
    print('Corrected119-batch chapter heading and40-site operational labels. Allcoverage counts/records/ROMs unchanged;original119-credit receipt preserved.')
