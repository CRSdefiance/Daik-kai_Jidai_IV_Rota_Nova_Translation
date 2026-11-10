"""Credit23 source Help articles once only after registered clean patch/own startup/name bindings pass."""
import gzip,os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Early_HELP23_release_verified_20261104')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/help_early23_contextual_final_review_v1.json')
KEY='shared_HELP_T00_T20_contextual_20261104'
FAMILY='shared_HELP_early23_complete_contextual_release_20261104'
if __name__=='__main__':
    assert not (ROOT/'completion_checkpoint.json').exists()
    release_path=ROOT/'registered_release_verification.json';startup_path=ROOT/'own_registered_startup_verification.json'
    names_path=ROOT/'own_Fernan_name_getter_verification.json'
    doc,release,startup,names=map(load,[FINAL,release_path,startup_path,names_path])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(startup_path.read_bytes())==release['own_registered_startup_sha256']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==startup['candidate_sha256']==names['runtime']['candidate_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks'])==(671,114,26)
    assert release['all_eight_registered_final_stages_preserved'] and release['all23_exact_integrated_references_bound']
    assert all(load(release['manifest'])['checks'].values())
    assert sha(Path('translations/release_stack.json').read_bytes())==release['registry_sha256']
    assert sha(Path(release['canonical_base']).read_bytes())==release['canonical_sha256']
    assert startup['actual_captain_getter']==startup['actual_route_word']==0 and startup['changed_HELP_exact_to_separately_observed25_pages']
    assert names['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    assert len(doc['records'])==23 and (doc['proposed_revisions'],doc['justified_retentions'])==(16,7)
    actual=load(release['actual_help_proof']);assert (actual['actual_pages'],actual['actual_articles'],actual['cold_boot_frames'])==(25,23,32761)
    assert actual['all25_complete_actual_pages_andnative_child_targets_pass']
    assert len(actual['original_forward_back_andL_R_history_returns'])==3
    bindings=load(ROOT/'exact_integrated_record_bindings.json');assert len(bindings['records'])==23
    assert {r['id'] for r in bindings['records']}=={r['id'] for r in doc['records']} and all(all(r['review'].values()) for r in bindings['records'])
    before=LEDGER.read_bytes();prior=load(LEDGER)
    assert prior['records_editorially_completed']==11313 and prior['current_integrated_candidate']['sha256']==release['parent_sha256']
    assert prior[KEY].get('new_credit',0)==0 and not prior['full_goal_complete']
    assert not any(r['id']==FAMILY for r in prior['coverage_units'])
    context=deepcopy(prior['contextual_story_natural_dialogue_pass_v1871']);keys=[dict(file_path=r['file_path'],id=r['id']) for r in doc['records']]
    old={(r['file_path'],r['id']) for r in context['record_keys']};assert len(old)==len(context['integrated_record_keys'])==11313
    assert not old&{(r['file_path'],r['id']) for r in keys}
    scope=dict(actual_ordinary_Help_frames=32761,actual_articles=23,actual_pages=25,offline_only_articles=0,
        native_pages=25,own_registered_Rafael_startup_frames=4001,all_three_continuation_history_return_pairs_verified=True,
        actual_proof=release['actual_help_proof'],actual_proof_sha256=release['actual_help_proof_sha256'],
        title_menu_Help_not_story_playthrough=True,full_route=False,hardware=False,guide_photos=False)
    family=dict(id=FAMILY,kind='help-articles',file_path=doc['file_path'],records=23,help_articles=23,record_IDs=[r['id'] for r in doc['records']],
        final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),revised_count=16,retained_count=7,fresh_revisions=16,fresh_retentions=7,
        actual_verification_scope=scope,integrated_record_bindings=str(ROOT/'exact_integrated_record_bindings.json'))
    ledger=dict(prior);ledger['completed_editorial_families']=[*prior['completed_editorial_families'],family]
    ledger['coverage_units']=[*prior['coverage_units'],dict(**family,status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=23,release_verification=str(release_path),release_verification_sha256=sha(release_path.read_bytes()),full_goal_complete=False)]
    for key,n in [('records_editorially_completed',23),('records_revised_and_integrated',16),('retained_wordings_editorially_completed',7),
        ('records_with_source_and_prose_pass',23),('records_with_source_prose_drafts',23)]:ledger[key]+=n
    for field in ['record_keys','integrated_record_keys']:context[field].extend(keys)
    context['record_IDs'].extend(r['id'] for r in doc['records']);context['fresh_pass_records_explicitly_reread']+=23;context['fresh_pass_records_integrated']+=23
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY,records=23,help_articles=23,final_review=str(FINAL),new_revisions=16,justified_retentions=7,
        new_completed_records=23,historical_reconciliation_only=False,actual_verification_scope=scope))
    ledger['contextual_story_natural_dialogue_pass_v1871']=context
    ledger[KEY]={**prior[KEY],**dict(new_credit=23,completion_credit_added=23,registered_integration_pending=False,
        only_research_HELP_changed_registered_output_pending=False,final_manifest_patch_andown_RAM_binding_pending=False,
        registered_build=dict(session=61834,PID=102816,terminal=True,exit_code=0),
        registered_release_verification=str(release_path),registered_release_verification_sha256=sha(release_path.read_bytes()),
        own_registered_startup=str(startup_path),own_registered_startup_sha256=sha(startup_path.read_bytes()),
        own_Fernan_name_getters=str(names_path),own_Fernan_name_getters_sha256=sha(names_path.read_bytes()),main_unchanged=True)}
    image=NdsImage.open(release['candidate'])
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),HELP_sha256=sha(image.read_file('/COMMON/HELP.DK4')),
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(release_path),experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint']='Early Help23 registered andcredited once:11336 completions/6582 revisions/4754 retentions;671 entries/all eight stages/exact clean patch/own Rafael startup pass. Next town Help23 research/all broader scope active;main preserved.'
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==11336
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(6582,4754)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==11339
    allowed={'completed_editorial_families','coverage_units','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','records_with_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',KEY,'current_integrated_candidate','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in prior.items() if k not in allowed}
    for field in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:
        assert context[field][:len(prior['contextual_story_natural_dialogue_pass_v1871'][field])]==prior['contextual_story_natural_dialogue_pass_v1871'][field]
    backup=ROOT/'ledger_before_completion.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);temp=LEDGER.with_name('editorial_review_current.early_HELP23_completion.pending.json')
    assert not temp.exists() and LEDGER.read_bytes()==before;temp.write_bytes(encoded);os.replace(temp,LEDGER);assert LEDGER.read_bytes()==encoded
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=23,counts=dict(completed=11336,revised=6582,retained=4754),
        ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),all_unrelated_keys_andearlier_record_prefixes_exact=True,
        source_prose_draft_historical_counts=11339,main_unchanged=True,full_goal_complete=False,guide_photos=False))
    print('23 Help articles credited once:11336 completions/6582 revisions/4754 retentions;full goal active/main unchanged.')
