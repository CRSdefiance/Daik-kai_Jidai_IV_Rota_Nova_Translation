"""Assemble all final offline display proofs without advancing editorial credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import CURRENT, OBJECTS, PROSE, ROOT, STAGED, TWO_MENUS, digest
from scripts.refine_rafael_B201_B220_wraps_v2 import OUT as MANUSCRIPT


OUT = ROOT/'offline_display_package_v1'
PLAN = ROOT/'ordinary_plans_v4/automatic_plans.json'
NATIVE = [ROOT/f'{name}/compiled_native_pages.json' for name in (
    'ordinary_native_v1','ordinary_native_delta_v1','ordinary_native_delta_v2')]
STAGES = [
    (STAGED,ROOT/'staged_FE_native_v1/staged_display.json'),
    (ROOT/'source_staged_parrot_FE_inputs_v1.json',ROOT/'staged_parrot_FE_native_v1/staged_display.json'),
]
TWO = ROOT/'two_choice_native_v1/complete_choice_objects.json'
THREE = ROOT/'three_choice_native_v1/menu_provider_and_planes.json'
NAMES = ROOT/'scoped_name_planes_v1/native_name_planes.json'
CAPTION_SHEETS = ROOT/'caption_visual_sheets_v1/sheet_index.json'


def main():
    assert not OUT.exists()
    context,manifest,plan,current,objects,names = map(load,(PROSE,MANUSCRIPT,PLAN,CURRENT,OBJECTS,NAMES))
    runtime=context['runtime']
    assert all(doc['runtime']==runtime for doc in (manifest,current,objects,names))
    assert (names['scoped_actors'],names['distinct_strings'])==(41,29)
    assert not plan['failures'] and plan['manuscript_sha256']==digest(MANUSCRIPT)
    for entry in plan['records']:
        assert all(issue['severity']=='info' for issue in entry['base_QA']['issues'])
    source_rows={r['id']:r for r in context['records']}
    rows={r['id']:r for r in manifest['records']}
    plans={r['id']:r for r in plan['records']}
    plain=list(map(load,NATIVE))
    assert [(len(doc['records']),doc['pages']) for doc in plain]==[(381,382),(11,13),(2,2)]
    assert len({doc['font_sha256'] for doc in plain})==1
    selected={}
    for doc in plain:
        assert doc['runtime']==runtime and not doc['actual_gameplay']
        assert doc['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert doc['complete_consumption_andpagination_exact'] and doc['FE_actual_glyph_row_membership_checked']
        selected.update({r['id']:r for r in doc['records']})
    assert selected.keys()==plans.keys()
    for ident,entry in plans.items():
        assert selected[ident]['compiled_hex']==entry['encoded_hex']
    for staged_path,native_path in STAGES:
        staged,native=map(load,(staged_path,native_path))
        assert staged['runtime']==native['runtime']==runtime and not native['failed']
        row,=staged['records']
        proof,=native['records']
        ident=row['id']
        assert ident==proof['id'] and row['english']==proof['logical_English']
        assert proof['all_visible_row_origins_and_full_glyphs_exact']
        assert len(proof['native_macro_alignments']['cases'])==4
        assert digest(Path(proof['plane']))==proof['plane_sha256']
        assert digest(Path(proof['logical_plane']))==proof['logical_plane_sha256']
        png=Path(proof['plane']).with_suffix('.png')
        display={**proof['complete_native_English_display'],'native_plane':proof['plane'],
            'native_plane_sha256':proof['plane_sha256'],'native_logical_plane':proof['logical_plane'],
            'native_logical_plane_sha256':proof['logical_plane_sha256'],'preview':str(png),'preview_sha256':digest(png),
            'planned_native_row_comparison':dict(complete_glyph_row_membership_exact=True,
                complete_visible_row_origins_exact=True,planned_visible_rows=proof['planned_visible_rows'])}
        rows[ident]={**row,'source_staging_reason':proof['source_staging_reason']}
        selected[ident]=dict(id=ident,block=row['block'],kind='system-FE',source_reference=row['source_reference'],
            current_reference=row['current_reference'],compiled_hex=proof['encoded_hex'],expanded_native_hex=proof['expanded_hex'],
            logical_English=row['english'],native_alignment=proof['native_macro_alignments'],
            complete_native_English_display=display,source_staged_FE=True)
        plans[ident]=dict(id=ident,source_hex=row['source_hex'],block=row['block'],source_selector=254,
            source_record_index=row['source_record_index'],kind='system-FE',logical_English=row['english'],
            encoded_hex=proof['encoded_hex'],formatted_markup=row['planned_English_markup'],expected_native_pages=1,
            source_staged_FE=True,approved_native_structural_layout=proof['planned_visible_rows'],
            base_QA=dict(issues=[],native_staged_consumer_exact=True),original_usable_width_px=228)
    assert len(rows)==len(source_rows)==403 and len(plans)==len(selected)==382
    assert rows.keys()==source_rows.keys()
    page_count=0
    for ident,row in rows.items():
        assert all(row[k]==source_rows[ident][k] for k in ('source_reference','current_reference','source_hex','current_hex','review'))
        assert row['editorial_logical_English']==source_rows[ident]['english'] or row['visual_revision_previous_English']==source_rows[ident]['english']
        if row['kind']=='typed-choice-label':
            continue
        proof=selected[ident]
        assert all(row[k]==proof[k] for k in ('source_reference','current_reference','kind'))
        assert row['english']==proof['logical_English']==plans[ident]['logical_English']
        display=proof['complete_native_English_display']
        pages=[display] if row['kind']=='system-FE' else display['pages']
        assert len(pages)==plans[ident]['expected_native_pages']
        assert all(digest(Path(page['native_plane']))==page['native_plane_sha256'] for page in pages)
        page_count+=len(pages)
    assert page_count==383 and sum(r['kind']=='system-FE' for r in rows.values())==34
    assert not objects['style_objects']
    assert sum(c['word']==0x2000 for g in current['groups'] for c in g['all_source_commands'])==1
    assert sum(c['word']==0x2100 for g in current['groups'] for c in g['all_source_commands'])==9
    assert sum(c['word']==0x2200 for g in current['groups'] for c in g['all_source_commands'])==1
    menus=[]
    two,three=map(load,(TWO,THREE))
    for entry in two['objects']:
        receipt=Path(entry['receipt'])
        proof=load(receipt)
        assert proof['runtime']==runtime and digest(receipt)==entry['receipt_sha256']
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        path=Path(entry['compiled_path'])
        assert digest(path)==entry['compiled_sha256']
        menus.append(dict(block=entry['block'],source_command_offset=entry['source_command_offset'],
            record_IDs=entry['record_ids'],target_object_hex=path.read_bytes().hex(),source_word=0x2100,
            native_receipt=str(receipt),native_receipt_sha256=digest(receipt)))
    assert {(r['block'],r['source_command_offset']) for r in menus}==TWO_MENUS
    assert three['runtime']==runtime and three['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert len(three['menus'])==1 and (three['menus'][0]['block'],three['menus'][0]['source_command_offset'])==(209,230)
    menus.append({**three['menus'][0],'source_word':0x2200,'native_receipt':str(THREE),'native_receipt_sha256':digest(THREE)})
    assert sorted(ident for menu in menus for ident in menu['record_IDs'])==sorted(
        row['id'] for row in rows.values() if row['kind']=='typed-choice-label')
    assert load(CAPTION_SHEETS)['caption_style_planes']==42
    ids=list(source_rows)
    body_ids=[ident for ident in ids if ident in plans]
    evidence={str(path):digest(path) for path in (PROSE,MANUSCRIPT,PLAN,CURRENT,OBJECTS,*NATIVE,
        *(p for pair in STAGES for p in pair),TWO,THREE,NAMES,CAPTION_SHEETS,Path(__file__))}
    OUT.mkdir()
    mf,pl,na=[OUT/f'{name}.json' for name in ('formatting_manuscript','automatic_plans','compiled_native_pages')]
    save(mf,{**manifest,'records':[rows[ident] for ident in ids],'physical_speech_objects':382,
        'ordinary_speech_objects':382,'typed_choice_objects':21,'source_staged_FE_panels':2,
        'compiled_layouts_use_native_structural_anchors_only':True,'evidence':evidence})
    shared=dict(manuscript=str(mf),manuscript_sha256=digest(mf),runtime=runtime,new_credit=0)
    save(pl,{**plan,**shared,'records':[plans[ident] for ident in body_ids],'pages':page_count,'evidence':evidence})
    shared.update(plan=str(pl),plan_sha256=digest(pl))
    save(na,{**plain[0],**shared,'records':[selected[ident] for ident in body_ids],'pages':page_count,
        'review_sheets':[],'body_sheet_generation_pending':True,'selected_compiled_alignments':382*4,
        'fresh_compiled_alignments_total_across_retained_attempts':(381+11+2+2)*4,'evidence':evidence})
    save(OUT/'menu_before_visual.json',{**shared,'offline_visual_approved':False,'direct_view_pending':True,
        'menus':menus,'typed_labels':21,'caption_planes':42})
    save(OUT/'styles.json',{**shared,'objects':[],'complete_clean_current_census_proves_no4100_objects':True})
    print('Assembled',page_count,'exact final body pages, 21 captions, 41 actor labels. Direct body review pending.')


if __name__ == '__main__':
    main()

