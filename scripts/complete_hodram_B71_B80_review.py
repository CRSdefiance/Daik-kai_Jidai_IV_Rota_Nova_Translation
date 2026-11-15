"""Credit this verified cumulative release once, retaining every earlier ledger value."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B71_B80_release_verified_20261101')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/hodram_B71_B80_contextual_final_review_v1.json')
RELEASE=ROOT/'registered_release_verification.json'
STARTUP=ROOT/'own_registered_startup_verification.json'
FAMILY='Hodram_SC1B71_B80_complete_contextual_release_20261101'

if __name__=='__main__':
    doc,release,startup=map(load,[FINAL,RELEASE,STARTUP])
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert sha(STARTUP.read_bytes())==release['own_registered_startup_sha256']
    assert release['candidate_sha256']==startup['candidate_sha256']==sha(Path(release['candidate']).read_bytes())
    assert release['complete_stack_entries']==652 and release['accepted_layers']==114 and release['passing_release_checks']==19
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_reconstruction']).read_bytes())==release['candidate_sha256']
    assert len(doc['records'])==144 and doc['revised']==100 and doc['retained']==44
    assert all(all(row['review'][gate] for gate in ['source','context','localization','naturalness','formatting']) for row in doc['records'])
    image=NdsImage.open(release['candidate'])
    blocks=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    assert sha(image.read_file(doc['file_path']))==doc['records'][0]['planned_integrated_reference']['target_archive_sha256']
    frames={6:3360,13:4320,21:4800,29:5280,36:5760,44:6240,51:6720,55:7200,
        62:7680,69:8160,77:8640,85:9120,91:9600,94:10080,102:10560,110:11040,117:11520}
    observations={f'DK4_MES_B72_R{index:04d}':dict(frame=frame,
        capture_folder='work/emulation_v193/Hodram_B71_B80_B72_20261101',
        page=2 if index==55 else 1,complete_speech=index not in [55,91]) for index,frame in frames.items()}
    observations.update({f'DK4_MES_B76_R{index:04d}':dict(frame=frame,
        capture_folder='work/emulation_v193/Hodram_B71_B80_B76_20261101',page=1,complete_speech=True)
        for index,frame in [(6,4000),(9,4080)]})
    bindings=[]
    for row in doc['records']:
        final=deepcopy(row['planned_integrated_reference']);raw=bytes.fromhex(final.pop('exact_stored_hex'))
        at=final['offset'];block=blocks[row['block']]
        assert block[at:at+len(raw)+1]==raw+b'\0'
        assert block[:at].count(b'\0')==final['record_index']
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        observed=observations.get(row['id'])
        if observed:
            capture=Path(observed['capture_folder'])/f'frame_{observed["frame"]:06d}_cold_boot.png'
            assert capture.exists()
            observed={**observed,'capture':str(capture),'capture_sha256':sha(capture.read_bytes()),
                'visually_identified_not_independent_native_pixel_match':True}
        bindings.append(dict(id=row['id'],file_path=row['file_path'],source_reference=row['source_reference'],
            source_hex=row['source_hex'],current_reference=row['current_reference'],current_hex=row['current_hex'],
            registered_reference=final,registered_stored_hex=raw.hex(),registered_ROM_sha256=release['candidate_sha256'],
            decision=row['decision'],finding=row['finding'],localization_note=row['localization_note'],
            retention_reason=row['retention_reason'],review=row['review'],actual_sample=observed,
            offline_complete_pages_andrepresentative_gameplay_distinguished=True))
    assert len(observations)==19 and sum(o['complete_speech'] for o in observations.values())==17
    binding_path=ROOT/'integrated_record_bindings.json';assert not binding_path.exists()
    save(binding_path,dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        records=bindings,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        documented_partial_orcomplete_speech_objects=19,documented_complete_speech_objects=17,
        objects_without_documented_screen_sample=125,
        other_eight_scenes_andB76_conditional_dialogue_offline_only=True,
        B72_unsampled_does_not_mean_unexecuted_orindividually_verified=True,
        no_natural_activation_hardware_orfull_route_claim=True,new_credit=0))
    before=LEDGER.read_bytes();ledger=load(LEDGER)
    assert ledger['records_editorially_completed']==7543
    assert not any(row['id']==FAMILY for row in ledger['coverage_units'])
    context=ledger['contextual_story_natural_dialogue_pass_v1871']
    keys=[dict(file_path=row['file_path'],id=row['id']) for row in doc['records']]
    old={(row['file_path'],row['id']) for row in context['record_keys']}
    assert len(old)==len(context['integrated_record_keys'])==7543
    assert not old & {(row['file_path'],row['id']) for row in keys}
    backup=ROOT/'ledger_before_completion.json';assert not backup.exists();backup.write_bytes(before)
    scope=dict(initialized_fixture_runs=2,fixture_frames=25002,own_registered_startup_frames=4001,
        documented_speech_objects_at_least_one_page=19,documented_complete_speech_objects=17,
        documented_partial_multi_page_objects=2,objects_without_documented_screen_sample=125,
        other_eight_scenes_andB76_seven_progressive_lines_offline_only=True,
        sampled_FE_notices_andprogressive_continuation_andtown_returns=True,
        no_natural_optional_activation_original_location_full_route_orhardware_claim=True)
    family=dict(id=FAMILY,file_path=doc['file_path'],blocks=doc['blocks'],
        record_IDs=[row['id'] for row in doc['records']],records=144,final_review=str(FINAL),
        revised_count=100,retained_count=44,fresh_revisions=100,fresh_retentions=44,
        actual_verification_scope=scope,integrated_record_bindings=str(binding_path))
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append(dict(id=FAMILY,
        status='complete-contextual-native-stored-representative-registered-release',
        file_path=doc['file_path'],blocks=doc['blocks'],completion_credit_added=144,
        final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),record_IDs=family['record_IDs'],
        revised_count=100,retained_count=44,glyph_only_revisions=8,actual_verification_scope=scope,
        integrated_record_bindings=str(binding_path),integrated_record_bindings_sha256=sha(binding_path.read_bytes()),
        release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),full_goal_complete=False))
    for key,increment in [('records_editorially_completed',144),('records_revised_and_integrated',100),
            ('retained_wordings_editorially_completed',44),('records_with_source_and_prose_pass',144),
            ('records_with_source_prose_drafts',144)]:ledger[key]+=increment
    context['record_keys'].extend(keys);context['integrated_record_keys'].extend(keys)
    context['record_IDs'].extend(row['id'] for row in doc['records'])
    context['fresh_pass_records_explicitly_reread']+=144;context['fresh_pass_records_integrated']+=144
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    prior_id='Hodram_SC1B61_B70_complete_contextual_release_20261101'
    if not any(row['id']==prior_id for row in context['reconciled_families']):
        prior=next(row for row in ledger['completed_editorial_families'] if row['id']==prior_id)
        context['reconciled_families'].append(dict(id=prior_id,records=224,physical_speeches=224,typed_choices=0,
            final_review=prior['final_review'],new_revisions=132,justified_retentions=92,new_completed_records=224,
            completion_already_in_global_totals=True,this_index_reconciliation_added_credit=0,
            review_not_repeated=True))
    context['reconciled_families'].append(dict(id=FAMILY,records=144,physical_speeches=144,typed_choices=0,
        final_review=str(FINAL),new_revisions=100,justified_retentions=44,new_completed_records=144,
        historical_reconciliation_only=False,actual_optional_event_selected=False,
        actual_verification_scope=scope,all_prior_scene_proofs_reused_without_replay=True))
    pending=ledger['Hodram_B71_B80_editorial_20261101']
    pending.update(registered_integration_pending=False,build_status='complete',build_exit_code=0,
        startup_session=67861,startup_exit_code=0,completion_credit_added=144,
        registered_manifest_patch_startup_andcompletion_credit_pending=False,
        release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()))
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],
        profile=release['profile'],MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),
        ARM9_sha256=sha(image.read_file('/__arm9__.bin')),patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],registered_release_verification=str(RELEASE),
        experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint']='2026-11-01 registered Hodram B71-B80:144 once-only completions;7687 total,100 revisions/44 retentions.652-entry manifest/114 accepted layers/19 checks,exact clean-input patch andown4001-frame startup pass. Main unchanged;full goal active. Next B81-B90 has304 clean speech meanings plus2typed-choice meanings,older English unconsulted. See docs/editorial_hodram_B71_B80_20261101.md.'
    ledger['Hodram_B81_B90_clean_next_20261101']=dict(
        source_packet='work/analysis/Hodram_B81_B90_clean_20261101/clean_source_packet.json',
        meanings='work/analysis/Hodram_B81_B90_clean_20261101/all304_clean_meanings_before_English.json',
        choices='work/analysis/Hodram_B81_B90_clean_20261101/B87_two_clean_choice_meanings_before_English.json',
        speech_meanings=304,typed_choice_meanings=2,spoken_blocks=9,control_only_blocks=[90],
        earlier_English_unconsulted=True,source_identity_terminology_control_context_andlocalization_pending=True,new_credit=0)
    counts=Counter(row['file_path'] for row in context['record_keys'])
    assert counts['/data/SC1.DK4']==607 and len(context['record_keys'])==len(context['integrated_record_keys'])==7687
    assert ledger['records_editorially_completed']==7687
    assert ledger['records_revised_and_integrated']==4770 and ledger['retained_wordings_editorially_completed']==2917
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==7690
    assert not ledger['full_goal_complete']
    assert ledger['current_native_relocation_reference']==load(backup)['current_native_relocation_reference']
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger)
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=144,counts=dict(completed=7687,
        source_prose_anddrafts=7690,integrated_revisions=4770,retentions=2917),completed_by_file=dict(counts),
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),
        own_startup=str(STARTUP),own_startup_sha256=sha(STARTUP.read_bytes()),
        ledger_before=str(backup),ledger_before_sha256=sha(before),ledger_after_sha256=sha(LEDGER.read_bytes()),
        earlier_7543_credits_retained_and144_added_once=True,shared_COMMON_relocation_reference_unchanged=True,
        main_not_promoted=True,next_clean_speeches=304,next_clean_choice_labels=2,full_goal_complete=False))
    print('144 once-only completions recorded:7687 total,4770 revisions,2917 retentions. Main unchanged;full goal active.')
