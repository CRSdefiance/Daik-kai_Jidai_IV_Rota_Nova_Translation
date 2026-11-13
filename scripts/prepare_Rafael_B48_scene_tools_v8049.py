"""Prepare full original B48 entry fixtures andidentical-input40001-frame readonly scene runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B48_scene_tools_v8049')
if __name__=='__main__':
    assert not ROOT.exists()
    results=[derive('scripts/create_Rafael_B47_fixtures_v7997.py','scripts/create_Rafael_B48_fixtures_v8049.py',{
        'scripts.create_Rafael_B47_reference_v7994':'scripts.create_Rafael_B48_reference_v8046',
        'Rafael_B47_scene_fixtures_v7997':'Rafael_B48_scene_fixtures_v8049',
        'Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json':
            'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B47_reference_census_v7996/all48_commands24_relative_sites15_speeches_EV0_entry_shipped_callers.json':
            'Rafael_B48_reference_census_v8048/all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json',
        'Rafael_B47_relocated_controls_v7991/15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json':
            'Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json',
        'Rafael_B46_context_runs_v7966/route0/run_plan.json':'Rafael_B47_context_runs_v8015/route0/run_plan.json',
        "len(controls['final_dispatches'])==15 and len(refs['all_command_maps'])==48":
            "len(controls['final_dispatches'])==91 and len(refs['all_command_maps'])==163",
        "out/Rafael_B47_{v}_v7997_RESEARCH_ONLY.nds":"out/Rafael_B48_{v}_v8049_RESEARCH_ONLY.nds",
        "g['block']==cg['block']==47":"g['block']==cg['block']==48",
        "blocks[47] if version":"blocks[48] if version",
        "len(source_commands)+10==58":"len(source_commands)+10==173",
        "len(g['text_records'])==15":"len(g['text_records'])==91",
        'original_block=47':'original_block=48','source_block=47':'source_block=48',
        'len(objects)==48 and len(texts)==15 and relative_count==24':
            'len(objects)==163 and len(texts)==91 and relative_count==28',
        'all24_relative_spans_unchanged_under_constant32_byte_shift':'all28_relative_spans_unchanged_under_constant32_byte_shift',
        "Rafael B47 complete {f['version']} 15-speech/48-command exchange with all24 original relative sites andsix predicates":
            "Rafael B48 complete {f['version']} 91-speech/163-command exchange with all28 relative sites,five raw predicates,two completion queries,four FEpanels andall scene/effect commands",
        'not natural B47 activation':'not natural B48 activation',
        'all15_source_speeches48_commands24_relative_sites6_predicates_preserved_in_both_languages':
            'all91_source_speeches163_commands28_relatives_five_raw_predicates_two_queries_fourFE_andall_effects_preserved',
        'only_disclosed_opening_ROM_entry_fixture_not_natural_B47_activation_ororiginal_location':
            'only_disclosed_opening_ROM_entry_fixture_not_natural_B48_activation_ororiginal_location',
        'actual_capture_body_header_R53_two_page_transition_andreturn_checks_pending':
            'actual_body_headers_R347_page_turn_fourFE_joining_transitions_andreturn_checks_pending',
        'Two pinned complete B47 fixtures:15speeches/48commands/24relative sites/6predicates plusoriginal10-command B44 prelude.No condition/state forcing.':
            'Two pinned complete B48 fixtures:91speeches/163commands/28relatives/5rawpredicates/2queries/fourFE/all scene effects plusoriginal10-command B44prelude.No state forcing.',
    })]
    results.append(derive('scripts/run_Rafael_B47_scenes_v7998.py','scripts/run_Rafael_B48_scenes_v8050.py',{
        'Rafael_B47_scene_runs_v7998':'Rafael_B48_scene_runs_v8050',
        'Rafael_B47_scene_fixtures_v7997':'Rafael_B48_scene_fixtures_v8049',
        'Rafael_B47_route':'Rafael_B48_route','_v7998':'_v8050',
        'range(4000,15501,240)':'range(4000,39521,240)',
        'range(2350,16001,60))|{16000}':'range(2350,40001,60))|{40000}',
        'frames=16001':'frames=40001',"'16001'":"'40001'",
        "report['frames']==16001":"report['frames']==40001",
        'original_exchange_commands=48,original_exchange_speeches=15':'original_exchange_commands=163,original_exchange_speeches=91',
        ':16001-frame fixture capture terminal':':40001-frame fixture capture terminal',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_derivations.json',dict(derivations=results,
        full_original163_command_block_not_linearized_omitted_orcondition_forced=True,
        identical_ordinary_inputs_A4000_thenevery240_until39520=True,
        paired_cold_boot_horizon40001_frames_each=True,
        extra_English_page_ortransition_not_controller_retimed=True,
        actual_selected_path_must_be_observed_not_assumed78=True,
        source_fixture_Japanese_script_oncurrent_translated_UI_names_not_fullclean_ROM=True,
        new_credit=0,full_goal_complete=False))
    print('Prepared full B48 fixtures andpaired40001-frame readonly runner. Identical ordinaryinputs;no natural activation/route orhardware claim.')
