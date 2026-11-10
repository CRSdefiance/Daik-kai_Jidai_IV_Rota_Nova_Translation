"""Credit351 unique contextual reviews only after registered patch and own-startup proofs."""
import gzip
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Rafael867_extended_release_verified_v3_20261105')
FINAL=Path('translations/rafael351_integrated_final_review_v2.json')
FAMILY='Rafael_SC0_B121_B140_contextual_integrated_20261105'
BATCH='Rafael_SC0_B121_B140_clean_20261105'
CONTEXT='contextual_story_natural_dialogue_pass_v1871'


def main():
    assert not FINAL.exists() and not (ROOT/'completion_checkpoint.json').exists()
    rp,sp,np=[ROOT/p for p in ['registered_release_verification.json','own_registered_startup_verification.json','own_Fernan_name_getter_verification.json']]
    release,startup,names=map(load,[rp,sp,np])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(sp.read_bytes())==release['own_registered_startup_sha256']
    candidate=Path(release['candidate'])
    assert sha(candidate.read_bytes())==release['candidate_sha256']==startup['candidate_sha256']==names['runtime']['candidate_sha256']
    assert candidate.read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks'])==(681,114,26)
    assert release['all_eight_registered_final_stages_preserved'] and release['exact_all_integrated_references_bound']
    assert sha(Path('translations/release_stack.json').read_bytes())==release['registry_sha256']
    assert startup['actual_captain_getter']==startup['actual_route_word']==0
    assert names['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    for path in ['work/analysis/Rafael867_extended_release_verify_gc_v3_20261105/completion.json',
        'work/analysis/Rafael867_extended_startup_gc_v3_20261105/completion.json',
        'work/analysis/Rafael867_extended_Fernan_gc_v3_20261105/completion.json']:
        t=load(path);assert t['terminal'] and t['completed_without_exception'] and t['all_locked_sources_unchanged']
        assert not t['garbage_collection']['errors']
    prep=load(release['preparation']);assert len(prep['configs'])==1
    conf=load(prep['configs'][0]);origin=Path(conf['manuscript']);doc=load(origin)
    bp=Path(release['exact_record_bindings']);assert sha(bp.read_bytes())==release['exact_record_bindings_sha256']
    bindings=load(bp)['records'];originals={(r['file_path'],r['id']):r for r in doc['records']}
    rows=[]
    for bound in bindings:
        row=deepcopy(originals[(bound['file_path'],bound['id'])])
        assert all(row[k]==bound[k] for k in ['source_reference','source_hex','current_reference','current_hex','decision','finding','review'])
        assert len(row['review'])==5 and all(row['review'].values())
        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_andcompletion_credit_pending')
        row.update(planned_integrated_reference=bound['registered_reference'],registered_integration_pending=False,
            registered_release_andcompletion_credit_pending=False,new_source_credit_eligible=True,
            registered_target_ROM=str(candidate),registered_target_ROM_sha256=release['candidate_sha256'],
            source_review_manuscript=str(origin),source_review_manuscript_sha256=sha(origin.read_bytes()))
        rows.append(row)
    keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows]
    assert len(rows)==len(originals)==len({(r['file_path'],r['id']) for r in rows})==351
    assert (sum(r['decision']=='revision' for r in rows),sum(r['decision']=='retention' for r in rows))==(201,150)
    ledger_path=Path('translations/editorial_review_current_v1.json');before=ledger_path.read_bytes();prior=load(ledger_path)
    assert prior['records_editorially_completed']==12361 and not prior['full_goal_complete']
    assert prior[BATCH]['new_credit']==0 and prior['current_integrated_candidate']['sha256']==release['parent_sha256']
    assert FAMILY not in prior and not any(u['id']==FAMILY for u in prior['coverage_units'])
    context=deepcopy(prior[CONTEXT]);oldkeys={(r['file_path'],r['id']) for r in context['record_keys']}
    assert len(oldkeys)==len(context['integrated_record_keys'])==12361
    assert not oldkeys & {(r['file_path'],r['id']) for r in keys}
    scope=dict(source_variants=341,native_body_pages=344,typed_labels=10,observed_source_variants=132,
        observed_body_pages=134,offline_only_source_variants=209,actual_review=conf['actual'],
        actual_review_sha256=sha(Path(conf['actual']).read_bytes()),actual_menu_cursor_states=[0],
        other_menu_states_returns_branches_andcancellation_offline_only=True,
        own_registered_startup_frames=4001,natural_conditional_activation=False,original_locations=False,
        earned_chronology=False,full_route=False,hardware=False,full_catalogue_UI_unvisited=True,guide_photos=False)
    save(FINAL,dict(format='dk4-composite-integrated-editorial-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=rows,records_count=351,new_source_records=351,proposed_new_revisions=201,justified_new_retentions=150,
        all351_individual_five_gates_pass=True,target_ROM=str(candidate),target_ROM_sha256=release['candidate_sha256'],
        registered_release=str(rp),registered_release_sha256=sha(rp.read_bytes()),actual_verification_scope=scope,
        full_goal_complete=False,new_credit=0,guide_photos=False,evidence={str(p):sha(p.read_bytes()) for p in [bp,rp,sp,np,origin,Path(__file__)]}))
    family=dict(id=FAMILY,kind='story-contextual-records',records=351,record_keys=keys,final_review=str(FINAL),
        final_review_sha256=sha(FINAL.read_bytes()),revised_count=201,retained_count=150,fresh_revisions=201,
        fresh_retentions=150,actual_verification_scope=scope,integrated_record_bindings=str(bp))
    ledger=dict(prior)
    ledger['completed_editorial_families']=[*prior['completed_editorial_families'],family]
    ledger['coverage_units']=[*prior['coverage_units'],dict(**family,status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=351,release_verification=str(rp),release_verification_sha256=sha(rp.read_bytes()),full_goal_complete=False)]
    for field,n in [('records_editorially_completed',351),('records_revised_and_integrated',201),
        ('retained_wordings_editorially_completed',150),('records_with_source_and_prose_pass',351),('records_with_source_prose_drafts',351)]:ledger[field]+=n
    for field in ['record_keys','integrated_record_keys']:context[field].extend(keys)
    context['record_IDs'].extend(r['id'] for r in rows)
    context['fresh_pass_records_explicitly_reread']+=351;context['fresh_pass_records_integrated']+=351
    context.update(latest_completed_family=FAMILY,latest_final_review=str(FINAL))
    context['reconciled_families'].append(dict(id=FAMILY,records=351,final_review=str(FINAL),new_revisions=201,justified_retentions=150,
        new_completed_records=351,historical_reconciliation_only=False,actual_verification_scope=scope))
    ledger[CONTEXT]=context
    completed=dict(registered_integration_pending=False,completed_in_combined_family=FAMILY,
        registered_release_verification=str(rp),registered_release_verification_sha256=sha(rp.read_bytes()),
        own_registered_startup=str(sp),own_registered_startup_sha256=sha(sp.read_bytes()),
        own_Fernan_name_getters=str(np),own_Fernan_name_getters_sha256=sha(np.read_bytes()),main_unchanged=True)
    ledger[BATCH]={**prior[BATCH],**completed,'new_credit':351,'completion_credit_added':351,'all_five_registered_review_gates_pass':True}
    ledger[FAMILY]=dict(**completed,new_credit=0,total_new_source_records_credited=351,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()))
    combined='Rafael867_qualified_cumulative_research_20261105'
    ledger[combined]={**prior[combined],**completed,'new_credit':0,'remaining_new_source_credit':0,
        'registered_integration_andclean_input_patch_pending':False,'all867_registered_andcredited_in_two_disjoint_families':True}
    current=deepcopy(prior['current_integrated_candidate'])
    current.update(path=str(candidate),sha256=release['candidate_sha256'],profile=release['profile'],SC0_sha256=release['target_SC0_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(rp),experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    ledger['current_integrated_candidate']=current
    ledger['latest_checkpoint']='Rafael351 integrated once after516:12712 complete/7283 revisions/5429 retentions;681 entries/114 accepted layers/eight stages/exact clean patch/own startup/Fernan getters pass. All867 research reviews are integrated. Continue Rafael early story/tutorial priority;main/full scope unchanged.'
    allowed={'completed_editorial_families','coverage_units','records_editorially_completed','records_revised_and_integrated',
        'retained_wordings_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts',CONTEXT,BATCH,FAMILY,combined,'current_integrated_candidate','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in prior.items() if k not in allowed}
    for field in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:assert context[field][:len(prior[CONTEXT][field])]==prior[CONTEXT][field]
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==12712
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(7283,5429)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==12715
    backup=ROOT/'ledger_before_completion.json.gz';assert not backup.exists()
    backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);pending=ledger_path.with_name('editorial_review_current.Rafael351_completion_v2.pending.json')
    assert not pending.exists() and ledger_path.read_bytes()==before;pending.write_bytes(encoded)
    save(ROOT/'completion_mutation_plan.json',dict(ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),pending=str(pending),family=FAMILY,
        new_credit=351,all_unrelated_keys_andearlier_record_prefixes_exact=True))
    os.replace(pending,ledger_path);assert ledger_path.read_bytes()==encoded
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=351,counts=dict(completed=12712,revised=7283,retained=5429),
        source_prose_draft_historical_counts=12715,ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),
        all_unrelated_keys_andearlier_record_prefixes_exact=True,main_unchanged=True,full_goal_complete=False,guide_photos=False))
    print('Credited351 unique source reviews once:12712 complete/7283 revisions/5429 retentions. All867 nowintegrated;main unchanged/full goal active.')


if __name__=='__main__':main()
