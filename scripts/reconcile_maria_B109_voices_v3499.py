"""Fetch four current names/voices using the actual Maria captain3 context."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.reconcile_lil_shrines_voices_v3167 import names
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B109_voices_v3499')
SOURCE=Path('work/analysis/maria_B109_source_v3498/all26_clean_current_complete_context.json')
def resolve(arm,common,raw,plan,values):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);captain=get(0x7F244);assert captain==3 and int.from_bytes(raw[0x2796B0:0x2796B4],'little')==3;rows=[]
    for value in values:
        actor=get(0x2434C,value);assert actor==value<207;pointer=root+0x19E4 if actor==captain else root+4+32*actor;voice=get(0x7E988,pointer);assert 0<=voice<8;rows.append(dict(source_selector=value,resolved_actor_ID=actor,actor_object=pointer,original_voice_class=voice,static_not_dynamic_role=True))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before;return dict(rows=rows,captain=captain,no_role_roster_event_RNG_or_unowned4MiB_mutation=True,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);im=NdsImage.open(source['current_ROM']);expected={3:'Maria Huamei Li',11:'Jam Jack Ludwyan',21:'Ian Dukov',74:'Richard Townsend'};assert source['source_selectors']==list(expected)
    text=inspect.getsource(names);changes=[('assert get(0x7F244)==2','assert get(0x7F244)==3'),('for ident in range(207):','for ident in SELECTED_ACTORS:'),('if ident==2 else','if ident==3 else')]
    for x,y in changes:assert text.count(x)==1,x;text=text.replace(x,y)
    env={**names.__globals__,'SELECTED_ACTORS':list(expected)};exec(compile(text,str(Path(__file__))+'::four_current_names','exec'),env)
    ROOT.mkdir(parents=True);context=ROOT/'historical_source_context.json';save(context,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],current_ARM9_sha256=source['current_ARM9_sha256'],current_COMMON_sha256=sha(im.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(context)))
    ctx=CurrentContext(inp,source['historical_snapshot_ROM'],ROOT/'current_context');fresh=ctx.execute(env['names']);ctx.machines.pop();resolution=ctx.execute(resolve,list(expected));ctx.machines.pop();assert not ctx.machines
    for r in fresh['rows']:assert r['current_catalog_name']==expected[r['actor_ID']],r
    save(ROOT/'current_four_Maria_static_names_voices_and_native_context.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),fresh_four_actor_names=fresh,original_static_selector_resolution=resolution,original_name_ring_scratch_restored_recovers_all4MiB=True,current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),scoped_source_owned_getter_function=text,captain3_Maria_actual_context_not_Lil_fixture=True,no_new_nameplate_observation_or_role_roster_event_assignment=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print({r['actor_ID']:r['current_catalog_name'] for r in fresh['rows']})
