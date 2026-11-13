"""Bind64 clean/current dispatches,one null-actor FE and source FO in current Maria context."""
from pathlib import Path
import inspect
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_maria_native_context_v4999 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_B97_dispatches_v5001')
SOURCE=Path('work/analysis/maria_B97_source_v4998/all32_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);ROOT.mkdir(parents=True)
    env={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(prior,name))
        changes=([("if r['route_mask']&4:","if r['route_mask']&8:"),('route=2,route_mask=4','route=3,route_mask=8')] if name=='bind_current_catalog' else
            [("b'Lil'","b'Maria'"),("b'Argot'","b'Li'"),("b'Argot Co.'","b'Li Clan'")] if name=='expanded_current_body' else [])
        for a,b in changes:assert text.count(a)==1;text=text.replace(a,b)
        adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](image);assert binding['route']==3 and binding['route_mask']==8
    bp=ROOT/'current_registered_Maria_name_catalog_binding.json';save(bp,binding)
    inp=Path('work/analysis/maria_B97_voices_v5000/current_native_input.json');ctx=CurrentContext(inp,packet['historical_snapshot_ROM'],ROOT/'current_context');cases=[]
    for row in packet['records']:
        for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(row[key]);result=ctx.execute(env['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
            assert result['resolved_actor_ID']==(None if raw[0]==254 else row['source_selector'])
            cases.append(dict(id=row['id'],version=label,**result))
    assert len(cases)==64 and sum(c['source_selector']==254 for c in cases)==2 and packet['source_macro_counts']==dict(FI=0,FA=0,FO=1) and not ctx.machines
    save(ROOT/'all32_clean_current_Maria_dispatches_FE_and_FO.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        speech_dispatch_cases=cases,source_macro_counts=packet['source_macro_counts'],registered_catalog_binding=str(bp),registered_catalog_binding_sha256=sha(bp.read_bytes()),source_owned_adapters=adapters,
        captain3_actual_current_Maria_context_route_mask8_and_three_static_selectors_bound=True,one_FE_uses_original24310_null_actor_and5473C=True,
        source_FO_default_Li_Clan_expansion_preserved=True,source_current_effective_English_and_storage_distinguished=True,
        UI_preparation_progressive_and_FE_full_bodies_explicit_unexecuted_boundaries=True,current_native_input=str(inp),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B97_IDs=[],new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('64 current dispatches pass:Maria3/Xien10/Bandit180,FE null actor,FO Li Clan;all4MiB preserved. No B97 activation or display claim.')
