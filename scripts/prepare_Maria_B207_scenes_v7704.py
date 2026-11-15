"""Prepare paired complete scenes behind the actually observed seven-command Maria prelude."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_scene_tools_v7704')
if __name__=='__main__':
    assert not ROOT.exists()
    fixture=derive('scripts/create_papal_trade_scene_fixtures_v7648.py','scripts/create_Maria_B207_scene_fixtures_v7704.py',{
        'each actually observed opening prelude':'the actually observed Maria opening prelude',
        'from pathlib import Path':'from pathlib import Path\nfrom scripts.maria_existing_unlock_contract_v7680 import HISTORICAL,validate_fixture',
        'from scripts.create_papal_trade_reference_v7642 import PARENT,PLAN':'from scripts.create_Maria_B207_reference_v7698 import PARENT,PLAN',
        'from scripts.draft_papal_trade_prose_v7631 import CURRENT':'from scripts.draft_Maria_B207_prose_v7687 import CURRENT',
        'papal_trade_scene_fixtures_v7648':'maria_B207_scene_fixtures_v7704',
        'papal_trade_initializer_binding_v7647/two_actual_opening_preludes18_commands_bound_before_optional_scene_fixture':'maria_B207_initializer_binding_v7702/Maria_actual_B33_prelude7_commands_bound_before_optional_scene_fixture',
        'papal_trade_reference_census_v7644/all40_commands_two_block_entries_one_fresh_shipped_caller_census':'maria_B207_reference_census_v7700/Maria_all20_commands_one_entry_one_fresh_shipped_caller_census',
        'papal_trade_relocated_controls_v7645/all36_final_dispatches_two_A000_exact_reuse50_fresh_seeded_ends':'maria_B207_relocated_controls_v7703/Maria18_final_dispatches_two_effect_reuses25_relocated_seeded_ends',
        "len(controls['groups'])==2":"len(controls['dispatch_cases'])==18",
        'papal_trade_route{route}_{version}_v7648':'Maria_B207_route{route}_{version}_v7704',
        'for route in [0,1]':'for route in [3]',
        "current['groups']":"[current]",
        '{0:10,1:8}[route]':'{3:7}[route]',
        "'English':1506":"'English':1470",
        'fixtures.append(dict(route=route':"fp=ROOT/('existing_system_unlock_'+version+'.json');unlock=read(HISTORICAL);unlock.update(production_ROM=str(out),production_ROM_sha256=sha(out.read_bytes()),current_test_scope='Complete Maria B207 initialized source/English scene;system-only unlock not earned.');save(fp,unlock);validate_fixture(fp)\n            fixtures.append(dict(existing_system_unlock_manifest=str(fp),existing_system_unlock_manifest_sha256=sha(fp.read_bytes()),earned_unlock_verified=False,route=route",
        'four_complete_source_English_original_route_prelude_fixtures':'Maria_two_complete_source_English_original_prelude_fixtures',
        'all_four_complete18_speech20_command_exchanges_preserved':'both_complete18_speech20_command_exchanges_preserved',
        'only_original_actually_observed_ten_or8_command_preludes_added':'only_original_actually_observed_seven_command_Maria_prelude_added',
        'no_manual_source_conditions_roles_roster_funds_RNG_results_battery_savestate_orRAM_forcing':'existing_system_only_unlock_fixture_not_earned=True,no_manual_source_conditions_roles_roster_funds_RNG_results_savestate_orRAM_forcing',
        'Four pinned source/English fixtures preserve all18 speeches/20 commands perexchange plus actual original route preludes (Rafael10/Hodram8).':'Two pinned Maria source/English fixtures preserve all18 speeches/20 commands plusthe actual original seven-command prelude,including the A-wait.',
    })
    capture=derive('scripts/run_papal_trade_scenes_v7649.py','scripts/run_Maria_B207_scenes_v7705.py',{
        'from pathlib import Path':'from pathlib import Path\nfrom scripts.maria_existing_unlock_contract_v7680 import validate_fixture,validate_capture',
        'papal_trade_scene_runs_v7649':'maria_B207_scene_runs_v7705',
        'papal_trade_scene_fixtures_v7648/four_complete_source_English_original_route_prelude_fixtures':'maria_B207_scene_fixtures_v7704/Maria_two_complete_source_English_original_prelude_fixtures',
        'choices=[0,1]':'choices=[3]',
        'papal_trade_route{route}_{version}_v7649':'Maria_B207_route{route}_{version}_v7705',
        "source_inputs=Path(f'work/analysis/papal_trade_route_runs_v7625/route{route}/ordinary_NewGame_inputs.json')":"source_inputs=Path('work/analysis/maria_B207_original_initializer_v7701c/route3/ordinary_Maria_inputs_with_A4200.json');fp=Path(selected['existing_system_unlock_manifest']);assert sha(fp.read_bytes())==selected['existing_system_unlock_manifest_sha256'];fixture=validate_fixture(fp)",
        "max(r['start'] for r in base)<=2200":"max(r['start'] for r in base)==4200",
        'range(4000,15501,240)':'range(4600,15501,240)',
        'range(2350,16001,60)':'range(3500,16001,60)',
        'no_battery_savestate_RAM_code_role_roster_funds_RNG_condition_orresult_forcing=True':'existing_system_only_unlock_manifest=str(fp),existing_system_only_unlock_manifest_sha256=sha(fp.read_bytes()),earned_unlock_verified=False,no_savestate_RAM_code_role_roster_funds_RNG_condition_orresult_forcing=True',
        "'--inputs-json',str(inputs),":"'--inputs-json',str(inputs),'--battery-save',fixture['fixture_save'],'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(fp),'--touchscreen',",
        "assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']":"assert report['frames']==16001;validate_capture(report)",
        'new_credit=0,full_goal_complete=False))':'existing_system_only_unlock_fixture=True,earned_unlock_verified=False,new_credit=0,full_goal_complete=False))',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_Maria_two_complete_scene_tests.json',dict(fixture=fixture,capture=capture,all_original_native_high_constants_andmultiplicity_preserved=True,existing_system_only_unlock_earned_false=True,new_credit=0,full_goal_complete=False))
