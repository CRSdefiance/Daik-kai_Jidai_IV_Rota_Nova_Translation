"""Seal the 187 directly reviewed offline pages and exact inputs for reconstruction."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B166_B167_ordinary_v1 import CURRENT, ROOT

OUT=ROOT/'offline_display_package_v1'
PROSE=Path('translations/rafael_B166_B167_contextual_review_v5.json')
PLAIN=ROOT/'ordinary_formatting_manuscript_v4.json'
STAGED=ROOT/'source_staged_FE_inputs_v2.json'
FINAL_PLAN=ROOT/'ordinary_plans_v10/automatic_plans.json'
PLAIN_NATIVE=[ROOT/f'{name}/compiled_native_pages.json' for name in (
    'ordinary_native_v1','ordinary_wrap_delta_native_v1','ordinary_wrap_delta_native_v2')]
STAGED_NATIVE=ROOT/'staged_FE_native_v7/staged_display.json'
NAME_NATIVE=ROOT/'name_planes_v1/native_name_planes.json'


def digest(p):
    return sha(Path(p).read_bytes())


def main():
    assert not OUT.exists()
    manuscript,ordinary,staged,ordinary_plan,staged_display,names,current=map(load,
        (PROSE,PLAIN,STAGED,FINAL_PLAN,STAGED_NATIVE,NAME_NATIVE,CURRENT))
    rt=manuscript['runtime']
    assert all(p['runtime']==rt for p in (ordinary,staged,staged_display,names,current))
    assert staged['manuscript_sha256']==digest(PROSE)
    assert ordinary_plan['manuscript_sha256']==digest(PLAIN)
    assert all(c['word'] not in (0x2100,0x2200,0x4100) for g in current['groups'] for c in g['all_source_commands'])
    assert not ordinary_plan['failures'] and all(i['severity'] not in ('warning','error')
        for r in ordinary_plan['records'] for i in r['base_QA']['issues'])
    plain_displays=list(map(load,PLAIN_NATIVE))
    selected={}
    sheets=[]
    for proof in plain_displays:
        assert proof['runtime']==rt
        assert proof['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert proof['complete_consumption_andpagination_exact'] and proof['FE_actual_glyph_row_membership_checked']
        for r in proof['records']:
            selected[r['id']]=r
        sheets.extend(proof['review_sheets'])
    assert [(len(d['records']),d['pages']) for d in plain_displays]==[(164,165),(24,25),(2,3)]
    assert len(selected)==len(ordinary_plan['records'])==164
    for r in ordinary_plan['records']:
        assert selected[r['id']]['compiled_hex']==r['encoded_hex']
    assert len(staged_display['records'])==22 and not staged_display['failed']
    assert names['scoped_actors']==names['distinct_strings']==24 and names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    sheets.extend(staged_display['review_sheets'])
    sheets.extend(names['review_sheets'])
    assert len(sheets)==24 and all(digest(s['path'])==s['sha256'] for s in sheets)
    source={r['id']:r for r in manuscript['records']}
    rows=sorted(ordinary['records']+staged['records'],key=lambda r:(r['block'],r['source_reference']['offset']))
    assert len(rows)==len(source)==186
    for r in rows:
        original=source[r['id']]
        assert r['editorial_logical_English']==original['english']
        assert all(r[k]==original[k] for k in ['source_reference','current_reference','source_hex','current_hex','review'])
    plans={r['id']:r for r in ordinary_plan['records']}
    staged_rows={r['id']:r for r in staged['records']}
    for proof in staged_display['records']:
        ident=proof['id'];row=staged_rows[ident]
        assert row['english']==proof['logical_English']
        assert proof['all_visible_row_origins_and_full_glyphs_exact']
        assert digest(proof['plane'])==proof['plane_sha256'] and digest(proof['logical_plane'])==proof['logical_plane_sha256']
        assert len(proof['native_macro_alignments']['cases'])==4
        display={**proof['complete_native_English_display'],'native_plane':proof['plane'],
            'native_plane_sha256':proof['plane_sha256'],'native_logical_plane':proof['logical_plane'],
            'native_logical_plane_sha256':proof['logical_plane_sha256'],
            'planned_native_row_comparison':dict(complete_glyph_row_membership_exact=True,
                complete_visible_row_origins_exact=True,planned_visible_rows=proof['planned_visible_rows'])}
        selected[ident]=dict(id=ident,block=166,kind='system-FE',source_reference=row['source_reference'],
            current_reference=row['current_reference'],compiled_hex=proof['encoded_hex'],
            expanded_native_hex=proof['expanded_hex'],logical_English=row['english'],native_alignment=proof['native_macro_alignments'],
            complete_native_English_display=display,source_staged_FE=True)
        plans[ident]=dict(id=ident,source_hex=row['source_hex'],block=166,source_selector=254,
            source_record_index=row['source_record_index'],kind='system-FE',logical_English=row['english'],
            encoded_hex=proof['encoded_hex'],formatted_markup=row['planned_English_markup'],
            expected_native_pages=1,source_staged_FE=True,approved_native_structural_layout=proof['planned_visible_rows'],
            base_QA=dict(issues=[],native_staged_consumer_exact=True),original_usable_width_px=228)
    assert len(selected)==len(plans)==186
    for r in rows:
        proof=selected[r['id']]
        assert proof['logical_English']==r['english'] and proof['source_reference']==r['source_reference'] and proof['current_reference']==r['current_reference']
        display=proof['complete_native_English_display']
        pages=[display] if r['kind']=='system-FE' else display['pages']
        assert len(pages)==plans[r['id']]['expected_native_pages']
        assert all(digest(p['native_plane'])==p['native_plane_sha256'] for p in pages)
    OUT.mkdir()
    mf,pl,na=[OUT/f'{k}.json' for k in ('formatting_manuscript','automatic_plans','compiled_native_pages')]
    save(mf,{**manuscript,'records':rows,'physical_speech_objects':186,'ordinary_speech_objects':186,
        'typed_choice_objects':0,'source_staged_FE_panels':22,'compiled_layouts_use_native_structural_anchors_only':True})
    save(pl,{**ordinary_plan,'manuscript':str(mf),'manuscript_sha256':digest(mf),
        'records':[plans[r['id']] for r in rows],'pages':187,'exact_staged_FE_proof':str(STAGED_NATIVE)})
    evidence={str(p):digest(p) for p in (PROSE,PLAIN,STAGED,FINAL_PLAN,*PLAIN_NATIVE,STAGED_NATIVE,NAME_NATIVE,CURRENT,Path(__file__))}
    save(na,{**plain_displays[0],'manuscript':str(mf),'manuscript_sha256':digest(mf),'plan':str(pl),'plan_sha256':digest(pl),
        'records':[selected[r['id']] for r in rows],'pages':187,'review_sheets':sheets[:-2],
        'fresh_compiled_alignments':744,'direct_visual_review_pending':False,'evidence':evidence})
    shared=dict(manuscript=str(mf),manuscript_sha256=digest(mf),plan=str(pl),plan_sha256=digest(pl),
        runtime=rt,new_credit=0)
    save(OUT/'menu.json',{**shared,'offline_visual_approved':True,'direct_view_pending':False,'menus':[],'typed_labels':0,
        'complete_clean_current_census_proves_no_choice_objects':True})
    save(OUT/'styles.json',{**shared,'objects':[],'complete_clean_current_census_proves_no4100_objects':True})
    save(OUT/'visual_review.json',{**shared,'native':str(na),'native_sha256':digest(na),'body_pages':187,
        'scoped_name_count':24,'source_staged_FE_pages':22,'all_body_and_name_sheets_directly_viewed':True,
        'all_final_direct_visual_findings_resolved':True,'actual_gameplay':False,'sheets':sheets,
        'source_only_actor8_contextual_header_risk_pending':True,'stored_branch_loader_and_gameplay_checks_pending':True,
        'names':str(NAME_NATIVE),'names_sha256':digest(NAME_NATIVE),'evidence':evidence})
    print('Sealed 186 exact bodies, 187 pages and 24 default nameplates. All fifth gates remain pending stored and focused gameplay checks.')


if __name__=='__main__':
    main()
