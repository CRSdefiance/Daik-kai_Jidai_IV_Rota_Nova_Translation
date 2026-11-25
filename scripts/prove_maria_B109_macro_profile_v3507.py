"""Measure route3 default macro lengths without adding macros to source dialogue."""
import inspect
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B109_macro_profile_v3507')
SOURCE=Path('work/analysis/maria_B109_source_v3498/all26_clean_current_complete_context.json')
def expand(arm,common,raw,plan,body,prefix):
    cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184);captain=get(0x7F244);identity=get(0x2434C,prefix);assert identity==prefix and captain==3;actor=root+0x19E4 if identity==captain else root+4+32*identity;before=bytes(cpu.mem_read(0x02000000,0x400000));cases=[]
    h=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    try:
        for phase in range(4):
            inp,out=0x02660000+phase,0x02662000;cpu.mem_write(inp-16,b'\xA5'*2080);cpu.mem_write(inp,body+b'\0');input_before=bytes(cpu.mem_read(inp-16,2080));cpu.mem_write(out-16,b'\xA5'*4128);call(cpu,0x242C8,(out,inp,actor),instruction_limit=400000);value=bytes(cpu.mem_read(out,4096)).split(b'\0')[0];expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan');assert value==expected and bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(inp-16,2080))==input_before
            assert bytes(cpu.mem_read(out-16,16))==b'\xA5'*16 and bytes(cpu.mem_read(out+len(value)+1,4095-len(value)))==b'\xA5'*(4095-len(value));cases.append(dict(input_alignment=phase,output_hex=value.hex(),original_macro_ABI_input_output_canaries_and_all4MiB_exact=True))
    finally:cpu.hook_del(h)
    return dict(original_selector=identity,actor_object=actor,source_prefix=prefix,captain=captain,cases=cases,current_executed_instruction_addresses=len(provider.executed_current),original_242CC_UI_boundary_unexecuted=True,no_model_event_RNG_or_roster_mutation=True)
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert packet['source_macro_counts']=={'FI':0,'FA':0,'FO':0};ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/maria_B109_voices_v3499/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');results=[]
    for prefix in [3,11,21,74]:results.append(ctx.execute(expand,b'FI FA FO',prefix));ctx.machines.pop()
    assert not ctx.machines and all(bytes.fromhex(c['output_hex'])==b'Maria Li Li Clan' for r in results for c in r['cases'])
    save(ROOT/'four_static_actors_default_macro_lengths16_alignment_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=results,macro_ascii_lengths={'FI':5,'FA':2,'FO':7},source_macro_counts={'FI':0,'FA':0,'FO':0},explicit_synthetic_macro_probe_only_not_added_to_shipped_source=True,all_four_static_actors_expand_default_Maria_names_and_lengths=True,native_alignment_cases=16,portable_source_owned_adapter=inspect.getsource(expand),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_UI_setup_and_focused_actual_display_separate_pending=True,new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Four actors/16 current macro cases confirm Maria5/Li2/LiClan7. Source has zero macros;none added to dialogue.')
