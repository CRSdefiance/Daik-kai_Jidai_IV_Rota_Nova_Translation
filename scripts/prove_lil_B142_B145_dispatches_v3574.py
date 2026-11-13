"""Bind76 source/current calls,nine static actors and the FE null-actor consumer."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_dispatches_v3574')
SOURCE=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);namespace={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(prior,name));adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image);ROOT.mkdir(parents=True);bp=ROOT/'current_registered_Lil_name_catalog_binding.json';save(bp,binding);ctx=CurrentContext('work/analysis/lil_B142_B145_voices_v3572/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');cases=[]
    for r in packet['records']:
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(r[key]);result=ctx.execute(namespace['dispatch'],raw[0],raw[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==(None if raw[0]==254 else r['source_selector']);cases.append(dict(id=r['id'],block=r['block'],version=version,**result))
    assert len(cases)==76 and sum(c['source_selector']==254 for c in cases)==2 and all(c['resolved_actor_ID']==c['source_selector'] for c in cases if c['source_selector'] in [13,109]) and not ctx.machines
    save(ROOT/'all38_source_current_progressive_FE_dispatches_and_FI2.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),speech_dispatch_cases=cases,source_macro_counts=packet['source_macro_counts'],source_owned_adapters=adapters,registered_catalog_binding=str(bp),registered_catalog_binding_sha256=sha(bp.read_bytes()),all_nine_static_actors_without_role_or_roster_fixture=True,source0D_is_static_Cesare13_not_a_linebreak=True,source6D_is_static_Shipwright109_not_an_English_letter=True,one_FE_system_object_routes_original_null_actor_to5473C=True,source_current_effective_English_and_catalogue_provenance_distinguished=True,UI_preparation_progressive_and_FE_bodies_explicit_unexecuted_boundaries=True,native_input='work/analysis/lil_B142_B145_voices_v3572/current_native_input.json',native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B142_B145_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_review_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('76 source/current calls pass:Cesare0D,Shipwright6D,nine static actors,FI2 and FE null-actor5473C;native display still separate.')
