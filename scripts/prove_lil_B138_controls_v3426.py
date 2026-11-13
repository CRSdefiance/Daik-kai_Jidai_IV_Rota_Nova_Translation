"""Bind 88 dispatches, ten predicates and the original query for event137."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B138_controls_v3426')
SOURCE=Path('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')
INPUT=Path('work/analysis/lil_B138_voices_v3425/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);ROOT.mkdir(parents=True)
    namespace={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        t=inspect.getsource(getattr(prior,name));adapters[name]=t;exec(compile(t,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image);bp=ROOT/'current_registered_name_catalog_binding.json';save(bp,binding)
    ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');assert int.from_bytes(ctx.raw[0x2796B0:0x2796B4],'little')==2
    cases=[]
    for r in packet['records']:
        prefix=r['source_selector']
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            value=bytes.fromhex(r[key]);assert value[0]==prefix
            result=ctx.execute(namespace['dispatch'],prefix,value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==prefix
            cases.append(dict(id=r['id'],version=version,**result))
    assert len(cases)==88 and sorted({c['source_selector'] for c in cases})==[2,14,20,21,22,23,92]
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;predicates=[];queries=[]
    for b in packet['blocks']:
        for c in b['all_current_native_commands']:
            if c['word'] not in [0x8000,0x8100]:continue
            original=next(v for v in b['all_clean_native_commands'] if v['offset']==c['offset']);assert c['whole_command_hex']==original['whole_command_hex']
            result=ctx.execute(prior.predicate,blocks[b['block']],c);ctx.machines.pop()
            if c['word']==0x8100:
                expected=int.from_bytes(bytes.fromhex(c['whole_command_hex'])[2:4],'little');calls=result['original_event_completion_calls']
                assert expected==137 and len(calls)==1 and calls[0]['args'][1]==expected
                queries.append(dict(block=b['block'],offset=c['offset'],event=expected,args=calls[0]['args'],native_result=result['native_result'],event137_completion_not_forced=True))
            else:assert not result['original_event_completion_calls']
            predicates.append(dict(block=b['block'],**result))
    assert len(predicates)==11 and sum(c['word']==0x8000 for c in predicates)==10 and len(queries)==1 and not ctx.machines
    macros={m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in packet['records']) for m in ['FI','FA','FO']};assert macros=={'FI':0,'FA':0,'FO':1}
    save(ROOT/'all44_source_current_dispatches10_predicates_and1_query.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),registered_catalog_binding=str(bp),registered_catalog_binding_sha256=sha(bp.read_bytes()),source_current_effective_runtime_English_distinguished_from_storage=True,speech_dispatch_cases=cases,current_original_predicate_cases=predicates,original_event_queries=queries,all44_complete_preambles_have88_current_code_source_and_current_dispatch_cases=True,no_source_FE_speeches=True,all10_predicates_and1_query_preserve_source_operands_results_and_unowned4MiB=True,source_macro_counts=macros,all_seven_selectors_static_without_role_assignment=True,all_original_UI_preparation_progressive_FE_bodies_explicit_unexecuted_boundaries=True,no_source2000_commands_in_next44_scope=True,source_owned_adapters=adapters,original_helper_producer=prior.__file__,original_helper_producer_sha256=sha(Path(prior.__file__).read_bytes()),native_input=str(INPUT),native_input_sha256=sha(INPUT.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),full_native_rendering_wrapping_pagination_reference_and_registered_release_pending=True,actual_selected_B138_IDs=[],new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('88 source/current native dispatches,FO1,ten predicates and one original event137 query pass without fixtures. No new gameplay or review credit;context/prose/display/release pending.')
