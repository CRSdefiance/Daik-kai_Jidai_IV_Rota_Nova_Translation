"""Reconcile reusable actual display evidence and distinct current native tests."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_shrines_research_v3194 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Shrines_Temples_sampling_v3198')
DOC=Path('translations/lil_shrines_temples_editorial_manuscript_v7.json')
CONTROL=Path('work/analysis/lil_Shrines_Temples_relocated_controls_v3197/all220_dispatch16_style_commands3312_getters21_predicate_pairs.json')
REFERENCE=Path('work/analysis/lil_Shrines_Temples_reference_census_v3196/all421_commands114_relative_sites_and_shipped_entry_census.json')
PADDING=Path('work/analysis/lil_Shrines_Temples_research_v3194/research_image_receipt.json')
HISTORY=Path('work/analysis/lil_Seville_sampling_v2721b/representative_rule_reconciliation.json')
START=Path('work/analysis/lil_Crew_Items_startup_v3147/cold_boot_Lil_startup_town_verification.json')
FE=Path('work/analysis/lil_Shrines_Temples_FE_v3184/current_FE_macro_font_and_typed_paper_proof.json')
MENU=Path('work/analysis/lil_Shrines_Temples_choices_v3188/all5_typed_menu_native_proof.json')
MARGINS=Path('work/analysis/lil_Speyer_choice_calibration_v1939/original_current_menu_fixed_margin_calibration.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,control,reference,padding,history,start,plan,fe,menus,margins=map(read,[DOC,CONTROL,REFERENCE,PADDING,HISTORY,START,PLAN,FE,MENU,MARGINS])
    parent,image,historical=[NdsImage.open(p) for p in [PARENT,ROM,history['candidate']]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==start['candidate_sha256']
    assert sha(ROM.read_bytes())==reference['research_ROM_sha256']==control['research_ROM_sha256']==padding['research_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')==historical.read_file('/__arm9__.bin')
    for path in ['/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:
        assert image.read_file(path)==parent.read_file(path)==historical.read_file(path)
    current_blocks,old_blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,historical]]
    for n in [22,74]:assert current_blocks[n]==old_blocks[n]
    assert history['all4_historical_progressive_holds_freshly_match_current_full_ink_gray_blank_masks']
    assert history['historical_B74_whole_source_block_equal_current']
    assert history['original_presenter_return_choice_VM_and_text_render_spans_historical_current_exact']
    assert history['no_open_translation_specific_display_or_control_finding']
    assert start['all_current_requested_and_final_framebuffers_equal_V3103'] and start['current_Lil_captain2_and_B22_payload_verified']
    assert padding['all220_final_targets_complete_native_planes_equal_reviewed_planes']
    assert padding['current_final_padded_macro_alignment_cases']==880
    assert control['all220_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text']
    assert control['all3312_pointer_cases_and_all_source_alias_groups_preserved']
    assert control['all21_current_relocated_predicate_results_and_source_operands_equal']
    assert len(control['relocated_predicate_pairs'])==21 and control['original_event_queries']==[]
    assert fe['all30_one_native_page_consumes_complete_target']
    assert fe['all30_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask']
    assert menus['native_selection_cancel_cases']==40 and menus['complete_current_and_reviewed_style_label_planes']==60
    assert margins['calibrated_only_from_original_menu_before_revised_pixels']
    assert (margins['margin_x'],margins['margin_y'],margins['row_height'])==(16,12,20)
    three_option=[]
    for m in menus['menus']:
        assert sha(Path(m['proof']).read_bytes())==m['sha256']
        proof=read(m['proof']);spec=next(b for b in plan['blocks'] if b['block']==m['block'])
        obj=next(c for c in spec['choice_commands'] if c['old_offset']==m['command_offset'])
        target=next(c for c in proof['current_and_reviewed_VM_and_font_cases'] if c['version']=='reviewed-research')
        assert target['object_hex']==obj['target_hex'] and obj['text_base']==8 and obj['count']==3
        vm=target['native_VM_getters_geometry_and_selection']
        assert [c['modal_selection'] for c in vm['VM_cases']]==[0,1,2,-1]
        rect=vm['native_menu_rectangle'];width=target['source_derived_text_canvas_width']
        assert rect[2]-rect[0]==width+32 and rect[3]-rect[1]==3*20+24
        assert 0<=rect[0]<rect[2]<=256 and 0<=rect[1]<rect[3]<=192
        assert rect[0]+rect[2]==256 and rect[1]+rect[3]==192
        row_origins=[]
        for i in range(3):
            left,top=rect[0]+16,rect[1]+12+i*20
            assert rect[0]<=left and left+width<=rect[2]
            assert rect[1]<=top and top+20<=rect[3]
            row_origins.append([left,top])
        assert all(p['storage_padding_all_blank'] and p['independent_complete_native_pixels_match'] and p['visible_cell_center_twice']==width for p in target['all_six_style_label_planes'])
        three_option.append(dict(block=m['block'],old_command_offset=m['command_offset'],new_command_offset=obj['new_offset'],
            native_rectangle=rect,text_canvas_width=width,three_row_origins=row_origins,
            original_count3_VM_third_result_cancel_and_all6_full_label_planes_pass=True,
            exact_relocated_object_matches_tested_native_object=True,
            calibrated_actual_two_option_row_margins_inherited_by_unchanged_generic_native_renderer=True,
            actual_three_option_scene_activation_not_observed=True))
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json')
    current_review=Path('work/analysis/lil_Crew_Items_completion_v3148/current_six_frame_visual_review.json')
    for path in [historical_review,current_review]:
        review=read(path);assert review['viewed'] and sha(Path(review['sheet']).read_bytes())==review['sha256']
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,CONTROL,REFERENCE,PADDING,HISTORY,START,PLAN,FE,MENU,MARGINS,
        historical_review,current_review,Path('docs/editorial_testing_scope_v1870.md'),Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(ROOT/'relocated_predicates_and_representative_rule_reconciliation.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,
        relocated_predicate_pairs=control['relocated_predicate_pairs'],original_event_queries=[],
        historical_complete_ink_gray_blank_masks_reused_without_new_RGB_execution=True,
        historical_B74_and_current_B22_whole_blocks_exact=True,
        current_ARM9_COMMON_EV2_font_and_shared_consumer_bytes_exact=True,
        prior_current_Lil_and_town_startup31frames_inherited_not_new_runs=True,
        prior_current_startup=str(START),historical_representative_proof=str(HISTORY),
        historical_FE_geometry_calibrated_all30_current_unlabeled_panels_verified=True,
        three_option_distinct_count_geometry_and_result_tests=three_option,
        source_4100_voice_selection_distinct_from_player_choices=True,
        current4100_original_D0_roles_all56_bodies_all64_aliases_and_all207_catalog_styles_bound=True,
        inherited_three_access_travel_funds_fixtures_and_five_ship_town_battery_not_earned=True,
        no_new_fixture_or_event_roster_RNG_health_outcome_mutation=True,
        policy_resolution=('The user permits reusable source-bound rules and focused native checks instead of visiting every conditional line. Historical actual progressive holds, FE tutorial and two-option modal holds remain representative by exact ARM9,COMMON,EV2,font andB74/B22data. Current220complete paragraph planes/1760logical-compiled macro cases/880final stored-target cases pass. The distinct4100actor-style provider is proved through16whole commands,3312current-relocated catalog pointers,all56body planes andpreserved64aliases without role fixtures. Five source2200menus receive count3 getters,third-answer/cancel VMreturns,native geometry,all60labelplanes andfixed-margin three-row bounds onthe original256x192screen. Those are offline native tests; no actual three-option shrine menu activation orbutton-to-visible-selection gameplay is claimed. The concrete tightly fitted denial leading-Tloss was resolved faithfully andcomplete replacement plane rechecked. All114relative spans/570relocated cases,21predicate pairs,421commands,inverse bytes,336loaders/two parent modes andthreeentrycensuses pass. No remaining translation-specific display/controlrisk requires individual visits under the user policy. Allnewscene rewards,injuries,progress andrumor outcomes stayunearned. Fresh registered cumulative build,exactcleanpatch andcurrentstartup remainmandatory. Wider editorial scope,graphics separation andlater older-record technical re-audit remainopen.'),
        no_open_translation_specific_display_or_control_finding=True,
        individual_selected_Shrines_Temples_visits_not_required_for_reusable_rules=True,
        actual_selected_Shrines_Temples_IDs=[],actual_three_option_menu_gameplay_coverage=[],
        new_individual_nameplate_observations=[],new_emulator_runs=0,
        registered_release_and_current_startup_still_pending=True,full_goal_complete=False))
    print('Source-bound shared actual rules reconciled;distinct4100 andcount3/third-answer/cancel/3row menus receive focused offline native checks. No selected shrine gameplay claim;registered release/startup pending.')
