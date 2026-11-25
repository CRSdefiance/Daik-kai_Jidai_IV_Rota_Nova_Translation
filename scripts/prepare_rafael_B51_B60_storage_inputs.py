"""Bind completed body/menu/name display decisions to the current mixed-block rebuild."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

RUNTIME=Path('work/analysis/Rafael_B51_B60_current_runtime_20261104')
DISPLAY=Path('work/analysis/Rafael_B51_B60_formatting_20261104')
NAME_PLANES=Path('work/analysis/Rafael_B51_B60_progressive_name_planes_20261104/native_name_planes.json')
NAMES=Path('translations/rafael_B51_B60_scoped_progressive_names_v1.json')
FINAL_NAMES=Path('translations/rafael_B51_B60_scoped_progressive_names_final_v1.json')

if __name__=='__main__':
    assert not FINAL_NAMES.exists() and not (RUNTIME/'compatible_menu_objects.json').exists()
    manuscript=RUNTIME/'formatting_input.json';plan_path=RUNTIME/'compatible_plans.json'
    doc,plan,qual,names,planes=map(load,[manuscript,plan_path,RUNTIME/'dependency_qualification.json',NAMES,NAME_PLANES])
    assert names['runtime']==planes['runtime']==qual['runtime']
    assert len(planes['planes'])==17 and planes['scoped_actors']==18
    for sheet in planes['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    final=deepcopy(names);by_text={p['text']:p for p in planes['planes']}
    for row in final['records']:
        assert row['english'] in by_text and by_text[row['english']]['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        row['review']['formatting']=True
        if row['actor_ID'] in [114,116]:row['source_meaning']='A familiar older man at the port office; no family relationship is established.'
        elif row['actor_ID']==84:row['source_meaning']='The shop owner in the town square.'
        elif row['actor_ID']==151:row['source_meaning']='An anonymous subordinate in these crew exchanges.'
        else:row['source_meaning']='Source-defined progressive given-name/surname identity: '+row['english']+'.'
        row.update(native_plane_reference=dict(path=str(NAME_PLANES),sha256=sha(NAME_PLANES.read_bytes()),text=row['english']),
            formatting_scope='Complete style11 native name glyphs and bounds; two legible sheets directly viewed. Actual scene header activation remains pending.')
    final.update(format='dk4-scoped-progressive-name-final-v1',encoder='dialogue-relocatable-v1',
        all_five_individual_gates_pass_in_scoped_research=True,all17_strings_directly_viewed=True,
        Fernan_rebased_proposal=str(RUNTIME/'Fernan_owned_fields_proposal.json'),
        source_name_review=str(NAMES),source_name_review_sha256=sha(NAMES.read_bytes()),
        native_name_planes=str(NAME_PLANES),native_name_planes_sha256=sha(NAME_PLANES.read_bytes()),
        full_catalogue_UI_andglobal207_review_still_open=True,registered_deployment_pending=True,new_credit=0)
    validate_natural_dialogue_batch(final);save(FINAL_NAMES,final)
    choices_path=DISPLAY/'two_choices_native_v1/complete_choice_objects.json';choices=load(choices_path);menus=[]
    for item in choices['objects']:
        proof=load(item['receipt']);assert sha(Path(item['receipt']).read_bytes())==item['receipt_sha256']
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and len(proof['compiler_negatives_rejected'])==7
        rows=sorted([r for r in doc['records'] if r.get('kind')=='typed-choice-label' and r['source_command_offset']==item['source_command_offset']],key=lambda r:r['source_index'])
        source,current=map(bytes.fromhex,[rows[0]['source_choice_object_hex'],rows[0]['current_choice_object_hex']])
        compiled=compile_choices(source,current,rows,require_formatting=False)
        assert compiled==Path(item['compiled_path']).read_bytes() and compiled.hex()==proof['native_choice_object_hex']
        menus.append(dict(block=item['block'],source_command_offset=item['source_command_offset'],target_object_hex=compiled.hex(),
            source_native_receipt=item['receipt'],source_native_receipt_sha256=item['receipt_sha256'],
            current_4b10fd67_code_font_andinput_dependency_reuse=str(RUNTIME/'dependency_qualification.json')))
    digest=sha(manuscript.read_bytes())
    save(RUNTIME/'compatible_menu_objects.json',dict(runtime=qual['runtime'],manuscript=str(manuscript),manuscript_sha256=digest,
        menus=menus,offline_visual_approved=True,direct_view_pending=False,
        no_new_provider_planes_oractual_controller_execution_claim=True,
        previous_menu_proof=str(choices_path),previous_menu_proof_sha256=sha(choices_path.read_bytes()),
        exact_dependency_qualification=str(RUNTIME/'dependency_qualification.json'),new_credit=0))
    packet=load(RUNTIME/'current_effective.json')
    assert not any(c['word']==16640 for g in packet['groups'] for c in g['all_source_commands'])
    save(RUNTIME/'no_style_objects.json',dict(runtime=qual['runtime'],manuscript_sha256=digest,plan_sha256=sha(plan_path.read_bytes()),
        objects=[],source_inventory_proves_no4100_objects=True,new_credit=0))
    save(RUNTIME/'scoped_name_visual_approval.json',dict(final=str(FINAL_NAMES),final_sha256=sha(FINAL_NAMES.read_bytes()),
        all18_source_name_decisions_and17_native_strings_reviewed=True,review_sheets=planes['review_sheets'],
        seventeen_retentions_one_glyph_revision_not_dialogue_credit=True,no_new_actual_headers_orcatalogue_UI_claim=True,new_credit=0))
    print('18 scoped names pass five research gates;2 complete menus andexplicit zero style objects bound to current storage inputs.')
