"""Freeze one-block research,original loaders/callers andtwo complete ordinary-input fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_confrontation_scene_tools_v7805')
MAP='work/analysis/maria_confrontation_relocation_v7802/one_block16_speeches_no_relative_fixups_exact_full_inverse.json'
STORED='work/analysis/maria_confrontation_stored_v7803/16_final_stored_targets64_alignments11_zero_ink_tails16_pages.json'
CONTROLS='work/analysis/maria_confrontation_controls_v7804/16_final_dispatches_six_numeric_leaves_623D_resources_setup_ends.json'
CURRENT='work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json'
NAMES='work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json'
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    results.append(derive('scripts/create_Maria_story_reference_v7760.py','scripts/create_Maria_confrontation_reference_v7805.py',{
        'maria_story_reference_v7760':'maria_confrontation_reference_v7805',
        'work/analysis/maria_story_final_relocation_v7758/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json':MAP,
        'work/analysis/maria_story_final_stored_v7759/67_final_v3_stored_pages33_tails_two_new_dispatches65_exact_reuse.json':STORED,
        'work/analysis/maria_story_final_controls_v7745/67_final_dispatches_numeric_leaves_opaque_controls_resources_pause_C200_ends.json':CONTROLS,
        'work/analysis/maria_story_final_native_v7757b/67_final_v3_native_pages_andfully_bound_logical_lineage.json':
        'work/analysis/maria_confrontation_native_view_v7801b/16_native_pages_three_sheets_one_final_preview_viewed.json',
        'all_routes_combined_v7717_candidate.nds':'all_routes_combined_v7779_candidate.nds',
        'all-routes-unified-v7717':'all-routes-unified-v7779',"len(manifest['batches'])==629":"len(manifest['batches'])==630",
        'all67_final_stored_targets_equal_reviewed_complete_native_ink':'all16_stored_targets_equal_reviewed_complete_native_ink',
        "view['all67_single_native_four_row_pages_complete_glyph_bounds_andconsumption']":"view['all_three_original_sheets_andone_final_changed_preview_individually_viewed']",
        "len(controls['final_dispatches'])==67":"len(controls['final_dispatches'])==16",
        '[34,35,108]':'[36]','all300_otherSC3_blocks_andall_other_files_components_exact':'all302_otherSC3_blocks_andall_other_files_components_exact',
        'full67-speech':'full16-speech','SC3B34/B108/B35':'SC3B36','20 relative fixes':'no relative commands',
        '67 complete final-v3 native pages and33 zero-ink stored parity tails':'16 reviewed complete native pages and11 zero-ink stored parity tails',
        'these3 blocks change;300other':'B36 changes;302other',
        'Pinned three-block Maria research reference;300other SC3 blocks/allother files/components exact.CurrentV7717/mainV4701 unchanged.':
        'Pinned B36 research reference;302other SC3 blocks/allother files/components exact.CurrentV7779/mainV4701 unchanged.',
    }))
    results.append(derive('scripts/verify_Maria_story_loaders_v7761.py','scripts/verify_Maria_confrontation_loaders_v7806.py',{
        'create_Maria_story_reference_v7760':'create_Maria_confrontation_reference_v7805',
        'maria_story_loaders_v7761':'maria_confrontation_loaders_v7806',
        'maria_story_reference_v7760/research_image_receipt':'maria_confrontation_reference_v7805/research_image_receipt',
        'three-resized-original-loaders':'one-resized-original-loader',
    }))
    results.append(derive('scripts/verify_Maria_story_references_v7762.py','scripts/verify_Maria_confrontation_references_v7807.py',{
        'create_Maria_story_reference_v7760':'create_Maria_confrontation_reference_v7805',
        'maria_story_reference_census_v7762':'maria_confrontation_reference_census_v7807',
        'work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json':CURRENT,
        'maria_story_loaders_v7761':'maria_confrontation_loaders_v7806',
        "sum(len(g['all_command_maps']) for g in groups)==116 and sum(len(g['relative_operand_maps']) for g in groups)==20":
        "sum(len(g['all_command_maps']) for g in groups)==22 and sum(len(g['relative_operand_maps']) for g in groups)==0",
        'all116_commands20_relative_sites_original_entries_shipped_callers.json':'all22_commands_original_B36_entry_no_relative_sites_shipped_callers.json',
        'all116_source_current_target_commands_and20_relative_spans_bound_to_actual_ROM_bytes':'all22_source_current_target_commands_no_relative_sites_bound_to_actual_ROM_bytes',
        'complete_nested_ancestors67_sixbyte_speech_preambles_numeric_leaves_andfourbyte_ends_preserved':'all16_sixbyte_speech_preambles_six_numeric_leaves_andfourbyte_end_preserved',
        '116mapped commands/20relative sites/three original block entries':'22mapped commands/no relative sites/one original block entry',
    }))
    results.append(derive('scripts/create_Maria_story_scene_fixtures_v7749.py','scripts/create_Maria_confrontation_fixtures_v7808.py',{
        'create_Maria_story_reference_v7746':'create_Maria_confrontation_reference_v7805',
        'maria_story_scene_fixtures_v7749':'maria_confrontation_scene_fixtures_v7808',
        'work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json':CURRENT,
        'work/analysis/maria_story_reference_census_v7748/all116_commands20_relative_sites_original_entries_shipped_callers.json':
        'work/analysis/maria_confrontation_reference_census_v7807/all22_commands_original_B36_entry_no_relative_sites_shipped_callers.json',
        'work/analysis/maria_story_final_controls_v7745/67_final_dispatches_numeric_leaves_opaque_controls_resources_pause_C200_ends.json':CONTROLS,
        "len(controls['final_dispatches'])==67 and len(refs['groups'])==3":"len(controls['final_dispatches'])==16 and len(refs['groups'])==1",
        '_v7749_RESEARCH_ONLY.nds':'_v7808_RESEARCH_ONLY.nds',
        'values[:-6]':'values[:-2]',
        'six_complete_source_English_original_prelude_fixtures.json':'two_complete_source_English_original_prelude_fixtures.json',
        'all_three_full_exchanges67_positions_preserved_in_both_languages':'one_complete_exchange16_positions_preserved_in_both_languages',
        'Six pinned full source/English original-prelude fixtures ready.':'Two pinned full source/English original-prelude fixtures ready.',
    }))
    results.append(derive('scripts/run_Maria_story_scenes_v7750.py','scripts/run_Maria_confrontation_scenes_v7809.py',{
        'maria_story_scene_runs_v7750':'maria_confrontation_scene_runs_v7809',
        'maria_story_scene_fixtures_v7749/six_complete_source_English_original_prelude_fixtures':'maria_confrontation_scene_fixtures_v7808/two_complete_source_English_original_prelude_fixtures',
        'choices=[34,108,35]':'choices=[36]',
        'Maria_story_B{block}_route{route}_{version}_v7750':'Maria_confrontation_B{block}_route{route}_{version}_v7809',
    }))
    results.append(derive('scripts/prove_Maria_story_source_name_planes_v7751.py','scripts/prove_Maria_confrontation_source_planes_v7810.py',{
        'maria_story_source_name_planes_v7751':'maria_confrontation_source_name_planes_v7810',
        'work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json':CURRENT,
        'work/analysis/maria_story_effective_v7729/all67_effective_English_templates134_original_dispatches.json':
        'work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json',
        'work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json':NAMES,
        'work/analysis/maria_story_pages_v7738/67_compiled268_alignments68_complete_native_pages.json':
        'work/analysis/maria_confrontation_row_reasons_v7801b/16_native_pages_exact_with_nine_individual_row_reasons.json',
        'work/analysis/current_V7717_native_v7720/route3/current_native_input.json':'work/analysis/current_V7779_native_v7782/route3/current_native_input.json',
        'native_sixteen_progressive_and_full_name_consumers':'native_six_progressive_and_full_name_consumers',
        'len(nameplanes)==8 and len(sourcepages)==67':'len(nameplanes)==3 and len(sourcepages)==16',
        '67_clean_source_native_pages8_complete_name_planes32_literal_alignments.json':'16_clean_source_native_pages3_complete_name_planes12_literal_alignments.json',
        'current_name_literal_alignment_cases=32,eight_original_style11_progressive_name_planes_fresh=True':'current_name_literal_alignment_cases=12,three_original_style11_progressive_name_planes_fresh=True',
        'all67_original_Japanese_paragraphs_andmeasured_source_macros_preserved':'all16_original_Japanese_paragraphs_andmeasured_source_macros_preserved',
        'PASS:67source paragraphs/pages':'PASS:16source paragraphs/pages',
        '8fresh complete original-style11 headers/32literal alignments':'3fresh complete original-style11 headers/12literal alignments',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivations=results,
        all_original_native_numeric_constants_source_prelude_ownership_guards_andordinary_input_schedule_preserved=True,
        exact_current_V7779_parent_all630_batches114accepted_mainV4701_unchanged=True,
        paired_fixture16_original_speeches22_original_commands_plusseven_original_setup_commands=True,
        source_event_not_naturally_activated_existing_system_only_unlock_earned_false=True,
        no_savestate_RAM_code_role_roster_funds_RNG_conditions_orresults_forced=True,
        all_prior_ROMs_translations_andproofs_preserved=True,new_credit=0,full_goal_complete=False))
