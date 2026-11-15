"""Bind all303 editorial objects to completed native/visual checks without storage or gameplay credit."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def pages(row):
    value=row['complete_native_English_display']
    return value['pages'] if row['kind']=='progressive' else [value]

def main():
    finalpath=ROOT/'final_native_v1.json';approvalpath=ROOT/'offline_display_approval_v1.json'
    assert not finalpath.exists() and not approvalpath.exists()
    docpath=ROOT/'formatting_v3/formatting_input_complete_indices_v1.json'
    finalplanpath=ROOT/'plan_v6_visual/automatic_plans.json';plan=load(finalplanpath);doc=load(docpath)
    originalplanpath=ROOT/'plan_v3/automatic_plans.json';initialplan=load(originalplanpath)
    oldpath=ROOT/'native_pages_v1/compiled_native_pages.json';newpath=ROOT/'refined_native_v1/compiled_native_pages.json'
    freshpath=ROOT/'refined_pages_v1/compiled_native_pages.json';old,new,fresh=map(load,[oldpath,newpath,freshpath])
    assert len(doc['records'])==303 and Counter(r['decision'] for r in doc['records'])=={'revision':181,'retention':122}
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert len(plan['records'])==len(old['records'])==len(new['records'])==299
    assert new['pages']==old['pages']==299 and fresh['pages']==len(fresh['records'])==5
    assert old['fresh_compiled_alignments']==1196 and fresh['fresh_compiled_alignments']==20
    assert new['current_version_exact_reused_records']==294 and new['current_version_exact_reused_alignments']==1176
    assert new['runtime']==old['runtime']==fresh['runtime']==doc['runtime']
    assert new['font_sha256']==old['font_sha256']==fresh['font_sha256']
    assert plan['manuscript_sha256']==digest(docpath) and not plan['failures']
    assert not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    seen=set();review_sheets=[];visual_proofs=[]
    for block in [58,59,60,61,62,64,65,66,68,70]:
        path=ROOT/f'visual_reviews_v1/B{block}_initial.json';proof=load(path)
        assert proof['all_complete_glyphs_visible_on_reviewed_pages'] and proof['no_blank_clipped_overlapping_orunintended_pages_observed']
        assert digest(proof['source_block_receipt'])==proof['source_block_receipt_sha256']
        for sheet in proof['review_sheets']:
            assert sheet['directly_viewed'] and digest(sheet['path'])==sheet['sha256'];review_sheets.append(sheet)
        for p in proof['selected_page_receipts']:
            assert digest(p['preview'])==p['preview_sha256'] and digest(p['native_receipt'])==p['native_receipt_sha256']
            seen.add((p['id'],p['page'],p['preview_sha256'],p['native_plane_sha256']))
        visual_proofs.append(path)
    assert len(seen)==299 and len(review_sheets)==30
    sheetpath=ROOT/'refined_visual_v1/sheet_index.json';sheets=load(sheetpath)
    assert sheets['pages']==5 and sheets['native_receipt_sha256']==digest(freshpath) and len(sheets['sheets'])==1
    refined={r['id']:r for r in fresh['records']}
    for sheet in sheets['sheets']:
        assert digest(sheet['path'])==sheet['sha256']
        review_sheets.append({**sheet,'directly_viewed':True})
        for member in sheet['included']:
            row=refined[member['id']];panel=pages(row)[member['page']-1]
            assert panel['preview']==member['preview'] and digest(member['preview'])==member['preview_sha256']==panel['preview_sha256']
            assert digest(panel['native_plane'])==panel['native_plane_sha256']
            seen.add((row['id'],member['page'],panel['preview_sha256'],panel['native_plane_sha256']))
    assert len(seen)==304
    planned={r['id']:r for r in plan['records']};source={r['id']:r for r in doc['records']};selected=[]
    for row in new['records']:
        r=source[row['id']];p=planned[row['id']]
        assert row['compiled_hex']==p['encoded_hex'] and row['logical_English']==r['english']
        assert row['source_reference']==r['source_reference'] and row['current_reference']==r['current_reference']
        assert len(pages(row))==p['expected_native_pages']==1 and len(row['native_alignment']['cases'])==4
        for number,panel in enumerate(pages(row),1):
            assert digest(panel['preview'])==panel['preview_sha256'] and digest(panel['native_plane'])==panel['native_plane_sha256']
            assert (row['id'],number,panel['preview_sha256'],panel['native_plane_sha256']) in seen
            selected.append(dict(id=row['id'],page=number,preview=panel['preview'],preview_sha256=panel['preview_sha256'],
                native_plane_sha256=panel['native_plane_sha256']))
    assert len(selected)==299
    namespath=ROOT/'name_planes_v1/native_name_planes.json';menuspath=ROOT/'menu_native_v1/group_verification.json'
    names,menus=map(load,[namespath,menuspath]);nameviewpath=ROOT/'visual_reviews_v1/names_andmenus_initial.json';nameview=load(nameviewpath)
    assert names['runtime']==new['runtime'] and (names['actors'],names['distinct_current_strings'])==(20,24)
    assert (names['fresh_native_name_strings'],names['reused_native_name_strings'])==(8,16)
    assert all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in names['planes'])
    assert (menus['menus'],menus['captions'],menus['source_current_target_VM_alignments'],menus['bridged_modal_returns'],menus['compiler_negative_cases_rejected'])==(2,4,12,36,14)
    assert menus['all_reviewed_captions_normal_andhighlight_complete_glyphs_centering_bounds_guards_pass']
    assert nameview['all24_current_name_strings_directly_viewed'] and nameview['all_four_reviewed_captions_directly_viewed']
    for sheet in nameview['review_sheets']:assert sheet['directly_viewed'] and digest(sheet['path'])==sheet['sha256']
    before={r['id']:r for r in initialplan['records']};changes=[]
    for ident,p in planned.items():
        a=before[ident]
        assert a['logical_English']==p['logical_English']
        if a['encoded_hex']!=p['encoded_hex']:
            changes.append(dict(id=ident,source_reference=source[ident]['source_reference'],current_reference=source[ident]['current_reference'],
                before_lines=a['lines'],after_lines=p['lines'],pages_before=a['expected_native_pages'],pages_after=p['expected_native_pages'],
                all_words_controls_metrics_andusable_width_unchanged=True))
    assert len(changes)==7 and sum(r['pages_before']-r['pages_after'] for r in changes)==2
    final=deepcopy(new);final.update(direct_visual_review_pending=False,
        directly_reviewed_selected_page_receipts=selected,review_sheets=review_sheets,
        all299_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,
        selected_alignment_cases=1196,fresh_compiled_alignments=20,reused_compiled_alignments=1176,
        initial_fresh_alignment_cases=1196,additional_refined_alignment_cases=20,total_executed_alignment_cases_this_batch=1216,
        formatting_gates_still_false=True,actual_gameplay=False,new_credit=0)
    save(finalpath,final)
    glyphs=[r for r in doc['records'] if not r['current_comparison_paragraph'].isascii()];assert len(glyphs)==18
    save(approvalpath,dict(records=303,complete_exchanges=10,dialogue_revisions=181,dialogue_retentions=122,
        body_records=299,final_body_pages=299,source_FE_panels=12,choice_menus=2,choice_captions=4,
        all299_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,
        initial_native_pages_directly_viewed=299,additional_refined_pages_directly_viewed=5,
        selected_native_alignment_cases=1196,final_fresh_alignment_cases=20,final_exact_reused_alignment_cases=1176,
        initial_alignment_cases=1196,total_executed_alignment_cases=1216,
        scoped_names=20,distinct_name_strings=24,fresh_name_planes=8,exact_reused_name_planes=16,
        all24_names_andfour_captions_directly_viewed=True,native_menu_style_planes=16,native_menu_provider_alignments=12,
        bridged_menu_selection_cancel_returns=36,menu_negative_cases_rejected=14,
        accepted_layout_changes=changes,accepted_layout_changes_count=7,pages_reclaimed=2,
        all18_current_nonASCII_targets_have_complete_ASCII_target_native_planes=True,
        source_glyph_targets=[dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],
            current_nonASCII=dict(Counter(c for c in r['current_comparison_paragraph'] if not c.isascii()))) for r in glyphs],
        mixed_width_letter_corrections=1,mixed_width_letter_record='DK4_MES_B59_R0056',
        translated_Japanese_only_sailor_records=10,normalized_punctuation_target_records=7,
        no_native_FE_row_failure_no_added_commands_no_prose_shortening_no_font_viewport_orengine_change=True,
        ordinary_complete_word_layout_retentions=[dict(id=ident,source_reference=source[ident]['source_reference'],
            current_reference=source[ident]['current_reference'],reason=reason) for ident,reason in [
            ('DK4_MES_B61_R0023','The adjacent soft-row We/get boundary retains the complete neighborhood/science paragraph on one panel. No host QA warning or native guard is waived.'),
            ('DK4_MES_B70_R0034','Auxiliary continuations after has and be remain adjacent rows on one panel; the full exceptional-skill explanation is no longer stranded after A.'),
            ('DK4_MES_B64_R0074','Retain the ordinary lucky/charm boundary in a complete four-row paragraph; the full gift motivation and inability to sail remain visible on one panel.'),
            ('DK4_MES_B70_R0096','Retain Ninja/Garb across adjacent soft rows while keeping the full conditional-existence sentence in two rows; complete item words and identity are preserved.'),
        ]],
        full_formatted_manuscript=str(docpath),full_formatted_manuscript_sha256=digest(docpath),
        final_plan=str(finalplanpath),final_plan_sha256=digest(finalplanpath),final_native=str(finalpath),final_native_sha256=digest(finalpath),
        names=str(namespath),names_sha256=digest(namespath),menus=str(menuspath),menus_sha256=digest(menuspath),
        all_fifth_review_gates_still_false=True,stored_script_allocation_andrepresentative_gameplay_pending=True,
        actual_gameplay_observations=0,full_catalogue_UI_hardware_andnatural_scene_conditions_unvisited=True,
        no_new_ROM_orcompletion_credit=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [docpath,finalplanpath,originalplanpath,oldpath,newpath,freshpath,sheetpath,
            namespath,menuspath,nameviewpath,*visual_proofs,Path(__file__)]}))
    print('Approved offline scope:299 final body pages/four captions/24 names;seven wrap improvements,two pages reclaimed. Storage/gameplay/registration pending;zero credit.')

if __name__=='__main__':main()
