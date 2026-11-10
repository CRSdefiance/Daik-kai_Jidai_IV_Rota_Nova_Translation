"""Credit539 once only after cumulative release,clean patch andown startup are verified."""
import gzip,os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Rafael_B61_B80_release_verified_20261104')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/rafael_B61_B80_contextual_final_review_v1.json')
RELEASE=ROOT/'registered_release_verification.json';STARTUP=ROOT/'own_registered_startup_verification.json'
OWN_NAMES=ROOT/'own_Fernan_name_getter_verification.json'
ACTUAL=Path('work/analysis/Rafael_B61_B80_checked_20261104/actual_review.json')
PIXELS=Path('work/analysis/Rafael_B61_B80_names_pagination_pixels_v12_20261104/focused_actual_pixels.json')
CG=Path('work/analysis/Rafael_B69_complete_scene_pixels_v12_20261104/focused_actual_pixels.json')
KEY='Rafael_SC0_B61_B80_clean_20261104'
FAMILY='Rafael_SC0_B61_B80_complete_contextual_release_20261104'

if __name__=='__main__':
    assert not (ROOT/'completion_checkpoint.json').exists()
    doc,release,startup,names,actual,pixels,cg=map(load,[FINAL,RELEASE,STARTUP,OWN_NAMES,ACTUAL,PIXELS,CG])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(STARTUP.read_bytes())==release['own_registered_startup_sha256']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==startup['candidate_sha256']==names['runtime']['candidate_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert release['complete_stack_entries']==670 and release['accepted_layers']==114 and release['all_eight_registered_final_stages_preserved']
    assert all(load(release['manifest'])['checks'].values())
    assert sha(Path('translations/release_stack.json').read_bytes())==release['registry_sha256']
    assert sha(Path(release['canonical_base']).read_bytes())==release['canonical_sha256']
    assert startup['actual_captain_getter']==startup['actual_route_word']==0
    assert names['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    assert (len(doc['records']),doc['proposed_revisions'],doc['wording_retentions'])==(539,210,329)
    assert (actual['actual_utterances'],actual['actual_body_pages'],actual['offline_only_utterances'])==(95,101,444)
    assert (actual['qualifying_final_revision_frames'],actual['qualifying_final_revision_runs'])==(39002,2)
    assert actual['final_name_pixels_sha256']==sha(PIXELS.read_bytes()) and actual['final_CG_pixels_sha256']==sha(CG.read_bytes())
    assert actual['all17_final_sheets_directly_viewed_or_exact_sheet_pixel_reuse']
    assert actual['all_six_FE_speeches_all_six_two_page_cases_andall22_headers_observed']
    for evidence in [pixels,cg]:
        assert evidence['all_selected_pages_observed_in_exact_fixture_order']
        assert evidence['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert cg['complete_scene_commands_retained'] and not any(r['kind']=='typed-choice-label' for r in doc['records'])
    image=NdsImage.open(release['candidate']);archive=image.read_file(doc['file_path']);blocks=IlnkContainer.parse(archive).blocks
    bindings=[]
    for row in doc['records']:
        assert all(row['review'][gate] is True for gate in doc['review_gates'])
        ref=deepcopy(row['planned_integrated_reference']);raw=bytes.fromhex(ref.pop('exact_stored_hex'));at=ref['offset'];block=blocks[row['block']]
        assert sha(archive)==ref['target_archive_sha256'] and block[at:at+len(raw)+1]==raw+b'\0'
        assert block[:at].count(b'\0')==ref['record_index'] and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        samples=[s for evidence in [pixels,cg] for s in evidence['body_pages'] if s['id']==row['id']]
        bindings.append(dict(id=row['id'],file_path=row['file_path'],kind=row['kind'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_reference=ref,registered_stored_hex=raw.hex(),
            registered_ROM_sha256=release['candidate_sha256'],decision=row['decision'],finding=row['finding'],
            localization_note=row['localization_note'],retention_reason=row.get('retention_reason'),review=row['review'],
            actual_source_bound_samples=samples,actual_in_initialized_fixture=bool(samples),offline_only=not bool(samples),
            offline_complete_display_andrepresentative_initialized_gameplay_distinguished=True))
    assert sum(b['offline_only'] for b in bindings)==444
    before=LEDGER.read_bytes();prior=load(LEDGER)
    assert prior['records_editorially_completed']==10774 and prior['current_integrated_candidate']['sha256']==release['parent_sha256']
    assert prior[KEY].get('new_credit',0)==0 and not prior['full_goal_complete']
    assert not any(r['id']==FAMILY for r in prior['coverage_units'])
    context=deepcopy(prior['contextual_story_natural_dialogue_pass_v1871'])
    keys=[dict(file_path=r['file_path'],id=r['id']) for r in doc['records']]
    oldkeys={(r['file_path'],r['id']) for r in context['record_keys']}
    assert len(oldkeys)==len(context['integrated_record_keys'])==10774 and not oldkeys&{(r['file_path'],r['id']) for r in keys}
    binding_path=ROOT/'integrated_record_bindings.json';assert not binding_path.exists()
    scope=dict(initialized_fixture_runs=2,fixture_frames=39002,preserved_probe_runs=3,preserved_probe_frames=63003,
        own_registered_startup_frames=4001,actual_utterances=95,actual_body_pages=101,actual_choice_captions=0,
        offline_only_utterances=444,actual_name_header_planes=204,observed_actors=22,reviewed_actual_sheets=17,
        actual_review=str(ACTUAL),actual_review_sha256=sha(ACTUAL.read_bytes()),
        source00_FI_FA_FO_six_FE_I_ellipsis_names_six_page_transitions_andcomplete_CG_sequence_checked=True,
        all97_original_branch_sites485_native_cases_checked_offline=True,
        optional_condition_activation_andfull_catalogue_UI_unvisited=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,guide_photos=False)
    family=dict(id=FAMILY,file_path=doc['file_path'],blocks=doc['blocks'],record_IDs=[r['id'] for r in doc['records']],records=539,
        ordinary_speeches=539,progressive_speeches=533,FE_speeches=6,personality_alternatives=0,typed_choices=0,typed_choice_commands=0,
        final_review=str(FINAL),revised_count=210,retained_count=329,fresh_revisions=210,fresh_retentions=329,
        layout_findings_resolved=14,glyph_fixes=16,ellipsis_fixes=14,scoped_punctuation_normalizations=19,
        separate_name_field_dialogue_credit=0,scoped_name_term_decisions=22,native_name_strings=21,
        actual_verification_scope=scope,integrated_record_bindings=str(binding_path))
    ledger=dict(prior)
    ledger['completed_editorial_families']=[*prior['completed_editorial_families'],family]
    ledger['coverage_units']=[*prior['coverage_units'],dict(**family,status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=539,final_review_sha256=sha(FINAL.read_bytes()),release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),full_goal_complete=False)]
    for key,amount in [('records_editorially_completed',539),('records_revised_and_integrated',210),('retained_wordings_editorially_completed',329),
        ('records_with_source_and_prose_pass',539),('records_with_source_prose_drafts',539)]:ledger[key]+=amount
    for name in ['record_keys','integrated_record_keys']:context[name].extend(keys)
    context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread']+=539;context['fresh_pass_records_integrated']+=539
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY,records=539,ordinary_speeches=539,personality_alternatives=0,typed_choices=0,
        final_review=str(FINAL),new_revisions=210,justified_retentions=329,new_completed_records=539,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_verification_scope=scope))
    ledger['contextual_story_natural_dialogue_pass_v1871']=context
    ledger[KEY]={**prior[KEY],**dict(completion_credit_added=539,new_credit=539,registered_release_pending=False,registered_integration_pending=False,
        all_research_checks_passed_registered_integration_pending=False,
        final_candidate_verification_andpatch_andown_startup_pending=False,all_individual_fifth_gates_pending=False,
        own_registered_RAM_binding_pending=False,registered_build=dict(session=96622,PID=6100,terminal=True,exit_code=0),
        no_live_job=True,no_live_jobs=True,remaining=[],registered_release_verification=str(RELEASE),registered_release_verification_sha256=sha(RELEASE.read_bytes()),
        own_registered_startup=str(STARTUP),own_registered_startup_sha256=sha(STARTUP.read_bytes()),
        own_Fernan_name_getters=str(OWN_NAMES),own_Fernan_name_getters_sha256=sha(OWN_NAMES.read_bytes()),
        all539_source_current_final_refs_andfive_gates=str(binding_path),main_unchanged=True,
        next_action='Remaining early help/tutorial prose andRafael priority;all wider scope remains active.')}
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE),experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint']='Rafael539 registered andcredited once:11313 completions/6566 revisions/4747 retentions;670 entries/all eight stages/exact clean patch/own Rafael startup pass. Remaining early Help/tutorials first;all prior work/full scope/main preserved.'
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==11313
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(6566,4747)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==11316
    allowed={'completed_editorial_families','coverage_units','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','records_with_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',KEY,'current_integrated_candidate','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in prior.items() if k not in allowed}
    for name in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:
        assert context[name][:len(prior['contextual_story_natural_dialogue_pass_v1871'][name])]==prior['contextual_story_natural_dialogue_pass_v1871'][name]
    save(binding_path,dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],records=bindings,
        final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_verification_scope=scope))
    ledger['coverage_units'][-1]['integrated_record_bindings_sha256']=sha(binding_path.read_bytes())
    backup=ROOT/'ledger_before_completion.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0))
    assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);temporary=LEDGER.with_name('editorial_review_current.Rafael_B61_B80_completion.pending.json')
    assert not temporary.exists() and LEDGER.read_bytes()==before;temporary.write_bytes(encoded);os.replace(temporary,LEDGER)
    assert LEDGER.read_bytes()==encoded
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=539,counts=dict(completed=11313,revised=6566,retained=4747),
        ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),all_unrelated_keys_andearlier_record_prefixes_exact=True,
        integrated_record_bindings=str(binding_path),integrated_record_bindings_sha256=sha(binding_path.read_bytes()),
        source_prose_draft_historical_counts=11316,main_unchanged=True,full_goal_complete=False,guide_photos=False))
    print('539 Rafael reviews credited once:11313 completions/6566 revisions/4747 retentions;444 offline-only explicit;full goal active/main unchanged.')
