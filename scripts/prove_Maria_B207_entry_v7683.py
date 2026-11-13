"""Bind original EV3 B207 action/dependencies to the own-current Maria native getters."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.prove_maria_B97_entry_v5002 import native_entry
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_entry_v7683')
SOURCE=Path('work/analysis/maria_B207_current_v7670/all18_complete_Maria_clean_current_refs_CS0101_before_new_prose.json')
CONTEXT=Path('work/analysis/maria_B207_native_v7681/own_current_Maria_captain3_strict2b6_context_binding.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,context=map(read,[SOURCE,CONTEXT]);current,clean=[NdsImage.open(p) for p in [packet['current_ROM'],'work/clean.nds']]
    assert packet['current_ROM_sha256']==context['candidate_sha256']==sha(Path(packet['current_ROM']).read_bytes())
    ev=current.read_file('/data/EV3.DK4');assert ev==clean.read_file('/data/EV3.DK4')
    events=parse_events(ev);chosen=[r for r in events if r['script_block']==207];assert len(chosen)==1
    ids={chosen[0]['event_ID'],*[v for r in chosen for v in r['must_be_completed']+r['must_not_be_completed'] if v!=65535]}
    selected=[r for r in events if r['event_ID'] in ids]
    adapter=checked_text(inspect.getsource(native_entry),{
        'not_current_eligibility_or_selected_B97_activation':'not_current_eligibility_or_selected_B207_activation',
        'original_completion_flag_in_historical_opening':'original_completion_flag_in_own_current_opening_with_test_unlock',
    })
    env=dict(native_entry.__globals__);exec(compile(adapter,__file__+'::source-EV3-getters','exec'),env)
    inp=Path(context['input']);assert sha(inp.read_bytes())==context['input_sha256']
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context')
    native=ctx.execute(env['native_entry'],ev,selected);ctx.machines.pop();assert not ctx.machines
    save(ROOT/'original_EV3_B207_action_dependencies_andown_Maria_getters.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),own_current_Maria_context=str(CONTEXT),own_current_Maria_context_sha256=sha(CONTEXT.read_bytes()),event_file='/data/EV3.DK4',event_file_sha256=sha(ev),all_original_source_events=events,selected_source_event=chosen[0],selected_source_event_anddependency_native_getters=native,source_owned_getter_adapter=adapter,source_owned_event_parser=inspect.getsource(parse_events),actual_original_captain_ID=3,original_event_file_andaction_table_exact=True,no_eligibility_activation_location_earned_progress_orfull_effect_claim=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,actual_selected_optional_event_IDs=[],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTEXT,Path(native_entry.__code__.co_filename),Path(parse_events.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    print(dict(event=chosen[0]['event_ID'],action=chosen[0]['action_index'],requires=chosen[0]['must_be_completed'],excludes=chosen[0]['must_not_be_completed'],native_getter_cases=len(native['rows']),optional_activation=False))
