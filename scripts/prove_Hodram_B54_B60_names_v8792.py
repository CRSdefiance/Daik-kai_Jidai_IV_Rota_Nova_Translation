"""Bind ten source identities and current native names/voices; no scene or full-catalogue claim."""
import inspect,struct
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B31_B53_registered_route_context_v8781 import RouteCurrentContext
from scripts.prove_Hodram_B31_actor34_names_v8719 import current_fields
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts.audit_native_given_name_table import string,ordinary_getter
from scripts.execute_map_entity_tooltip_copy import machine_for,BASE,STACK,STOP
from scripts import lil_B207_name_style_v6354d as style
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from types import FunctionType

ROOT=Path('work/analysis/Hodram_B54_B60_names_v8792')
GLOSS=Path('work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json')
CONTROL=Path('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json')
INPUT=Path('work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json')
VIEW=Path('work/analysis/Hodram_B31_B53_registered_startup_view_v8782/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
CLEAN_PRECEDENT=Path('work/analysis/Hodram_actor34_clean_name_composition_v8732/clean_source_full_andprogressive_name_composition.json')

if __name__=='__main__':
    assert not ROOT.exists();gloss,control,inp,view,precedent=map(read,[GLOSS,CONTROL,INPUT,VIEW,CLEAN_PRECEDENT])
    assert control['current_B54_B60_English_dialogue_bodies_still_unconsulted'] and gloss['all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English']
    actors=sorted({r['source_selector'] for g in gloss['groups'] for r in g['records'] if r['source_selector']!=254})
    assert actors==[1,20,23,24,36,84,113,114,119,141] and sum(r['source_selector']==254 for g in gloss['groups'] for r in g['records'])==1
    current,clean=NdsImage.open(inp['current_ROM']),NdsImage.open('work/clean.nds');arm=current.read_file('/__arm9__.bin');ja=clean.read_file('/__arm9__.bin')
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==control['candidate_sha256']==view['candidate_sha256']
    assert view['viewed'] and view['whole_actors_equal'] and sha(ja)==precedent['clean_ARM9_sha256']
    for span in precedent['complete_clean_current_original_consumer_spans']:
        assert arm[span['start']:span['end']]==ja[span['start']:span['end']] and sha(ja[span['start']:span['end']])==span['source_andcurrent_sha256']
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    fields_text=checked_text(inspect.getsource(current_fields),{'for ident in [34, 113]:':'for ident in ACTORS:'})
    env={**current_fields.__globals__,'ACTORS':actors};exec(compile(fields_text,__file__+'::current-fields','exec'),env)
    fields=ctx.execute(env['current_fields']);ctx.machines.pop()
    voice_text=checked_text(inspect.getsource(selectors),{'assert captain==2':'assert captain==1'})
    env={**selectors.__globals__};exec(compile(voice_text,__file__+'::current-voices','exec'),env)
    voices=ctx.execute(env['selectors'],actors);ctx.machines.pop();objects={r['source_selector']:r['actor_object'] for r in voices['rows']}
    names_text=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in ACTORS:',
        'actor = root+4+32*ident':'actor = ACTOR_OBJECTS[ident]',
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_twenty_original_consumers_and_owned_or_readonly_memory_paths_exact',
    })
    env={**names.__globals__,'ACTORS':actors,'ACTOR_OBJECTS':objects};exec(compile(names_text,__file__+'::current-names','exec'),env)
    getters=ctx.execute(env['names']);ctx.machines.pop();assert len(getters['rows'])==20 and len(voices['rows'])==10 and not ctx.machines
    static=[];source_given=[]
    actor_root=precedent['source_native_getters'][0]['actor_fixture']-4-32*34
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    for row in fields['rows']:
        ident=row['actor_ID'];versions={}
        for label,data in [('clean',ja),('current',arm)]:
            values=[]
            for f in row['fields']:
                at=f['table_field'];pointer=struct.unpack_from('<I',data,at)[0]
                values.append(dict(kind=f['kind'],table_field=at,table_field_hex=data[at:at+4].hex(),null_pointer_is_not_empty_string=pointer==0,**string(data,pointer)))
            versions[label]=values
        static.append(dict(actor_ID=ident,**versions))
        cpu=machine_for(ja);before=bytes(cpu.mem_read(BASE,len(ctx.raw)));writes=[];executed=set()
        for i,reg in enumerate(regs):cpu.reg_write(reg,0x5A00+i)
        saved=[cpu.reg_read(r) for r in regs]
        def exact(u,pc,size,unused):
            assert BASE<=pc and pc+size<=BASE+len(ja) and bytes(u.mem_read(pc,size))==ja[pc-BASE:pc-BASE+size]
            executed.add(pc)
        h=cpu.hook_add(UC_HOOK_CODE,exact)
        w=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(address=address,size=size,value=value)),begin=BASE,end=BASE+len(ctx.raw)-1)
        try:pointer=ordinary_getter(ja,ident,machine=cpu)
        finally:cpu.hook_del(h);cpu.hook_del(w)
        given=next(f for f in versions['clean'] if f['kind']=='given');value=bytes(cpu.mem_read(pointer,given['byte_length']+1))
        actor=actor_root+4+32*ident;assert value==bytes.fromhex(given['hex'])+b'\0' and writes and all(v['address']==actor and v['size']==4 for v in writes)
        assert [cpu.reg_read(r) for r in regs]==saved and cpu.reg_read(UC_ARM_REG_SP)==STACK and cpu.reg_read(UC_ARM_REG_PC)==STOP
        cpu.mem_write(actor,before[actor-BASE:actor-BASE+4]);assert bytes(cpu.mem_read(BASE,len(ctx.raw)))==before
        source_given.append(dict(actor_ID=ident,text=given['text'],text_hex=given['hex'],native_given_pointer=pointer,original_ordinary_constructor_fixture=actor,
            constructor_writes=writes,all_original_callee_saved_ABI_stack_stop_andunowned_memory_exact=True,all_constructor_writes_reversed_to_initial_clean_memory=True,
            every_instruction_exact_clean_ARM9=True,executed_instruction_addresses=len(executed),not_actual_clean_header_fullname_orcatalogue_UI=True))
    digest=sha(arm);caller=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':digest},argdefs=style.style_source_proof.__defaults__)
    raster=FunctionType(style.native_name_raster.__code__,{**style.native_name_raster.__globals__,'style_source_proof':caller},argdefs=style.native_name_raster.__defaults__)
    pixels,unused,oracle=bind(current);planes=[];pictures=[]
    for n,text in enumerate(dict.fromkeys(r['text'] for r in getters['rows'])):
        encoded=text.encode('cp932');plane,events,font=raster(arm,encoded);emitted,flushes=original_name_events(events,encoded)
        assert font==current.read_file('/GRP/KANJI.FNT') and plane==pixels(arm,font,events) and emitted==codes(encoded)
        assert all(e['style']==11 and e['x']>=0 and e['x']+(6 if e['kind']=='ascii' else 12)<=216 and 0<=e['y']<64 for e in events)
        path=ROOT/f'name{n:02d}.bin';path.write_bytes(plane);picture=Image.new('RGB',(216,64));picture.putdata([(98,97,98) if p else (250,245,223) for p in plane]);preview=path.with_suffix('.png');picture.save(preview)
        planes.append(dict(text=text,input_hex=encoded.hex(),native_glyph_events=events,source_owned_zero_ink_flushes=flushes,native_plane=str(path),native_plane_sha256=sha(plane),preview=str(preview),preview_sha256=sha(preview.read_bytes()),complete_first_internal_final_characters_andbounds=True,full_getter_literal_plane_not_actual_fullcatalogue_UI=True))
        pictures.append((text,picture))
    sheet=Image.new('RGB',(912,((len(pictures)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,picture) in enumerate(pictures):
        x,y=i%2*456,i//2*160;draw.text((x+3,y+3),label+' offline native',fill='white');sheet.paste(picture.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
    sheetfile=ROOT/'ten_actor_current_names.png';sheet.save(sheetfile)
    save(ROOT/'ten_source_identities_current_getters_voices_andplanes.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],ARM9_sha256=digest,
        complete_clean_current_static_fields=static,exact_current_RAM_fields=fields,ten_clean_ordinary_given_getters=source_given,
        fresh_twenty_progressive_andfull_current_getters=getters,ten_source_selector_voices=voices,native_name_planes=planes,
        source_getter_fixture_is_not_actual_clean_player_roster_orfullcatalogue_UI=True,current_captain_object_uses_original_resolver_pointer=True,
        source_fullname_composition_all_speakers_still_requires_separate_scope_qualification=True,
        generic_regional_surname_metadata_not_automatically_personal_surname_nationality_rank_orbiography=True,
        FE254_excluded_from_static_actor_name_getters_andvoice_calls=True,
        current_B54_B60_English_dialogue_bodies_unconsulted=True,scoped_name_editorial_retention_orrevision_still_pending=True,
        no_actual_source_scene_headers_all207_fullcatalogue_orcustomname_approval=True,
        original_name_adapter=names_text,original_voice_adapter=voice_text,original_RAM_field_adapter=fields_text,
        current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        original_style11_caller=caller(arm),font_oracle_binding=oracle,review_sheet=dict(path=str(sheetfile),sha256=sha(sheetfile.read_bytes())),direct_view_pending=True,
        new_credit=0,new_emulator_runs=0,no_ROM_registry_ledger_orprior_artifact_change=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,CONTROL,INPUT,VIEW,CLEAN_PRECEDENT,Path(__file__)]}))
    print('Ten clean given identities /20 current original getters/10voices/'+str(len(planes))+'complete name planes pass. Sourcefull composition/name editorial scope anddirectview pending;no priorEnglish,gameplay,ROM orcredit.',flush=True)
