"""Relocated native predicates and exact shared representative-rule inheritance."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_mediterranean_africa_controls_v2761 import predicate
from scripts.prepare_lil_mediterranean_africa_research_v2777 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Mediterranean_Africa_sampling_v2780')
DOC=Path('translations/lil_mediterranean_africa_editorial_manuscript_v4.json')
CONTROL=Path('work/analysis/lil_Mediterranean_Africa_controls_v2761/source_bound146_preambles_FE_and_original_conditional_predicates.json')
REFERENCE=Path('work/analysis/lil_Mediterranean_Africa_reference_census_v2779/all353_commands124_relative_sites_and_shipped_entry_census.json')
HISTORY=Path('work/analysis/lil_Seville_sampling_v2721b/representative_rule_reconciliation.json')
START=Path('work/analysis/lil_post_Seville_startup_v2753/cold_boot_Lil_startup_town_verification.json')

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
    assert start['all_current_requested_and_final_framebuffers_equal_V2724'] and start['current_Lil_captain2_and_B22_payload_verified']
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_Mediterranean_Africa_fonts_v2770/current_native_input.json',read(doc['source_context'])['historical_snapshot_ROM'],ROOT/'current_relocated_predicate_context')
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;cases=[]
    for old in control['current_original_predicate_cases']:
        spec=next(b for b in reference['blocks'] if b['block']==old['block'])
        mapped=next(c for c in spec['mapped_commands'] if c['old_offset']==old['offset'])
        command=next(c for c in spec['native_walks']['research'] if c['offset']==mapped['new_offset'])
        assert command['word']==old['word'] and command['whole_command_hex']==old['source_command_hex']
        result=ctx.execute(predicate,blocks[old['block']],command);ctx.machines.pop()
        assert result['native_result']==old['native_result']
        for original_call,relocated_call in zip(old['original_event_completion_calls'],result['original_event_completion_calls'],strict=True):
            assert original_call['address']==relocated_call['address'] and original_call['args'][:3]==relocated_call['args'][:3]
            assert original_call['args'][3]==0x02660000+old['offset'] and relocated_call['args'][3]==0x02660000+command['offset']

        cases.append(dict(block=old['block'],source_offset=old['offset'],target_offset=command['offset'],source_operand_and_original_predicate_result_exact=True,event_getter_arguments0_1_2_exact_and_caller_r3_source_cursor_mapped=True,
            source_alignment_scratch_writes=old['original_unaligned_operand_read_scratch_writes'],relocated_predicate=result))
    assert len(cases)==28 and not ctx.machines
    # Source-controlled four-byte read scratch is the only permitted parser write.
    for case in cases:assert case['relocated_predicate']['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and case['relocated_predicate']['sole_scratch_restore_recovers_all4MiB_exact']
    release=read('work/analysis/lil_post_Seville_release_v2751/registered_release_verification.json')
    assert release['candidate_sha256']==doc['current_ROM_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,CONTROL,REFERENCE,HISTORY,START,PLAN,Path('docs/editorial_testing_scope_v1870.md'),Path(ctx.proof_path),Path(__file__)]}
    evidence[history['review_sheet']]=history['review_sheet_sha256'];evidence[start['review_sheet']]=start['review_sheet_sha256']
    for p,digest in evidence.items():assert sha(Path(p).read_bytes())==digest
    save(ROOT/'relocated_predicates_and_representative_rule_reconciliation.json',dict(candidate=str(PARENT),candidate_sha256=doc['current_ROM_sha256'],research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,all28_relocated_original_predicates_preserve_source_operands_results_and_event_query_arguments=True,
        relocated_predicate_cases=cases,all_unowned4MiB_actor_event_RNG_and_input_bytes_exact=True,original_4byte_alignment_read_scratch_restored_exact=True,
        historical_complete_ink_gray_blank_masks_reused_without_new_RGB_execution=True,historical_B74_and_current_B22_whole_blocks_exact=True,
        current_ARM9_COMMON_EV2_font_and_shared_consumer_bytes_exact=True,prior_current_Lil_and_town_startup31frames_inherited_not_new_runs=True,
        prior_current_startup=str(START),historical_representative_proof=str(HISTORY),
        historical_actual_menu_and_FE_rules_reused_by_exact_consumer_font_and_object_geometry=True,
        inherited_three_access_travel_funds_fixtures_and_five_ship_town_battery_not_earned=True,
        no_new_fixture_or_event_roster_RNG_health_outcome_mutation=True,
        policy_resolution='User representative policy applies to145original progressive speeches,one originalFEsystempanel andthree typed two-choice objects. Every complete speaker preamble,macro order,all353commands/124spans/620relocated cases and336loader/two-parent contracts are source-bound. All28original predicates execute fromtheir mapped addresses withthe same operands/results/eventgetterarguments0/1/2,andincidentalr3is the mappedsourcecursor. Only originalsource-owned02279600scratch maychange andrestoringit recovers4MiB. Current146complete nativeplanes/1168logical-compiled macro cases/584finalparity cases plus24menustyleplanes/18bridgedVMreturns verify completeglyphs,paper/bounds/pagination/menuorder/results. The failed114pxfull-length19cellmenu is not used orvalidated. Final actionlabels omit only sentenceperiods,matchingJapanese action-menu style;allactual finalglyphs/center/bounds pass. Historical progressive ink/gray/blank,typedchoice andFEactual holds andnormalreturn remain bound byexactcurrentARM9/COMMON/EV2/font/B74/sharedconsumer bytes. Prior currentV2750Lil/town startup31frames is separately inherited. No new distinct unresolved translation-specific display/control risk requires individual conditional/speaker/nameplate visits. No selected Mediterranean/Africa gameplay,newfixture,earnedtravel orhardware verification is claimed. Required registered cumulative build,exact cleanpatch andcurrentstartup remain pending.',
        no_open_translation_specific_display_or_control_finding=True,individual_selected_Mediterranean_Africa_visits_not_required_for_reusable_rules=True,
        actual_selected_Mediterranean_Africa_IDs=[],new_individual_nameplate_observations=[],new_emulator_runs=0,
        registered_release_and_current_startup_still_pending=True,full_goal_complete=False))
    print('28relocated native predicates preserve source results/arguments/allunowned state;source-owned read scratch exact. Shared historical/current startup rules inherited by byte identity;registered release/startup pending.')
