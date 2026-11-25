"""Approve19 native layout refinements and reuse304 exact records;retain one better-balanced original."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.plan_rafael_B81_B84_semantic_pages_v3 import main as plan_main

ROOT=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
DOC=ROOT/'native_ready_subset_v1/manuscript.json'
BASE=ROOT/'native_subset_v2/compiled_native_pages.json'
DELTA=ROOT/'native_delta_v4/compiled_native_pages.json'

if __name__=='__main__':
    import sys
    output=ROOT/'combined_native_v5.json';preferences=ROOT/'preferences_v5.json';assert not output.exists() and not preferences.exists()
    prefs=load(ROOT/'preferences_v4.json');entry=prefs['records'].pop('DK4_MES_B82_R0183')
    assert entry['line_phrases']==['get it, do you? Hah!']
    reason='Retain the original balanced two-row question:the attempted whole predicate/tag/laugh constraint creates a sparse You really opening. The original keeps it,do you? Hah! together on the same page andhas no short final row. No prose change oradditional native execution is needed for its exact earlier bytes.'
    prefs.update(previous_preferences=str(ROOT/'preferences_v4.json'),previous_preferences_sha256=sha((ROOT/'preferences_v4.json').read_bytes()),
        justified_layout_retention=dict(id='DK4_MES_B82_R0183',reason=reason),new_credit=0)
    save(preferences,prefs)
    oldargv=sys.argv
    try:
        sys.argv=['semantic_page_planner','--manuscript',str(DOC),'--preferences',str(preferences),'--out',str(ROOT/'automatic_subset_v5')]
        plan_main()
    finally:sys.argv=oldargv
    pp=ROOT/'automatic_subset_v5/automatic_plans.json';plans,doc,base,delta=map(load,[pp,DOC,BASE,DELTA])
    assert base['runtime']==delta['runtime'] and base['font_sha256']==delta['font_sha256']
    assert base['manuscript_sha256']==sha(DOC.read_bytes()) and not plans['failures']
    assert len(base['records'])==323 and base['pages']==332 and len(delta['records'])==20 and delta['pages']==27
    review=load(ROOT/'native_subset_v2/direct_visual_review_with_findings.json')
    assert review['all30_readable_sheets_directly_viewed'] and review['all332_complete_native_pages_directly_viewed']
    assert review['native_proof_sha256']==sha(BASE.read_bytes())
    assert len(delta['review_sheets'])==5
    for sheet in delta['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    a,b=[{r['id']:r for r in proof['records']} for proof in [base,delta]]
    records=[];origins={};fresh=reused=freshpages=reusedpages=0
    for p in plans['records']:
        ident=p['id'];match=b.get(ident)
        if match is not None and match['compiled_hex']==p['encoded_hex']:
            row=deepcopy(match);origin=DELTA;fresh+=1;freshpages+=p['expected_native_pages']
        else:
            row=deepcopy(a[ident]);origin=BASE;reused+=1;reusedpages+=p['expected_native_pages']
        assert row['compiled_hex']==p['encoded_hex'] and row['logical_English']==p['logical_English']
        assert len(row['native_alignment']['cases'])==4 and all(c['output_hex']==row['expanded_native_hex'] for c in row['native_alignment']['cases'])
        display=row['complete_native_English_display']
        if row['kind']=='system-FE':
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
            assert sha(Path(display['native_plane']).read_bytes())==display['native_plane_sha256']
            pages=1
        else:
            assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
            assert display['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            pages=len(display['pages'])
            for page in display['pages']:
                assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
        assert pages==p['expected_native_pages']
        records.append(row);origins[ident]=dict(native_proof=str(origin),native_proof_sha256=sha(origin.read_bytes()),
            compiled_bytes_logical_prose_complete_source_preamble_andnative_pages_exact=True,
            direct_visual_review_reused_for_exact_native_page=True)
    assert (fresh,reused,freshpages,reusedpages)==(19,304,26,306)
    approval=ROOT/'native_delta_v4/direct_visual_approval_v5.json'
    save(approval,dict(native_proof=str(DELTA),native_proof_sha256=sha(DELTA.read_bytes()),all_five_readable_delta_sheets_directly_viewed=True,
        all27_newly_generated_delta_pages_directly_viewed=True,approved_final_changed_records=19,approved_final_changed_pages=26,
        rejected_layout_record_ID='DK4_MES_B82_R0183',retained_original_layout_reason=reason,
        seven_page_boundaries_and12_phrase_wraps_improved_without_prose_shortening_oradditional_pages=True,
        formatter_owned_unused_rows_at_complete_sentence_boundaries_native_checked_no_blank_page=True,
        representative_actual_transition_check_still_required=True,actual_gameplay=False,new_credit=0))
    save(output,dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(pp),plan_sha256=sha(pp.read_bytes()),
        runtime=base['runtime'],font_sha256=base['font_sha256'],records=records,origins=origins,pages=332,
        fresh_final_layout_records=19,fresh_final_layout_pages=26,exact_reused_records=304,exact_reused_pages=306,
        all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,complete_consumption_andpagination_exact=True,
        direct_visual_review_pending=False,all332_complete_pages_directly_viewed=True,all323_subset_body_layouts_approved=True,
        full_330_object_batch_display_complete=False,two_long_FE_paragraphs_andfive_menu_objects_still_pending=True,
        formatting_gates_still_false=True,stored_actual_names_andregistered_integration_pending=True,
        actual_gameplay=False,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,pp,BASE,DELTA,approval,Path(__file__)]}))
    print('Approved323 bodies/332 native-viewed pages:19 refined records/26 pages and304 exact reuses;seven page-turn fixes. Two FE paragraphs/five captions andstored/actual/release remain.')
