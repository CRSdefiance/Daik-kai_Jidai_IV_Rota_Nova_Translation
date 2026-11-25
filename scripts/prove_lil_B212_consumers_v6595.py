"""Bind actual name getters, voice, effective speech templates and typed source labels offline."""
import inspect,struct
from pathlib import Path
from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_consumers_v6595');SOURCE=Path('work/analysis/lil_B212_source_v6594b/all14_clean_current_complete_exchange_with_two_three_choices.json');INPUT=Path('work/analysis/current_V6584_native_v6593/current_native_input.json')
def choice_getters(arm,command):
    value=bytes.fromhex(command['whole_command_hex']);word=struct.unpack_from('<H',value)[0];assert word in [0x2100,0x2200];count={0x2100:2,0x2200:3}[word];base=2+2*count;versions=[]
    for phase in [0,2]:
        cpu=machine(arm);stream,owner=0x02660000+phase,0x02662000
        cpu.mem_write(stream-16,b'\xa5'*(len(value)+32));cpu.mem_write(stream,value);cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<3I',0,0,stream));owned=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(BASE,0x400000))
        call(cpu,0x2A3B8,(owner,));assert cpu.reg_read(UC_ARM_REG_R0)==count;labels=[]
        for option in range(count):
            relative=base+struct.unpack_from('<H',value,2+2*option)[0];assert base<=relative<len(value);call(cpu,0x2A30C,(owner,option));pointer=cpu.reg_read(UC_ARM_REG_R0);assert pointer==stream+relative;body=value[relative:value.index(0,relative)];assert body
            labels.append(dict(option_index=option,relative_offset=relative,offset=command['offset']+relative,hex=body.hex(),text=body.decode('cp932')))
        assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owned and bytes(cpu.mem_read(stream,len(value)))==value and bytes(cpu.mem_read(stream-16,16))==bytes(cpu.mem_read(stream+len(value),16))==b'\xa5'*16
        versions.append(dict(input_alignment=phase,count=count,labels=labels,original_count_pointer_ABI_all4MiB_owner_stream_and_guards_exact=True))
    return versions
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert packet['all9_speech_and5_choice_glosses_precede_old_English'] and packet['source_static_actor_selectors']==[149] and packet['source_macro_counts']==dict(FI=0,FA=0,FO=0);image=NdsImage.open(packet['current_ROM']);clean=NdsImage.open('work/clean.nds');original=clean.read_file('/__arm9__.bin');arm=image.read_file('/__arm9__.bin')
    assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']==read(INPUT)['current_ROM_sha256']
    for a,b in [(0x7ED88,0x7EE50),(0x2A1D8,0x2A414),(0x7E988,0x7E9A0)]:assert arm[a:b]==original[a:b]
    namespace={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(inherited,name))
        if name=='bind_current_catalog':text=checked_text(text,{'assert len(payload)==123040':"assert len(payload)==123264 and sha(arm)=='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'"})
        adapters[name]=text;exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image)
    name_adapter=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in [149]:','all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_two_original_consumers_and_owned_or_readonly_memory_paths_exact'});env=dict(names.__globals__);exec(compile(name_adapter,__file__+'::actor149','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');native=ctx.execute(env['names']);ctx.machines.pop();static=ctx.execute(selectors,[149]);ctx.machines.pop();assert len(native['rows'])==2
    payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264 and arm.count(payload)==1;payload_at=arm.index(payload);fields=[]
    for delta in [0,4,8]:
        at=TABLE+149*32+delta;sp,cp=[struct.unpack_from('<I',a,at)[0] for a in [original,arm]];assert bool(sp)==bool(cp)
        if not sp:fields.append(dict(pointer_field=at,column=delta,source_null=True,current_null=True));continue
        src=cstring(original,sp-BASE)
        if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);storage=payload_at+off;kind='verified-current-staged-payload'
        else:storage=cp-BASE;value=cstring(arm,storage);kind='original-static-ARM9'
        fields.append(dict(pointer_field=at,column=delta,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=src.hex(),Japanese=src[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=storage,current_storage_kind=kind,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932')))
    cases=[];effective=[];voice=static['rows'][0]['original_voice_class']
    for row in packet['records']:
        for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            value=bytes.fromhex(row[key]);assert value[0]==149;result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==149 and result['source_voice_class']==voice;cases.append(dict(id=row['id'],version=label,**result))
            if label=='current-English':
                boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');body=bytes.fromhex(boundary['text_hex']);expected,match=namespace['expanded_current_body'](value[1:]);assert body==expected and result['registered_catalog_match']==match is None
                effective.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],current_raw_storage_hex=value[1:].hex(),current_effective_runtime_template_hex=value[1:].hex(),current_expanded_runtime_hex=body.hex(),current_effective_runtime_English=body.decode('cp932'),effective_predecessor_paragraph=' '.join(body.decode('cp932').split()),source_selector=149,resolved_actor_ID=149,source_voice_class=voice,registered_catalogue_match=None,native_UI_body_unexecuted=True))
    assert len(cases)==18 and len(effective)==9 and not ctx.machines
    save(ROOT/'nine_effective_bodies18_dispatches_actor149_two_name_consumers.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_name_fields=[dict(actor_ID=149,fields=fields)],native_two_distinct_name_consumers=native,original_static_selector=static,all18_source_current_dispatches=cases,effective_current_records=effective,all9_current_templates_equal_raw_storage_without_catalogue_override=True,current_name_catalog_binding=binding,source_owned_dispatch_adapters=adapters,source_owned_name_adapter=name_adapter,name_wording_complete_native_font_planes_actual_headers_controls_entry_and_effects_pending=True,current_full_catalogue_UI_not_visited=True,no_new_name_asset_207_name_approval_or_gameplay_claim=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(names.__code__.co_filename),Path(selectors.__code__.co_filename),Path(inherited.__file__),Path(__file__)]},source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    getters=[]
    for menu in packet['blocks'][0]['choices']:
        versions=[]
        for version,code,command in [('clean',original,menu['source_command']),('current',arm,menu['current_command'])]:
            proof=choice_getters(code,command);assert len(proof)==2
            for r in menu['records']:
                got=proof[0]['labels'][r['option_index']];assert got['hex']==r['source_hex' if version=='clean' else 'current_hex'] and got['offset']==r['source_reference' if version=='clean' else 'current_reference']['offset']
            versions.append(dict(version=version,alignment_cases=proof))
        getters.append(dict(command_offset=menu['command_offset'],word=menu['word'],versions=versions))
    save(ROOT/'two_and_three_choice_original_getters_clean_current_even_alignments.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),menus=getters,native_count_cases=8,native_label_pointer_cases=20,all_five_labels_two_versions_two_even_alignments_exact=True,source_current_original_choice_getter_code_spans_exact=True,full_UI_renderer_input_and_choice_result_routing_unexecuted=True,no_ROM_or_ledger_change=True,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(current_name_consumers=[(r['consumer'],r['text']) for r in native['rows']],voice=voice,current_fields=[r.get('current_English') for r in fields],effective_bodies=9,dispatches=18,count_cases=8,label_cases=20,credit=0))
