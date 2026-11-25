"""Derive source-complete B50 initialized fixtures and identical-input capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_scene_tools_v8154')
if __name__=='__main__':
    assert not ROOT.exists()
    fixture=derive('scripts/create_Rafael_B49_fixtures_v8105.py','scripts/create_Rafael_B50_fixtures_v8154.py',{
        'Preserve all154 B49 commands':'Preserve all37 B50 commands',
        'scripts.create_Rafael_B49_reference_v8102':'scripts.create_Rafael_B50_reference_v8151',
        'Rafael_B49_scene_fixtures_v8105':'Rafael_B50_scene_fixtures_v8154',
        'Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B49_reference_census_v8104/all154_commands56_relative_sites61_speeches_C281_EV0_entry_shipped_callers.json':'Rafael_B50_reference_census_v8153/all37_commands_zero_relative_sites28_speeches_4821_EV0_entry_shipped_callers.json',
        'Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json':'Rafael_B50_relocated_controls_v8148/28_stored_dispatches_nine_controls_zero_relatives_relocated4821_25_seeded_ends.json',
        'Rafael_B48_context_runs_v8068/route0/run_plan.json':'Rafael_B49_context_runs_v8124/route0/run_plan.json',
        "len(controls['final_dispatches'])==61 and len(refs['all_command_maps'])==154":"len(controls['final_dispatches'])==28 and len(refs['all_command_maps'])==37",
        'out/Rafael_B49_{v}_v8105_RESEARCH_ONLY.nds':'out/Rafael_B50_{v}_v8154_RESEARCH_ONLY.nds',
        "g['block']==cg['block']==49":"g['block']==cg['block']==50",'blocks[49] if version':'blocks[50] if version',
        'len(source_commands)+10==164':'len(source_commands)+10==47',"len(g['text_records'])==61":"len(g['text_records'])==28",
        'original_block=49':'original_block=50','source_block=49':'source_block=50',
        'len(objects)==154 and len(texts)==61 and relative_count==56':'len(objects)==37 and len(texts)==28 and relative_count==0',
        'all56_relative_spans_unchanged_under_constant32_byte_shift':'zero_relative_sites_no_span_relocation_under_constant32_byte_shift',
        "Rafael B49 complete {f['version']} 61-speech/154-command exchange with all56 relative sites,13 raw predicates,one completion query,sevenA000 effects,C281 andall scene/resource commands":"Rafael B50 complete {f['version']} 28-speech/37-command exchange with zero relative/predicate/query sites,oneA000 effect,4821/4720/4681 andall scene/resource commands",
        'not natural B49 activation':'not natural B50 activation',
        'all61_source_speeches154_commands56_relatives_13raw_predicates_one_query_sevenA000_C281_andall_effects_preserved':'all28_source_speeches37_commands_zero_relative_predicate_query_sites_oneA000_4821_4720_4681_andall_effects_preserved',
        'only_disclosed_opening_ROM_entry_fixture_not_natural_B49_activation_ororiginal_location':'only_disclosed_opening_ROM_entry_fixture_not_natural_B50_activation_ororiginal_location',
        'actual_body_headers_Lil_Camille_C281_transitions_andreturn_checks_pending':'actual_body_three_headers_4821_4720_4681_transitions_andreturn_checks_pending',
        'Two pinned complete B49 fixtures:61speeches/154commands/56relatives/13rawpredicates/onequery/sevenA000/C281/all scene effects plusoriginal10-command B44prelude.No state forcing.':'Two pinned complete B50 fixtures:28speeches/37commands/zero relative-predicate-query sites/oneA000/4821/4720/4681/all scene effects plusoriginal10-command B44prelude.No state forcing.',
    })
    runner=derive('scripts/run_Rafael_B49_scenes_v8106.py','scripts/run_Rafael_B50_scenes_v8155.py',{
        'Rafael_B49_scene_runs_v8106':'Rafael_B50_scene_runs_v8155',
        'Rafael_B49_scene_fixtures_v8105':'Rafael_B50_scene_fixtures_v8154',
        'Rafael_B49_route':'Rafael_B50_route','_v8106':'_v8155',
        'range(4000,23521,240)':'range(4000,15521,240)',
        'range(2350,24001,60))|{24000}':'range(2350,16001,60))|{16000}',
        'frames=24001':'frames=16001',"'24001'":"'16001'","report['frames']==24001":"report['frames']==16001",
        'original_exchange_commands=154,original_exchange_speeches=61':'original_exchange_commands=37,original_exchange_speeches=28',
        ':24001-frame fixture capture terminal':':16001-frame fixture capture terminal',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(derivations=[fixture,runner],
        complete37command28speech_B50_andoriginal10command_B44_prelude_preserved=True,
        source_Japanese_script_oncurrent_translated_UI_names=True,not_natural_event50_activation=True,
        identical_ordinary_Ainputs_every240_frames_after4000=True,paired_horizon16001_each=True,
        actual_selection_completion_picture_transition_andnormal_return_not_assumed=True,
        no_RAM_roster_role_funds_RNG_condition_result_orcontroller_retiming_forcing=True,
        new_credit=0,full_goal_complete=False))
    print('Prepared B50 complete fixtures andpaired16001-frame scene runner;actual coverage remains unobserved.')
