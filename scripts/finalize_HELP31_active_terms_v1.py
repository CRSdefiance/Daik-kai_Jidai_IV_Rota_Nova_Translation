"""Seal corrected Deck30 plus zero-credit Coerce33 with disjoint current page proofs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.reviewed_help_pages_v12 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/HELP31_active_terms_20261105')
OLD = Path('work/analysis/Shared_HELP_T103_T132_formatting_20261104')
FINAL = Path('translations/help_deck30_Coerce33_active_terms_final_review_v1.json')

if __name__ == '__main__':
    assert not FINAL.exists() and not (ROOT/'production_plan_v1.json').exists()
    paths = [ROOT/'automatic_plans_v1.json', ROOT/'native_pages_v1/native_help_pages.json',
             ROOT/'preview_qualification_v1/direct_visual_approval.json',
             ROOT/'focused_navigation_checked_v1/ordinary_gameplay_verification.json',
             OLD/'production_plan_v1.json', OLD/'focused_navigation_checked_v1/ordinary_gameplay_verification.json',
             OLD/'focused_navigation_checked_v1/direct_actual_visual_approval.json']
    plan, native, visual, fresh, oldplan, oldactual, oldvisual = map(load, paths)
    assert native['plan_sha256'] == sha(paths[0].read_bytes())
    assert visual['native_proof_sha256'] == sha(paths[1].read_bytes())
    assert visual['all31_pages_approved'] and native['fresh_page_IDs'] == [33,116,117,118,121,126]
    assert native['exact_reused_pages'] == 25 and native['native_pages'] == 31
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    assert native['all_executed_current_instruction_bytes_exact']
    assert fresh['actual_pages'] == 9 and len(fresh['readable_actual_sheets']) == 3
    assert fresh['all_selected_complete_actual_pages_andnative_child_targets_pass']
    assert oldvisual['actual_proof_sha256'] == sha(paths[5].read_bytes())
    assert oldvisual['all30_observed_pages_approved'] and oldvisual['all_eight_actual_sheets_directly_viewed']
    for group in [fresh, oldactual]:
        assert group['actual_ordinary_controls_no_state_injection'] and not group['full_story_playthrough'] and not group['hardware']
        for sheet in group['readable_actual_sheets']:
            assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    # Actual proof reuse requires matching renderer, common UI and font, not the whole Help archive.
    a, b = [NdsImage.open(d['research_ROM']) for d in [fresh, oldactual]]
    assert all(a.read_file(p) == b.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    assert all(sha(Path(d['research_ROM']).read_bytes()) == d['research_ROM_sha256'] for d in [fresh,oldactual])
    oldpages = {p['topic_id']:p for p in oldplan['pages']}
    freshcases = {p['topic_id']:p for p in fresh['actual_HELP_cases']}
    oldcases = {p['topic_id']:p for p in oldactual['actual_HELP_cases']}
    assert set(freshcases) == {33,103,105,110,116,117,118,121,126}
    cases = []
    for page in plan['pages']:
        t = page['topic_id']; isfresh = t in freshcases
        if not isfresh:
            assert page == oldpages[t] and t in native['exact_reused_page_IDs']
        case = deepcopy((freshcases if isfresh else oldcases)[t])
        assert case['all_first_internal_final_glyphs_andblank_gaps_exact']
        assert sha(Path(case['capture']).read_bytes()) == case['capture_sha256']
        assert sha(Path(case['RAM']['path']).read_bytes()) == case['RAM']['sha256']
        case.update(actual_proof=str(paths[3] if isfresh else paths[5]),
                    actual_proof_sha256=sha(paths[3 if isfresh else 5].read_bytes()),
                    research_ROM=(fresh if isfresh else oldactual)['research_ROM'],
                    research_ROM_sha256=(fresh if isfresh else oldactual)['research_ROM_sha256'],
                    current_page_encoded_hex=page['encoded_hex'],exact_prior_observation_reused=not isfresh)
        cases.append(case)
    assert len(cases) == 31 and sum(c['exact_prior_observation_reused'] for c in cases) == 22
    approval = ROOT/'focused_navigation_checked_v1/direct_actual_visual_approval.json'
    assert not approval.exists()
    save(approval, dict(actual_proof=str(paths[3]),actual_proof_sha256=sha(paths[3].read_bytes()),
        all_three_fresh_actual_sheets_directly_viewed=True,all9_fresh_observed_pages_approved=True,
        exact_prior_actual_pages_reused=22,all31_pages_have_individual_current_observation_bindings=True,
        cases=cases,no_single31_page_current_playthrough_claim=True,new_credit=0))
    doc = deepcopy(load(plan['manuscript'])); resource = Path(plan['research_resource']).read_bytes()
    for row in doc['records']:
        row['review']['formatting'] = True
        row.update(offline_only=False,registered_integration_pending=True,fresh_active_term_correction_needs_display=False,
                   fresh_display_allocation_widgets_andintegration_pending=False,all_fresh_display_gates_pending=False)
        row['planned_stored_pages'] = []
        for p in [p for p in plan['pages'] if p['source_article_id'] == row['topic_id']]:
            t=p['topic_id']; nr=next(r for r in native['records'] if r['topic_id']==t); ar=next(r for r in cases if r['topic_id']==t)
            raw=bytes.fromhex(p['encoded_hex']); at=int.from_bytes(resource[8+4*t:12+4*t],'little')
            assert nr['encoded_hex']==p['encoded_hex'] and resource[at:at+len(raw)]==raw
            row['planned_stored_pages'].append(dict(file_path=doc['file_path'],block=t,archive_offset=at,bytes=len(raw),
                offset_table_slot=8+4*t,exact_stored_hex=raw.hex(),target_archive_sha256=sha(resource),
                native_preview=nr['preview'],native_preview_sha256=nr['preview_sha256'],
                actual_frame=ar['frame'],actual_capture=ar['capture'],actual_capture_sha256=ar['capture_sha256'],
                actual_binding=ar))
    assert sum(r['decision']=='revision' for r in doc['records'])==11
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness','formatting']) for r in doc['records'])
    doc.update(format='dk4-deck30-Coerce33-active-terms-final-review-v1',all31_individual_five_gates_pass=True,
        all_fifth_gates_pending=False,pending_fresh_formatting_topic_IDs=[],native_andvisually_approved_pages=31,
        fresh_native_pages=6,exact_reused_native_pages=25,actual_pages=31,actual_articles=31,
        fresh_actual_pages=9,exact_reused_actual_pages=22,offline_only_pages=0,offline_only_articles=0,
        current_page_proof_composition=str(approval),current_page_proof_composition_sha256=sha(approval.read_bytes()),
        previous_wrong_static_skill_inference_superseded=True,registered_integration_pending=True,
        new_credit=0,new_source_records=30,new_source_revisions=10,new_source_retentions=20,
        previously_credited_amendments=[33],guide_photos=False,full_goal_complete=False)
    doc['evidence'].update({str(p):sha(p.read_bytes()) for p in [*paths,approval,Path(__file__),Path('dk4tool/dialogue/reviewed_help_pages_v12.py')]})
    image=NdsImage.open(doc['current_ROM']); clean=NdsImage.open('work/clean.nds'); base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    file=doc['file_path']; compiled_resource,compiled=plan_articles(doc,clean.read_file(file),base.read_file(file),image.read_file(file))
    assert compiled_resource==resource and compiled['pages']==plan['pages']
    save(FINAL,doc)
    save(ROOT/'production_plan_v1.json',dict(**compiled,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
        research_resource=plan['research_resource'],current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
        all_source_native_actual_visual_andindividual_five_gates_bound=True,registered_integration_pending=True,new_credit=0))
    print('31 five-gate research reviews:30 new-source candidates (10 revisions/20 retentions),Coerce33 amendment zero credit;6 fresh native/9 fresh actual,exact prior proofs reused.')
