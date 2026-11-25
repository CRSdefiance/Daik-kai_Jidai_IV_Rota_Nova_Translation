"""Bind the raw FE06 predicate to original actor availability without forcing state."""
from pathlib import Path
import inspect
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B194_predicate_binding_v5495e')
SOURCE=Path('work/analysis/lil_B194_source_v5489/all11_clean_current_complete_context.json')
TRACE=Path('work/analysis/lil_B194_predicate_trace_v5495b/unforced_original_calls.json')
def availability(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);captain=get(0x7F244)
    actor=root+4+6*32;company_root=get(0xCB160);current_company=get(0x397D8,company_root)
    actor_company=get(0x7E958,actor);member=get(0x7DBC0,actor);available=get(0x7DB14,actor)
    assert captain==2 and actor_company!=current_company and member==available==0
    assert bytes(cpu.mem_read(actor+5,1))==bytes([actor_company])
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(actor_ID=6,actor_root=root,actor_object=actor,current_captain=captain,company_root=company_root,current_company_value=current_company,
        actor_company_value=actor_company,original_7DBC0_result=member,original_7DB14_result=available,
        all4MiB_actor_roster_event_RNG_and_ABI_exact=True,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();packet,trace=map(read,[SOURCE,TRACE]);assert trace['source_context_sha256']==sha(SOURCE.read_bytes())
    current=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=[(0x25490,0x255E8),(0x256A0,0x25734),(0x29874,0x299C8),(0x7DB14,0x7DC00),(0x7E958,0x7E960)]
    assert all(current[a:b]==clean[a:b] for a,b in spans)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B194_voices_v5490/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    result=ctx.execute(availability);ctx.machines.pop();assert not ctx.machines
    calls=trace['result']['original_unconditional_BL_calls']
    matched=[r for r in calls if r['target']==0x0207DB14];assert len(matched)==1 and matched[0]['args'][0]==result['actor_object']
    assert trace['result']['source_command_hex']=='0080ffff06fe0030' and trace['result']['native_result']==[2,0,0,0,0,0]
    assert trace['result']['no_predicate_or_event_flag_forced']
    save(ROOT/'source_FE06_actor6_availability_and_unforced_current_false_result.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        trace=str(TRACE),trace_sha256=sha(TRACE.read_bytes()),current_native_availability=result,source_owned_readonly_adapter=inspect.getsource(availability),
        exact_source_handler_spans=[dict(start=a,end=b,sha256=sha(current[a:b])) for a,b in spans],original_call_to_7DB14=matched[0],
        raw_FE06_is_conditional_actor_operand_not_FE_system_presentation_selector=True,
        current_false_result_explained_by_original_company_check_not_assumed_roster_fixture=True,
        source_true_path_and_later_fleet_availability_filters_not_observed_in_this_false_snapshot=True,
        company_values_do_not_assign_prose_relationship_rank_or_employment=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Raw FE06 resolves actor6 through original7DB14. Original differing company values yield unforced false;all state remains exact. True path not observed.')
