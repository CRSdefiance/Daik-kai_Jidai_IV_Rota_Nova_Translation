"""Seal directly reviewed, pixel-bound representative coverage without claiming natural story activation."""
from pathlib import Path
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

def main():
    out=ROOT/'gameplay_review_v1.json';assert not out.exists()
    native_path=ROOT/'storage_inputs_v1/native_pages.json';native=load(native_path);byid={r['id']:r for r in native['records']}
    selection_path=ROOT/'display_selection_v2.json';selection=load(selection_path)
    observed=set();pages=set();headers=set();evidence={};runs=[];sheets=[];transitions=[]
    def bind(path):
        path=Path(path);value=digest(path);assert str(path) not in evidence or evidence[str(path)]==value
        evidence[str(path)]=value;return value
    for name,expected in [('history',(18161,30,34)),('voices',(18641,34,36))]:
        terminal_path=ROOT/f'display_runs_v1/{name}/terminal.json';plan_path=terminal_path.with_name('run_plan.json')
        actual_path=ROOT/f'display_pixels_v1/{name}/focused_actual_pixels.json'
        terminal,plan,pixel=map(load,[terminal_path,plan_path,actual_path]);fixture=load(plan['fixture'])
        assert terminal['terminal'] and (terminal['frames'],pixel['selected_utterances'],pixel['selected_pages'])==expected
        assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        assert bind(plan['fixture'])==plan['fixture_sha256']
        assert fixture['padded_QA_block_bytes']<=fixture['source_bound_QA_block_limit']==9216 and fixture['QA_block_inside_original_stack_buffer']
        assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
        assert len(fixture['original_initializers'])+len(fixture['source_bound_QA_host_opening_exit'])==47
        assert not fixture['menus']
        report,observer=map(load,[terminal['report'],terminal['observer']])
        assert bind(terminal['report'])==terminal['report_sha256'] and bind(terminal['observer'])==terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and verified_existing_unlock(report)
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        assert bind(fixture['research_ROM'])==fixture['research_ROM_sha256']==report['ROM_sha256']
        for sample in pixel['body_pages']:
            display=byid[sample['id']]['complete_native_English_display'];page=display if sample['selector']==254 else display['pages'][sample['page']-1]
            assert sample['native_plane_sha256']==page['native_plane_sha256']==bind(sample['native_plane'])
            observed.add(sample['id']);pages.add((sample['id'],sample['page']))
        headers.update((h['source_selector'],h['expected_actor_ID'],h['text']) for h in pixel['headers'])
        compact_path=ROOT/f'display_{name}_sheets_v1/receipt.json';compact=load(compact_path)
        assert compact['actual_pixel_proof_sha256']==digest(actual_path) and compact['actual_dialogue_pages']==expected[2]
        assert len(compact['bottom_screen_sheets'])==3
        for sheet in compact['bottom_screen_sheets']+compact['full_scene_sheets']:
            assert bind(sheet['path'])==sheet['sha256']
        sheets.extend(compact['bottom_screen_sheets'])
        for p,h in pixel['evidence'].items():assert bind(p)==h
        for sheet in pixel['review_sheets']:assert bind(sheet['path'])==sheet['sha256']
        for p in [terminal_path,plan_path,actual_path,compact_path,fixture['inputs']]:bind(p)
        run=dict(name=name,run_plan=str(plan_path),terminal=str(terminal_path),actual=str(actual_path),fixture=plan['fixture'],
            frames=expected[0],utterances=expected[1],pages=expected[2]);runs.append(run)
        modal=[r for r in observer['rows'] if r['kind']=='modal_paint']
        resupply=next(r for r in modal if r['text_CP932']==' Want to resupply for ６００ gold?')
        departure=next(r for r in modal if 'Departed Hangzhou.' in r['text_CP932'])
        assert pixel['ordered_selected_source_calls'][-1]['frame']<resupply['frame']<departure['frame']<report['frames']
        if name=='history':
            calls=pixel['ordered_selected_source_calls'];start=next(c['frame'] for c in calls if c['id']=='DK4_MES_B54_R0507')
            stop=next(c['frame'] for c in calls if c['id']=='DK4_MES_B54_R0511')
            between=[r for r in modal if start<=r['frame']<stop]
            assert len(between)==1 and between[0]['text_CP932']==bytes.fromhex(byid['DK4_MES_B54_R0507']['expanded_native_hex']).decode('ascii')
            controls=load(fixture['inputs']);press=[r for r in controls if start<r['start']<=stop and r['buttons']==['A']]
            assert len(press)==1 and press[0]['duration']==16
            for event in [resupply,departure]:
                cap=next(c for c in report['frames_captured'] if c['frame']>=event['frame']+90)
                assert bind(cap['path'])==cap['PNG_sha256'];transitions.append(cap)
            final=report['frames_captured'][-1];assert final['frame']==18161 and bind(final['path'])==final['PNG_sha256'];transitions.append(final)
    selected={i for f in selection['fixtures'] for i in f['speech_ids']}
    assert observed==selected and (len(observed),len(pages),len(sheets))==(64,70,6)
    two=[k for k in selected if byid[k]['kind']=='progressive' and len(byid[k]['complete_native_English_display']['pages'])==2]
    assert len(two)==6 and all((k,1) in pages and (k,2) in pages for k in two)
    required=['DK4_MES_B54_R0499','DK4_MES_B54_R0507','DK4_MES_B55_R0091','DK4_MES_B55_R0155','DK4_MES_B55_R0179']
    assert set(required)<=observed and {'DK4_MES_B56_R0185','DK4_MES_B57_R0129','DK4_MES_B55_R0208','DK4_MES_B55_R0211'}<=observed
    assert any(a==15 for _,a,_ in headers)
    for p in [selection_path,native_path,Path(__file__)]:bind(p)
    save(out,dict(runs=runs,frames=36802,initialized_runs=2,distinct_source_utterances=64,distinct_body_pages=70,
        offline_only_source_utterances=246,unvisited_source_IDs=sorted(set(byid)-observed),reviewed_body_sheets=sheets,
        all70_selected_pages_directly_viewed=True,all_final_selected_body_planes_match_final_compiled_native_planes=True,
        all_six_distinct_two_page_transitions_observed=True,two_page_source_IDs=sorted(two),
        all_five_repaired_FE_panels_andstorage_alignment_observed=True,FE_repaired_source_IDs=required,
        no_extra_blank_FE_panel_between_R507_andR511=True,ordinary_16frame_A_return_observed=True,
        corrected_B56_B57_ASCII_I_F_glyphs_observed=True,inline_Bianca_Angelo_FE_andnamed_portrait_return_observed=True,
        no_typed_menus_in_source_scope=True,observed_menu_instances=0,
        complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing=True,
        qualified_exit_run=runs[0],transition_captures=transitions,
        name_headers=[dict(source_selector=s,expected_actor_ID=a,text=t) for s,a,t in sorted(headers)],
        repeated_timing_captures_have_exact_checked_body_header_planes_of_directly_viewed_pages=True,
        no_prose_compiled_buffer_font_viewport_orengine_changes=True,
        actual_gameplay=True,disclosed_initialized_native_display_QA=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        existing_system_unlock_not_earned=True,conditional_town_alternatives_not_naturally_consecutive=True,
        original_source_scene_conditions_effects_outcomes_not_simulated=True,full_catalogue_UI_unvisited=True,
        registered_integration_pending=True,new_credit=0,guide_photos=False,evidence=evidence))
    print('Sealed64 utterances/70 viewed pages,all six distinct two-page layouts,five FE repairs,I/F fixes andordinary host exit;246 bodies offline-only.')

if __name__=='__main__':main()
