"""Current dispatch, six variable style selectors, native predicates and query."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_controls_v3219')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3217b/complete150_reachable_Lil_clean_current_context.json')
INPUT=Path('work/analysis/lil_B111_B119_voices_v3218/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists()
    packet=read(SOURCE);ROOT.mkdir(parents=True)
    namespace={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}}
    adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch','whole_style_command','catalog_style_getters']:
        text=inspect.getsource(getattr(prior,name))
        if name=='catalog_style_getters':
            assert text.count('len(rows)==3312')==1
            text=text.replace('len(rows)==3312','len(rows)==2484')
        adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context')
    image=NdsImage.open(packet['current_ROM'])
    lookup,binding=namespace['bind_current_catalog'](image);namespace['CATALOG_LOOKUP']=lookup
    assert int.from_bytes(ctx.raw[0x2796B0:0x2796B4],'little')==2
    bindingpath=ROOT/'current_registered_name_catalog_binding.json';save(bindingpath,binding)
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    cases=[]
    for row in packet['records']+packet['typed_actor_style_records']:
        prefix=row['source_selector'];speech=row['kind']!='typed-4100-actor-style-alternative'
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            value=bytes.fromhex(row[key]);body=value[1:] if speech else value
            result=ctx.execute(namespace['dispatch'],prefix,body);ctx.machines.pop()
            cases.append(dict(id=row['id'],version=version,**result))
    assert len(cases)==300 and sum(c['source_selector']==254 for c in cases)==2
    whole=[];objects=[o for b in packet['blocks'] for o in b['actor_style_objects']]
    for b in packet['blocks']:
        for obj in b['actor_style_objects']:
            for version,key in [('clean','source_command'),('current','current_command')]:
                im=NdsImage.open('work/clean.nds') if version=='clean' else image
                block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[b['block']]
                result=ctx.execute(namespace['whole_style_command'],block,obj[key]);ctx.machines.pop()
                whole.append(dict(block=b['block'],command_offset=obj['command_offset'],version=version,**result))
    assert len(whole)==12 and {c['source_selector'] for c in whole}=={208,209,214,215,220}
    catalog=ctx.execute(namespace['catalog_style_getters'],objects);ctx.machines.pop()
    predicates=[]
    for b in packet['blocks']:
        for c in b['all_current_native_commands']:
            if c['word'] not in [0x8000,0x8100]:continue
            result=ctx.execute(prior.predicate,blocks[b['block']],c);ctx.machines.pop()
            predicates.append(dict(block=b['block'],**result))
    queries=[dict(block=p['block'],offset=p['offset'],event=q['args'][1],args=q['args'])
        for p in predicates for q in p['original_event_completion_calls']]
    expected=[dict(block=b['block'],offset=c['offset'],event=int.from_bytes(bytes.fromhex(c['whole_command_hex'])[2:4],'little'))
        for b in packet['blocks'] for c in b['all_current_native_commands'] if c['word']==0x8100]
    assert len(predicates)==16 and sum(p['word']==0x8000 for p in predicates)==15
    assert [{k:q[k] for k in ['block','offset','event']} for q in queries]==expected==[dict(block=114,offset=46,event=319)]
    assert not ctx.machines and len(catalog['cases'])==2484
    macros={m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in packet['records']+packet['typed_actor_style_records'])
        for m in ['FI','FA','FO']}
    assert macros=={'FI':3,'FA':0,'FO':1}
    save(ROOT/'all150_source_current_dispatch_variable_styles_predicates_and_query.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        registered_catalog_binding=str(bindingpath),registered_catalog_binding_sha256=sha(bindingpath.read_bytes()),
        source_current_effective_runtime_English_distinguished_from_storage=True,
        speech_and_stored_alternative_dispatch_cases=cases,whole_original4100_command_cases=whole,
        all207_actor_style_source_pointer_cases=catalog,current_original_predicate_cases=predicates,original_event_queries=queries,
        all116speech_complete_preambles_and34_alternatives_have300current_dispatch_cases=True,
        all12_original4100_commands_select_each_actual_source_prefix_and_original_actor_style=True,
        all2484_catalog_getters_preserve_each_original_style_pointer_and_alias=True,
        all15_predicates_and_one_event319_query_preserve_operands_results_and_unowned4MiB=True,
        actual_historical_London_completion_query_is_not_new_earned_progress=True,
        source_macro_counts=macros,one_FE_before_dynamic_fallback208_uses5473C_and24310_null_actor=True,
        FE_incidental_r1_not_geometry=True,all_original_UI_progressive_FE_bodies_explicit_unexecuted_boundaries=True,
        source_dynamic_selectors=[207,208,209,214,215,220],no_dynamic_role_or_roster_assignment=True,
        canonical_Maria32_copy_not_dispatched_under_Lil_context=True,
        source_owned_adapters=adapters,original_helper_producer=prior.__file__,
        original_helper_producer_sha256=sha(Path(prior.__file__).read_bytes()),
        native_input=str(INPUT),native_input_sha256=sha(INPUT.read_bytes()),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        full_native_rendering_wrapping_pagination_reference_and_registered_release_pending=True,
        actual_selected_B111_B119_IDs=[],new_emulator_runs=0,source_prose_or_completion_credit_added=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('300current dispatches/12whole variable-selector4100commands/2484catalog-style pointers/15predicates/oneevent319query pass. FI3/FO1/nullactorFE preserve source;no forcedroles ornewprogress.')
