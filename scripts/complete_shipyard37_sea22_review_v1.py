"""Credit59 Help source articles once after the Command amendment,675 stack,clean patch andown startup pass."""
import gzip,os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Sea22_Fleet66_release_verified_20261105')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/help_shipyard_sea59_integrated_final_review_v1.json')
FAMILY='shared_HELP_shipyard37_sea22_Command66_complete_contextual_release_20261105'
KEY37='shared_HELP_T44_T80_contextual_20261104'
KEY22='shared_HELP_T81_T102_contextual_20261104'
KEY66='shared_HELP66_Command_amendment_20261104'
COMBINED='sea22_fleet66_registered_cumulative_20261105'
INPUTS=[Path('translations')/p for p in ['help_shipyard37_contextual_final_review_v3.json','help_sea22_contextual_final_review_v1.json','help_fleet66_Command_contextual_amendment_v2.json']]

if __name__=='__main__':
    assert not FINAL.exists() and not (ROOT/'completion_checkpoint.json').exists()
    rp,sp,np=[ROOT/p for p in ['registered_release_verification.json','own_registered_startup_verification.json','own_Fernan_name_getter_verification.json']]
    release,startup,names=map(load,[rp,sp,np])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(sp.read_bytes())==release['own_registered_startup_sha256']
    candidate=Path(release['candidate']);assert sha(candidate.read_bytes())==release['candidate_sha256']==startup['candidate_sha256']==names['runtime']['candidate_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes()==candidate.read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks'])==(675,114,26)
    assert release['all_eight_registered_final_stages_preserved'] and release['all59_exact_integrated_references_bound']
    assert all(load(Path(release['manifest']))['checks'].values()) and sha(Path('translations/release_stack.json').read_bytes())==release['registry_sha256']
    assert startup['actual_captain_getter']==startup['actual_route_word']==0
    assert startup['changed_HELP_bound_to60_native_39_observed_21_offline_pages_across_three_proof_groups']
    assert names['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    cp=Path(release['composite_page_coverage']);coverage=load(cp);assert sha(cp.read_bytes())==release['composite_page_coverage_sha256']
    assert not coverage['all60_observed_on_one_final_ROM']
    assert (coverage['native_andvisually_reviewed_pages'],coverage['observed_pages'],coverage['observed_articles'],coverage['offline_only_pages'])==(60,39,38,21)
    binding_path=ROOT/'exact_integrated_record_bindings.json';bindings=load(binding_path)
    assert sha(binding_path.read_bytes())==release['exact_record_bindings_sha256'] and len(bindings['records'])==59
    bound={r['topic_id']:r for r in bindings['records']};assert set(bound)==set(range(44,103))
    clean=NdsImage.open('work/clean.nds').read_file('/COMMON/HELP.DK4');resource=NdsImage.open(candidate).read_file('/COMMON/HELP.DK4')
    selected={};origins={}
    for path in INPUTS:
        doc=load(path);current=NdsImage.open(doc['current_ROM']).read_file('/COMMON/HELP.DK4')
        assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
        for row in doc['records']:
            sr,cr=row['source_reference'],row['current_reference'];source,prior=map(bytes.fromhex,[row['source_hex'],row['current_hex']])
            assert clean[sr['archive_offset']:sr['archive_offset']+len(source)]==source
            assert current[cr['archive_offset']:cr['archive_offset']+len(prior)]==prior
            assert sr['bytes']==len(source) and cr['bytes']==len(prior) and all(row['review'].values())
            selected[row['topic_id']]=deepcopy(row);origins[row['topic_id']]=dict(manuscript=str(path),manuscript_sha256=sha(path.read_bytes()),
                current_comparison_ROM=doc['current_ROM'],current_comparison_ROM_sha256=doc['current_ROM_sha256'])
    assert set(selected)==set(bound)
    rows=[]
    for topic,row in sorted(selected.items()):
        pages=bound[topic]['registered_pages'];assert bound[topic]['source_hex']==row['source_hex'] and bound[topic]['current_hex']==row['current_hex']
        samples=[]
        for page in pages:
            at=page['archive_offset'];raw=bytes.fromhex(page['exact_stored_hex']);assert resource[at:at+len(raw)]==raw
            if 'actual_frame' in page:
                actual=load(Path(page['source_page_proof']))
                sample=next(s for s in actual['actual_HELP_cases'] if s['topic_id']==page['block'])
                assert sample['frame']==page['actual_frame'] and sample['all_first_internal_final_glyphs_andblank_gaps_exact'];samples.append(sample)
        row.update(planned_stored_pages=pages,actual_source_bound_samples=samples,actual_gameplay=bool(samples),offline_only=not samples,
            registered_integration_pending=False,fresh_display_allocation_widgets_andintegration_pending=False,
            formatting_parent_reference_is_planned_not_yet_verified_cumulative=False,
            exact_source_current_reference_context=origins[topic],registered_target_ROM=str(candidate),registered_target_ROM_sha256=release['candidate_sha256'])
        rows.append(row)
    assert len(rows)==59 and (sum(r['decision']=='revision' for r in rows),sum(r['decision']=='retention' for r in rows))==(44,15)
    final=dict(format='dk4-composite-integrated-help-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/COMMON/HELP.DK4',
        records=rows,records_count=59,proposed_revisions=44,justified_retentions=15,all59_individual_five_gates_pass=True,
        target_ROM=str(candidate),target_ROM_sha256=release['candidate_sha256'],target_HELP_sha256=sha(resource),
        reference_policy='Each source/current pair is bound to its explicit per-record comparison ROM;registered pages use final archive offsets. Three actual proof groups are not one final-ROM playthrough.',
        native_andviewed_pages=60,observed_pages=39,observed_articles=38,offline_only_pages=21,offline_only_articles=21,
        amendment66_is_part_of_its_single_original_source_credit=True,registered_release=str(rp),registered_release_sha256=sha(rp.read_bytes()),
        full_goal_complete=False,new_credit=0,guide_photos=False,evidence={str(p):sha(p.read_bytes()) for p in [*INPUTS,binding_path,rp,sp,np,cp,Path(__file__)]})
    before=LEDGER.read_bytes();prior=load(LEDGER)
    assert prior['records_editorially_completed']==11359 and not prior['full_goal_complete']
    p37=load(Path('work/analysis/Shipyard_HELP37_release_verified_20261104/registered_release_verification.json'))
    assert prior['current_integrated_candidate']['sha256']==p37['parent_sha256'] and release['parent_sha256']==p37['candidate_sha256']
    for key in [KEY37,KEY22,KEY66,COMBINED]:assert key in prior and prior[key].get('new_credit',0)==0
    assert not any(r['id']==FAMILY for r in prior['coverage_units'])
    context=deepcopy(prior['contextual_story_natural_dialogue_pass_v1871'])
    keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows];old={(r['file_path'],r['id']) for r in context['record_keys']}
    assert len(old)==len(context['integrated_record_keys'])==11359 and not old&{(r['file_path'],r['id']) for r in keys}
    save(FINAL,final)
    scope=dict(native_pages=60,actual_pages=39,actual_articles=38,offline_only_pages=21,offline_only_articles=21,
        actual_page_proof_groups=coverage['proof_groups'],one_final_ROM_60_page_playthrough=False,own_registered_Rafael_startup_frames=4001,
        composite_provenance=str(cp),composite_provenance_sha256=sha(cp.read_bytes()),full_route=False,hardware=False,guide_photos=False)
    family=dict(id=FAMILY,kind='help-articles',file_path='/COMMON/HELP.DK4',records=59,help_articles=59,record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),revised_count=44,retained_count=15,fresh_revisions=44,fresh_retentions=15,
        actual_verification_scope=scope,integrated_record_bindings=str(binding_path))
    ledger=dict(prior);ledger['completed_editorial_families']=[*prior['completed_editorial_families'],family]
    ledger['coverage_units']=[*prior['coverage_units'],dict(**family,status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=59,release_verification=str(rp),release_verification_sha256=sha(rp.read_bytes()),full_goal_complete=False)]
    for key,n in [('records_editorially_completed',59),('records_revised_and_integrated',44),('retained_wordings_editorially_completed',15),('records_with_source_and_prose_pass',59),('records_with_source_prose_drafts',59)]:ledger[key]+=n
    for field in ['record_keys','integrated_record_keys']:context[field].extend(keys)
    context['record_IDs'].extend(r['id'] for r in rows);context['fresh_pass_records_explicitly_reread']+=59;context['fresh_pass_records_integrated']+=59
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY,records=59,help_articles=59,final_review=str(FINAL),new_revisions=44,justified_retentions=15,
        new_completed_records=59,historical_reconciliation_only=False,actual_verification_scope=scope))
    ledger['contextual_story_natural_dialogue_pass_v1871']=context
    for key,count in [(KEY37,37),(KEY22,22)]:
        ledger[key]={**prior[key],**dict(new_credit=count,completion_credit_added=count,registered_integration_pending=False,
            final_manifest_patch_andown_RAM_binding_pending=False,only_research_HELP_changed_registered_output_pending=False,
            completed_in_combined_family=FAMILY,registered_release_verification=str(rp),registered_release_verification_sha256=sha(rp.read_bytes()),
            registered_build_live=False,final_registered_release_patch_own_startup_andcredit_pending=False,main_unchanged=True)}
    for key in [KEY66,COMBINED]:
        ledger[key]={**prior[key],**dict(new_credit=0,total_new_source_records_credited_as_combined_family=59 if key==COMBINED else 0,
            registered_integration_pending=False,build_live=False,registered_build_live=False,registered_cumulative_build_live=False,
            build_terminal=True,build_exit_code=0,registered_build=dict(session=71768,PID=113672,terminal=True,exit_code=0),
            registered_release_verification=str(rp),registered_release_verification_sha256=sha(rp.read_bytes()),
            own_registered_startup=str(sp),own_registered_startup_sha256=sha(sp.read_bytes()),own_Fernan_name_getters=str(np),own_Fernan_name_getters_sha256=sha(np.read_bytes()),
            final_registered_release_patch_own_startup_andcredit_pending=False,completed_in_combined_family=FAMILY,main_unchanged=True)}
    image=NdsImage.open(candidate)
    ledger['current_integrated_candidate']=dict(path=str(candidate),sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),HELP_sha256=sha(resource),
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(rp),experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint']='Shipyard37 plusSea22 integrated/credited once withCommand66 corrected:11418 completions/6645 revisions/4773 retentions.675 entries/114 layers/eightstages/exact clean patch/ownstartup pass.97 Help sources plusCoerce33 amendment awaitintegration;Rafael330 source/prose/display work continues,main unchanged.'
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==11418
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(6645,4773)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==11421
    allowed={'completed_editorial_families','coverage_units','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','records_with_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',KEY37,KEY22,KEY66,COMBINED,'current_integrated_candidate','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in prior.items() if k not in allowed}
    for field in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:
        assert context[field][:len(prior['contextual_story_natural_dialogue_pass_v1871'][field])]==prior['contextual_story_natural_dialogue_pass_v1871'][field]
    backup=ROOT/'ledger_before_completion.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);temp=LEDGER.with_name('editorial_review_current.shipyard_sea59_completion.pending.json');assert not temp.exists() and LEDGER.read_bytes()==before
    temp.write_bytes(encoded);os.replace(temp,LEDGER);assert LEDGER.read_bytes()==encoded
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=59,counts=dict(completed=11418,revised=6645,retained=4773),
        ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),all_unrelated_keys_andearlier_record_prefixes_exact=True,
        source_prose_draft_historical_counts=11421,main_unchanged=True,full_goal_complete=False,guide_photos=False))
    print('Credited59 Help source articles once:11418 completions/6645 revisions/4773 retentions;Command66 corrected. Fullgoalactive/main unchanged.')
