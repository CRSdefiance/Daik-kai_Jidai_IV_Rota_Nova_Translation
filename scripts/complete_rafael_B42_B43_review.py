"""Credit forty tutorials once after final registered identity and own startup pass."""
import gzip,os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Rafael_early_tutorial_release_verified_20261104')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/rafael_B42_B43_contextual_final_review_v1.json')
RELEASE=ROOT/'registered_release_verification.json'
STARTUP=ROOT/'own_registered_startup_verification.json'
ACTUAL=Path('work/analysis/Rafael_early_tutorial_B42_B43_checked_20261104/actual_visual_approval.json')
PIXELS=Path('work/analysis/Rafael_early_tutorial_B42_B43_actual_pixels_20261104/focused_actual_pixels.json')
KEY='Rafael_SC0_B42_B43_early_tutorial_20261104'
FAMILY='Rafael_SC0_B42_B43_complete_contextual_release_20261104'

if __name__=='__main__':
    assert not (ROOT/'completion_checkpoint.json').exists()
    doc,release,startup,actual,pixels=map(load,[FINAL,RELEASE,STARTUP,ACTUAL,PIXELS])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(STARTUP.read_bytes())==release['own_registered_startup_sha256']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==startup['candidate_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert release['complete_stack_entries']==665 and release['accepted_layers']==114 and release['all_six_registered_final_stages_preserved']
    assert all(load(release['manifest'])['checks'].values())
    assert startup['actual_captain_getter']==startup['actual_route_word']==0
    assert (len(doc['records']),doc['proposed_revisions'],doc['wording_retentions'])==(40,19,21)
    assert actual['read_only_pixel_proof_sha256']==sha(PIXELS.read_bytes())
    assert actual['all42_target_pages_observed_in_order'] and len(actual['all_review_sheets_directly_viewed'])==2
    assert pixels['all_required_distinct_display_cases_match'] and len(pixels['body_pages'])==92
    assert [(r['run'],r['calls']) for r in pixels['ordered_linear_scene_sequences']]==[('first_voyage',29),('crew_duties',13)]
    assert all(r['complete_ordered_calls_match_all_copied_source_speeches'] for r in pixels['ordered_linear_scene_sequences'])
    image=NdsImage.open(release['candidate']);archive=image.read_file(doc['file_path']);blocks=IlnkContainer.parse(archive).blocks
    bindings=[]
    for row in doc['records']:
        assert all(row['review'][gate] is True for gate in doc['review_gates'])
        reference=deepcopy(row['planned_integrated_reference']);raw=bytes.fromhex(reference.pop('exact_stored_hex'))
        at=reference['offset'];block=blocks[row['block']]
        assert sha(archive)==reference['target_archive_sha256']
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==reference['record_index']
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        samples=[s for s in pixels['body_pages'] if s['id']==row['id']]
        assert samples and all(s['complete_native_glyph_plane_andblank_guards_equal'] for s in samples)
        bindings.append(dict(id=row['id'],file_path=row['file_path'],kind=row['kind'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_reference=reference,registered_stored_hex=raw.hex(),
            registered_ROM_sha256=release['candidate_sha256'],decision=row['decision'],finding=row['finding'],localization_note=row['localization_note'],
            retention_reason=row['retention_reason'],review=row['review'],actual_source_bound_samples=samples,
            offline_complete_display_andrepresentative_initialized_gameplay_distinguished=True))
    before=LEDGER.read_bytes();prior=load(LEDGER)
    assert prior['records_editorially_completed']==10306 and prior['current_integrated_candidate']['sha256']==release['parent_sha256']
    assert not prior['full_goal_complete'] and not any(r['id']==FAMILY for r in prior['coverage_units'])
    context=deepcopy(prior['contextual_story_natural_dialogue_pass_v1871'])
    keys=[dict(file_path=r['file_path'],id=r['id']) for r in doc['records']]
    oldkeys={(r['file_path'],r['id']) for r in context['record_keys']}
    assert len(oldkeys)==len(context['integrated_record_keys'])==10306
    assert not oldkeys & {(r['file_path'],r['id']) for r in keys}
    binding_path=ROOT/'integrated_record_bindings.json';assert not binding_path.exists()
    scope=dict(initialized_fixture_runs=2,fixture_frames=25002,own_registered_startup_frames=4001,captured_body_planes_matched=92,
        native_record_page_observations=42,actual_name_headers=5,reviewed_actual_sheets=2,actual_review=str(ACTUAL),actual_review_sha256=sha(ACTUAL.read_bytes()),
        source00_FI_FE_andboth_two_page_transitions_observed=True,complete_ordered_tutorial_source_calls=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,guide_photos=False)
    family=dict(id=FAMILY,file_path=doc['file_path'],blocks=doc['blocks'],record_IDs=[r['id'] for r in doc['records']],records=40,
        ordinary_speeches=40,personality_alternatives=0,typed_choices=0,typed_choice_commands=0,final_review=str(FINAL),
        revised_count=19,retained_count=21,fresh_revisions=19,fresh_retentions=21,layout_findings_resolved=2,
        scoped_name_term_decisions=4,native_name_strings=4,actual_verification_scope=scope,integrated_record_bindings=str(binding_path))
    ledger=dict(prior)
    ledger['completed_editorial_families']=[*prior['completed_editorial_families'],family]
    ledger['coverage_units']=[*prior['coverage_units'],dict(**family,status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=40,final_review_sha256=sha(FINAL.read_bytes()),release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),full_goal_complete=False)]
    for key,amount in [('records_editorially_completed',40),('records_revised_and_integrated',19),('retained_wordings_editorially_completed',21),
        ('records_with_source_and_prose_pass',40),('records_with_source_prose_drafts',40)]:ledger[key]+=amount
    context['record_keys'].extend(keys);context['integrated_record_keys'].extend(keys);context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread']+=40;context['fresh_pass_records_integrated']+=40
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY,records=40,ordinary_speeches=40,personality_alternatives=0,typed_choices=0,
        final_review=str(FINAL),new_revisions=19,justified_retentions=21,new_completed_records=40,historical_reconciliation_only=False,
        actual_optional_event_selected=False,actual_verification_scope=scope))
    ledger['contextual_story_natural_dialogue_pass_v1871']=context
    ledger[KEY]={**prior[KEY],**dict(completion_credit_added=40,new_credit=40,registered_release_pending=False,
        final_candidate_verification_andpatch_andown_startup_pending=False,all_fifth_formatting_gates_pending=False,
        registered_build=dict(session=15896,terminal=True,exit_code=0),no_live_job=True,remaining=[],
        registered_release_verification=str(RELEASE),registered_release_verification_sha256=sha(RELEASE.read_bytes()),
        own_registered_startup=str(STARTUP),own_registered_startup_sha256=sha(STARTUP.read_bytes()),all40_source_current_final_refs_andfive_gates=str(binding_path),
        historical_intake_flags_superseded_by_complete_release=True,main_unchanged=True)}
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE),experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint']='Rafael B42/B43 tutorials registered andcredited once:40 reviews,19 revisions/21 retentions;10346 integrated completions.665 entries,114 accepted layers,six final stages,exact clean patch andown Rafael startup pass. Next175 prose/native/stored reviews preserved;main/full scope/allROMs unchanged;no guide photos.'
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==10346
    assert sum(r['file_path']=='/data/SC0.DK4' for r in context['record_keys'])==408
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(6177,4169)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==10349
    allowed={'completed_editorial_families','coverage_units','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','records_with_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',KEY,'current_integrated_candidate','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in prior.items() if k not in allowed}
    for name in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:
        assert context[name][:len(prior['contextual_story_natural_dialogue_pass_v1871'][name])]==prior['contextual_story_natural_dialogue_pass_v1871'][name]
    save(binding_path,dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],records=bindings,final_review=str(FINAL),
        final_review_sha256=sha(FINAL.read_bytes()),actual_verification_scope=scope))
    ledger['coverage_units'][-1]['integrated_record_bindings_sha256']=sha(binding_path.read_bytes())
    backup=ROOT/'ledger_before_completion.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);temporary=LEDGER.with_name('editorial_review_current_v1.pending_Rafael_tutorial_completion.json')
    assert not temporary.exists() and LEDGER.read_bytes()==before
    temporary.write_bytes(encoded);os.replace(temporary,LEDGER);assert LEDGER.read_bytes()==encoded
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=40,counts=dict(completed=10346,revised=6177,retained=4169),
        ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),all_unrelated_keys_andearlier_record_prefixes_exact=True,
        integrated_record_bindings=str(binding_path),integrated_record_bindings_sha256=sha(binding_path.read_bytes()),main_unchanged=True,full_goal_complete=False,guide_photos=False))
    print('40 tutorials credited once:10346 completions,6177 revisions/4169 retentions;full goal active andmain unchanged.')
