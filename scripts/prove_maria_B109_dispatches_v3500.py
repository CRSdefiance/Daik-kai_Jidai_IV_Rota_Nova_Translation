"""Bind52 clean/current speech dispatches under the original Maria route context."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B109_dispatches_v3500')
SOURCE=Path('work/analysis/maria_B109_source_v3498/all26_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);ROOT.mkdir(parents=True);namespace={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(prior,name))
        if name=='bind_current_catalog':
            for x,y in [("if r['route_mask']&4:","if r['route_mask']&8:"),('route=2,route_mask=4','route=3,route_mask=8')]:assert text.count(x)==1;text=text.replace(x,y)
        if name=='expanded_current_body':
            for x,y in [("b'Lil'","b'Maria'"),("b'Argot'","b'Li'"),("b'Argot Co.'","b'Li Clan'")]:assert text.count(x)==1;text=text.replace(x,y)
        adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image);assert binding['route']==3 and binding['route_mask']==8;bp=ROOT/'current_registered_Maria_name_catalog_binding.json';save(bp,binding)
    inp=Path('work/analysis/maria_B109_voices_v3499/current_native_input.json');ctx=CurrentContext(inp,packet['historical_snapshot_ROM'],ROOT/'current_context');assert int.from_bytes(ctx.raw[0x2796B0:0x2796B4],'little')==3;cases=[]
    for row in packet['records']:
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(row[key]);assert raw[0]==row['source_selector'];result=ctx.execute(namespace['dispatch'],raw[0],raw[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==row['source_selector'];cases.append(dict(id=row['id'],version=version,**result))
    assert len(cases)==52 and sorted({c['source_selector'] for c in cases})==[3,11,21,74] and not ctx.machines and packet['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    save(ROOT/'all26_source_current_Maria_dispatches_and_catalog.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),registered_catalog_binding=str(bp),registered_catalog_binding_sha256=sha(bp.read_bytes()),speech_dispatch_cases=cases,source_macro_counts=packet['source_macro_counts'],source_owned_adapters=adapters,all_four_selectors_static_without_role_assignment=True,captain3_actual_Maria_context_and_route_mask8_bound=True,source_current_effective_runtime_English_distinguished_from_storage=True,all_original_UI_preparation_and_progressive_bodies_explicit_unexecuted_boundaries=True,native_input=str(inp),native_input_sha256=sha(inp.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),packed_UI_prefix_repair_pause_C200_and_entry_contracts_still_pending=True,actual_selected_B109_IDs=[],new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('52 source/current Maria dispatches,four static speakers,route-mask8 catalogue andzero source macros pass. Packed-prefix repair,other controls,entry,fonts andactual display remain separate.')
