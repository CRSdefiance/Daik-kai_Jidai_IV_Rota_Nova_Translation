"""Keep the modern observer; label the additional test as eight-speech display only."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_intro_run_tools_v8228')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/run_Gerhard_scenes_v8225.py','scripts/run_Gerhard_intro_v8228.py',{
        'Paired previous/revised English full-script entry fixtures;ordinary identical inputs andreadonly traces.':'Paired eight-speech introduction display slices;original outercondition andremaining B27 notexecuted.',
        'Gerhard_scene_runs_v8225':'Gerhard_intro_display_runs_v8228',
        'Gerhard_scene_fixtures_v8224/four_complete_parent_revised_SC2_scripts_original_Lil_prelude_fixtures.json':'Gerhard_intro_display_fixtures_v8227/two_focused_parent_revised_eight_speech_intro_display_fixtures.json',
        'choices=[27,74]':'choices=[27]',
        'Gerhard_B{block}_route{route}_{version}_v8225':'Gerhard_intro_B{block}_route{route}_{version}_v8228',
        'range(4000,31521,240)':'range(4000,11521,240)','range(2350,32001,60)':'range(2350,12001,60)','|{32000}':'|{12000}',
        'frames=32001':'frames=12001',"'--frames','32001'":"'--frames','12001'","report['frames']==32001":"report['frames']==12001",
        'disclosed_ROM_entry_fixture_not_natural_optional_activation_ororiginal_location=True,':'disclosed_ROM_entry_fixture_not_natural_optional_activation_ororiginal_location=True,focused_intro_display_only_original_outer_condition_andremaining_B27_NOT_executed=True,',
        'not_natural_optional_activation_location_earned_progress_full_route_orhardware_coverage=True,':'not_natural_optional_activation_location_earned_progress_full_route_orhardware_coverage=True,not_full_B27_script_ororiginal_outer_conditional_effect_coverage=True,',
        '32001-frame fixture capture terminal':'12001-frame focused introduction display capture terminal',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        additional_UI_display_test_not_full_B27_conditional_membership=True,
        original_readonly_observer_all_host_restoration_input_andruntime_guards_preserved=True,
        no_actual_sourceflags_predicate_returns_roster_orRNG_forced=True,new_credit=0,full_goal_complete=False))
    print('Prepared paired12k-frame introduction display runs;scopeexplicit,all originalobserver guards retained.')
