"""Seal exact representative pixels, ordinary menu returns and the narrow host exit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

ROOT=Path('work/Maria_B37_B50_clean_20261109')
OUT=ROOT/'gameplay270_review_v1.json'

def main():
    assert not OUT.exists()
    native_path=ROOT/'storage270_inputs_v1/native_pages.json'
    native=load(native_path);byid={r['id']:r for r in native['records']}
    selection_path=ROOT/'representative270_selection_v1.json';selection=load(selection_path)
    evidence={};runs=[];sheets=[];observed=set();pages=set();headers=set()
    def bind(path):
        path=Path(path);value=digest(path)
        assert str(path) not in evidence or evidence[str(path)]==value
        evidence[str(path)]=value;return value
    for name,expected in [('indian',(11201,24,25)),('rafael',(10001,18,21)),
                          ('caribbean',(10721,21,23)),('exit',(10001,2,3))]:
        terminal_path=ROOT/f'display270_{name}_run_v1/terminal.json'
        actual_path=ROOT/f'display270_{name}_pixels_v1/focused_actual_pixels.json'
        plan_path=ROOT/f'display270_{name}_run_v1/run_plan.json'
        terminal,pixel,plan=map(load,[terminal_path,actual_path,plan_path])
        assert terminal['terminal'] and (terminal['frames'],pixel['selected_utterances'],pixel['selected_pages'])==expected
        assert pixel['all_selected_pages_observed_in_exact_fixture_order']
        assert pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        assert digest(plan['fixture'])==plan['fixture_sha256'];fixture=load(plan['fixture'])
        assert fixture['padded_QA_block_bytes']<=fixture['source_bound_QA_block_limit']==9216
        assert fixture['QA_block_inside_original_stack_buffer']
        assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
        assert len(fixture['original_initializers'])+len(fixture['source_bound_QA_host_opening_exit'])==47
        report,observer=map(load,[terminal['report'],terminal['observer']])
        assert bind(terminal['report'])==terminal['report_sha256']
        assert bind(terminal['observer'])==terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert verified_existing_unlock(report)
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        assert digest(fixture['research_ROM'])==fixture['research_ROM_sha256']==report['ROM_sha256']
        for sample in pixel['body_pages']:
            display=byid[sample['id']]['complete_native_English_display']
            page=display if sample['selector']==254 else display['pages'][sample['page']-1]
            assert sample['native_plane_sha256']==page['native_plane_sha256']==digest(sample['native_plane'])
            observed.add(sample['id']);pages.add((sample['id'],sample['page']))
        headers.update((h['source_selector'],h['expected_actor_ID'],h['text']) for h in pixel['headers'])
        for p,h in pixel['evidence'].items():assert bind(p)==h
        sheets.extend(pixel['review_sheets'])
        for path in [terminal_path,actual_path,plan_path,plan['fixture']]:bind(path)
        runs.append(dict(name=name,run_plan=str(plan_path),run_plan_sha256=digest(plan_path),
            terminal=str(terminal_path),actual=str(actual_path),fixture=plan['fixture'],
            frames=expected[0],utterances=expected[1],pages=expected[2],new_distinct_coverage=name!='exit'))
    assert observed==set(selection['selected_speech_ids']) and (len(observed),len(pages))==(63,69)
    assert sorted(set(byid)-observed)==selection['unvisited_body_ids']
    for ident in selection['all_six_two_page_cases_selected']:
        assert (ident,1) in pages and (ident,2) in pages
    assert ('DK4_MES_B46_R0004',1) in pages and ('DK4_MES_B46_R0009',1) in pages
    returns=[]
    for name,block,offset,before_id,after_id,press in [
        ('indian',38,616,'DK4_MES_B38_R0029','DK4_MES_B38_R0044',6160),
        ('caribbean',49,2416,'DK4_MES_B49_R0174','DK4_MES_B49_R0188',7840)]:
        menu_path=ROOT/f'display270_{name}_menu_pixels_v2/menu_actual_pixels.json';menu=load(menu_path)
        assert menu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert len(menu['menus'])==1;item=menu['menus'][0]
        assert (item['block'],item['source_command_offset'],item['count'],item['observed_selected_options'])==(block,offset,2,[0])
        assert item['complete_live_samples']==len(menu['menu_samples'])==2
        pixels=load(ROOT/f'display270_{name}_pixels_v1/focused_actual_pixels.json')
        calls=pixels['ordered_selected_source_calls']
        before=max(r['frame'] for r in calls if r['id']==before_id)
        after=min(r['frame'] for r in calls if r['id']==after_id)
        assert all(before<s['frame']<after for s in menu['menu_samples'])
        visible=max(s['frame'] for s in menu['menu_samples'] if s['visible_selected_option']==0)
        fixture=load(next(r['fixture'] for r in runs if r['name']==name));controls=load(fixture['inputs'])
        assert [r['start'] for r in controls if r['buttons']==['A'] and visible<r['start']<=after]==[press]
        assert next(r for r in controls if r['start']==press)['duration']==16
        returns.append(dict(**item,preceding_speech=before_id,preceding_call_frame=before,
            following_speech=after_id,following_call_frame=after,ordinary_A_frame=press))
        sheets.append(menu['review_sheet']);bind(menu_path)
    assert len(sheets)==16
    for sheet in sheets:assert bind(sheet['path'])==sheet['sha256']
    exit_run=runs[-1];exit_terminal=load(exit_run['terminal'])
    exit_report=load(exit_terminal['report']);exit_observer=load(exit_terminal['observer'])
    modal=[r for r in exit_observer['rows'] if r['kind']=='modal_paint']
    resupply=next(r for r in modal if r['text_CP932']==' Want to resupply for ６００ gold?')
    departure=next(r for r in modal if 'Departed Hangzhou.' in r['text_CP932'])
    assert resupply['frame']<departure['frame']<exit_report['frames']
    transitions=[]
    for event in [resupply,departure]:
        cap=next(c for c in exit_report['frames_captured'] if c['frame']>=event['frame']+90)
        assert bind(cap['path'])==cap['PNG_sha256'];transitions.append(cap)
    final=exit_report['frames_captured'][-1]
    assert final['frame']==10001 and bind(final['path'])==final['PNG_sha256'];transitions.append(final)
    # Every listed sheet and the three transition captures have been directly
    # inspected by the editorial reviewer before executing this seal.
    for p in [native_path,selection_path,ROOT/'exit270_selection_v1.json',Path(__file__)]:bind(p)
    save(OUT,dict(runs=runs,frames=41924,initialized_runs=4,broad_display_runs=3,narrow_exit_probes=1,
        distinct_source_utterances=63,distinct_body_pages=69,offline_only_source_utterances=203,
        unvisited_source_IDs=sorted(set(byid)-observed),reviewed_body_sheets=sheets,
        all_selected_pages_directly_viewed=True,all_final_selected_body_planes_match_final_compiled_native_planes=True,
        all_six_two_page_transitions_observed=True,FE_to_named_speaker_transition_observed=True,
        both_reclaimed_B49_single_pages_andcomplete_question_tag_observed=True,
        name_headers=[dict(source_selector=s,expected_actor_ID=a,text=t) for s,a,t in sorted(headers)],
        observed_menu_instances=2,observed_choice_labels=4,menus=returns,
        ordinary_default_menu_returns_to_next_fixture_speech_observed=True,
        other_choices_cancel_numeric_VM_returns_andoriginal_conditional_branches_offline_only=True,
        complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing=True,
        qualified_exit_run=exit_run,transition_captures=transitions,
        host_resupply_modal_frame=resupply['frame'],host_departure_modal_frame=departure['frame'],
        broad_runs_end_before_host_exit_completed_no_production_fault_claim=True,
        no_prose_compiled_body_orengine_change_from_gameplay_review=True,
        actual_gameplay=True,disclosed_initialized_native_display_QA=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        existing_system_unlock_not_earned=True,full_catalogue_UI_unvisited=True,registered_integration_pending=True,
        guide_photos=False,new_credit=0,evidence=evidence))
    print('Sealed63 utterances/69 pages,twomenus/ordinary A returns andsource-complete host exit;203 bodies offline-only.')

if __name__=='__main__':main()
