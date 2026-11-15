"""Prove the proposed name through new ordinary constructors, not an old RAM overlay."""
import inspect
import struct
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace,FunctionType
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_glyph_v1 import plan_arm9_name_glyph
from scripts.audit_story_glyph_consistency import load,save
from scripts.execute_map_entity_tooltip_copy import machine_for
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.probe_button_prompt_native import call,machine as paint_machine
from scripts.prove_lil_B167_names_v4124b import names as original_names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import lil_B207_name_style_v6354d as style
from scripts.shady_man_font_oracles_v6263 import PROGRESSIVE_ORACLE_SOURCE
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events

PROPOSAL=Path('work/analysis/Emilio_name_glyph_20261101/owned_field_proposal.json')
NAMES=Path('work/analysis/Hodram_B81_B90_new_names_20261101/names.json')
ROOT=Path('work/analysis/Emilio_name_glyph_native_20261101')

if __name__=='__main__':
    assert not ROOT.exists();proposal,binding=map(load,[PROPOSAL,NAMES])
    parent=NdsImage.open(proposal['runtime']['candidate']);arm=parent.read_file('/__arm9__.bin')
    assert sha(Path(proposal['runtime']['candidate']).read_bytes())==proposal['runtime']['candidate_sha256']
    target,proof=plan_arm9_name_glyph(arm,proposal);ROOT.mkdir(parents=True)
    targetpath=ROOT/'proposed_name_data_ARM9_RESEARCH_ONLY.bin';targetpath.write_bytes(target)
    adapter=binding['source_owned_current_adapter'];versions=[];all_executed=set()
    for version,value in [('current',arm),('proposed',target)]:
        sections=MainCodeFile(value,BASE).sections;payload=bytes(sections[3].data[:-48]);state={}
        def machine(a,c,r,p):
            assert a==value and c==b'' and r==b'' and p=={'ordinary_constructor_fixture':True}
            cpu=machine_for(a);cpu.mem_write(POOL,payload);before=bytes(cpu.mem_read(BASE,0x400000));executed=set()
            def exact(u,pc,size,_):
                if POOL<=pc and pc+size<=POOL+len(payload):expected=payload[pc-POOL:pc-POOL+size]
                else:
                    assert BASE<=pc and pc+size<=BASE+len(a),hex(pc)
                    expected=a[pc-BASE:pc-BASE+size]
                assert bytes(u.mem_read(pc,size))==expected,hex(pc);executed.add(pc)
            hook=cpu.hook_add(UC_HOOK_CODE,exact)
            ordinary_getter(a,14,machine=cpu)
            root=struct.unpack_from('<I',a,0xCB18C)[0];actor=root+4+14*32
            constructed=bytes(cpu.mem_read(BASE,0x400000));inverse=bytearray(constructed)
            inverse[actor-BASE:actor-BASE+4]=before[actor-BASE:actor-BASE+4]
            assert bytes(inverse)==before
            def get(offset,*args):
                call(cpu,offset,tuple(args));return cpu.reg_read(UC_ARM_REG_R0)
            state.update(cpu=cpu,before=before,constructed=constructed,actor=actor,hook=hook)
            return cpu,get,SimpleNamespace(executed_current=executed)
        env={**original_names.__globals__,'ACTORS':[14],'machine':machine}
        exec(compile(adapter,__file__+'::ordinary-constructor-name-fixture','exec'),env)
        result=env['names'](value,b'',b'',{'ordinary_constructor_fixture':True})
        assert [r['text'] for r in result['rows']]==[proposal['current_full_andprogressive_name'] if version=='current' else proposal['proposed_full_andprogressive_name']]*2
        cpu=state['cpu'];assert bytes(cpu.mem_read(BASE,0x400000))==state['constructed']
        actor=state['actor'];cpu.mem_write(actor,state['before'][actor-BASE:actor-BASE+4])
        assert bytes(cpu.mem_read(BASE,0x400000))==state['before'];cpu.hook_del(state['hook'])
        versions.append(dict(version=version,ARM9_sha256=sha(value),names=result,
            ordinary_constructor_andname_ring_inverse_recovers_all4MiB=True,
            current_startup_RAM_andhistorical_RAM_never_loaded=True))
    oracle_env={**expected_pixels.__globals__}
    exec(compile(PROGRESSIVE_ORACLE_SOURCE,__file__+'::independent-complete-font','exec'),oracle_env)
    planes=[];sheet=Image.new('RGB',(900,180),'#263238');draw=ImageDraw.Draw(sheet)
    for index,(version,value) in enumerate([('current',arm),('proposed',target)]):
        # Rebind only the exact current ARM9 identity; unchanged style caller is
        # independently compared with clean Japanese by the original proof.
        source_style=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':sha(value)})
        styleproof=source_style(value)
        sections=MainCodeFile(value,BASE).sections;payload=bytes(sections[3].data[:-48]);owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
        def machine_for_paint(a):
            assert a==value;cpu=paint_machine(a)
            def exact(u,pc,size,_):
                hit=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
                assert len(hit)==1,hex(pc)
                owner=hit[0];assert bytes(u.mem_read(pc,size))==bytes(owner.data[pc-owner.ramAddress:pc-owner.ramAddress+size])
                all_executed.add(pc)
            cpu.hook_add(UC_HOOK_CODE,exact);return cpu
        env={**style.inherited_raster.__globals__,'machine':machine_for_paint}
        exec(compile(style.NATIVE_NAME_RASTER_SOURCE,__file__+'::original-style11','exec'),env)
        raw=bytes.fromhex(versions[index]['names']['rows'][0]['text_hex'])
        pixels,events,font=env['raster'](value,raw)
        assert font==parent.read_file('/GRP/KANJI.FNT')
        assert pixels==oracle_env['expected_pixels'](value,font,events)
        visible,flushes=original_name_events(events,raw);assert visible==codes(raw)
        assert all(e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events)
        if version=='proposed':assert all(e['kind']=='ascii' for e in events) and raw==b'Emilio Ferog'
        pic=Image.new('RGB',(216,64));pic.putdata([(65,53,42) if p else (250,245,223) for p in pixels])
        preview=ROOT/f'{version}_complete_native_name.png';pic.save(preview)
        plane=ROOT/f'{version}_complete_native_name.bin';plane.write_bytes(pixels)
        draw.text((4,index*90+3),version+' '+raw.decode('cp932'),fill='white')
        sheet.paste(pic.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(4,index*90+22))
        planes.append(dict(version=version,text=raw.decode('cp932'),plane=str(plane),plane_sha256=sha(pixels),events=events,
            source_character_codes=visible,only_native_zero_ink_flushes=flushes,style_proof=styleproof,
            preview=str(preview),preview_sha256=sha(preview.read_bytes()),complete_glyphs_bounds_andindependent_pixels_pass=True))
    sheetpath=ROOT/'current_andproposed_native_name.png';sheet.save(sheetpath)
    negatives=[]
    for kind in ['stale-parent','wrong-source','adjacent-slot','false-owner']:
        other=deepcopy(proposal);rawarm=arm
        if kind=='stale-parent':rawarm=arm[:-1]+bytes([arm[-1]^1])
        elif kind=='wrong-source':other['source_hex']='00'*8
        elif kind=='adjacent-slot':other['following8_Ferid_hex']='00'*8
        else:other['all207_name_fields_interior_oralias_owners']=[]
        try:plan_arm9_name_glyph(rawarm,other)
        except ValueError:negatives.append(kind)
        else:raise AssertionError(kind)
    save(ROOT/'native_name_glyph_verification.json',dict(proposal=str(PROPOSAL),proposal_sha256=sha(PROPOSAL.read_bytes()),
        name_data_plan=proof,proposed_ARM9=str(targetpath),versions=versions,planes=planes,negative_cases_rejected=negatives,
        offline_constructor_fixture_not_own_coldboot_context=True,no_historical_RAM_overlay=True,
        original_progressive_andfull_name_getters_pass=True,actual_header_catalogue_UI_startup_andregistered_deployment_pending=True,
        direct_view_pending=True,review_sheet=dict(path=str(sheetpath),sha256=sha(sheetpath.read_bytes())),
        no_ROM_created=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PROPOSAL,NAMES,Path(style.__file__),Path('dk4tool/patch/owned_name_glyph_v1.py'),Path(__file__)]}))
    print(dict(getters=4,name_planes=2,negatives=len(negatives),proposed_ARM9_sha256=sha(target),no_ROM_created=True,actual_pending=True))
