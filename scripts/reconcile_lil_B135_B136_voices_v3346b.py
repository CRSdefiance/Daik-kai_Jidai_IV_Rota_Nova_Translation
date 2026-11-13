"""Bind eight current static speakers while reusing the exact207-actor catalog."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.reconcile_lil_shrines_voices_v3167 import names
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B135_B136_voices_v3346b')
SOURCE=Path('work/analysis/lil_remaining_B135_B140_source_v3345b/next35_B135_B136_clean_current_context.json')
PRIOR=Path('work/analysis/lil_B111_B119_voices_v3218/current207_catalog_eight_voices_and_CF_D0_D1_D6_D7_DC_roles.json')

def selectors(arm,common,raw,plan,values):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);captain=get(0x7F244);rows=[]
    assert captain==2
    for value in values:
        actor=get(0x2434C,value);assert actor==value<207
        pointer=root+0x19E4 if actor==captain else root+4+32*actor
        voice=get(0x7E988,pointer);assert 0<=voice<8
        rows.append(dict(source_selector=value,resolved_actor_ID=actor,actor_object=pointer,original_voice_class=voice,static_not_dynamic_role=True))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=rows,no_role_roster_event_RNG_or_unowned4MiB_mutation=True,current_executed_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists();source,prior=map(read,[SOURCE,PRIOR]);image,old=NdsImage.open(source['current_ROM']),NdsImage.open(prior['candidate'])
    assert sha(Path(source['current_ROM']).read_bytes())==source['current_ROM_sha256'] and sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:assert image.read_file(path)==old.read_file(path)
    assert len(prior['catalog']['rows'])==207 and {r['original_voice_class'] for r in prior['catalog']['rows']}==set(range(8))
    chosen=sorted({r['source_selector'] for r in source['records'] if r['source_selector']<207});assert chosen==[2,9,14,36,47,96]
    assert not any(207<=r['source_selector']<224 for r in source['records'])
    text=inspect.getsource(names);anchor='for ident in range(207):';assert text.count(anchor)==1;text=text.replace(anchor,'for ident in SELECTED_ACTORS:')
    env={**names.__globals__,'SELECTED_ACTORS':chosen};exec(compile(text,str(Path(__file__))+'::six_names','exec'),env)
    ROOT.mkdir(parents=True);context=ROOT/'historical_source_context.json';save(context,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],current_ARM9_sha256=source['current_ARM9_sha256'],current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(context)))
    ctx=CurrentContext(inp,source['historical_snapshot_ROM'],ROOT/'current_context')
    fresh=ctx.execute(env['names']);ctx.machines.pop();resolution=ctx.execute(selectors,chosen);ctx.machines.pop();assert not ctx.machines
    expected={r['actor_ID']:r for r in prior['catalog']['rows']}
    for r in fresh['rows']:
        for k in ['actor_ID','actor_object','getter','current_catalog_name','original_voice_class']:assert r[k]==expected[r['actor_ID']][k],(r['actor_ID'],k)
    save(ROOT/'current_six_static_names_voices_and207_catalog_rebind.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),reused_catalog_proof=str(PRIOR),reused_catalog_proof_sha256=sha(PRIOR.read_bytes()),all207_catalog_and_eight_voice_groups_bound_by_exact_runtime_COMMON_EV2_font_and_same_snapshot=True,fresh_six_actor_names=fresh,original_static_selector_resolution=resolution,no_source00_orFE_speeches_in_selected35=True,no_source_dynamic_selectors_or4100_objects=True,all35_progressive_dispatches_still_require_separate_proof=True,current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),scoped_source_owned_getter_function=text,no_new_nameplate_observation_or_name_asset_change=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Six current static names/voices pass;207catalog rebound byexact runtime/data. No rolefixtures,newnameplates orreviewcredit.')
    print({r['actor_ID']:r['current_catalog_name'] for r in fresh['rows']})
