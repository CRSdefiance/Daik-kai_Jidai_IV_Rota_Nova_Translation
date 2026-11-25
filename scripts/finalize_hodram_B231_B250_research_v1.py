"""Seal individual v2 gates from exact stored, native, visual and representative evidence."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.approve_hodram_B231_B250_display_v2 import OUT as INPUT,VIEW,ROOT

REBUILT=ROOT/'research_rebuilt_v1/reconstruction.json'
STORED=ROOT/'stored_v1/stored_native_verification.json'
LOOKUP=ROOT/'stored_catalogue_all_v1/all223_stored_effective_body_bindings.json'
LOADERS=ROOT/'loaders_v1/verification.json'
NATIVE=INPUT/'native_pages.json';PLAN=INPUT/'compiled_plans.json';MANUSCRIPT=INPUT/'storage_manuscript.json'
LIVE=ROOT/'actual_pixels_v1/focused_actual_pixels.json'
MENU=ROOT/'actual_menus_band_v1/menu_actual_pixels.json'
NAMES=ROOT/'name_plane_inputs_v1/names.json'
NAME_PLANES=ROOT/'name_planes_v1/native_name_planes.json'
FIXTURE=ROOT/'focused_fixtures_v1/hodram_letters_rose_figurehead_and_survey_fixture.json'
OUT=ROOT/'research_final_v1'
FINAL=Path('translations/hodram_B231_B250_final_review_v1.json')
FINAL_NAMES=Path('translations/hodram_B231_B250_scoped_names_final_v1.json')
READY=OUT/'research_completion.json'

def main():
    assert not any(p.exists() for p in (OUT,FINAL,FINAL_NAMES))
    paths=(REBUILT,STORED,LOOKUP,LOADERS,NATIVE,PLAN,MANUSCRIPT,LIVE,MENU,NAMES,NAME_PLANES,VIEW,FIXTURE,
        ROOT/'actual_menus_band_v1/model_qualification.json')
    rebuilt,stored,lookup,loaders,native,plan,doc,live,menu,names,nameplanes,visual,fixture,model=map(load,paths)
    assert rebuilt['manuscript_sha256']==native['manuscript_sha256']==digest(MANUSCRIPT)
    assert rebuilt['native_sha256']==stored['native_sha256']==digest(NATIVE)
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==digest(REBUILT)
    assert native['plan_sha256']==digest(PLAN) and lookup['stored_sha256']==digest(STORED)
    assert native['runtime']==stored['runtime']==lookup['runtime']==nameplanes['runtime']==names['runtime']
    assert lookup['all223_ordinary_and_style_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['complete_stored_pages'],stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(228,108,120,170)
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(325,36,614)
    assert len(rebuilt['changed_blocks'])==18 and rebuilt['unchanged_control_only_blocks']==[235] and 237 not in rebuilt['reviewed_blocks']
    assert rebuilt['command_count']==359 and rebuilt['relative_sites']==34
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and rebuilt['all_other_files_components_exact']
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256'] and digest(rebuilt['target_archive'])==rebuilt['target_archive_sha256']
    assert visual['final_speech_pages_visually_approved'] and visual['all17_new_native_pages_directly_viewed'] and visual['all_name_andmenu_sheets_directly_viewed']
    assert nameplanes['scoped_actors']==nameplanes['distinct_strings']==len(names['records'])==19
    assert nameplanes['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert live['all_selected_pages_observed_in_exact_fixture_order'] and live['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert (live['frames'],live['selected_utterances'],live['selected_pages'],live['complete_body_planes'],live['complete_header_planes'])==(21521,63,68,144,136)
    assert len(live['review_sheets'])==12 and len(live['observed_source_selectors'])==13
    assert not any(live[k] for k in ('natural_activation','original_location','earned_chronology','full_route','hardware'))
    assert menu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert menu['byte_identical_menu_occurrences_bound_by_exact_source_keys_andordered_surrounding_calls']
    assert {(m['block'],m['source_command_offset'],tuple(m['observed_selected_options'])) for m in menu['menus']}=={(243,674,(0,))}
    assert model['all6_pixel_andcursor_mutations_rejected'] and menu['original_flat_highlight_checker_rejected_preserved']
    sheets=live['review_sheets']+[menu['review_sheet']]
    assert all(digest(s['path'])==s['sha256'] for s in sheets)
    bodies={r['id']:r for r in stored['records']+stored['style_records']}
    captions={r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    layouts={r['id']:r for r in plan['records']};seen={r['id'] for r in live['body_pages']}
    assert len(bodies)==223 and len(captions)==2 and bodies.keys()==layouts.keys() and len(seen)==63
    assert {r['id'] for r in doc['records'] if r.get('source_selector')==254}<=seen
    assert {'DK4_MES_B239_R0039','DK4_MES_B244_R0014','DK4_MES_B248_R0016'}<=seen
    assert sum(r.get('native_object_kind')=='4100-style-alternative' for r in fixture['selected_records'])==2
    blocks=IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    OUT.mkdir();actual_path=OUT/'actual_review.json';visual_path=OUT/'complete_visual_approval.json'
    evidence={str(p):digest(p) for p in (*paths,Path(__file__))}
    save(actual_path,dict(total_frames=21521,initialized_fixture_runs=1,source_speech_variants_observed=63,native_body_pages_observed=68,
        complete_body_planes=144,complete_header_planes=136,observed_source_selectors=live['observed_source_selectors'],
        source_IDs_observed=sorted(seen),offline_only_source_IDs=sorted(bodies.keys()-seen),offline_only_speech_variants=160,
        all_four_FE_panels_FI_expansions_two_voice_objects_andrepresentative_pagination_observed=True,
        source_menu_occurrences_complete_pixel_approved=[dict(block=m['block'],source_command_offset=m['source_command_offset'],stored_command_offset=m['stored_command_offset'],options=m['observed_selected_options'],window=m['occurrence_window']) for m in menu['menus']],
        menus=menu['menus'],cursor_background_model=menu['cursor_background_model'],cursor_model_qualification=str(paths[-1]),
        actual_nondefault_menu_index_andcancellation_unvisited=True,copied_display_sequence_not_original_branch_routing=True,
        original_scene_activation_conditions_battle_transitions_full_catalogue_UI_unvisited=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        evidence=evidence,new_credit=0,guide_photos=False))
    save(visual_path,dict(body_pages=228,body_pages_offline_native_approved=True,observed_pages=68,actual_sheets_directly_viewed=13,
        reviewed_actual_sheets=sheets,all_body_caption_andname_planes_approved=True,all_actual_generated_pages_andrepresentative_menus_directly_viewed=True,
        source_visual_approval=str(VIEW),source_visual_approval_sha256=digest(VIEW),visual_layout_revisions=13,visual_candidate_retentions=9,
        no_QA_waiver=True,evidence=evidence,new_credit=0))
    final=deepcopy(doc)
    for row in final['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        if row['kind']=='typed-choice-label':
            obj,saved=captions[row['id']];at=saved['offset'];raw=bytes.fromhex(saved['stored_hex'])
            ref=dict(command_offset=obj['offset'],source_index=row['source_index'],record_index=saved['record_index'],native_command_word=obj['word'])
        else:
            saved=bodies[row['id']];at=saved['new_offset'];raw=bytes.fromhex(saved['stored_hex']);ref=dict(record_index=saved['new_record_index'])
            if saved.get('virtual_prefix_not_stored'):
                ref.update(command_offset=saved['final_command_offset'],source_style_indices=saved['source_style_indices'],source_header_hex=saved['source_header_hex'],virtual_prefix_not_stored=True)
            else:
                assert blocks[row['block']][at-5:at+1].hex()==row['source_complete_preamble_hex']
                ref.update(header_offset=at-5,complete_source_preamble_hex=row['source_complete_preamble_hex'])
            row['planned_English_markup']=layouts[row['id']]['formatted_markup']
        assert blocks[row['block']][at:at+len(raw)+1]==raw+b'\0'
        row['review']['formatting']=True
        row.update(planned_integrated_reference=dict(file_path=row['file_path'],block=row['block'],offset=at,bytes=len(raw),exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'],**ref),
            actual_utterance_observed_in_disclosed_fixture=row['id'] in seen,fresh_formatting_binding_pending=False,registered_release_andcompletion_credit_pending=True)
    assert Counter(r['decision'] for r in final['records'])=={'revision':115,'retention':110}
    for group in rebuilt['groups']:
        for obj in group['native_objects']:
            rows=[r for r in final['records'] if r['id'] in {v['id'] for v in obj['records']}]
            if obj['word']==0x4100:value=compile_styles(bytes.fromhex(obj['source_hex']),bytes.fromhex(obj['current_hex']),sorted(rows,key=lambda r:r['source_reference']['offset']),layouts)
            else:value=compile_choices(bytes.fromhex(obj['source_hex']),bytes.fromhex(obj['current_hex']),sorted(rows,key=lambda r:r['source_index']))
            assert value.hex()==obj['compiled_hex']
    for row in names['records']:
        row.update(id=f'ACTOR_NAME_{row["actor_ID"]:03d}',speaker='Speaker name or role',
            context='Source-qualified speaker in complete Hodram B231–B250 exchanges; exact contextual IDs remain on this record.',
            source_meaning='Source table components (region metadata is not a surname or biography): '+' '.join(f['text'] for column in (0,8,4) for f in row['clean_fields'] if f['column']==column and f['text']).strip())
        row['review']['formatting']=True
        row.update(actual_header_observed_in_disclosed_fixture=row['actor_ID'] in {int(v) for v in fixture['expected_header_actor_ID_by_selector'].values()},full_catalogue_UI_unvisited=True)
    names.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],all_five_gates_pass_in_scoped_context=True,
        native_rendering_andvisual_review_pending=False,full_catalogue_UI_unvisited=True,no_global207_name_approval=True,no_new_dialogue_credit=True,new_credit=0)
    validate_natural_dialogue_batch(names);save(FINAL_NAMES,names)
    final.update(encoder='dialogue-relocatable-v1',all_individual_five_gates_pass=True,all_individual_fifth_gates_still_pending=False,all_final_display_gates_pending=False,
        scoped_name_review=str(FINAL_NAMES),scoped_name_review_sha256=digest(FINAL_NAMES),formatting_evidence=dict(native=str(NATIVE),stored=str(STORED),catalogue=str(LOOKUP),loaders=str(LOADERS),visual=str(visual_path),actual=str(actual_path)),
        registered_release_andcompletion_credit_pending=True,new_credit=0)
    validate_natural_dialogue_batch(final);save(FINAL,final)
    release_plan=OUT/'release_plans.json';save(release_plan,{**plan,'manuscript':str(FINAL),'manuscript_sha256':digest(FINAL),'exact_all_prose_andcompiled_bytes_unchanged':True})
    save(READY,dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),plan=str(release_plan),plan_sha256=digest(release_plan),all_individual_five_gates_pass=True,
        records=225,revisions=115,retentions=110,body_pages=228,typed_labels=2,scoped_names=19,actual_source_variants=63,actual_pages=68,
        actual_distinct_menu_behaviors=1,offline_only_source_variants=160,registered_integration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**{str(p):digest(p) for p in (FINAL,FINAL_NAMES,release_plan,visual_path,actual_path)}}))
    print('Sealed 225 five-gate reviews, 228 stored pages and 68 observed pages. Registered integration remains.')

if __name__=='__main__':main()
