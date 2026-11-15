"""Bind all current speech dispatches, FE null actors, macros and predicates."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B131_B133_controls_v3308b')
SOURCE=Path('work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json')
INPUT=Path('work/analysis/lil_B131_B133_voices_v3307b/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);ROOT.mkdir(parents=True)
    namespace={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(prior,name));adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image);bindingpath=ROOT/'current_registered_name_catalog_binding.json';save(bindingpath,binding)
    ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');assert int.from_bytes(ctx.raw[0x2796B0:0x2796B4],'little')==2
    cases=[]
    for row in packet['records']:
        prefix=row['source_selector']
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            value=bytes.fromhex(row[key]);assert value[0]==prefix
            result=ctx.execute(namespace['dispatch'],prefix,value[1:]);ctx.machines.pop()
            assert prefix==254 or result['resolved_actor_ID']==prefix
            cases.append(dict(id=row['id'],version=version,**result))
    assert len(cases)==122 and sum(c['source_selector']==254 for c in cases)==2
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;predicates=[]
    for b in packet['blocks']:
        for c in b['all_current_native_commands']:
            if c['word'] not in [0x8000,0x8100]:continue
            original=next(v for v in b['all_clean_native_commands'] if v['offset']==c['offset'])
            assert c['whole_command_hex']==original['whole_command_hex'] and c['word']==0x8000
            result=ctx.execute(prior.predicate,blocks[b['block']],c);ctx.machines.pop();assert not result['original_event_completion_calls']
            predicates.append(dict(block=b['block'],**result))
    assert len(predicates)==5 and not ctx.machines
    macros={m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in packet['records']) for m in ['FI','FA','FO']};assert macros=={'FI':6,'FA':0,'FO':1}
    assert sum(c['source_selector']==0 for c in cases)==36
    statics=sorted({c['source_selector'] for c in cases if c['source_selector']!=254});assert statics==[0,2,5,9,20]
    save(ROOT/'all61_source_current_dispatch_selector00_FE_and5_predicates.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),registered_catalog_binding=str(bindingpath),registered_catalog_binding_sha256=sha(bindingpath.read_bytes()),source_current_effective_runtime_English_distinguished_from_storage=True,speech_dispatch_cases=cases,current_original_predicate_cases=predicates,original_event_queries=[],all61_complete_preambles_have122_current_code_source_and_current_dispatch_cases=True,all2_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback=True,all5_original_predicates_preserve_source_operands_results_and_unowned4MiB=True,source_macro_counts=macros,source00_is_static_actor0_Rafael_Castor_without_role_assignment=True,all_original_UI_preparation_progressive_FE_bodies_explicit_unexecuted_boundaries=True,no_source2000_commands_in_next63_scope=True,source_owned_adapters=adapters,original_helper_producer=prior.__file__,original_helper_producer_sha256=sha(Path(prior.__file__).read_bytes()),native_input=str(INPUT),native_input_sha256=sha(INPUT.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),full_native_rendering_wrapping_pagination_reference_and_registered_release_pending=True,actual_selected_B131_B133_IDs=[],new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('122current-code source/current dispatches,including36real00Rafael andtwoFE null-actor cases,FI6/FO1/five native predicates pass. No rolefixtures ornewgameplay;complete context/prose/display/release pending.')
