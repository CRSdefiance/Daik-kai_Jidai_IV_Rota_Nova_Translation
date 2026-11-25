"""Credit the verified211-record cumulative release once andretain the full objective."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B91_B110_release_verified_20261101')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/hodram_B91_B110_contextual_final_review_v1.json')
RELEASE=ROOT/'registered_release_verification.json'
STARTUP=ROOT/'own_registered_startup_verification.json'
FAMILY='Hodram_SC1B91_B110_complete_contextual_release_20261101'

if __name__=='__main__':
    doc,release,startup=map(load,[FINAL,RELEASE,STARTUP])
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert sha(STARTUP.read_bytes())==release['own_registered_startup_sha256']
    assert release['candidate_sha256']==startup['candidate_sha256']==sha(Path(release['candidate']).read_bytes())
    assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks'])==(656,114,21)
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_reconstruction']).read_bytes())==release['candidate_sha256']
    assert len(doc['records'])==211 and (doc['revised'],doc['retained'])==(129,82)
    image=NdsImage.open(release['candidate']);archive=image.read_file(doc['file_path']);blocks=IlnkContainer.parse(archive).blocks
    pixels=load('work/analysis/Hodram_B91_B110_actual_pixels_20261101d/focused_actual_pixels.json')
    observed={}
    for row in pixels['body_pages']:observed.setdefault(row['id'],[]).append(row)
    for row in [r for r in doc['records'] if r['kind']=='typed-choice-label']:
        observed[row['id']]=[dict(**sample,source_index=row['source_index']) for sample in pixels['menu_samples']]
    bindings=[]
    for row in doc['records']:
        assert all(row['review'][g] for g in doc['review_gates'])
        reference=deepcopy(row['planned_integrated_reference']);raw=bytes.fromhex(reference.pop('exact_stored_hex'));block=blocks[row['block']];at=reference['offset']
        assert block[at:at+len(raw)+1]==raw+b'\0' and sha(archive)==reference['target_archive_sha256']
        if row['kind']!='typed-choice-label':
            assert block[:at].count(b'\0')==reference['record_index']
            assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        bindings.append(dict(id=row['id'],file_path=row['file_path'],kind=row['kind'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_reference=reference,registered_stored_hex=raw.hex(),registered_ROM_sha256=release['candidate_sha256'],
            decision=row['decision'],finding=row['finding'],localization_note=row['localization_note'],retention_reason=row['retention_reason'],review=row['review'],
            actual_ID_bound_samples=observed.get(row['id'],[]),offline_complete_display_andrepresentative_gameplay_distinguished=True))
    scope=dict(initialized_fixture_runs=3,fixture_frames=28003,own_registered_startup_frames=4001,
        explicitly_pixel_bound_speech_objects=5,explicitly_pixel_bound_speech_pages=6,explicitly_bound_menu_captions=2,
        other_objects_without_individual_ID_pixel_receipt=204,absence_of_individual_receipt_not_a_claim_that_line_was_unobserved=True,
        actual_name_headers=6,actual_menu_samples=3,initial_highlight_partial_andmoved_second_highlight_complete=True,
        unvisited_andfixture_limits='See work/analysis/Hodram_B91_B110_editorial_20261101/actual_review.json. Other exchanges,three monkey FE bodies,B91R61 complete sample andSamwell full-catalogue UI remain offline-only;no natural activation,earned chronology,fullroute orhardware claim.')
    binding_path=ROOT/'integrated_record_bindings.json';assert not binding_path.exists()
    save(binding_path,dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],records=bindings,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_verification_scope=scope,new_credit=0))
    before=LEDGER.read_bytes();ledger=load(LEDGER);assert ledger['records_editorially_completed']==7993
    assert not any(r['id']==FAMILY for r in ledger['coverage_units'])
    context=ledger['contextual_story_natural_dialogue_pass_v1871'];keys=[dict(file_path=r['file_path'],id=r['id']) for r in doc['records']]
    existing={(r['file_path'],r['id']) for r in context['record_keys']}
    assert len(existing)==len(context['integrated_record_keys'])==7993 and not existing & {(r['file_path'],r['id']) for r in keys}
    backup=ROOT/'ledger_before_completion.json';assert not backup.exists();backup.write_bytes(before)
    family=dict(id=FAMILY,file_path=doc['file_path'],blocks=doc['blocks'],record_IDs=[r['id'] for r in doc['records']],records=211,physical_speeches=209,typed_choices=2,final_review=str(FINAL),
        revised_count=129,retained_count=82,fresh_revisions=129,fresh_retentions=82,page_findings_resolved=5,additional_name_metadata_fields=2,actual_verification_scope=scope,integrated_record_bindings=str(binding_path))
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append(dict(**family,status='complete-contextual-native-stored-representative-registered-release',completion_credit_added=211,final_review_sha256=sha(FINAL.read_bytes()),integrated_record_bindings_sha256=sha(binding_path.read_bytes()),release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),full_goal_complete=False))
    for key,amount in [('records_editorially_completed',211),('records_revised_and_integrated',129),('retained_wordings_editorially_completed',82),('records_with_source_and_prose_pass',211),('records_with_source_prose_drafts',211)]:ledger[key]+=amount
    context['record_keys'].extend(keys);context['integrated_record_keys'].extend(keys);context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread']+=211;context['fresh_pass_records_integrated']+=211
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY,records=211,physical_speeches=209,typed_choices=2,final_review=str(FINAL),new_revisions=129,justified_retentions=82,new_completed_records=211,historical_reconciliation_only=False,actual_optional_event_selected=False,actual_verification_scope=scope))
    ledger['Hodram_B91_B110_five_gate_research_20261101'].update(registered_release_andcompletion_credit_pending=False,completion_credit_added=211,build_session=55876,build_status='complete',build_exit_code=0,release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()))
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],registered_release_verification=str(RELEASE),experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    nextroot=Path('work/analysis/Hodram_B111_B130_clean_20261101');nextcheck=load(nextroot/'intake_scope_checkpoint.json')
    ledger['Hodram_B111_B130_clean_next_20261101']={**nextcheck,'checkpoint':str(nextroot/'intake_scope_checkpoint.json'),'checkpoint_sha256':sha((nextroot/'intake_scope_checkpoint.json').read_bytes())}
    ledger['latest_checkpoint']='Registered B91-B110/names successor verified:211 once-only completions;8204 completed.129 revisions/82 retentions,five page fixes,two additional name fields.656 manifest entries/114 accepted layers/21 checks,exact clean patch andown startup pass. Main unchanged. Next323 clean-first prose objects:260 speeches+48 style alternatives/64 aliases+15 menu labels;earlier English unconsulted. Full goal active;no guide photos.'
    counts=Counter(r['file_path'] for r in context['record_keys']);assert counts['/data/SC1.DK4']==1124
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==8204
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5121,3083)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==8207
    assert ledger['current_native_relocation_reference']==load(backup)['current_native_relocation_reference'] and not ledger['full_goal_complete']
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger)
    pins_path=Path('translations/rom_retention_pins.json');pins=load(pins_path)
    work=Path('work/analysis/Hodram_B91_B110_registered_build_20261101')
    for path in [work/'owned_names/runtime_bounds/canonical_reconstruction_stage.nds',work/'owned_names/runtime_bounds/complete_reviewed_target_RESEARCH_ONLY.nds',work/'owned_names/post_bounds_RESEARCH_ONLY.nds',work/'post_Emilio_RESEARCH_ONLY.nds']:
        assert path.exists();absolute=str(path.resolve())
        if not any(r['path']==absolute for r in pins):pins.append(dict(path=absolute,reason='Preserve registered B91-B110 cumulative reconstruction stage;all ROMs retained. SHA256 '+sha(path.read_bytes())))
    save(pins_path,pins)
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=211,counts=dict(completed=8204,source_prose_anddrafts=8207,integrated_revisions=5121,retentions=3083),completed_by_file=dict(counts),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],release_verification=str(RELEASE),release_verification_sha256=sha(RELEASE.read_bytes()),own_startup=str(STARTUP),own_startup_sha256=sha(STARTUP.read_bytes()),all_generated_ROMs_andprior_work_preserved=True,main_unchanged=True,full_goal_complete=False))
    print('211 once-only completions:8204 total;5121 revisions/3083 retentions. Next323 source-first objects;earlier English unconsulted. Main unchanged;full goal active.')
