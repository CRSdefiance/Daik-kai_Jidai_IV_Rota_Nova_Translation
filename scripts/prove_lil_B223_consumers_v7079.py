"""Bind all seventeen effective bodies, original automatic aliases, names and voices to current V7067."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.reconcile_lil_shrines_voices_v3167 import names,dynamic
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B223_source_v7078/all17_clean_current_letter_notices_reactions_full1316_inverse.json')
INPUT=Path('work/analysis/current_V7067_native_v7077/current_native_input.json')
ROOT=Path('work/analysis/lil_B223_consumers_v7079')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert packet['all17_source_glosses_precede_old_English_comparison']
    image=NdsImage.open(packet['current_ROM']);clean=NdsImage.open('work/clean.nds');assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']==read(INPUT)['current_ROM_sha256']
    ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch','whole_style_command','catalog_style_getters']:
        text=inspect.getsource(getattr(inherited,name))
        if name=='bind_current_catalog':text=checked_text(text,{'assert len(payload)==123040':"assert len(payload)==123264 and sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'"})
        if name=='catalog_style_getters':text=checked_text(text,{'len(rows)==3312':'len(rows)==414'})
        adapters[name]=text;exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    catalog=ctx.execute(names);ctx.machines.pop();roles=ctx.execute(dynamic);ctx.machines.pop();static=ctx.execute(selectors,[2,13,21]);ctx.machines.pop()
    assert len(catalog['rows'])==207 and {r['original_voice_class'] for r in catalog['rows']}==set(range(8));d0=next(r for r in roles['rows'] if r['source_selector']==208)
    bp=ROOT/'all467_current_name_catalog_rows_bound.json';save(bp,binding);cases=[];effective=[]
    for row in packet['records']+packet['typed_actor_style_records']:
        spoken=row['kind']=='progressive'
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            value=bytes.fromhex(row[key]);body=value[1:] if spoken else value;prefix=row['source_selector'];result=ctx.execute(ns['dispatch'],prefix,body);ctx.machines.pop()
            assert result['resolved_actor_ID']==(prefix if prefix<207 else d0['resolved_actor_ID']);cases.append(dict(id=row['id'],version=version,**result))
            if version=='current-English':
                boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');runtime=bytes.fromhex(boundary['text_hex']);expected,match=ns['expanded_current_body'](body);assert runtime==expected and result['registered_catalog_match']==match is None
                effective.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],stored_template_hex=body.hex(),effective_runtime_template_hex=body.hex(),expanded_runtime_hex=runtime.hex(),effective_runtime_English=runtime.decode('cp932'),effective_predecessor_paragraph=' '.join(runtime.decode('cp932').split()),registered_catalogue_match=None,source_selector=prefix,resolved_actor_ID=result['resolved_actor_ID'],source_voice_class=result['source_voice_class'],native_UI_body_unexecuted=True))
    whole=[];objects=[]
    for obj in packet['blocks'][0]['actor_style_objects']:
        versions=[]
        for label,key,im in [('clean','source_command',clean),('current','current_command',image)]:
            block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[223];command=obj[key];result=ctx.execute(ns['whole_style_command'],block,command);ctx.machines.pop();whole.append(dict(version=label,block=223,command_offset=obj['command_offset'],**result))
            value=bytes.fromhex(command['whole_command_hex']);slots=[]
            for style in range(8):
                relative=20+struct.unpack_from('<H',value,2+style*2)[0];body=value[relative:value.index(0,relative)];slots.append(dict(style_index=style,relative_offset=relative,hex=body.hex()))
            versions.append(dict(version=label,command_hex=value.hex(),style_slots=slots))
        objects.append(dict(block=223,command_offset=obj['command_offset'],versions=versions))
    styleproof=ctx.execute(ns['catalog_style_getters'],objects);ctx.machines.pop()
    assert len(cases)==34 and len(effective)==17 and len(whole)==2 and len(styleproof['cases'])==414 and not ctx.machines
    save(ROOT/'all17_effective_bodies34_dispatches_two_whole_commands414_style_pointers.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),catalog=catalog,dynamic_roles=roles,static_selectors=static,actual_D0_current_opening_resolution=d0,all207_names_and_eight_styles_bound_not_new_editorial_approval=True,speech_and_alternative_dispatch_cases=cases,effective_current_records=effective,whole_4100_commands=whole,all207_catalog_style_pointer_cases=styleproof,source_aliases_preserved_by_exact_headers_and_getters=True,no_forced_actor_role_roster_or_event=True,current_opening_context_not_natural_B223_activation=True,registered_catalog_binding=str(bp),registered_catalog_binding_sha256=sha(bp.read_bytes()),source_owned_adapters=adapters,related_Timur_mail_item_title_and_consumers_pending=True,all_source_macro_counts=packet['source_macro_counts'],all_UI_bodies_explicit_unexecuted_boundaries=True,source4500_4621_letter_picture_staging_relative_predicate_effect_and_complete_end_semantics_pending=True,current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),names_contextual_retention_or_revision_native_font_proof_and_all17_prose_decisions_pending=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(inherited.__file__),Path(__file__)]},full_goal_complete=False))
    print(dict(dispatches=34,effective_bodies=17,whole_commands=2,style_pointers=414,D0=d0));print('Names',[(r['actor_ID'],r['current_catalog_name'],r['original_voice_class']) for r in catalog['rows'] if r['actor_ID'] in [2,13,21,d0['resolved_actor_ID']]])
