"""Seal observed final pages, menu returns and corrected headers without natural-activation claims."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
OUT=ROOT/'gameplay_review_v1.json'
RUNS=[('bounded_run_1_v1','bounded_pixels_1_v1','bounded_body_contacts_v1'),
      ('name_headers_run_v1','name_headers_pixels_v1','name_headers_contact_v1'),
      ('wrap_followup_run_v1','wrap_followup_pixels_v1','wrap_followup_contact_v1')]

def main():
    assert not OUT.exists()
    native_path=ROOT/'storage_inputs_v3/native_pages.json';native=load(native_path)
    natives={r['id']:r for r in native['records']};evidence={};sheets=[];runs=[];chosen={};headers=[];sourceids=set()
    def bind(path):
        p=Path(path);value=digest(p);assert str(p) not in evidence or evidence[str(p)]==value;evidence[str(p)]=value
    for run,pixels,contacts in RUNS:
        tp=ROOT/run/'terminal.json';ap=ROOT/pixels/'focused_actual_pixels.json';cp=ROOT/contacts/'receipt.json'
        terminal,actual,contact=map(load,(tp,ap,cp))
        assert terminal['terminal'] and terminal['frames']==actual['frames']
        assert actual['all_selected_pages_observed_in_exact_fixture_order'] and actual['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert all(not actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        assert contact['actual_pixel_proof_sha256']==digest(ap)
        for sheet in contact['bottom_screen_sheets']+contact['full_scene_sheets']:
            assert digest(sheet['path'])==sheet['sha256'];sheets.append(sheet);bind(sheet['path'])
        report_path=Path(terminal['report']);observer_path=Path(terminal['observer'])
        assert digest(report_path)==terminal['report_sha256'] and digest(observer_path)==terminal['observer_sha256']
        report,observer=map(load,(report_path,observer_path))
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        follow=[r for r in observer['rows'] if r['kind']=='modal_paint' and r['frame']>=actual['following_nonfixture_modal_frame']]
        assert [' '.join(r['text_CP932'].split()) for r in follow[-2:]]==['Manuel, ready to depart?',
            'Ah, Admiral. I was just about to take on supplies. Tell us what you need.']
        final=report['frames_captured'][-1];assert digest(final['path'])==final['PNG_sha256'];bind(final['path'])
        assert final['frame']==terminal['frames']
        for call in actual['ordered_selected_source_calls']:
            key=call['id'],call['page'];sample=next(s for s in actual['body_pages'] if (s['id'],s['page'])==key)
            chosen[key]=dict(sample,actual_proof=str(ap),actual_proof_sha256=digest(ap),terminal=str(tp),terminal_sha256=digest(tp))
            sourceids.add(call['id'])
        headers+=actual['headers']
        for p,h in actual['evidence'].items():assert digest(p)==h;bind(p)
        runs.append(dict(terminal=str(tp),terminal_sha256=digest(tp),actual_proof=str(ap),actual_proof_sha256=digest(ap),
            frames=terminal['frames'],utterances=actual['selected_utterances'],pages=actual['selected_pages'],
            following_resupply_dialogue_observed=True,final_capture=final,final_capture_directly_viewed=True,
            complete_body_holds=actual['complete_body_planes'],complete_header_holds=actual['complete_header_planes']))
        for p in [tp,ap,cp,report_path,observer_path]:bind(p)
    assert len(sheets)==17 and len(sourceids)==169 and len(chosen)==170 and sum(r['frames'] for r in runs)==57363
    for (ident,number),sample in chosen.items():
        display=natives[ident]['complete_native_English_display']
        pages=[display] if natives[ident]['kind']=='system-FE' else display['pages'];page=pages[number-1]
        assert sample['native_plane_sha256']==page['native_plane_sha256'] and digest(sample['native_plane'])==page['native_plane_sha256']
    corrected=load(ROOT/'name_headers_pixels_v1/focused_actual_pixels.json')['headers']
    labels={55:'David Flahven',56:'Georg Salzgitter',57:'Nagayoshi Kamuro'}
    assert {h['expected_actor_ID'] for h in corrected}==set(labels)
    assert all(h['text']==labels[h['expected_actor_ID']] and h['complete_name_glyphs_andblank_guards_exact'] for h in corrected)
    # Latest samples for the three changed headers must come from the tested field target.
    for ident in ['DK4_MES_B38_R0059','DK4_MES_B38_R0063','DK4_MES_B39_R0009']:
        assert chosen[ident,1]['actual_proof']==str(ROOT/'name_headers_pixels_v1/focused_actual_pixels.json')
    assert chosen['DK4_MES_B29_R0059',1]['actual_proof']==str(ROOT/'wrap_followup_pixels_v1/focused_actual_pixels.json')
    mp=ROOT/'bounded_menus_1_v1/menu_actual_pixels.json';menus=load(mp)
    assert menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert menus['byte_identical_menu_occurrences_bound_by_exact_source_keys_andordered_surrounding_calls']
    fixture_path=ROOT/'focused_fixtures_bounded_v1/hodram_residual_part1_fixture.json';fixture=load(fixture_path)
    controls=load(fixture['inputs']);assert digest(fixture['inputs'])==fixture['inputs_sha256']
    assert {(m['block'],m['source_command_offset']) for m in menus['menus']}=={(30,1100),(33,414),(37,216)}
    returns=[]
    for m in menus['menus']:
        assert m['count']==2 and m['observed_selected_options']==[0]
        samples=[s for s in menus['menu_samples'] if s['source_command_offset']==m['source_command_offset']]
        assert len(samples)==m['complete_live_samples'] and all(m['occurrence_window'][0]<s['frame']<m['occurrence_window'][1] for s in samples)
        selected=[s for s in samples if s['visible_selected_option'] is not None];assert selected
        last=max(s['frame'] for s in selected)
        presses=[r['start'] for r in controls if r['buttons']==['A'] and last<r['start']<=m['occurrence_window'][1]]
        assert len(presses)==1;returns.append(dict(**m,ordinary_A_return_frame=presses[0]))
        assert digest(m['proof'])==m['proof_sha256'];bind(m['proof'])
    sheet=menus['review_sheet'];assert digest(sheet['path'])==sheet['sha256'];bind(sheet['path'])
    assert load(ROOT/'opaque_pixel_model_qualification_v1.json')['all8_mutations_rejected']
    for p in [mp,fixture_path,Path(fixture['inputs']),native_path,ROOT/'opaque_pixel_model_qualification_v1.json',Path(__file__)]:bind(p)
    save(OUT,dict(runs=runs,frames=57363,initialized_runs=3,distinct_source_utterances=169,distinct_body_pages=170,
        offline_only_source_utterances=388-169,final_observed_samples=list(chosen.values()),
        all_final_selected_body_planes_match_final_compiled_native_planes=True,
        all170_broad_pages_three_corrected_headers_andfinal_wrap_directly_viewed=True,
        reviewed_body_sheets=sheets,menu_sheet=sheet,menus=returns,
        all_three_native_menus_default_selection_andordinary_A_returns_observed=True,
        other_choices_cancellation_numeric_returns_andoriginal_branches_offline_only=True,
        all_three_final_resupply_returns_directly_viewed=True,
        name_headers=[dict(h,label=h['text']) for h in corrected],
        all_three_changed_progressive_names_observed_complete=True,
        source_actor_IDs_from_qualified_controls_not_inferred_from_pixels=True,
        full_catalogue_UI_unvisited=True,natural_activation=False,earned_chronology=False,hardware=False,
        actual_gameplay=True,disclosed_initialized_native_display_QA=True,registered_integration_pending=True,new_credit=0,evidence=evidence))
    print('Sealed169 final observed utterances/170 pages,three corrected headers,three menus/A returns andthree resupply transitions;57363 frames. No integration credit.')

if __name__=='__main__':main()
