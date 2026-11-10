"""Credit the verified306-record cumulative release once; retain the full wider scope."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B81_B89_release_verified_20261101')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/hodram_B81_B89_contextual_final_review_v1.json')
RELEASE=ROOT/'registered_release_verification.json'
STARTUP=ROOT/'own_registered_startup_verification.json'
FAMILY='Hodram_SC1B81_B89_complete_contextual_release_20261101'

if __name__=='__main__':
    doc,release,startup=map(load,[FINAL,RELEASE,STARTUP])
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert sha(STARTUP.read_bytes())==release['own_registered_startup_sha256']
    assert release['candidate_sha256']==startup['candidate_sha256']==sha(Path(release['candidate']).read_bytes())
    assert release['complete_stack_entries']==654 and release['accepted_layers']==114 and release['passing_release_checks']==20
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_reconstruction']).read_bytes())==release['candidate_sha256']
    assert len(doc['records'])==306 and doc['revised']==222 and doc['retained']==84
    image=NdsImage.open(release['candidate']);archive=image.read_file(doc['file_path']);blocks=IlnkContainer.parse(archive).blocks
    observations={
        'DK4_MES_B84_R0012':dict(frames=[4320],folder='Hodram_B81_B89_B84_20261101',complete=True,pages=[1],pixel_match=False),
        'DK4_MES_B85_R0018':dict(frames=[4800,5040],folder='Hodram_B81_B89_B85_20261101',complete=True,pages=[1,2],pixel_match=True),
        'SC1_B87_NATIVE_CHOICE_302_0':dict(frames=[5500],folder='Hodram_B87_decline_20261101',complete=True,caption=True,pixel_match=True),
        'SC1_B87_NATIVE_CHOICE_302_1':dict(frames=[5620],folder='Hodram_B87_decline_20261101',complete=True,caption=True,pixel_match=True),
    }
    bindings=[]
    for row in doc['records']:
        assert all(row['review'][gate] for gate in ['source','context','localization','naturalness','formatting'])
        reference=deepcopy(row['planned_integrated_reference']);raw=bytes.fromhex(reference.pop('exact_stored_hex'))
        block=blocks[row['block']];at=reference['offset']
        assert block[at:at+len(raw)+1]==raw+b'\0' and sha(archive)==reference['target_archive_sha256']
        if row['kind']!='typed-choice-label':
            assert block[:at].count(b'\0')==reference['record_index']
            assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        observed=deepcopy(observations.get(row['id']))
        if observed:
            observed['captures']=[]
            for frame in observed['frames']:
                p=Path('work/emulation_v193')/observed['folder']/f'frame_{frame:06d}_cold_boot.png'
                assert p.exists();observed['captures'].append(dict(path=str(p),sha256=sha(p.read_bytes())))
        bindings.append(dict(id=row['id'],file_path=row['file_path'],kind=row['kind'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_reference=reference,registered_stored_hex=raw.hex(),
            registered_ROM_sha256=release['candidate_sha256'],decision=row['decision'],finding=row['finding'],localization_note=row['localization_note'],
            retention_reason=row['retention_reason'],review=row['review'],actual_ID_bound_sample=observed,
            offline_complete_display_andrepresentative_gameplay_distinguished=True))
    binding_path=ROOT/'integrated_record_bindings.json';assert not binding_path.exists()
    scope=dict(initialized_fixture_runs=4,fixture_frames=41004,own_registered_startup_frames=4001,
        explicitly_ID_bound_complete_speeches=2,explicitly_ID_bound_menu_captions=2,other_objects_without_individual_ID_sample_receipt=302,
        absence_of_individual_ID_receipt_is_not_a_claim_the_line_was_unobserved=True,
        actual_seven_Emilio_headers_fourteen_menu_captions_andboth_rejection_pages_equal_native_pixels=True,
        B81_B82_B83_B86_B88_B89_late_B85_andfive_new_FE_bodies_offline_only=True,
        unvisited_andfixture_limits='See the complete actual_review receipt; no natural activation,original location,earned chronology,fullroute orhardware claim.')
    save(binding_path,dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],records=bindings,
        final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_verification_scope=scope,new_credit=0))
    before=LEDGER.read_bytes();ledger=load(LEDGER);assert ledger['records_editorially_completed']==7687
    assert not any(row['id']==FAMILY for row in ledger['coverage_units'])
    context=ledger['contextual_story_natural_dialogue_pass_v1871'];keys=[dict(file_path=r['file_path'],id=r['id']) for r in doc['records']]
    existing={(r['file_path'],r['id']) for r in context['record_keys']}
    assert len(existing)==len(context['integrated_record_keys'])==7687 and not existing & {(r['file_path'],r['id']) for r in keys}
    backup=ROOT/'ledger_before_completion.json';assert not backup.exists();backup.write_bytes(before)
    family=dict(id=FAMILY,file_path=doc['file_path'],blocks=doc['blocks'],record_IDs=[r['id'] for r in doc['records']],records=306,
        physical_speeches=304,typed_choices=2,final_review=str(FINAL),revised_count=222,retained_count=84,fresh_revisions=222,fresh_retentions=84,
        wording_name_revisions=216,punctuation_glyph_revisions=6,additional_name_metadata_fix=1,
        actual_verification_scope=scope,integrated_record_bindings=str(binding_path))
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append(dict(**family,status='complete-contextual-native-stored-representative-registered-release',completion_credit_added=306,
        final_review_sha256=sha(FINAL.read_bytes()),integrated_record_bindings_sha256=sha(binding_path.read_bytes()),
        release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),full_goal_complete=False))
    for key,amount in [('records_editorially_completed',306),('records_revised_and_integrated',222),('retained_wordings_editorially_completed',84),
        ('records_with_source_and_prose_pass',306),('records_with_source_prose_drafts',306)]:ledger[key]+=amount
    context['record_keys'].extend(keys);context['integrated_record_keys'].extend(keys);context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread']+=306;context['fresh_pass_records_integrated']+=306
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY,records=306,physical_speeches=304,typed_choices=2,final_review=str(FINAL),new_revisions=222,
        justified_retentions=84,new_completed_records=306,historical_reconciliation_only=False,actual_optional_event_selected=False,actual_verification_scope=scope))
    pending=ledger['Hodram_B81_B89_five_gate_research_20261101']
    pending.update(registered_release_andcompletion_credit_pending=False,completion_credit_added=306,build_session=92792,build_status='complete',build_exit_code=0,
        release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()))
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE),experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    nextroot=Path('work/analysis/Hodram_B91_B110_clean_20261101')
    ledger['Hodram_B91_B110_clean_next_20261101']=dict(source_packet=str(nextroot/'clean_source_packet.json'),
        meanings=str(nextroot/'all209_clean_meanings_before_English.json'),choices=str(nextroot/'B91_two_clean_choice_meanings_before_English.json'),
        clean_names=str(nextroot/'clean_name_fields.json'),item_terms=str(nextroot/'source_bound_item_terminology.json'),
        speech_meanings=209,typed_choice_meanings=2,spoken_blocks=14,control_only_blocks=[94,96,98,99,106,107],
        earlier_English_unconsulted=True,native_names_preambles_CF_role0_FE_FI_andbranch_context_pending=True,new_credit=0)
    ledger['latest_checkpoint']='Registered B81-B89/Emilio successor verified:306 once-only completions;7993 completed.216 wording/name revisions,6 punctuation glyph revisions,84 retentions;one additional name glyph fix.654 manifest entries/114 accepted layers/20 checks,exact clean patch andown startup pass. Main unchanged. Next209 clean speech meanings+2 typed-choice meanings;earlier English unconsulted. Full goal active;no guide photos.'
    counts=Counter(r['file_path'] for r in context['record_keys']);assert counts['/data/SC1.DK4']==913
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==7993
    assert ledger['records_revised_and_integrated']==4992 and ledger['retained_wordings_editorially_completed']==3001
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==7996
    assert ledger['current_native_relocation_reference']==load(backup)['current_native_relocation_reference'] and not ledger['full_goal_complete']
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger)
    pinpath=Path('translations/rom_retention_pins.json');pins=load(pinpath)
    for path in [Path('work/analysis/Hodram_B81_B89_registered_build_20261101/runtime_bounds/canonical_reconstruction_stage.nds'),
        Path('work/analysis/Hodram_B81_B89_registered_build_20261101/runtime_bounds/complete_reviewed_target_RESEARCH_ONLY.nds'),
        Path('work/analysis/Hodram_B81_B89_registered_build_20261101/post_bounds_RESEARCH_ONLY.nds')]:
        assert path.exists();resolved=str(path.resolve())
        if not any(p['path']==resolved for p in pins):pins.append(dict(path=resolved,reason='Preserve registered B81-B89 canonical andpost-bounds reconstruction stages;all ROMs retained. SHA256 '+sha(path.read_bytes())))
    save(pinpath,pins)
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=306,counts=dict(completed=7993,source_prose_anddrafts=7996,integrated_revisions=4992,retentions=3001),
        completed_by_file=dict(counts),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),own_startup=str(STARTUP),own_startup_sha256=sha(STARTUP.read_bytes()),
        all_generated_ROMs_andprior_work_preserved=True,main_unchanged=True,full_goal_complete=False))
    print('306 once-only completions:7993 total;4992 revisions/3001 retentions. Next209+2 clean meanings,earlier English unconsulted. Main unchanged;full goal active.')
