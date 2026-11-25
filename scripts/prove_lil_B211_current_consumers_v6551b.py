"""Bind two named actors, the distinct FE animal panels and all twelve effective predecessor bodies."""
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
ROOT=Path('work/analysis/lil_B211_current_consumers_v6551b');SOURCE=Path('work/analysis/lil_B211_source_v6550c/twelve_clean_current_complete_exchange_source_references.json');INPUT=Path('work/analysis/current_V6541_native_v6549/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert packet['all12_clean_glosses_precede_old_English_comparison'] and packet['source_static_actor_selectors']==[2,7] and not packet['source_dynamic_selectors'] and packet['system_FE_panels']==3 and packet['source_macro_counts']==dict(FI=1,FA=0,FO=0);image=NdsImage.open(packet['current_ROM']);clean=NdsImage.open('work/clean.nds')
    namespace={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(inherited,name))
        if name=='bind_current_catalog':text=checked_text(text,{'assert len(payload)==123040':"assert len(payload)==123264 and sha(arm)=='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'"})
        adapters[name]=text;exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image)
    name_adapter=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in [2,7]:','actor = root+4+32*ident':'actor = root+0x19E4 if ident==2 else root+4+32*ident','all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_four_original_consumers_and_owned_or_readonly_memory_paths_exact'})
    env=dict(names.__globals__);exec(compile(name_adapter,__file__+'::two-source-static-names','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');native=ctx.execute(env['names']);ctx.machines.pop();static=ctx.execute(selectors,[2,7]);ctx.machines.pop();assert len(native['rows'])==4
    original=clean.read_file('/__arm9__.bin');arm=ctx.arm;payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264 and arm.count(payload)==1;payload_at=arm.index(payload);fields=[]
    for ident in [2,7]:
        row=[]
        for delta in [0,4,8]:
            at=TABLE+ident*32+delta;sp,cp=[struct.unpack_from('<I',a,at)[0] for a in [original,arm]];assert bool(sp)==bool(cp)
            if not sp:row.append(dict(pointer_field=at,column=delta,source_null=True,current_null=True));continue
            src=cstring(original,sp-BASE)
            if POOL<=cp<POOL+len(payload):off=cp-POOL;value=cstring(payload,off);storage=payload_at+off;kind='verified-current-staged-payload'
            else:storage=cp-BASE;value=cstring(arm,storage);kind='original-static-ARM9'
            row.append(dict(pointer_field=at,column=delta,source_pointer=sp,source_storage_offset=sp-BASE,source_terminated_hex=src.hex(),Japanese=src[:-1].decode('cp932'),current_pointer=cp,current_storage_offset=storage,current_storage_kind=kind,current_terminated_hex=value.hex(),current_English=value[:-1].decode('cp932')))
        progressive=next(r['text'] for r in native['rows'] if r['actor_ID']==ident and r['consumer']=='progressive-nameplate');full=next(r['text'] for r in native['rows'] if r['actor_ID']==ident and r['consumer']=='full-catalogue');voice=next(r['original_voice_class'] for r in static['rows'] if r['source_selector']==ident);fields.append(dict(actor_ID=ident,fields=row,progressive=progressive,catalogue=full,voice=voice,contextual_name_wording_decision_pending=True))
    cases=[];effective=[]
    for row in packet['records']:
        fe=row['source_selector']==254
        for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            value=bytes.fromhex(row[key]);assert value[0]==row['source_selector'];result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==(None if fe else value[0]) and result['source_voice_class']==(None if fe else next(r['voice'] for r in fields if r['actor_ID']==value[0]));cases.append(dict(id=row['id'],version=label,**result))
            if label=='current-English':
                boundary=next(b for b in result['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if fe else 'unexecuted-progressive-body'));body=bytes.fromhex(boundary['text_hex']);expected,match=namespace['expanded_current_body'](value[1:]);assert body==expected and result['registered_catalog_match']==match is None;text=body.decode('cp932');effective.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],current_raw_storage_hex=value[1:].hex(),current_effective_runtime_template_hex=value[1:].hex(),current_expanded_runtime_hex=body.hex(),current_effective_runtime_English=text,effective_predecessor_paragraph=' '.join(value[1:].decode('cp932').split()),expanded_predecessor_paragraph=' '.join(text.split()),source_selector=value[0],resolved_actor_ID=result['resolved_actor_ID'],source_voice_class=result['source_voice_class'],registered_catalogue_match=None,native_UI_body_unexecuted=True,FE_modal_animal_sound_without_named_actor=fe))
    assert len(cases)==24 and len(effective)==12 and not ctx.machines and sum(r['FE_modal_animal_sound_without_named_actor'] for r in effective)==3
    save(ROOT/'twelve_effective_bodies24_dispatches_two_names_four_getters_and_FE_source_ownership.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_name_fields=fields,native_four_distinct_name_consumers=native,original_static_selectors=static,all24_source_current_dispatches=cases,effective_current_records=effective,all12_templates_equal_raw_storage_without_catalogue_override=True,original_FI_expands_to_Lil_at_source_owned_native_macro_path=True,all12_clean_glosses_precede_old_English_comparison=True,three_FE_animal_panels_original_null_actor_macro_path_bound=True,nine_progressive_panels_two_static_actors_and_one_FI_substitution_template_bound=True,no_dynamic_role_or_typed_style_consumer_inherited=True,source_macro_counts=packet['source_macro_counts'],current_name_catalog_binding=binding,source_owned_dispatch_adapters=adapters,source_owned_name_adapter=name_adapter,name_wording_native_complete_font_planes_actual_headers_FI_expansion_controls_entry_and_full_effect_semantics_pending=True,current_full_catalogue_UI_not_visited=True,no_new_name_asset_207_name_global_approval_or_original_Latin_artwork_claim=True,no_new_gameplay_ROM_or_editorial_credit=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(names.__code__.co_filename),Path(selectors.__code__.co_filename),Path(inherited.__file__),Path(__file__)]},source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    for r in fields:print(r['actor_ID'],[(f.get('Japanese'),f.get('current_English')) for f in r['fields']],r['progressive'],r['catalogue'],r['voice'])
    print('Twelve effective bodies/24 dispatches,four name getters and three distinct null-actor FE panels pass. FI native expansion bound;complete source/native display,name decisions,controls andrelease remain pending;zero credit.')
