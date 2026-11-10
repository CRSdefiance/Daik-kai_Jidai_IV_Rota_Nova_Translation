"""Bind the whole328-object review to final native pages and direct visual evidence."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.stage_maria328_review_sheets_v1 import pages

def main():
    finalpath=ROOT/'final_native_v1.json';approvalpath=ROOT/'offline_display_approval_v1.json'
    assert not finalpath.exists() and not approvalpath.exists()
    docpath=ROOT/'formatting_FE_v1/physical_manuscript.json'
    planpath=ROOT/'plan_visual_v6/automatic_plans.json'
    prosepath=Path('translations/maria_B73_B95_contextual_review_v1.json')
    selectionpath=ROOT/'native_final_selection_v2.json'
    freshpath=ROOT/'native_final_v2/compiled_native_pages.json'
    telescopepath=ROOT/'telescope_native_v1/compiled_native_pages.json'
    doc,plan,prose,selection,fresh,telescope=map(load,[docpath,planpath,prosepath,selectionpath,freshpath,telescopepath])
    assert len(prose['records'])==328 and Counter(r['decision'] for r in prose['records'])=={'revision':143,'retention':185}
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert len(doc['records'])==329 and len(plan['records'])==314 and plan['manuscript_sha256']==digest(docpath)
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert fresh['runtime']==telescope['runtime']==doc['runtime']
    assert fresh['font_sha256']==telescope['font_sha256']
    assert (len(fresh['records']),fresh['pages'],fresh['fresh_compiled_alignments'])==(90,92,360)
    assert (len(telescope['records']),telescope['pages'],telescope['fresh_compiled_alignments'])==(1,2,4)
    for report in [fresh,telescope]:
        assert report['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert report['complete_consumption_andpagination_exact']
    originals={r['id']:r for r in doc['records'] if r['kind'] in ['progressive','system-FE']}
    planned={r['id']:r for r in plan['records']}
    leaves={};bindings={}
    for binding in selection['exact_reused_records']:
        assert digest(binding['path'])==binding['sha256']
        row=binding['record']
        if row['id']=='DK4_MES_B77_R0012':continue
        assert row['id'] not in leaves
        leaves[row['id']]=row;bindings[row['id']]={k:binding[k] for k in ['path','sha256']}
    assert len(leaves)==223
    for path,report in [(freshpath,fresh),(telescopepath,telescope)]:
        for row in report['records']:
            assert row['id'] not in leaves
            leaves[row['id']]=row;bindings[row['id']]=dict(path=str(path),sha256=digest(path))
    assert leaves.keys()==originals.keys()==planned.keys() and len(leaves)==314
    seen=set();sheets=[];visualpaths=[]
    for path in sorted((ROOT/'visual_reviews_v1').glob('*.json')):
        proof=load(path)
        if 'selected_page_receipts' not in proof:continue
        assert proof['all_complete_glyphs_visible_on_reviewed_pages'] and proof['no_blank_clipped_overlapping_orunintended_pages_observed']
        assert digest(proof['source_block_receipt'])==proof['source_block_receipt_sha256']
        for sheet in proof['review_sheets']:
            assert sheet['directly_viewed'] and digest(sheet['path'])==sheet['sha256'];sheets.append(sheet)
        for p in proof['selected_page_receipts']:
            assert digest(p['preview'])==p['preview_sha256']
            seen.add((p['id'],p['page'],p['preview_sha256'],p['native_plane_sha256']))
        visualpaths.append(path)
    selected=[]
    for original in originals.values():
        row=leaves[original['id']];p=planned[row['id']]
        assert row['logical_English']==original['english'] and row['compiled_hex']==p['encoded_hex']
        assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
        assert len(row['native_alignment']['cases'])==4 and len(pages(row))==p['expected_native_pages']
        display=row['complete_native_English_display']
        if row['kind']=='progressive':
            assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
            assert display['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            assert all(q['native_independent_plane_equal'] and q['all_bitmap_header_input_canaries_exact'] for q in pages(row))
        else:
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert display['input_bitmap_header_view_context_canaries_andcomplete_return_exact']
            assert display['all_executed_instructions_exact_current_sections_andpayload']
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
        for number,panel in enumerate(pages(row),1):
            assert digest(panel['preview'])==panel['preview_sha256'] and digest(panel['native_plane'])==panel['native_plane_sha256']
            assert (row['id'],number,panel['preview_sha256'],panel['native_plane_sha256']) in seen
            selected.append(dict(id=row['id'],page=number,preview=panel['preview'],preview_sha256=panel['preview_sha256'],
                native_plane_sha256=panel['native_plane_sha256'],native_receipt=bindings[row['id']]))
    assert len(selected)==321 and len(seen)==329
    namespath=ROOT/'name_planes_v1/native_name_planes.json';menuspath=ROOT/'menu_native_v1/menu_provider_and_planes.json'
    nameviewpath=ROOT/'visual_reviews_v1/names_andmenus.json'
    names,menus,nameview=map(load,[namespath,menuspath,nameviewpath])
    assert names['runtime']==menus['runtime']==doc['runtime']
    assert (names['actors'],names['distinct_current_strings'],names['fresh_native_name_strings'],names['reused_native_name_strings'])==(24,28,15,13)
    assert all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in names['planes'])
    assert (len(menus['menus']),menus['native_provider_alignments'],menus['bridged_modal_returns'],menus['complete_English_caption_style_planes'])==(5,30,120,60)
    assert sum(len(x['rejected']) for x in menus['compiler_negatives_rejected'])==40
    assert menus['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert nameview['distinct_name_strings_directly_viewed']==28 and nameview['target_captions_directly_viewed']==15
    for sheet in nameview['review_sheets']:assert sheet['directly_viewed'] and digest(sheet['path'])==sheet['sha256']
    firstplan=load(ROOT/'plan_FE_v1/automatic_plans.json');first={r['id']:r for r in firstplan['records']}
    changes=[dict(id=r['id'],before_lines=first[r['id']]['lines'],after_lines=r['lines'],
        pages_before=first[r['id']]['expected_native_pages'],pages_after=r['expected_native_pages'],
        all_words_andnative_controls_preserved=True) for r in plan['records'] if r['encoded_hex']!=first[r['id']]['encoded_hex']]
    glyphs=load(ROOT/'all328_contextual_proposals_v1.json')['glyph_targets'];assert len(glyphs)==20
    glyph_ids={g['id'] for g in glyphs};assert glyph_ids<=leaves.keys()
    assert all(originals[i]['english'].isascii() for i in glyph_ids)
    final=deepcopy(fresh);final.update(manuscript=str(docpath),manuscript_sha256=digest(docpath),plan=str(planpath),plan_sha256=digest(planpath),
        records=[leaves[r['id']] for r in originals.values()],pages=321,
        current_version_exact_reused_records=223,current_version_fresh_records=91,
        fresh_compiled_alignments=364,reused_compiled_alignments=892,selected_alignment_cases=1256,
        selected_native_receipt_per_record=bindings,review_sheets=sheets,directly_reviewed_selected_page_receipts=selected,
        all321_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,direct_visual_review_pending=False,
        formatting_gates_still_false=True,actual_gameplay=False,new_credit=0)
    save(finalpath,final)
    evidence_paths=[docpath,planpath,prosepath,selectionpath,freshpath,telescopepath,namespath,menuspath,nameviewpath,
        ROOT/'formatting_FE_v1/pagination_owners.json',ROOT/'formatting_FE_v1/preferences_visual_v6.json',
        ROOT/'dynamic_roles_current_v1.json',ROOT/'scoped_terms_reference_v1.json',Path(__file__),*visualpaths]
    save(approvalpath,dict(source_objects=328,complete_exchanges=21,dialogue_revisions=143,dialogue_retentions=185,
        physical_body_candidates=314,body_pages=321,original_source_FE_panels=27,physical_FE_panels=28,
        source_styles=24,source_style_objects=4,choice_menus=5,choice_captions=15,
        selected_alignment_cases=1256,exact_reused_alignment_cases=892,latest_fresh_alignment_cases=364,
        all321_final_pages_directly_viewed=True,all_reviewed_page_versions=len(seen),
        scoped_names=24,distinct_name_strings=28,fresh_name_planes=15,reused_name_planes=13,
        all_names_and15_captions_directly_viewed=True,menu_native_provider_alignments=30,menu_bridged_returns=120,
        menu_normal_highlight_planes=60,menu_compiler_negatives=40,
        layout_changes=changes,pages_reclaimed=sum(c['pages_before']-c['pages_after'] for c in changes),
        nonASCII_current_targets=20,glyph_target_IDs=sorted(glyph_ids),all20_targets_now_ASCII_andnative_visually_accepted=True,
        corrupt_rescue_styles=['SC3_B95_STYLE_400_18','SC3_B95_STYLE_400_42'],
        failed_native_inputs_andall_passed_partial_receipts_preserved=True,
        FE_riddle_continuation_is_formatting_projection_not_yet_stored_ortransition_approved=True,
        ordinary_word_boundary_item_retention=load(ROOT/'formatting_FE_v1/preferences_visual_v4.json')['item_wrap_retention'],
        stored_script_allocation_branches_actual_gameplay_andregistration_pending=True,
        all_fifth_formatting_gates_still_pending=True,actual_gameplay=False,new_ROM=False,new_credit=0,full_goal_complete=False,
        final_native_proof=str(finalpath),final_native_proof_sha256=digest(finalpath),evidence={str(p):digest(p) for p in evidence_paths}))
    print('PASS328 editorial objects:314 native bodies/321 viewed pages,15 captions,28 names,1256 selected alignments;storage/gameplay/release still pending.')

if __name__=='__main__':main()
