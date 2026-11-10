"""Credit249 once after all eight release stages,patch,own startup andname getters pass."""
import gzip
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Rafael_B51_B60_release_verified_20261104')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/rafael_B51_B60_contextual_final_review_v1.json')
RELEASE=ROOT/'registered_release_verification.json'
STARTUP=ROOT/'own_registered_startup_verification.json'
OWN_NAMES=ROOT/'own_Fernan_name_getter_verification.json'
ACTUAL=Path('work/analysis/Rafael_B51_B60_checked_20261104/actual_review.json')
PIXELS=Path('work/analysis/Rafael_B51_B60_focused_pixels_20261104/focused_actual_pixels.json')
MENU_PIXELS=Path('work/analysis/Rafael_B60_menu_actual_pixels_20261104/menu_actual_pixels.json')
KEY='Rafael_SC0_B51_B60_contextual_20261104'
FAMILY='Rafael_SC0_B51_B60_complete_contextual_release_20261104'

if __name__=='__main__':
    assert not (ROOT/'completion_checkpoint.json').exists()
    doc,release,startup,own_names,actual,pixels,menu_pixels=map(load,[FINAL,RELEASE,STARTUP,OWN_NAMES,ACTUAL,PIXELS,MENU_PIXELS])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(STARTUP.read_bytes())==release['own_registered_startup_sha256']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==startup['candidate_sha256']==own_names['runtime']['candidate_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert release['complete_stack_entries']==669 and release['accepted_layers']==114 and release['all_eight_registered_final_stages_preserved']
    assert all(load(release['manifest'])['checks'].values())
    assert startup['actual_captain_getter']==startup['actual_route_word']==0
    assert own_names['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    assert (len(doc['records']),doc['proposed_revisions'],doc['wording_retentions'])==(249,102,147)
    assert (actual['actual_utterances'],actual['actual_body_pages'],actual['offline_only_utterances'],actual['actual_choice_captions'])==(32,35,213,4)
    assert actual['focused_pixels_sha256']==sha(PIXELS.read_bytes()) and actual['menu_pixels_sha256']==sha(MENU_PIXELS.read_bytes())
    assert actual['all_six_QA_sheets_directly_viewed'] and actual['all_required_distinct_wrap_glyph_macro_pagination_andmenu_cases_pass']
    assert pixels['all_selected_pages_observed_in_exact_fixture_order'] and pixels['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert menu_pixels['first_menu_cursor_down_up_andsecond_menu_cursor_down_observed'] and menu_pixels['A_acceptance_followed_by_original_next_fixture_speech_observed']
    image=NdsImage.open(release['candidate']);archive=image.read_file(doc['file_path']);blocks=IlnkContainer.parse(archive).blocks
    bindings=[]
    for row in doc['records']:
        assert all(row['review'][gate] is True for gate in doc['review_gates'])
        reference=deepcopy(row['planned_integrated_reference']);raw=bytes.fromhex(reference.pop('exact_stored_hex'))
        at=reference['offset'];block=blocks[row['block']]
        assert sha(archive)==reference['target_archive_sha256'] and block[at:at+len(raw)+1]==raw+b'\0'
        if row['kind']=='typed-choice-label':
            samples=[s for s in menu_pixels['menu_samples'] if s['source_command_offset']==row['source_command_offset']]
            assert samples and all(any(v['index']==row['source_index'] and v['text']==row['english'] for v in s['labels']) for s in samples)
            assert block[reference['command_offset']:reference['command_offset']+len(bytes.fromhex(reference['exact_choice_object_hex']))].hex()==reference['exact_choice_object_hex']
        else:
            assert block[:at].count(b'\0')==reference['record_index']
            assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            samples=[s for s in [*pixels['body_pages'],*menu_pixels['body_pages']] if s['id']==row['id']]
        bindings.append(dict(id=row['id'],file_path=row['file_path'],kind=row['kind'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_reference=reference,registered_stored_hex=raw.hex(),
            registered_ROM_sha256=release['candidate_sha256'],decision=row['decision'],finding=row['finding'],localization_note=row['localization_note'],
            retention_reason=row['retention_reason'],review=row['review'],actual_source_bound_samples=samples,
            actual_in_initialized_fixture=bool(samples),offline_only=not bool(samples),
            offline_complete_display_andrepresentative_initialized_gameplay_distinguished=True))
    assert sum(b['offline_only'] for b in bindings)==213
    before=LEDGER.read_bytes();prior=load(LEDGER)
    assert prior['records_editorially_completed']==10525 and prior['current_integrated_candidate']['sha256']==release['parent_sha256']
    assert prior[KEY].get('new_credit',0)==0 and not prior['full_goal_complete']
    assert not any(r['id']==FAMILY for r in prior['coverage_units'])
    context=deepcopy(prior['contextual_story_natural_dialogue_pass_v1871'])
    keys=[dict(file_path=r['file_path'],id=r['id']) for r in doc['records']]
    oldkeys={(r['file_path'],r['id']) for r in context['record_keys']}
    assert len(oldkeys)==len(context['integrated_record_keys'])==10525 and not oldkeys & {(r['file_path'],r['id']) for r in keys}
    binding_path=ROOT/'integrated_record_bindings.json';assert not binding_path.exists()
    scope=dict(initialized_fixture_runs=2,fixture_frames=18662,own_registered_startup_frames=4001,actual_utterances=32,
        actual_body_pages=35,actual_choice_captions=4,offline_only_utterances=213,actual_name_header_planes=58,observed_actors=18,
        reviewed_actual_sheets=6,actual_review=str(ACTUAL),actual_review_sha256=sha(ACTUAL.read_bytes()),
        source00_FI_FA_FO_three_FE_three_I_Fernan_F_pagination_andmenus_checked=True,
        numeric_return_register_original_menu_branches_andcancellation_not_observed=True,
        original_branch_sites_andbridged_return_values_checked_offline=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,guide_photos=False)
    family=dict(id=FAMILY,file_path=doc['file_path'],blocks=doc['blocks'],record_IDs=[r['id'] for r in doc['records']],records=249,
        ordinary_speeches=245,personality_alternatives=0,typed_choices=4,typed_choice_commands=2,final_review=str(FINAL),
        revised_count=102,retained_count=147,fresh_revisions=102,fresh_retentions=147,layout_findings_resolved=38,glyph_fixes=3,
        separate_Fernan_name_field_corrections=1,separate_name_field_dialogue_credit=0,
        scoped_name_term_decisions=18,native_name_strings=17,actual_verification_scope=scope,integrated_record_bindings=str(binding_path))
    ledger=dict(prior)
    ledger['completed_editorial_families']=[*prior['completed_editorial_families'],family]
    ledger['coverage_units']=[*prior['coverage_units'],dict(**family,status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=249,final_review_sha256=sha(FINAL.read_bytes()),release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),full_goal_complete=False)]
    for key,amount in [('records_editorially_completed',249),('records_revised_and_integrated',102),('retained_wordings_editorially_completed',147),
        ('records_with_source_and_prose_pass',249),('records_with_source_prose_drafts',249)]:ledger[key]+=amount
    context['record_keys'].extend(keys);context['integrated_record_keys'].extend(keys);context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread']+=249;context['fresh_pass_records_integrated']+=249
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY,records=249,ordinary_speeches=245,personality_alternatives=0,typed_choices=4,
        final_review=str(FINAL),new_revisions=102,justified_retentions=147,new_completed_records=249,historical_reconciliation_only=False,
        actual_optional_event_selected=False,actual_verification_scope=scope))
    ledger['contextual_story_natural_dialogue_pass_v1871']=context
    ledger[KEY]={**prior[KEY],**dict(completion_credit_added=249,new_credit=249,registered_release_pending=False,registered_integration_pending=False,
        final_candidate_verification_andpatch_andown_startup_pending=False,all_fifth_formatting_gates_pending=False,
        own_registered_RAM_binding_pending=False,build_process_confirmed_live_at_language_checkpoint=False,
        registered_build=dict(session=94922,PID=24560,terminal=True,exit_code=0),no_live_job=True,remaining=[],
        registered_release_verification=str(RELEASE),registered_release_verification_sha256=sha(RELEASE.read_bytes()),
        own_registered_startup=str(STARTUP),own_registered_startup_sha256=sha(STARTUP.read_bytes()),
        own_Fernan_name_getters=str(OWN_NAMES),own_Fernan_name_getters_sha256=sha(OWN_NAMES.read_bytes()),
        all249_source_current_final_refs_andfive_gates=str(binding_path),historical_intake_flags_superseded_by_complete_release=True,main_unchanged=True)}
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE),experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint']='Rafael B51-B60 registered andcredited once:249 reviews/102 revisions/147 retentions;10774 integrated completions.669 entries/114 accepted layers/eight stages/exact clean patch/own Rafael startup andFernan getters pass. Next539 source meanings/197 drafts/77 comparisons preserved;main/full scope/all ROMs unchanged;no guide photos.'
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==10774
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(6356,4418)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==10777
    allowed={'completed_editorial_families','coverage_units','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','records_with_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',KEY,'current_integrated_candidate','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in prior.items() if k not in allowed}
    for name in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:
        assert context[name][:len(prior['contextual_story_natural_dialogue_pass_v1871'][name])]==prior['contextual_story_natural_dialogue_pass_v1871'][name]
    save(binding_path,dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],records=bindings,final_review=str(FINAL),
        final_review_sha256=sha(FINAL.read_bytes()),actual_verification_scope=scope))
    ledger['coverage_units'][-1]['integrated_record_bindings_sha256']=sha(binding_path.read_bytes())
    backup=ROOT/'ledger_before_completion.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0))
    assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);temporary=LEDGER.with_name('editorial_review_current_v1.pending_Rafael_B51_B60_completion.json')
    assert not temporary.exists() and LEDGER.read_bytes()==before
    temporary.write_bytes(encoded);os.replace(temporary,LEDGER);assert LEDGER.read_bytes()==encoded
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=249,counts=dict(completed=10774,revised=6356,retained=4418),
        ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),all_unrelated_keys_andearlier_record_prefixes_exact=True,
        integrated_record_bindings=str(binding_path),integrated_record_bindings_sha256=sha(binding_path.read_bytes()),
        source_prose_draft_historical_counts=10777,main_unchanged=True,full_goal_complete=False,guide_photos=False))
    print('249 Rafael reviews credited once:10774 completions/6356 revisions/4418 retentions;213 offline-only speeches explicit;full goal active/main unchanged.',flush=True)
