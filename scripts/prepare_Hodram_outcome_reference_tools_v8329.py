"""Source-lock research reference, native whole-archive loaders and caller census to two outcomes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_reference_tools_v8329');assert not root.exists();tools=[]
    mapping='work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json'
    stored='work/analysis/Hodram_outcome_stored_v8327/six_stored_bodies8_fresh16_reused_alignments_six_exact_native_pages.json'
    controls='work/analysis/Hodram_outcome_final_dispatch_v8328/six_final_dispatches9_exact_nontext_commands_FE_FI_andcomplete_ends.json'
    current='work/analysis/Hodram_B47_B48_current_v8317c/six_exact_source_current_effective_refs_after_whole_clean_gloss_andnative_source_view.json'
    tools.append(derive('scripts/create_Hodram_reference_v8276.py','scripts/create_Hodram_outcomes_reference_v8329.py',{
        'Hodram_reference_v8276':'Hodram_outcome_reference_v8329','Hodram_B137_B45_B46_reference_v8276':'Hodram_B47_B48_reference_v8329',
        'translations/hodram_B137_B45_B46_editorial_manuscript_v3.json':'translations/hodram_B47_B48_editorial_manuscript_v2.json',
        'work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json':mapping,
        'work/analysis/Hodram_three_block_stored_v8274/28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json':stored,
        'work/analysis/Hodram_final_controls_v8275/28_final_dispatches24_controls6_raw_evaluations_original4800_4700_requests.json':controls,
        "len(controls['final_dispatches'])==28":"len(controls['final_dispatches'])==6",'[45,46,137]':'[47,48]',
        'all322_other_SC1_blocks':'all323_other_SC1_blocks',
        'all28_complete_speaker_preambles60commands8relatives_two_rawqueries_zero_source_macros_andfullends_preserved':'all6_complete_speaker_preambles15commands_zero_relative_queries_one_FE_one_FI_andfullends_preserved',
        'V8259':'V8300','28 reviewed speeches inthree':'6 reviewed speeches intwo','Hodram28three-block':'Hodram6two-block',
        'onlySC1B137/B45/B46':'onlySC1B47/B48','actual4800-layout0/nameheaders/control/loader/census/policy/atomic/release':'actualFE/scene-controls/nameheaders/loader/census/policy/atomic/release',
        'loaders_caller_census_actual4800_layout0_hide4700_silences_nameheaders_policy_atomic_registered_release_pending':'loaders_caller_census_actual_FE_scene_effects_nameheaders_policy_atomic_registered_release_pending',
        'PinnedresearchHodram28 reference;onlySC1threeblocks change/322others':'PinnedresearchHodram6 reference;onlySC1twoblocks change/323others',
    }))
    tools.append(derive('scripts/verify_Hodram_loaders_v8277.py','scripts/verify_Hodram_outcome_loaders_v8330.py',{
        'scripts.create_Hodram_reference_v8276':'scripts.create_Hodram_outcomes_reference_v8329',
        'Hodram_loaders_v8277':'Hodram_outcome_loaders_v8330',
        'work/analysis/Hodram_reference_v8276/research_image_receipt.json':'work/analysis/Hodram_outcome_reference_v8329/research_image_receipt.json',
        '28-speech Hodram research image':'six-speech Hodram research image','exact_B137_B45_B46_headers':'exact_B47_B48_headers',
    }))
    tools.append(derive('scripts/verify_Hodram_references_v8278.py','scripts/verify_Hodram_outcome_references_v8331.py',{
        'Hodram_reference_census_v8278':'Hodram_outcome_reference_census_v8331',
        'work/analysis/Hodram_reference_v8276/research_image_receipt.json':'work/analysis/Hodram_outcome_reference_v8329/research_image_receipt.json',
        'work/analysis/Hodram_current_review_binding_v8272/28_exact_current_refs_registered_name_dependency_andnative_reuse.json':current,
        'work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json':mapping,
        'work/analysis/Hodram_loaders_v8277/325_whole_native_loads_cache_hits650_initial_parent_modes.json':'work/analysis/Hodram_outcome_loaders_v8330/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
        'work/analysis/Hodram_final_controls_v8275/28_final_dispatches24_controls6_raw_evaluations_original4800_4700_requests.json':controls,
        "sum(len(g['all_command_maps']) for g in groups)==60 and sum(len(g['relative_operand_maps']) for g in groups)==8":"sum(len(g['all_command_maps']) for g in groups)==15 and sum(len(g['relative_operand_maps']) for g in groups)==0",
        "sum(len(c['cases']) for g in groups for c in g['relocated_native_skip_cases'])==40":"sum(len(c['cases']) for g in groups for c in g['relocated_native_skip_cases'])==0",
        "len(controls['final_dispatches'])==28 and controls['fresh_raw_native_evaluations']==6":"len(controls['final_dispatches'])==6 and mapping['source_relative_sites']==0",
        'all60_commands8_relative_sites28_records_three_EV1_entries_shipped_callers':'all15_commands_zero_relative_sites6_records_two_EV1_entries_shipped_callers',
        'all60_source_current_target_commands8_relative_sites28_complete_preambles_bound':'all15_source_current_target_commands_zero_relative_sites6_complete_preambles_bound',
        'actual_B137_B45_B46_4800_layout0_hide4700_silences_headers_policy_atomic_registered_release_pending':'actual_B47_B48_FE_scene_effects_headers_policy_atomic_registered_release_pending',
        'Bind three native SC1 entries,60commands/eightrelatives':'Bind two native SC1 entries,15commands/zerorelatives',
        '60commands/eightrelatives/28records/threeEV1entries':'15commands/zerorelatives/6records/twoEV1entries',
    }))
    root.mkdir(parents=True);save(root/'source_locked_reference_loader_caller_derivations.json',dict(tools=tools,native_high_integer_constants_andmultiplicity_preserved=True,no_registered_ROM_orcredit_change=True,full_goal_complete=False))
