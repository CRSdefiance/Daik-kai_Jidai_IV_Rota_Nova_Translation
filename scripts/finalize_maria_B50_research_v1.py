"""Seal one complete held exchange after exact native/storage and actual continuation tests."""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

ROOT=Path('work/Maria_B50_FE_resolution_20261109_v3')
FINAL=Path('translations/maria_B50_final_review_v1.json')
def main():
    out=ROOT/'research_completion_v1.json';actual_path=ROOT/'gameplay_review_v1.json'
    assert not out.exists() and not actual_path.exists() and not FINAL.exists()
    paths=dict(source=ROOT/'source16_manuscript.json',physical=ROOT/'physical17_manuscript.json',
        native=ROOT/'final_native_v1.json',plan=ROOT/'plan_v5/automatic_plans.json',
        reconstruction=ROOT/'reconstruction_v1/reconstruction.json',stored=ROOT/'stored_v1/stored_native_verification.json',
        lookup=ROOT/'catalogue_v1/all17_stored_effective_body_bindings.json',loaders=ROOT/'loaders_v1/verification.json',
        visual=ROOT/'offline_approval_v1.json',terminal=ROOT/'display_run_v1/terminal.json',
        pixels=ROOT/'display_pixels_v1/focused_actual_pixels.json',run_plan=ROOT/'display_run_v1/run_plan.json',
        roles=ROOT/'role_bindings.json',macros=ROOT/'native_macro_measurements.json')
    d={k:load(p) for k,p in paths.items()};doc=deepcopy(d['source']);rebuilt=d['reconstruction'];stored=d['stored'];pixel=d['pixels'];terminal=d['terminal']
    runtime=d['native']['runtime'];assert runtime==stored['runtime']==d['lookup']['runtime']==d['source']['runtime']==d['macros']['runtime']
    assert len(doc['records'])==16 and (sum(r['decision']=='revision' for r in doc['records']),sum(r['decision']=='retention' for r in doc['records']))==(9,7)
    assert d['native']['pages']==stored['complete_stored_pages']==17 and len(stored['records'])==len(d['lookup']['records'])==17
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(8,9,0)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert d['lookup']['all17_physical_bodies_checked'] and d['lookup']['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (d['loaders']['fresh_whole_archive_loads_andcache_hits'],d['loaders']['fresh_parent_cases'])==(303,606)
    assert stored['reconstruction_sha256']==d['loaders']['reconstruction_sha256']==digest(paths['reconstruction'])
    assert d['lookup']['stored_sha256']==digest(paths['stored'])
    assert d['visual']['all17_final_panels_directly_viewed'] and d['visual']['no_QA_waivers_or_prose_font_viewport_orengine_changes']
    assert len(rebuilt['seven_FE_pagination_invalid_cases_rejected'])==7 and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert rebuilt['all_original_scene_controls_andconditional_scopes_preserved'] and rebuilt['source_owned_exact_FE_control_repeated_once']
    assert rebuilt['changed_blocks']==[50] and rebuilt['source_editorial_objects']==16 and rebuilt['native_speech_commands']==17
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    assert terminal['terminal'] and terminal['frames']==13001
    assert pixel['selected_utterances']==pixel['selected_pages']==17
    assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
    report,observer=map(load,[terminal['report'],terminal['observer']])
    assert digest(terminal['report'])==terminal['report_sha256'] and digest(terminal['observer'])==terminal['observer_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and verified_existing_unlock(report)
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    assert digest(d['run_plan']['fixture'])==d['run_plan']['fixture_sha256'];fixture=load(d['run_plan']['fixture'])
    assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
    assert len(fixture['original_initializers'])+len(fixture['source_bound_QA_host_opening_exit'])==47
    assert fixture['padded_QA_block_bytes']<=fixture['source_bound_QA_block_limit']==9216
    assert digest(fixture['research_ROM'])==fixture['research_ROM_sha256']==report['ROM_sha256']
    physical_ids={r['id'] for r in d['physical']['records']}
    observed={r['id'] for r in pixel['body_pages']};assert observed==physical_ids and len(observed)==17
    owner=d['physical']['pagination_owners'][0];first,second=owner['child_IDs']
    assert [r for r in pixel['ordered_selected_source_calls'] if r['id'] in [first,second,'DK4_MES_B50_R0046']]==[
        dict(frame=6185,id=first,page=1),dict(frame=6425,id=second,page=1),dict(frame=6665,id='DK4_MES_B50_R0046',page=1)]
    controls=load(fixture['inputs'])
    for frame in [6400,6640]:assert next(r for r in controls if r['start']==frame)==dict(start=frame,duration=16,buttons=['A'])
    assert max(r['frame'] for r in pixel['body_pages'] if r['id']==first)==6360
    assert max(r['frame'] for r in pixel['body_pages'] if r['id']==second)==6600
    modal=[r for r in observer['rows'] if r['kind']=='modal_paint']
    assert any(r['frame']==10019 and r['text_CP932']==' Want to resupply for ６００ gold?' for r in modal)
    assert any(r['frame']==10988 and 'Departed Hangzhou.' in r['text_CP932'] for r in modal)
    transitions=[next(c for c in report['frames_captured'] if c['frame']==f) for f in [10200,11160,13001]]
    sheets=pixel['review_sheets'];assert len(sheets)==3
    for p in [*sheets,*[dict(path=c['path'],sha256=c['PNG_sha256']) for c in transitions]]:assert digest(p['path'])==p['sha256']
    headers={(r['source_selector'],r['expected_actor_ID'],r['text']) for r in pixel['headers']}
    assert headers=={(3,3,'Maria Li'),(10,10,'Xien Yan')}
    actual=dict(frames=13001,initialized_runs=1,source_utterances_observed=16,native_commands_observed=17,native_body_pages_observed=17,
        source_FE_utterances=12,native_FE_panels=13,named_speeches_observed=4,offline_only_source_utterances=0,
        all17_native_panels_andboth_named_headers_complete_pixels_andblank_guards_match=True,
        all17_body_pages_directly_viewed=True,review_sheets=sheets,FE_first_panel_frame=6185,FE_continuation_frame=6425,
        following_source_FE_frame=6665,ordinary_A_frames=[6400,6640],full_paragraph_unchanged=True,
        exact_source_FE_control_andnull_actor_path_preserved=True,source_owned_continuation_A_andfollowing_return_observed=True,
        host_resupply_frame=10019,host_departure_frame=10988,host_sailing_final_frame=13001,
        source_complete_QA_host_exit_to_resupply_andsailing_observed=True,transition_captures=transitions,
        named_headers=[dict(source_selector=s,expected_actor_ID=a,text=t) for s,a,t in sorted(headers)],
        actual_gameplay=True,disclosed_initialized_native_command_display_QA=True,natural_activation=False,original_location=False,
        earned_chronology=False,full_route=False,hardware=False,original_B50_cutscene_art_effects_andevent_outcome_unvisited=True,
        existing_system_only_unlock_not_earned=True,guide_photos=False,new_credit=0,
        evidence={str(p):digest(p) for p in [paths['terminal'],paths['pixels'],paths['run_plan'],Path(terminal['report']),Path(terminal['observer']),Path(d['run_plan']['fixture']),Path(__file__)]})
    save(actual_path,actual)
    native={r['id']:r for r in d['native']['records']};plans={r['id']:r for r in d['plan']['records']};bodies={r['id']:r for r in stored['records']}
    bank=IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    source_plan=load(ROOT/'reconstruction_v1/source16_plans.json')
    by_source_plan={r['id']:r for r in source_plan['records']}
    old_prose=load('translations/maria_B37_B50_contextual_review_v1.json');old_byid={r['id']:r for r in old_prose['records']}
    for row in doc['records']:
        ident=row['id'];original=old_byid[ident]
        assert re.sub(r'\{MACRO:([A-Z]{2})\}',lambda m:m[1],row['english'])==original['english']
        assert all(row[k]==original[k] for k in ['source_hex','current_hex','source_reference','current_reference','decision','finding'])
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        ids=owner['child_IDs'] if ident==owner['source_ID'] else [ident];refs=[]
        for native_id in ids:
            item=bodies[native_id];at=item['new_offset'];raw=bytes.fromhex(item['stored_hex'])
            assert bank[50][at:at+len(raw)+1]==raw+b'\0' and bank[50][at-5:at+1].hex()==row['source_complete_preamble_hex']
            assert native[native_id]['compiled_hex']==plans[native_id]['encoded_hex']
            refs.append(dict(file_path='/data/SC3.DK4',block=50,offset=at,header_offset=at-5,record_index=item['new_record_index'],
                exact_stored_hex=raw.hex(),native_panel_ID=native_id,target_archive_sha256=rebuilt['target_archive_sha256']))
        row['planned_integrated_reference']=refs[0]
        row['planned_English_markup']=by_source_plan[ident]['formatted_markup']
        if len(ids)==2:
            assert ' '.join(plans[k]['logical_English'] for k in ids)==row['english']
            row.update(planned_integrated_native_pages=refs,formatter_owned_FE_pagination=owner,
                first_encoded_hex_represents_first_native_panel_only=True,complete_paragraph_has_two_source_owned_native_FE_panels=True)
        row['review']['formatting']=True
        row.update(fresh_formatting_binding_pending=False,actual_source_utterance_observed_in_disclosed_fixture=True,
            registered_release_andcompletion_credit_pending=True,new_credit=0,
            review_evidence=dict(offline_visual=str(paths['visual']),stored=str(paths['stored']),gameplay=str(actual_path),coverage='observed-disclosed-QA'))
    doc.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all_individual_five_gates_pass=True,all16_individual_five_gates_pass=True,all_fifth_formatting_gates_pending=False,
        physical_native_speech_commands_after_pagination=17,source_editorial_speeches=16,native_body_pages=17,
        actual_source_speech_variants=16,actual_body_pages=17,offline_only_source_speech_variants=0,
        registered_release_andcompletion_credit_pending=True,all16_prose_unchanged=True,new_credit=0,full_goal_complete=False)
    validate_natural_dialogue_batch(doc);save(FINAL,doc)
    source_plan.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL));save(ROOT/'source16_release_plans.json',source_plan)
    save(out,dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),all_individual_five_gates_pass=True,
        records=16,revisions=9,retentions=7,native_commands=17,native_pages=17,source_FE_records=12,native_FE_panels=13,
        FE_continuation_owners=1,additional_native_commands=1,source_record_credit_not_duplicated=True,
        exact_source6byte_FE_control_repeated_only=True,source_controls_runtime_substitutions_font_andviewport_preserved=True,
        ordinary_wrap_improvements=2,unintended_blank_FE_row_fixed=True,full139_character_counterfactual_preserved=True,
        actual_source_variants=16,actual_native_commands=17,actual_pages=17,offline_only_source_variants=0,
        actual_frames=13001,actual_runs=1,original_B50_natural_activation_cutscene_effects_andhardware_unvisited=True,
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(),actual_path,FINAL,ROOT/'source16_release_plans.json',Path(__file__)]}))
    print('Sealed16 five-gate reviews/17 observed native panels:9 revisions,7 retentions;full prose/control preserved;registered integration pending,zero new credit.')
if __name__=='__main__':main()
