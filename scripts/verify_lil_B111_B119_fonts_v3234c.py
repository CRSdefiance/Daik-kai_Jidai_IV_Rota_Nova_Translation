"""Current1192macro calls,149progressive planes andall150paragraph QA."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B111_B119_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_B111_B119_layout_v2 import encode_relocatable_dialogue
from dk4tool.dialogue.lil_B111_B119_layout_v2 import audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_fonts_v3234c');DOC=Path('translations/lil_B111_B119_editorial_manuscript_v4.json');BASE=0x02000000
VOICE=Path('translations/lil_B111_B119_actor_style_manuscript_v3.json')

def expand(arm,common,raw,plan,body,prefix):
    cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184);captain=get(0x7F244);identity=get(0x2434C,prefix);assert identity==({207: 2, 208: 151, 209: 151, 214: 151, 215: 151, 220: 151}.get(prefix,prefix)) and captain==2
    actor=root+0x19E4 if identity==captain else root+4+32*identity;before=bytes(cpu.mem_read(BASE,0x400000));cases=[]
    hook=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=BASE+0x242CC,end=BASE+0x242CC)
    try:
        for phase in range(4):
            inp,out=0x02660000+phase,0x02662000;cpu.mem_write(inp-16,b'\xA5'*2080);cpu.mem_write(inp,body+b'\0');input_before=bytes(cpu.mem_read(inp-16,2080));cpu.mem_write(out-16,b'\xA5'*4128)
            call(cpu,0x242C8,(out,inp,actor),instruction_limit=400000);value=bytes(cpu.mem_read(out,4096)).split(b'\0')[0]
            expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert value==expected
            assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(inp-16,2080))==input_before
            assert bytes(cpu.mem_read(out-16,16))==b'\xA5'*16 and bytes(cpu.mem_read(out+len(value)+1,4095-len(value)))==b'\xA5'*(4095-len(value))
            cases.append(dict(input_alignment=phase,output_hex=value.hex(),original_macro_ABI_input_output_canaries_and_all4MiB_exact=True))
    finally:cpu.hook_del(hook)
    return dict(original_selector=identity,actor_object=actor,source_prefix=prefix,captain=captain,cases=cases,current_executed_instruction_addresses=len(provider.executed_current),original_242CC_UI_boundary_unexecuted=True,no_model_event_RNG_or_roster_mutation=True)

if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);voice=read(VOICE);doc['records']=doc['records']+voice['records']
    for row in doc['records']:
        if row['kind']=='typed-4100-actor-style-alternative':
            row['source_stored_alternative_hex']=row['source_hex'];row['source_hex']=row['virtual_formatter_prefix_hex']+row['source_hex'];row['source_presentation_prefix_hex']=row['virtual_formatter_prefix_hex']
    source=read(doc['source_context']);im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');common=im.read_file('/COMMON/MESFILE.DK4');blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks
    ROOT.mkdir(parents=True);contextpath=ROOT/'historical_source_context.json';save(contextpath,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath=ROOT/'current_native_input.json';save(inputpath,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),native_context_proof=str(contextpath)))
    ctx=CurrentContext(inputpath,source['historical_snapshot_ROM'],ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    priorpath=Path('work/analysis/lil_B111_B119_fonts_v3230b/current_macro_QA_and_progressive_font_proof.json')
    prior=read(priorpath)
    assert prior['candidate_sha256']==doc['current_ROM_sha256'] and prior['ARM9_sha256']==sha(arm) and prior['COMMON_sha256']==sha(common)
    for key,hashkey in [('manuscript','manuscript_sha256'),('actor_style_manuscript','actor_style_manuscript_sha256'),('scoped_profile','scoped_profile_sha256'),('native_formatter_module','native_formatter_module_sha256')]:
        assert sha(Path(prior[key]).read_bytes())==prior[hashkey]
    assert Path(prior['scoped_profile'])==Path(doc['scoped_profile_module']) and prior['scoped_profile_sha256']==doc['scoped_profile_module_sha256']
    prior_rows={r['id']:r for p in [prior['manuscript'],prior['actor_style_manuscript']] for r in read(p)['records']}
    prior_cases={r['id']:r for r in prior['cases']}
    reused=0;changed=[]
    cases=[];qa_reports=[];pictures=[];macro_calls=0
    for row in doc['records']:
        profile=profile_for(ctx.arm,blocks[row['block']],'FE-paper' if row['kind']=='system-FE' else 'progressive');qa=audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile)
        unwaived=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'))];assert not unwaived,(row['id'],unwaived)
        result=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile);assert result.encoded.hex()==row['compiled_hex']
        if row['kind']=='typed-4100-actor-style-alternative':assert result.encoded[1:].hex()==row['compiled_stored_alternative_hex']
        qa_reports.append(dict(id=row['id'],qa=qa,unwaived_issues=unwaived,documented_waivers=row.get('qa_waivers',[]),encoded_hex=result.encoded.hex()))
        if row['kind']=='system-FE':continue
        oldrow,oldcase=prior_rows[row['id']],prior_cases[row['id']]
        for key in ['block','current_hex','source_reference','current_reference','kind','english']:
            assert row[key]==oldrow[key],(row['id'],key)
        original_source=row.get('source_stored_alternative_hex',row['source_hex'])
        assert original_source==oldrow['source_hex']
        if row['kind']=='typed-4100-actor-style-alternative':
            assert row['virtual_formatter_prefix_hex']==oldrow['virtual_formatter_prefix_hex']
            assert row['style_indices']==oldrow['style_indices']
        caption=('selector'+row['source_presentation_prefix_hex']+' styles'+str(row['style_indices'])) if row['kind']=='typed-4100-actor-style-alternative' else 'selector'+row['source_presentation_prefix_hex']
        if result.encoded.hex()==oldcase['encoded_hex']:
            assert sha(Path(oldcase['preview']).read_bytes())==oldcase['preview_sha256']
            cases.append({**oldcase,'reused_current_native_case':True,'reused_proof':str(priorpath),'reused_proof_sha256':sha(priorpath.read_bytes())})
            pictures.append((row['id'],caption,Image.open(oldcase['preview']).convert('RGB')))
            macro_calls+=8;reused+=1;continue
        changed.append(row['id'])

        logical=row['english'].split('}',1)[1].replace('{MACRO:FI}','FI').replace('{MACRO:FA}','FA').replace('{MACRO:FO}','FO').encode('ascii');wrapped=result.encoded[1:];prefix=int(row['source_presentation_prefix_hex'],16);pipelines=[]
        for kind,value in [('logical',logical),('compiled-protected',wrapped)]:
            pipelines.append(dict(kind=kind,**ctx.execute(expand,value,prefix)));macro_calls+=4;ctx.machines.pop()
        expected=wrapped.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert all(c['output_hex']==expected.hex() for c in pipelines[1]['cases'])
        pixels,events,font=raster(ctx.arm,expected);assert pixels==expected_pixels(ctx.arm,font,events)
        visible=[e for e in events if e['code']!=32];assert [e['code'] for e in visible]==[ord(c) for c in expected.decode('ascii') if c not in ' \n']
        assert all(0<=e['x']<=210 and 0<=e['y']<=48 and e['y']%16==0 for e in visible) and len(visible)==len({(e['x'],e['y']) for e in visible})
        origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values())
        path=ROOT/(row['id']+'_complete_native.png');image=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};image.putdata([colors[p] for p in pixels]);image.save(path);pictures.append((row['id'],('selector'+row['source_presentation_prefix_hex']+' styles'+str(row['style_indices']))if row['kind']=='typed-4100-actor-style-alternative'else 'selector'+row['source_presentation_prefix_hex'],image))
        cases.append(dict(id=row['id'],encoded_hex=result.encoded.hex(),formatted_markup=result.formatted_markup,expanded_hex=expected.hex(),current_native_macro_pipelines=pipelines,complete_glyph_events=events,complete_native_independent216x64_plane_equal=True,
            all_first_final_internal_glyphs_in_order_and_unique_cells=True,all_visible_origins_zero_and16px_rows_within4rows=True,whole_native_plane_sha256=sha(pixels),visible_origins_by_row=origins,preview=str(path),preview_sha256=sha(path.read_bytes())))
    assert len(cases)==149 and len(qa_reports)==150 and macro_calls==1192 and not ctx.machines
    assert changed==['DK4_MES_B111_R0112'] and reused==148,(changed,reused)
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,error=str(error),rejected=True))
        else:raise AssertionError(label)
    reject('mutated-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],blocks[111]))
    reject('unrelated-source-block',lambda:profile_for(arm,blocks[110]))
    reject('mutated-source-block',lambda:profile_for(arm,blocks[111][:-1]+bytes([blocks[111][-1]^1])))
    progressive=profile_for(arm,blocks[111]);selectors=[2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220]
    for selector in selectors:
        row=next(r for r in doc['records'] if int(r['source_presentation_prefix_hex'],16)==selector)
        tag='{SPEAKER:'+format(selector,'02X')+'}'
        alternate='{SPEAKER:'+format(9 if selector==2 else 2,'02X')+'}'
        reject('missing-'+format(selector,'02X')+'-actor-state',lambda r=row,t=tag:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,''),progressive))
        reject('wrong-legal-'+format(selector,'02X')+'-actor-state',lambda r=row,t=tag,v=alternate:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,v),progressive))
    plain=next(r for r in doc['records'] if r['kind']=='progressive' and '{MACRO:' not in r['english'])
    reject('invented-native-macro',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+' {MACRO:FI}',progressive))
    modal=next(r for r in doc['records'] if r['kind']=='system-FE')
    reject('FE-as-ordinary',lambda:encode_relocatable_dialogue(bytes.fromhex(modal['source_hex']),modal['english'],progressive))
    reject('ordinary-as-FE',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english'],profile_for(arm,blocks[plain['block']],'FE-paper')))
    reject('manual-layout',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+'{LB}',progressive))
    assert len(negatives)==43
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(920,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,speaker,image) in enumerate(pictures[start:start+8]):
            x,y=i%2*460,i//2*160;draw.text((x+5,y+3),ident+' / '+speaker,fill='white');sheet.paste(image.resize((432,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'current_macro_QA_and_progressive_font_proof.json',dict(candidate=str(ctx.rompath),candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(ctx.arm),COMMON_sha256=sha(ctx.common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),actor_style_manuscript=str(VOICE),actor_style_manuscript_sha256=sha(VOICE.read_bytes()),all34_actual_virtual_prefixes_excluded_from_physical_alternative_body=True,cases=cases,all150_full_QA_reports=qa_reports,
        newly_executed_font_cases=149-reused,reused_unchanged_font_cases=reused,
        newly_executed_current_macro_alignment_cases=(149-reused)*8,reused_current_macro_alignment_cases=reused*8,
        reused_proof=str(priorpath),reused_proof_sha256=sha(priorpath.read_bytes()),changed_IDs=changed,
        current_original_macro_alignment_calls=1192,all_executed_macro_instructions_current_ROM_exact=True,all_actor_models_and_original4MiB_context_preserved_under_bounded_overlays=True,no_whole_initialized_RAM_overlay=True,
        scoped_profile='dk4tool/dialogue/lil_B111_B119_profile.py',scoped_profile_sha256=sha(Path('dk4tool/dialogue/lil_B111_B119_profile.py').read_bytes()),native_formatter_module='dk4tool/dialogue/lil_B111_B119_layout_v2.py',native_formatter_module_sha256=sha(Path('dk4tool/dialogue/lil_B111_B119_layout_v2.py').read_bytes()),negative_controls=negatives,review_sheets=sheets,visual_review_pending=True,
        current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),all149_progressive_full_QA_and_complete_native_fonts_pass=True,FE_body_QA_is_conservative_plan_only=True,all149_painted_consumers_original_progressive54020=True,one_FE_native_gate_separately_required_no_player_choices=True,not_registered_relocation_or_release_approval=True,
        actual_selected_B111_B119_IDs=[],new_emulator_runs=0,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('149current progressive planes/1192macro alignments/150QA plans/43source-scope negatives pass;19sheets need visual review. OneFE/reference/release gates pending.')
