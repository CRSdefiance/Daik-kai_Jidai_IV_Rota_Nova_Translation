"""Credit four tutorial reviews once after seven-stage release andown startup pass."""
import gzip,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/shared_deck_four_panels_contextual_final_v1.json')
NAMES=Path('translations/pedro_hayreddin_catalogue_fields_final_v1.json')
RELEASE=ROOT/'registered_release_verification.json';STARTUP=ROOT/'own_registered_startup_verification.json'
KEY='shared_Deck_four_panel_contextual_20261104';NAME_KEY='Pedro_Hayreddin_full_catalogue_fields_20261104'
FAMILY='shared_Deck_four_panel_complete_contextual_release_20261104'
ACTUAL=Path('work/analysis/Shared_Deck_actual_UI_20261104/representative_UI_verification.json')

if __name__=='__main__':
    assert not (ROOT/'completion_checkpoint.json').exists()
    doc,names,release,startup,actual=map(load,[FINAL,NAMES,RELEASE,STARTUP,ACTUAL])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(STARTUP.read_bytes())==release['own_registered_startup_sha256']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==startup['candidate_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes()
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert release['complete_stack_entries']==667 and release['accepted_layers']==114 and release['all_seven_registered_final_stages_preserved']
    assert all(load(release['manifest'])['checks'].values())
    assert startup['actual_captain_getter']==startup['actual_route_word']==0
    assert len(doc['records'])==4 and len(names['records'])==2 and doc['one_terminology_revision']==1 and doc['justified_retentions']==3
    assert actual['complete_body_texture_andRGB_comparisons']==7 and actual['actual_frames']==21400
    assert actual['four_revised_special_static_paragraphs_not_activated_or_claimed_observed']
    image=NdsImage.open(release['candidate']);arm=image.read_file('/__arm9__.bin');bindings=[]
    owned={r['id']:r for r in release['owned_text_data_proof']['changed_records']}
    for row in doc['records']:
        assert all(row['review'][gate] is True for gate in doc['review_gates'])
        reference=deepcopy(row['planned_integrated_reference']);at=reference['offset'];raw=bytes.fromhex(reference['padded_hex'])
        assert len(raw)==reference['capacity'] and arm[at:at+len(raw)]==raw
        assert owned[row['id']]['physical_offset']==at and owned[row['id']]['new_hex']==raw.hex()
        assert not row['actual_target_paragraph_observed']
        bindings.append(dict(id=row['id'],file_path='/__arm9__.bin',source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_reference=reference,
            registered_ROM_sha256=release['candidate_sha256'],decision=row['decision'],finding=row['finding'],
            localization_note=row['localization_note'],retention_reason=row.get('retention_reason'),review=row['review'],
            actual_target_paragraph_observed=False,representative_same_consumer_bodies=7))
    for row in names['records']:
        p=owned[row['id']];assert p['kind']=='exclusive-name-component'
        assert arm[p['physical_offset']:p['physical_offset']+p['owned_bytes']].hex()==p['new_hex']
        assert all(row['review'][gate] for gate in ['source','context','localization','naturalness','formatting'])
    before=LEDGER.read_bytes();prior=load(LEDGER)
    assert prior['records_editorially_completed']==10521 and prior['current_integrated_candidate']['sha256']==release['parent_sha256']
    assert prior[KEY]['new_credit']==0 and prior[NAME_KEY]['new_credit']==0 and not prior['full_goal_complete']
    assert not any(r['id']==FAMILY for r in prior['coverage_units'])
    context=deepcopy(prior['contextual_story_natural_dialogue_pass_v1871'])
    keys=[dict(file_path='/__arm9__.bin',id=r['id']) for r in doc['records']]
    oldkeys={(r['file_path'],r['id']) for r in context['record_keys']}
    assert len(oldkeys)==len(context['integrated_record_keys'])==10521
    assert not oldkeys & {(r['file_path'],r['id']) for r in keys}
    binding_path=ROOT/'integrated_record_bindings.json';assert not binding_path.exists()
    scope=dict(actual_target_paragraphs=0,target_four_bodies_native_offline_andconnected_only=True,
        representative_same_consumer_bodies=7,representative_UI_frames=21400,own_registered_startup_frames=4001,
        actual_review=str(ACTUAL),actual_review_sha256=sha(ACTUAL.read_bytes()),full_catalogue_UI_unvisited=True,
        natural_activation=False,full_route=False,hardware=False,guide_photos=False)
    family=dict(id=FAMILY,file_path='/__arm9__.bin',blocks=[],record_IDs=[r['id'] for r in doc['records']],records=4,
        ordinary_speeches=0,fixed_tutorial_panels=4,personality_alternatives=0,typed_choices=0,typed_choice_commands=0,
        final_review=str(FINAL),revised_count=1,retained_count=3,fresh_revisions=1,fresh_retentions=3,
        layout_findings_resolved=4,separate_name_corrections_not_dialogue_credit=2,
        actual_verification_scope=scope,integrated_record_bindings=str(binding_path))
    ledger=dict(prior)
    ledger['completed_editorial_families']=[*prior['completed_editorial_families'],family]
    ledger['coverage_units']=[*prior['coverage_units'],dict(**family,status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=4,final_review_sha256=sha(FINAL.read_bytes()),release_verification=str(RELEASE),
        release_verification_sha256=sha(RELEASE.read_bytes()),full_goal_complete=False)]
    for key,amount in [('records_editorially_completed',4),('records_revised_and_integrated',1),('retained_wordings_editorially_completed',3),
        ('records_with_source_and_prose_pass',4),('records_with_source_prose_drafts',4)]:ledger[key]+=amount
    context['record_keys'].extend(keys);context['integrated_record_keys'].extend(keys);context['record_IDs'].extend(r['id'] for r in doc['records'])
    context['fresh_pass_records_explicitly_reread']+=4;context['fresh_pass_records_integrated']+=4
    context['latest_completed_family']=FAMILY;context['latest_final_review']=str(FINAL)
    context['reconciled_families'].append(dict(id=FAMILY,records=4,fixed_tutorial_panels=4,ordinary_speeches=0,
        final_review=str(FINAL),new_revisions=1,justified_retentions=3,new_completed_records=4,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_verification_scope=scope))
    ledger['contextual_story_natural_dialogue_pass_v1871']=context
    ledger[KEY]={**prior[KEY],**dict(completion_credit_added=4,new_credit=4,registered_integration_pending=False,
        registered_build_live_at_checkpoint=False,registered_build=dict(session=54457,terminal=True,exit_code=0),
        final_candidate_verification_andpatch_andown_startup_pending=False,remaining=[],no_live_job=True,
        registered_release_verification=str(RELEASE),registered_release_verification_sha256=sha(RELEASE.read_bytes()),
        own_registered_startup=str(STARTUP),own_registered_startup_sha256=sha(STARTUP.read_bytes()),
        all_four_source_current_final_refs_andfive_gates=str(binding_path),main_unchanged=True)}
    ledger[NAME_KEY]={**prior[NAME_KEY],**dict(new_credit=0,registered_deployment_pending=False,
        registered_candidate=release['candidate'],registered_candidate_sha256=release['candidate_sha256'],
        exactly_registered_owned_fields=True,full_catalogue_UI_unvisited=True,no_global_name_approval=True)}
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),ARM9_sha256=sha(arm),patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],registered_release_verification=str(RELEASE),
        experimental_not_promoted=True,own_registered_startup_verified=True,clean_input_patch_byte_exact=True)
    ledger['latest_checkpoint']='Four shared tutorials registered andcredited once;two separate name fields deployed.10525 completions,667 entries/114 accepted layers/seven stages,exact clean patch andown Rafael startup pass.Next249 prose/native pages preserved;full goal active,main unchanged.'
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==ledger['records_editorially_completed']==10525
    assert (ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(6254,4271)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==10528
    allowed={'completed_editorial_families','coverage_units','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','records_with_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',KEY,NAME_KEY,'current_integrated_candidate','latest_checkpoint'}
    assert {k:v for k,v in ledger.items() if k not in allowed}=={k:v for k,v in prior.items() if k not in allowed}
    for name in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:
        assert context[name][:len(prior['contextual_story_natural_dialogue_pass_v1871'][name])]==prior['contextual_story_natural_dialogue_pass_v1871'][name]
    save(binding_path,dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],records=bindings,
        final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_verification_scope=scope))
    ledger['coverage_units'][-1]['integrated_record_bindings_sha256']=sha(binding_path.read_bytes())
    backup=ROOT/'ledger_before_completion.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);temporary=LEDGER.with_name('editorial_review_current_v1.pending_shared_tutorial_completion.json')
    assert not temporary.exists() and LEDGER.read_bytes()==before
    temporary.write_bytes(encoded);os.replace(temporary,LEDGER);assert LEDGER.read_bytes()==encoded
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=4,counts=dict(completed=10525,revised=6254,retained=4271),
        ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),all_unrelated_keys_andearlier_record_prefixes_exact=True,
        integrated_record_bindings=str(binding_path),integrated_record_bindings_sha256=sha(binding_path.read_bytes()),
        separate_name_fields_deployed=2,name_fields_dialogue_credit=0,main_unchanged=True,full_goal_complete=False,guide_photos=False))
    print('4 tutorials credited once;2 name fields deployed without dialogue credit;10525 completions,6254 revisions/4271 retentions;main unchanged.')
