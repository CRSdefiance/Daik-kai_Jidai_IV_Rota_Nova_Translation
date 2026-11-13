"""Bind three actors, six distinct name consumers, eighteen effective bodies and original FI expansion."""
import inspect,struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B216_consumers_v6786');SOURCE=Path('work/analysis/lil_B216_source_v6785/eleven_clean_current_Arthur_exchange_source_references.json');INPUT=Path('work/analysis/current_V6775_native_v6784/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert packet['all11_clean_glosses_precede_old_English'] and packet['source_static_actor_selectors']==[2,9,82,151,169] and packet['source_macro_counts']==dict(FI=0,FA=0,FO=0);image=NdsImage.open(packet['current_ROM']);clean=NdsImage.open('work/clean.nds');original,arm=[i.read_file('/__arm9__.bin') for i in [clean,image]];assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']==read(INPUT)['current_ROM_sha256'];ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(inherited,name))
        if name=='bind_current_catalog':text=checked_text(text,{'assert len(payload)==123040':"assert len(payload)==123264 and sha(arm)=='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'"})
        adapters[name]=text;exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image);adapter=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in [2,9,82,151,169]:','all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact','actor = root+4+32*ident':'actor = root+0x19E4 if ident==2 else root+4+32*ident'});env=dict(names.__globals__);exec(compile(adapter,__file__+'::three-actors','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');native=ctx.execute(env['names']);ctx.machines.pop();static=ctx.execute(selectors,[2,9,82,151,169]);ctx.machines.pop();assert len(native['rows'])==10;voices={r['source_selector']:r['original_voice_class'] for r in static['rows']};payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264 and arm.count(payload)==1;payload_at=arm.index(payload);fields=[]
    for ident in [2,9,82,151,169]:
        one=[]
        for delta in [0,4,8]:
            at=TABLE+ident*32+delta;sp,cp=[struct.unpack_from('<I',a,at)[0] for a in [original,arm]];assert bool(sp)==bool(cp)
            if not sp:one.append(dict(pointer_field=at,column=delta,source_null=True,current_null=True));continue
            src=cstring(original,sp-BASE)
            if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);storage=payload_at+off;kind='verified-current-staged-payload'
            else:storage=cp-BASE;value=cstring(arm,storage);kind='original-static-ARM9'
            one.append(dict(pointer_field=at,column=delta,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=src.hex(),Japanese=src[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=storage,current_storage_kind=kind,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932')))
        fields.append(dict(actor_ID=ident,fields=one))
    cases=[];effective=[]
    for row in packet['records']:
        ident=row['source_selector']
        for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            value=bytes.fromhex(row[key]);assert value[0]==ident;result=ctx.execute(ns['dispatch'],ident,value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==ident and result['source_voice_class']==voices[ident];cases.append(dict(id=row['id'],version=label,**result))
            if label=='current-English':
                boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');body=bytes.fromhex(boundary['text_hex']);expected,match=ns['expanded_current_body'](value[1:]);assert body==expected and result['registered_catalog_match']==match is None;effective.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],current_raw_storage_hex=value[1:].hex(),current_effective_runtime_template_hex=value[1:].hex(),current_expanded_runtime_hex=body.hex(),current_effective_runtime_English=body.decode('cp932'),effective_predecessor_paragraph=' '.join(body.decode('cp932').split()),source_selector=ident,resolved_actor_ID=ident,source_voice_class=voices[ident],registered_catalogue_match=None,native_UI_body_unexecuted=True))
    assert len(cases)==22 and len(effective)==11 and not ctx.machines;save(ROOT/'eleven_effective_bodies22_dispatches_five_actors_ten_name_consumers.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_name_fields=fields,native_ten_distinct_name_consumers=native,original_static_selectors=static,all22_source_current_dispatches=cases,effective_current_records=effective,all11_current_templates_equal_raw_storage_without_catalogue_override=True,no_original_FI_FA_FO_substitutions=True,current_name_catalog_binding=binding,source_owned_dispatch_adapters=adapters,source_owned_name_adapter=adapter,name_wording_complete_native_font_planes_actual_headers_controls_entry_and_effects_pending=True,current_full_catalogue_UI_not_visited=True,no_new_name_asset_207_name_approval_or_gameplay_claim=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(Path(p).read_bytes()) for p in [SOURCE,INPUT,Path(names.__code__.co_filename),Path(selectors.__code__.co_filename),Path(inherited.__file__),Path(__file__)]},source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False));print(dict(voices=voices,names=[(r['actor_ID'],r['consumer'],r['text']) for r in native['rows']],bodies=11,dispatches=22,credit=0))
