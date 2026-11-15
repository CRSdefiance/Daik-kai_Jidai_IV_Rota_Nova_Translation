"""Verify absence of predicates and exact shared representative-rule inheritance."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prepare_lil_crew_items_research_v3138 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Crew_Items_sampling_v3141')
DOC=Path('translations/lil_crew_items_editorial_manuscript_v7.json')
CONTROL=Path('work/analysis/lil_Crew_Items_controls_v3114/source_bound198_preambles_FE_and_original_conditional_predicates.json')
REFERENCE=Path('work/analysis/lil_Crew_Items_reference_census_v3140/all268_commands4_relative_sites_and_shipped_entry_census.json')
HISTORY=Path('work/analysis/lil_Seville_sampling_v2721b/representative_rule_reconciliation.json')
START=Path('work/analysis/lil_Crew_Items_startup_v3106/cold_boot_Lil_startup_town_verification.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,control,reference,history,start,plan=map(read,[DOC,CONTROL,REFERENCE,HISTORY,START,PLAN])
    image,parent,historical=[NdsImage.open(p) for p in [ROM,PARENT,history['candidate']]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==start['candidate_sha256']
    assert sha(ROM.read_bytes())==reference['research_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')==historical.read_file('/__arm9__.bin')
    same_paths=['/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']
    for path in same_paths:assert image.read_file(path)==parent.read_file(path)==historical.read_file(path)
    current_blocks,old_blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,historical]]
    for n in [22,74]:assert current_blocks[n]==old_blocks[n]
    assert history['all4_historical_progressive_holds_freshly_match_current_full_ink_gray_blank_masks']
    assert history['historical_B74_whole_source_block_equal_current'] and history['original_presenter_return_choice_VM_and_text_render_spans_historical_current_exact']
    assert history['no_open_translation_specific_display_or_control_finding'] and history['actual_Seville_IDs']==[] and history['new_emulator_runs']==0
    assert start['all_current_requested_and_final_framebuffers_equal_V3066'] and start['current_Lil_captain2_and_B22_payload_verified']
    ROOT.mkdir(parents=True)
    assert control['current_original_predicate_cases']==[] and control['original_event_queries']==[] and control['source_command_event_queries']==[]
    assert all(c['word'] not in (0x8000,0x8100) for b in reference['blocks'] for c in b['mapped_commands'])
    cases=[]
    FE=Path('work/analysis/lil_Crew_Items_FE_v3129/current_FE_macro_font_and_typed_paper_proof.json');fe=read(FE)
    assert fe['ARM9_sha256']==sha(image.read_file('/__arm9__.bin')) and fe['COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4'))
    assert fe['all7_one_native_page_consumes_complete_target'] and fe['all7_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert len(fe['source_FI_null_actor_cases'])==2 and fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask']
    assert fe['all7_source_unlabeled_stat_notices_and_monkey_calls_preserved'] and fe['four_distinct_source_Luck_Spirit_notices_and_three_monkey_calls_preserved'] and fe['only2_source_FI_macros_preserved_no_invented_labels_or_kinship']
    MENU=Path('work/analysis/lil_Crew_Items_choices_v3130/all1_typed_menu_native_proof.json');menu=read(MENU)
    assert menu['native_selection_cancel_cases']==6 and menu['complete_current_and_reviewed_style_label_planes']==8
    assert menu['all2_labels_source_order_pointers_counts_and_original_selection_results_preserved']
    assert history['original_presenter_return_choice_VM_and_text_render_spans_historical_current_exact']
    for item in menu['menus']:
        assert sha(Path(item['proof']).read_bytes())==item['sha256'];detail=read(item['proof'])
        target=next(c for c in detail['current_and_reviewed_VM_and_font_cases'] if c['version']=='reviewed-research')
        block=next(b for b in plan['blocks'] if b['block']==detail['block'])
        choice=next(c for c in block['choice_commands'] if c['old_offset']==detail['original_command_offset'])
        assert target['object_hex']==choice['target_hex'] and target['source_derived_text_canvas_width']==48
        assert detail['stored_option_indices_and_original_selection_return_values_preserved']
        assert all(p['independent_complete_native_pixels_match'] and p['storage_padding_all_blank'] for p in target['all_four_style_label_planes'])
    release=read('work/analysis/lil_Crew_Items_release_v3104/registered_release_verification.json')
    assert release['candidate_sha256']==doc['current_ROM_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,CONTROL,REFERENCE,HISTORY,START,PLAN,FE,MENU,Path('docs/editorial_testing_scope_v1870.md'),Path(__file__)]}
    evidence[history['review_sheet']]=history['review_sheet_sha256'];evidence[start['review_sheet']]=start['review_sheet_sha256']
    for p,digest in evidence.items():assert sha(Path(p).read_bytes())==digest
    save(ROOT/'relocated_predicates_and_representative_rule_reconciliation.json',dict(candidate=str(PARENT),candidate_sha256=doc['current_ROM_sha256'],research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,no_predicate_or_event_query_commands_in_selected_blocks=True,
        relocated_predicate_cases=cases,no_predicate_execution_or_synthetic_state_fixture=True,
        historical_complete_ink_gray_blank_masks_reused_without_new_RGB_execution=True,historical_B74_and_current_B22_whole_blocks_exact=True,
        current_ARM9_COMMON_EV2_font_and_shared_consumer_bytes_exact=True,prior_current_Lil_and_town_startup31frames_inherited_not_new_runs=True,
        prior_current_startup=str(START),historical_representative_proof=str(HISTORY),
        historical_FE_geometry_calibrated_current_stat_notices_and_monkey_calls_verified=True,
        historical_actual_menu_and_FE_rules_reused_by_exact_consumer_font_and_object_geometry=True,
        relocated_menu_bytes_identical_to_native_6VM8plane_source_owned_proof=True,
        inherited_three_access_travel_funds_fixtures_and_five_ship_town_battery_not_earned=True,
        no_new_fixture_or_event_roster_RNG_health_outcome_mutation=True,
        policy_resolution='User representative policy applies to191ordinary speeches,seven source-unlabeled FE stat notices/monkey calls andone typed two-choice belief menu. Preserve268commands/fourrelative spans/20native relocated cases andinverse opaque-byte restoration. No predicate or event-query commands exist inthese14selected blocks; historical EV2 dependencies are not earned current progress.336wholeloaders/two parent modes/threeentrycensuses pass.198complete native planes/1584logical-compiled macro cases/792final parity cases preserve all glyphs,blank paper,origins,bounds andsingle page. TwoFI nullactor cases preserve Lil; four notices distinguish Luck andSpirit andthree monkey calls stayunlabeled. Menu22bytes/48px canvas preserves order,index0belief/index1disbelief,all8native style planes and6VMreturns. All26sheets viewed orhash-identical toviewed sheets;64rowcount-onlynotes. Shared actual progressive/menu/FE rules inherit byexact ARM9,COMMON,EV2,font,B74 andconsumer code. PriorV3103 startup31coldboot framepairs inherited separately. No unresolved translation-specific distinct display/controlrisk requires visiting every conditional or speaker. No selected crew/item scene,earnedgifts/statgains,location rumor confirmed,newnameplate,fullroute orhardware claim. Three access fixtures andfive-ship townbattery remain unearned. Allwider untouched story/sharedtown/random/help/player prose,separategraphics andlater older-record technical re-audit remainopen. Registeredcumulative build/exactcleanpatch/currentstartup pending.',
        no_open_translation_specific_display_or_control_finding=True,individual_selected_Crew_Items_visits_not_required_for_reusable_rules=True,
        actual_selected_Crew_Items_IDs=[],new_individual_nameplate_observations=[],new_emulator_runs=0,
        registered_release_and_current_startup_still_pending=True,full_goal_complete=False))
    print('No predicate/query commands in selectedblocks. Sharedrules inherited byexact consumers;seven FE notices/calls andtwo choices bound. Registeredrelease/startup pending.')
