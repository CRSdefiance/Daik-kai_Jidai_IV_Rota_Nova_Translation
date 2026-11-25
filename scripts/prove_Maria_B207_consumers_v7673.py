"""Bind36 Maria route-specific dispatches,four name getters,voices andeffective current bodies."""
import inspect
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_current_native_context_v7671 import MariaCurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_papal_trade_consumers_v7627b import expanded_zero_macro_body
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_consumers_v7673')
SOURCE=Path('work/analysis/maria_B207_current_v7670/all18_complete_Maria_clean_current_refs_CS0101_before_new_prose.json')
CONTEXT=Path('work/analysis/maria_B207_native_v7672/own_current_Maria_captain3_strict2b6_context_binding.json')
PRIOR=Path('work/analysis/papal_trade_consumers_v7627b/two_routes36_effective_bodies72_dispatches_eight_getters.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,context,prior=map(read,[SOURCE,CONTEXT,PRIOR]);oldgroup=prior['groups'][0];current=NdsImage.open(packet['current_ROM']);old=NdsImage.open(prior['candidate'])
    assert context['actual_original_captain_ID']==3 and packet['current_ROM_sha256']==context['candidate_sha256']==sha(Path(packet['current_ROM']).read_bytes())
    for file in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert old.read_file(file)==current.read_file(file)
    inp=Path(context['input']);assert sha(inp.read_bytes())==context['input_sha256'];ROOT.mkdir(parents=True);ctx=MariaCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context')
    ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{},'route':3,'route_mask':8};adapters={}
    for name in ['bind_current_catalog','install_boundaries','dispatch']:
        text=oldgroup['source_owned_dispatch_adapters'][name];adapters[name]=text;exec(compile(text,__file__+'::Maria-'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](current);assert binding['route']==3 and binding['route_mask']==8
    ns['expanded_current_body']=FunctionType(expanded_zero_macro_body.__code__,ns,argdefs=expanded_zero_macro_body.__defaults__)
    name_adapter=oldgroup['source_owned_name_adapter'];env=dict(names.__globals__);exec(compile(name_adapter,__file__+'::source-two-name-getters','exec'),env)
    voice_adapter=checked_text(inspect.getsource(selectors),{'assert captain==2':'assert captain==EXPECTED_CAPTAIN==3'});ve={**selectors.__globals__,'EXPECTED_CAPTAIN':3};exec(compile(voice_adapter,__file__+'::actual-Maria-voices','exec'),ve)
    native=ctx.execute(env['names']);ctx.machines.pop();voice=ctx.execute(ve['selectors'],[19,104]);ctx.machines.pop()
    voices={r['source_selector']:r['original_voice_class'] for r in voice['rows']};assert voices=={19:7,104:0}
    assert {(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']}=={(19,'progressive-nameplate'):'Carlo Sinat',(19,'full-catalogue'):'Carlo Sinat',(104,'progressive-nameplate'):'Trader',(104,'full-catalogue'):'Trader'}
    cases=[];effective=[]
    for row in packet['records']:
        selector=row['source_selector'];assert selector in [19,104] and selector!=3
        for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(row[key]);result=ctx.execute(ns['dispatch'],selector,raw[1:]);ctx.machines.pop()
            assert result['resolved_actor_ID']==selector and result['source_voice_class']==voices[selector];cases.append(dict(id=row['id'],file_path=packet['file_path'],version=label,**result))
            if label=='current-English':
                boundary=next(r for r in result['boundaries'] if r['kind']=='unexecuted-progressive-body');body=bytes.fromhex(boundary['text_hex']);expected,match=ns['expanded_current_body'](raw[1:])
                assert body==expected==raw[1:] and match is result['registered_catalog_match'] is None
                effective.append(dict(id=row['id'],file_path=packet['file_path'],source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=selector,source_voice_class=voices[selector],current_raw_storage_hex=raw[1:].hex(),current_effective_runtime_template_hex=raw[1:].hex(),current_expanded_runtime_hex=body.hex(),effective_predecessor_paragraph=' '.join(body.decode('cp932').split()),registered_catalogue_match=None,native_UI_body_unexecuted=True,whole_CS0101_header_effect_not_executed_by_isolated_dispatch=True))
    assert len(cases)==36 and len(effective)==18 and not ctx.machines and packet['source_macro_counts']==packet['current_raw_macro_counts']==dict(FI=0,FA=0,FO=0)
    save(ROOT/'all18_effective_Maria_bodies36_dispatches_four_getters_two_voices.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),own_current_Maria_context=str(CONTEXT),own_current_Maria_context_sha256=sha(CONTEXT.read_bytes()),current_strict_native_input=str(inp),current_strict_native_input_sha256=sha(inp.read_bytes()),actual_original_captain_ID=3,current_name_catalog_binding=binding,source_current_dispatches=cases,effective_current_records=effective,native_four_distinct_name_consumers=native,original_static_selectors=voice,source_name_fields=deepcopy(oldgroup['source_name_fields']),source_name_field_data_reused_by_exact_whole_ARM9_COMMON_FNT_andprior_ROM_bytes=True,source_owned_dispatch_adapters=adapters,source_owned_zero_macro_body_adapter=inspect.getsource(expanded_zero_macro_body),source_owned_name_adapter=name_adapter,source_owned_voice_adapter=voice_adapter,all18_effective_current_bodies_equal_raw_storage_no_catalogue_override=True,all_original_name_memory_ownership_paths_andprocessor_guards_preserved=True,complete_CS0101_header_native_parent_effect_andactual_scene_display_still_pending=True,all_source_current_zero_FI_FA_FO_no_invented_Maria_defaults=True,isolated_speech_dispatch_not_whole_VM_header_orUI_execution=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),full_catalogue_UI_naming_localization_entry_fonts_actual_release_pending=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTEXT,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('Maria3/mask8:36 dispatches,18 effective bodies,four original getters,voices19->7/104->0 pass. Raw bodies unchanged,no macros/defaults. WholeCS0101 header,actual UI andlocalization pending.')
