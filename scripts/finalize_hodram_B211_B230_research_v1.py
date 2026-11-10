"""Seal individual v2 gates from exact prose, native, stored and representative evidence."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.approve_hodram_B211_B230_display_v1 import OUT as INPUT,VIEW
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT

REBUILT=ROOT/'research_rebuilt_v1/reconstruction.json'
STORED=ROOT/'stored_v1/stored_native_verification.json'
LOOKUP=ROOT/'stored_catalogue_all_v1/all270_stored_effective_body_bindings.json'
LOADERS=ROOT/'loaders_v1/verification.json'
NATIVE=INPUT/'native_pages.json'
PLAN=INPUT/'compiled_plans.json'
MANUSCRIPT=INPUT/'storage_manuscript.json'
LIVE=ROOT/'actual_pixels_v1/focused_actual_pixels.json'
MENU=ROOT/'actual_menus_representative_v3/menu_actual_pixels.json'
NAMES=ROOT/'name_plane_inputs_v1/names.json'
NAME_PLANES=ROOT/'name_planes_v1/native_name_planes.json'
OUT=ROOT/'research_final_v1'
FINAL=Path('translations/hodram_B211_B230_final_review_v1.json')
FINAL_NAMES=Path('translations/hodram_B211_B230_scoped_names_final_v1.json')
READY=OUT/'research_completion.json'

def main():
    assert not any(p.exists() for p in (OUT,FINAL,FINAL_NAMES))
    paths=(REBUILT,STORED,LOOKUP,LOADERS,NATIVE,PLAN,MANUSCRIPT,LIVE,MENU,NAMES,NAME_PLANES,VIEW)
    rebuilt,stored,lookup,loaders,native,plan,doc,live,menu,names,nameplanes,visual=map(load,paths)
    assert rebuilt['manuscript_sha256']==native['manuscript_sha256']==digest(MANUSCRIPT)
    assert rebuilt['native_sha256']==stored['native_sha256']==digest(NATIVE)
    assert stored['reconstruction_sha256']==loaders['reconstruction_sha256']==digest(REBUILT)
    assert native['plan_sha256']==digest(PLAN) and lookup['stored_sha256']==digest(STORED)
    assert native['runtime']==stored['runtime']==lookup['runtime']==nameplanes['runtime']==names['runtime']
    assert lookup['all270_ordinary_and_style_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['complete_stored_pages'],stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(284,126,158,150)
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(325,38,612)
    assert len(rebuilt['changed_blocks'])==19 and rebuilt['unchanged_control_only_blocks']==[222]
    assert rebuilt['command_count']==348 and rebuilt['relative_sites']==30
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and rebuilt['all_other_files_components_exact']
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256'] and digest(rebuilt['target_archive'])==rebuilt['target_archive_sha256']
    assert visual['final_speech_pages_visually_approved'] and visual['all39_new_native_pages_directly_viewed']
    assert visual['all_name_andmenu_sheets_directly_viewed'] and visual['all7_caption_visual_checks_pass']
    assert nameplanes['scoped_actors']==len(names['records'])==23 and nameplanes['distinct_strings']==22
    assert nameplanes['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert live['all_selected_pages_observed_in_exact_fixture_order'] and live['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert (live['frames'],live['selected_utterances'],live['selected_pages'],live['complete_body_planes'],live['complete_header_planes'])==(23441,65,74,156,148)
    assert len(live['review_sheets'])==13 and len(live['observed_source_selectors'])==14
    assert not any(live[k] for k in ('natural_activation','original_location','earned_chronology','full_route','hardware'))
    assert menu['byte_identical_menu_occurrences_bound_by_exact_source_keys_andordered_surrounding_calls']
    assert menu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert {(m['block'],m['source_command_offset'],tuple(m['observed_selected_options'])) for m in menu['menus']}=={(216,64,(0,)),(216,230,(0,))}
    sheets=live['review_sheets']+[menu['review_sheet']]
    assert all(digest(s['path'])==s['sha256'] for s in sheets)
    bodies={r['id']:r for r in stored['records']+stored['style_records']}
    captions={r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    layouts={r['id']:r for r in plan['records']}
    assert len(bodies)==270 and len(captions)==7 and bodies.keys()==layouts.keys()
    seen={r['id'] for r in live['body_pages']};assert len(seen)==65
    assert {r['id'] for r in doc['records'] if r.get('source_selector')==254}<=seen
    assert 'DK4_MES_B215_R0040' in seen
    blocks=IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    OUT.mkdir()
    actual_path=OUT/'actual_review.json';visual_path=OUT/'complete_visual_approval.json'
    evidence={str(p):digest(p) for p in (*paths,Path(__file__))}
    save(actual_path,dict(total_frames=23441,initialized_fixture_runs=1,source_speech_variants_observed=65,native_body_pages_observed=74,
        complete_body_planes=156,complete_header_planes=148,observed_source_selectors=live['observed_source_selectors'],
        source_IDs_observed=sorted(seen),offline_only_source_IDs=sorted(bodies.keys()-seen),offline_only_speech_variants=205,
        all_four_FE_panels_FI_expansion_four_voice_objects_andrepresentative_pagination_observed=True,
        source_menu_occurrences_complete_pixel_approved=[dict(block=m['block'],source_command_offset=m['source_command_offset'],options=m['observed_selected_options'],window=m['occurrence_window']) for m in menu['menus']],
        repeated_B224_yes_no_menu=dict(source_command_offset=138,stored_source_bytes_andnative_providers_exact=True,
            representative_identical_object='SC1 B216 command 64',complete_occurrence_highlight_background_credit=False,
            reason='The original matcher assigned the first identical menu capture to both source keys. Reject that occurrence claim. The second window has readable complete glyphs but only transition-state background samples; its independently checked stored object is byte-identical to the qualified representative. Ordered dialogue after it is observed; no further animation investigation is needed for unchanged menu behavior.'),
        rejected_menu_receipt=str(ROOT/'actual_menus_v1/menu_actual_pixels.json'),
        distinct_three_choice_full_names_complete=True,actual_nondefault_menu_indices_andcancellation_unvisited=True,
        copied_display_sequence_not_original_branch_routing=True,original_scene_activation_conditions_andbattle_transitions_unvisited=True,
        full_catalogue_UI_unvisited=True,natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        evidence=evidence,new_credit=0,guide_photos=False))
    save(visual_path,dict(body_pages=284,body_pages_offline_native_approved=True,observed_pages=74,actual_sheets_directly_viewed=14,
        reviewed_actual_sheets=sheets,all_body_caption_andname_planes_approved=True,all_actual_generated_pages_andrepresentative_menus_directly_viewed=True,
        source_visual_approval=str(VIEW),source_visual_approval_sha256=digest(VIEW),
        visual_layout_revisions=27,visual_candidate_retentions=4,separate_FE_wrap_fix=1,
        exact_QA_line_ending_retention=visual['exact_QA_line_ending_retention'],evidence=evidence,new_credit=0))
    final=deepcopy(doc)
    for row in final['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        if row['kind']=='typed-choice-label':
            obj,saved=captions[row['id']];at=saved['offset'];raw=bytes.fromhex(saved['stored_hex'])
            ref=dict(command_offset=obj['offset'],source_index=row['source_index'],record_index=saved['record_index'],native_command_word=obj['word'])
        else:
            saved=bodies[row['id']];at=saved['new_offset'];raw=bytes.fromhex(saved['stored_hex'])
            ref=dict(record_index=saved['new_record_index'])
            if saved.get('virtual_prefix_not_stored'):
                ref.update(command_offset=saved['final_command_offset'],source_style_indices=saved['source_style_indices'],source_header_hex=saved['source_header_hex'],virtual_prefix_not_stored=True)
            else:
                assert blocks[row['block']][at-5:at+1].hex()==row['source_complete_preamble_hex']
                ref.update(header_offset=at-5,complete_source_preamble_hex=row['source_complete_preamble_hex'])
            row['planned_English_markup']=layouts[row['id']]['formatted_markup']
        assert blocks[row['block']][at:at+len(raw)+1]==raw+b'\0'
        row['review']['formatting']=True
        row.update(planned_integrated_reference=dict(file_path=row['file_path'],block=row['block'],offset=at,bytes=len(raw),
            exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'],**ref),
            actual_utterance_observed_in_disclosed_fixture=row['id'] in seen,fresh_formatting_binding_pending=False,
            registered_release_andcompletion_credit_pending=True)
        if row['id']=='DK4_MES_B229_R0036':
            retention=visual['exact_QA_line_ending_retention']['QA_line_ending_retention']
            row.update(qa_waivers=['weak-line-ending'],qa_waiver_reason=retention['reason'],exact_QA_line_ending_retention=retention)
    assert Counter(r['decision'] for r in final['records'])=={'revision':170,'retention':107}
    compiled={r['id']:r for r in plan['records']}
    for group in rebuilt['groups']:
        for obj in group['native_objects']:
            rows=[r for r in final['records'] if r['id'] in {r['id'] for r in obj['records']}]
            if obj['word']==0x4100:
                value=compile_styles(bytes.fromhex(obj['source_hex']),bytes.fromhex(obj['current_hex']),sorted(rows,key=lambda r:r['source_reference']['offset']),compiled)
            else:value=compile_choices(bytes.fromhex(obj['source_hex']),bytes.fromhex(obj['current_hex']),sorted(rows,key=lambda r:r['source_index']))
            assert value.hex()==obj['compiled_hex']
    for row in names['records']:
        row['review']['formatting']=True
        row.update(actual_header_observed_in_disclosed_fixture=row['actor_ID'] in {int(k) for k in load(ROOT/'focused_fixtures_v2/hodram_letters_swan_town_and_choices_fixture.json')['expected_header_actor_ID_by_selector'].values()},full_catalogue_UI_unvisited=True)
    names.update(encoder='dialogue-relocatable-v1',all_five_gates_pass_in_scoped_context=True,native_rendering_andvisual_review_pending=False,
        full_catalogue_UI_unvisited=True,no_global207_name_approval=True,no_new_dialogue_credit=True,new_credit=0)
    validate_natural_dialogue_batch(names);save(FINAL_NAMES,names)
    final.update(encoder='dialogue-relocatable-v1',all_individual_five_gates_pass=True,all_individual_fifth_gates_still_pending=False,
        all_final_display_gates_pending=False,scoped_name_review=str(FINAL_NAMES),scoped_name_review_sha256=digest(FINAL_NAMES),
        formatting_evidence=dict(native=str(NATIVE),stored=str(STORED),catalogue=str(LOOKUP),loaders=str(LOADERS),visual=str(visual_path),actual=str(actual_path)),
        registered_release_andcompletion_credit_pending=True,new_credit=0)
    validate_natural_dialogue_batch(final);save(FINAL,final)
    release_plan=OUT/'release_plans.json';save(release_plan,{**plan,'manuscript':str(FINAL),'manuscript_sha256':digest(FINAL),'exact_all_prose_andcompiled_bytes_unchanged':True})
    save(READY,dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),plan=str(release_plan),plan_sha256=digest(release_plan),
        all_individual_five_gates_pass=True,records=277,revisions=170,retentions=107,body_pages=284,typed_labels=7,scoped_names=23,
        actual_source_variants=65,actual_pages=74,actual_distinct_menu_behaviors=2,offline_only_source_variants=205,
        registered_integration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**{str(p):digest(p) for p in (FINAL,FINAL_NAMES,release_plan,visual_path,actual_path)}}))
    print('Sealed 277 individual five-gate reviews, 284 stored pages and 74 observed emulator pages. Registered integration pending.')

if __name__=='__main__':main()
