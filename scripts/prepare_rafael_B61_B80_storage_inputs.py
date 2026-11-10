"""Finalize scoped name research and explicitly bind the absence of compound text objects."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
RUNTIME=Path('work/analysis/Rafael_B61_B80_latest_runtime_20261104')
NAMES=Path('translations/rafael_B61_B80_scoped_names_andterms_v1.json')
PLANES=Path('work/analysis/Rafael_B61_B80_progressive_name_planes_20261104/native_name_planes.json')
FINAL=Path('translations/rafael_B61_B80_scoped_progressive_names_research_final_v1.json')

if __name__=='__main__':
    assert not FINAL.exists() and not (ROOT/'no_menu_objects.json').exists() and not (ROOT/'no_style_objects.json').exists()
    names,planes=map(load,[NAMES,PLANES]);bytext={r['text']:r for r in planes['planes']}
    assert len(names['records'])==22 and len(bytext)==21
    for sheet in planes['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    final=deepcopy(names)
    for row in final['records']:
        plane=bytext[row['english']]
        assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        row['review']['formatting']=True
        row.update(native_plane_reference=dict(path=str(PLANES),sha256=sha(PLANES.read_bytes()),text=row['english']),
            formatting_scope='Original progressive style11 glyphs,complete leading/trailing characters,font pixels andnative bounds;two readable sheets directly viewed. Actual scene header activation remains pending.')
    final.update(format='dk4-scoped-progressive-name-research-final-v1',encoder='dialogue-relocatable-v1',
        runtime=planes['runtime'],all_five_individual_name_gates_pass_in_scoped_research=True,
        all21_strings_directly_viewed=True,actual_scene_headers_unvisited=True,
        source_name_review=str(NAMES),source_name_review_sha256=sha(NAMES.read_bytes()),
        native_name_planes=str(PLANES),native_name_planes_sha256=sha(PLANES.read_bytes()),
        full_catalogue_UI_andglobal207_review_still_open=True,registered_deployment_pending=True,new_credit=0)
    validate_natural_dialogue_batch(final);save(FINAL,final)
    manuscript=ROOT/'formatting_input_v3.json';plan=ROOT/'automatic_v10/automatic_plans.json'
    current_path=RUNTIME/'all539_current_effective_qualified_v1.json';current=load(current_path)
    assert current['runtime']==planes['runtime']
    assert [g['block'] for g in current['groups']]==list(range(61,81))
    assert not any(c['word'] in [0x2100,0x2200,0x4100] for g in current['groups'] for c in g['all_source_commands'])
    assert not any(c['word'] in [0x2100,0x2200,0x4100] for g in current['groups'] for c in g['all_current_commands'])
    digest=sha(manuscript.read_bytes())
    base=dict(runtime=planes['runtime'],manuscript_sha256=digest,source_current_packet=str(current_path),
        source_current_packet_sha256=sha(current_path.read_bytes()),
        explicit_complete_source_current_command_inventory_not_inferred_from_decoded_text=True,new_credit=0)
    save(ROOT/'no_menu_objects.json',dict(**base,menus=[],source_inventory_proves_no2100_or2200_objects=True,
        offline_visual_approved=True,direct_view_pending=False,approval_applies_only_to_empty_scope_no_menu_rendering_claim=True))
    save(ROOT/'no_style_objects.json',dict(**base,objects=[],plan_sha256=sha(plan.read_bytes()),source_inventory_proves_no4100_objects=True))
    save(ROOT/'scoped_name_visual_approval.json',dict(final=str(FINAL),final_sha256=sha(FINAL.read_bytes()),
        all22_source_name_decisions_and21_native_strings_reviewed=True,review_sheets=planes['review_sheets'],
        eleven_fresh_planes_ten_exact_current_ARM9_reuses=True,no_name_data_changes=True,
        no_new_actual_headers_orcatalogue_UI_claim=True,new_credit=0))
    print('22 scoped names/21 native strings visually approved;explicit zero menus/styles bound. Research reconstruction canproceed;actual headers anddialogue fifth gates remain pending.',flush=True)
