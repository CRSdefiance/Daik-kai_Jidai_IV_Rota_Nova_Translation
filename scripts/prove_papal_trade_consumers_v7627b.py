"""Bind both actual route contexts, native route masks, voices and complete effective bodies."""
import inspect
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_consumers_v7627b')
SOURCE=Path('work/analysis/papal_trade_SC0_SC1_current_v7620/two_complete_current_exchanges36_source_current_refs_before_new_prose.json')
CONTEXTS=Path('work/analysis/papal_trade_route_native_v7626/two_own_current_route_contexts_actual_captains0_1_strict2b6.json')
PRIOR=Path('work/analysis/lil_B234_consumers_v7575/eighteen_effective_bodies36_dispatches_two_actors_four_name_consumers.json')
IDENTITY=Path('work/analysis/papal_trade_route_identity_v7624/route_identity_correction_no_ROM_prose_reference_orcredit_change.json')
def expanded_zero_macro_body(body):
    selected=CATALOG_LOOKUP.get(body);target=selected['target'] if selected else body
    assert not any(v in body or v in target for v in [b'FI',b'FA',b'FO'])
    return target,None if selected is None else {k:v for k,v in selected.items() if k!='target'}
if __name__=='__main__':
    assert not ROOT.exists();packet,contexts,prior,identity=map(read,[SOURCE,CONTEXTS,PRIOR,IDENTITY])
    assert packet['all36_clean_Japanese_gloss_bindings_precede_first_other_route_current_English_comparison'] and contexts['actual_original_captain_IDs']==[0,1] and packet['current_ROM_sha256']==contexts['candidate_sha256']
    old,current=[NdsImage.open(p) for p in [prior['candidate'],packet['current_ROM']]]
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert old.read_file(path)==current.read_file(path)
    ROOT.mkdir(parents=True);groups=[]
    for group in packet['groups']:
        route=group['route'];scope=next(r for r in identity['current_scope'] if r['expected_original_captain_ID']==route);context=next(r for r in contexts['contexts'] if r['route']==route);inp=Path(context['input']);assert sha(inp.read_bytes())==context['input_sha256']
        assert route in [0,1] and group['file_path']==f'/data/SC{route}.DK4' and group['block']==scope['block'] and group['source_macro_counts']==group['current_raw_macro_counts']==dict(FI=0,FA=0,FO=0)
        folder=ROOT/f'route{route}';folder.mkdir();ctx=RouteCurrentContext(inp,'unused-no-historical-ROM',folder/'current_context')
        ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{},'route':route,'route_mask':1<<route};adapters={}
        catalog=prior['source_owned_dispatch_adapters']['bind_current_catalog']
        catalog=checked_text(catalog,{"r['route_mask']&4":"r['route_mask']&route_mask",'route=2,route_mask=4':'route=route,route_mask=route_mask'})
        adapters['bind_current_catalog']=catalog;exec(compile(catalog,__file__+'::route-catalog','exec'),ns)
        ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](current)
        from types import FunctionType
        ns['expanded_current_body']=FunctionType(expanded_zero_macro_body.__code__,ns,argdefs=expanded_zero_macro_body.__defaults__)
        adapters['expanded_current_body']='expanded_zero_macro_body: original native catalogue target followed by explicit zero-FI/FA/FO assertion; no invented default captain/faction macro values'
        for name in ['install_boundaries','dispatch']:
            text=prior['source_owned_dispatch_adapters'][name];adapters[name]=text;exec(compile(text,__file__+'::'+name,'exec'),ns)
        env=dict(names.__globals__);name_adapter=prior['source_owned_name_adapter'];exec(compile(name_adapter,__file__+'::original-two-actor-getters','exec'),env)
        voice_adapter=checked_text(inspect.getsource(selectors),{'assert captain==2':'assert EXPECTED_CAPTAIN in [0,1] and captain==EXPECTED_CAPTAIN'})
        voice_env={**selectors.__globals__,'EXPECTED_CAPTAIN':route};exec(compile(voice_adapter,__file__+'::actual-route-voice','exec'),voice_env)
        native=ctx.execute(env['names']);ctx.machines.pop();static=ctx.execute(voice_env['selectors'],[19,104]);ctx.machines.pop()
        voices={r['source_selector']:r['original_voice_class'] for r in static['rows']};assert voices=={19:7,104:0}
        assert {(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']}=={(19,'progressive-nameplate'):'Carlo Sinat',(19,'full-catalogue'):'Carlo Sinat',(104,'progressive-nameplate'):'Trader',(104,'full-catalogue'):'Trader'}
        cases=[];effective=[]
        for row in group['records']:
            ident=row['source_selector'];assert ident not in [route]
            for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
                value=bytes.fromhex(row[key]);assert value[0]==ident;result=ctx.execute(ns['dispatch'],ident,value[1:]);ctx.machines.pop()
                assert result['resolved_actor_ID']==ident and result['source_voice_class']==voices[ident];cases.append(dict(id=row['id'],file_path=group['file_path'],route=route,version=label,**result))
                if label=='current-English':
                    boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');body=bytes.fromhex(boundary['text_hex']);expected,match=ns['expanded_current_body'](value[1:])
                    assert body==expected==value[1:] and result['registered_catalog_match']==match is None
                    effective.append(dict(id=row['id'],file_path=group['file_path'],route=route,source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=ident,resolved_actor_ID=ident,source_voice_class=voices[ident],current_raw_storage_hex=value[1:].hex(),current_effective_runtime_template_hex=value[1:].hex(),current_expanded_runtime_hex=body.hex(),current_effective_runtime_English=body.decode('cp932'),effective_predecessor_paragraph=' '.join(body.decode('cp932').split()),registered_catalogue_match=None,native_UI_body_unexecuted=True))
        assert len(cases)==36 and len(effective)==18 and not ctx.machines
        groups.append(dict(route=route,route_identity=scope['route_identity'],file_path=group['file_path'],block=group['block'],current_strict_native_input=str(inp),current_strict_native_input_sha256=sha(inp.read_bytes()),actual_original_captain_ID=route,route_mask=1<<route,current_name_catalog_binding=binding,native_four_distinct_name_consumers=native,original_static_selectors=static,source_name_fields=deepcopy(prior['source_name_fields']),name_fields_reuse_exact_whole_ARM9_andCOMMON_andfont_bytes_not_fresh_execution=True,source_owned_dispatch_adapters=adapters,source_owned_name_adapter=name_adapter,source_owned_voice_adapter=voice_adapter,source_current_dispatches=cases,effective_current_records=effective,all18_effective_current_bodies_equal_exact_raw_storage_no_catalogue_override=True,all_original_name_getter_memory_ownership_paths_andprocessor_guards_exact=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),name_wording_font_literal_ABI_actual_headers_EV_entry_controls_andrelease_pending=True))
    assert len(groups)==2 and sum(len(g['source_current_dispatches']) for g in groups)==72 and sum(len(g['effective_current_records']) for g in groups)==36
    save(ROOT/'two_routes36_effective_bodies72_dispatches_eight_getters.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),own_route_context_proof=str(CONTEXTS),own_route_context_proof_sha256=sha(CONTEXTS.read_bytes()),groups=groups,fresh_original_route_specific_dispatches=72,effective_current_speeches=36,fresh_original_name_getter_consumers=8,actual_original_captain_IDs=[0,1],actual_native_catalogue_route_masks=[1,2],source_name_field_data_reused_only_by_exact_ARM9_COMMON_font_andprior_ROM_hashes=True,current_raw_This_man_andHodram_full_width_F_confirmed_effective_processor_output=True,no_global_I_macro_orfont_rule_change_orinvented_route_default_substitution=True,all_original_source_andcurrent_zero_FI_FA_FO=True,all_current_headers_full_catalogue_UI_andoptional_scene_display_unvisited=True,no_current_localization_orfull207_name_orother_route_gameplay_approval=True,failed_7627_captain2_voice_guard_before_any_speech_checks_preserved=True,diagnostic_import_without_deps_path_preserved_not_rejection_credit=True,new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTEXTS,PRIOR,IDENTITY,Path(inherited.__file__),Path(selectors.__code__.co_filename),Path(names.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    for g in groups:print(dict(route=g['route_identity'],captain=g['actual_original_captain_ID'],route_mask=g['route_mask'],voices={r['source_selector']:r['original_voice_class'] for r in g['original_static_selectors']['rows']},bodies=len(g['effective_current_records']),dispatches=len(g['source_current_dispatches']),getters=len(g['native_four_distinct_name_consumers']['rows'])))
