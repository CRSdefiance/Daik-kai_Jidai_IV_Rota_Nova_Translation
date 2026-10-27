"""Bind all134 source/current progressive dispatches andFI7 independently of C200."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B139_B140_dispatches_v3462')
SOURCE=Path('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);ROOT.mkdir(parents=True);namespace={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(prior,name));adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image);bp=ROOT/'current_registered_name_catalog_binding.json';save(bp,binding)
    inp=Path('work/analysis/lil_B139_B140_voices_v3460/current_native_input.json');ctx=CurrentContext(inp,packet['historical_snapshot_ROM'],ROOT/'current_context');cases=[]
    for row in packet['records']:
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(row[key]);assert raw[0]==row['source_selector'];result=ctx.execute(namespace['dispatch'],raw[0],raw[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==row['source_selector'];cases.append(dict(id=row['id'],version=version,**result))
    assert len(cases)==134 and sorted({c['source_selector'] for c in cases})==[2,4,9,16,20,21,171] and not ctx.machines
    macros={m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in packet['records']) for m in ['FI','FA','FO']};assert macros=={'FI':7,'FA':0,'FO':0}
    save(ROOT/'all67_source_current_dispatches_and_FI7.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),registered_catalog_binding=str(bp),registered_catalog_binding_sha256=sha(bp.read_bytes()),speech_dispatch_cases=cases,source_macro_counts=macros,source_owned_adapters=adapters,all_seven_selectors_static_without_role_assignment=True,source_current_effective_runtime_English_distinguished_from_storage=True,all_original_UI_preparation_progressive_FE_bodies_explicit_unexecuted_boundaries=True,native_input=str(inp),native_input_sha256=sha(inp.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),predicate_query_C200_contracts_bound_separately=True,actual_selected_B139_B140_IDs=[],new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('134 source/current dispatches andFI7 pass;seven static names including Janus4,with no role fixture or new nameplate observation. C200 andconditional contracts remain separate;zero review credit.')
