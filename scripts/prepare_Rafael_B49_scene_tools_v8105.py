"""Prepare complete B49 initialized-entry fixtures and paired ordinary-input scene capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_scene_tools_v8105')
if __name__=='__main__':
    assert not ROOT.exists()
    fixtures=derive('scripts/create_Rafael_B48_fixtures_v8049.py','scripts/create_Rafael_B49_fixtures_v8105.py',{
        'Preserve all48 B47 commands':'Preserve all154 B49 commands',
        'scripts.create_Rafael_B48_reference_v8046':'scripts.create_Rafael_B49_reference_v8102',
        'Rafael_B48_scene_fixtures_v8049':'Rafael_B49_scene_fixtures_v8105',
        'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B48_reference_census_v8048/all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json':'Rafael_B49_reference_census_v8104/all154_commands56_relative_sites61_speeches_C281_EV0_entry_shipped_callers.json',
        'Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json':'Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json',
        'Rafael_B47_context_runs_v8015/route0/run_plan.json':'Rafael_B48_context_runs_v8068/route0/run_plan.json',
        "len(controls['final_dispatches'])==91 and len(refs['all_command_maps'])==163":"len(controls['final_dispatches'])==61 and len(refs['all_command_maps'])==154",
        'out/Rafael_B48_{v}_v8049_RESEARCH_ONLY.nds':'out/Rafael_B49_{v}_v8105_RESEARCH_ONLY.nds',
        "g['block']==cg['block']==48":"g['block']==cg['block']==49",
        'blocks[48] if version':'blocks[49] if version',
        'len(source_commands)+10==173':'len(source_commands)+10==164',
        "len(g['text_records'])==91":"len(g['text_records'])==61",
        'original_block=48':'original_block=49','source_block=48':'source_block=49',
        'len(objects)==163 and len(texts)==91 and relative_count==28':'len(objects)==154 and len(texts)==61 and relative_count==56',
        'all28_relative_spans_unchanged_under_constant32_byte_shift':'all56_relative_spans_unchanged_under_constant32_byte_shift',
        "Rafael B48 complete {f['version']} 91-speech/163-command exchange with all28 relative sites,five raw predicates,two completion queries,four FEpanels andall scene/effect commands":"Rafael B49 complete {f['version']} 61-speech/154-command exchange with all56 relative sites,13 raw predicates,one completion query,sevenA000 effects,C281 andall scene/resource commands",
        'not natural B48 activation':'not natural B49 activation',
        'all91_source_speeches163_commands28_relatives_five_raw_predicates_two_queries_fourFE_andall_effects_preserved':'all61_source_speeches154_commands56_relatives_13raw_predicates_one_query_sevenA000_C281_andall_effects_preserved',
        'only_disclosed_opening_ROM_entry_fixture_not_natural_B48_activation_ororiginal_location':'only_disclosed_opening_ROM_entry_fixture_not_natural_B49_activation_ororiginal_location',
        'actual_body_headers_R347_page_turn_fourFE_joining_transitions_andreturn_checks_pending':'actual_body_headers_Lil_Camille_C281_transitions_andreturn_checks_pending',
        'Two pinned complete B48 fixtures:91speeches/163commands/28relatives/5rawpredicates/2queries/fourFE/all scene effects plusoriginal10-command B44prelude.No state forcing.':'Two pinned complete B49 fixtures:61speeches/154commands/56relatives/13rawpredicates/onequery/sevenA000/C281/all scene effects plusoriginal10-command B44prelude.No state forcing.',
    })
    runner=derive('scripts/run_Rafael_B48_scenes_v8050.py','scripts/run_Rafael_B49_scenes_v8106.py',{
        'Rafael_B48_scene_runs_v8050':'Rafael_B49_scene_runs_v8106',
        'Rafael_B48_scene_fixtures_v8049':'Rafael_B49_scene_fixtures_v8105',
        'Rafael_B48_route':'Rafael_B49_route','_v8050':'_v8106',
        'range(4000,39521,240)':'range(4000,23521,240)',
        'range(2350,40001,60))|{40000}':'range(2350,24001,60))|{24000}',
        'frames=40001':'frames=24001',"'40001'":"'24001'",
        "report['frames']==40001":"report['frames']==24001",
        'original_exchange_commands=163,original_exchange_speeches=91':'original_exchange_commands=154,original_exchange_speeches=61',
        ':40001-frame fixture capture terminal':':24001-frame fixture capture terminal',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(derivations=[fixtures,runner],
        whole_original154_command_B49_block_preserved=True,source_Japanese_script_oncurrent_translated_UI_names=True,
        source_event49_not_naturally_selected=True,identical_ordinary_inputs_A4000_thenevery240_until23520=True,
        paired_cold_boot_horizon24001_frames_each=True,actual_selected_path_not_assumed50=True,
        no_state_condition_results_orcontroller_retiming_forcing=True,new_credit=0,full_goal_complete=False))
    print('Prepared B49 full fixtures and paired 24001-frame runner; actual complete exchange must be observed.')
