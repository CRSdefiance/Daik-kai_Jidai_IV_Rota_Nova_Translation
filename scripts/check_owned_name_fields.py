"""Check source-bound fixed-slot names with fresh constructors and native glyph planes."""
import argparse
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
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.audit_story_glyph_consistency import load,save
from scripts.execute_map_entity_tooltip_copy import machine_for
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.probe_button_prompt_native import call,machine as paint_machine
from scripts.prove_lil_B167_names_v4124b import names as original_names
from scripts import lil_B207_name_style_v6354d as style
from scripts.shady_man_font_oracles_v6263 import PROGRESSIVE_ORACLE_SOURCE
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels,raster
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ['proposal','names','out']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    proposal,binding=map(load,[args.proposal,args.names]);runtime=proposal['runtime']
    assert binding['runtime']==runtime
    parent=NdsImage.open(runtime['candidate']);arm=parent.read_file('/__arm9__.bin')
    assert sha(Path(runtime['candidate']).read_bytes())==runtime['candidate_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(clean)==load(proposal['clean_name_fields'])['source_ARM9_sha256']
    target,proof=plan_arm9_name_fields(arm,proposal,clean)
    args.out.mkdir(parents=True);targetpath=args.out/'proposed_owned_name_fields_ARM9_RESEARCH_ONLY.bin';targetpath.write_bytes(target)
    actors=sorted({r['actor'] for r in proposal['fields']})
    old_rows=[r for r in binding['current_names']['rows'] if r['actor_ID'] in actors]
    expected={(r['actor_ID'],r['consumer']):r['text'] for r in old_rows}
    adapter=binding['source_owned_current_adapter'];versions=[]
    for version,value in [('current',arm),('proposed',target)]:
        sections=MainCodeFile(value,BASE).sections;payload=bytes(sections[3].data[:-48]);state={}
        def machine(a,c,r,p):
            assert a==value and c==b'' and r==b'' and p=={'ordinary_constructor_fixture':True}
            cpu=machine_for(a);cpu.mem_write(POOL,payload);before=bytes(cpu.mem_read(BASE,0x400000));executed=set()
            owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
            def exact(u,pc,size,_):
                hit=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
                assert len(hit)==1,hex(pc)
                owner=hit[0];assert bytes(u.mem_read(pc,size))==bytes(owner.data[pc-owner.ramAddress:pc-owner.ramAddress+size]);executed.add(pc)
            hook=cpu.hook_add(UC_HOOK_CODE,exact)
            root=struct.unpack_from('<I',a,0xCB18C)[0];objects=[]
            for ident in actors:
                ordinary_getter(a,ident,machine=cpu);objects.append(root+4+ident*32)
            constructed=bytes(cpu.mem_read(BASE,0x400000));inverse=bytearray(constructed)
            for actor in objects:inverse[actor-BASE:actor-BASE+4]=before[actor-BASE:actor-BASE+4]
            assert bytes(inverse)==before
            def get(offset,*values):
                call(cpu,offset,tuple(values));return cpu.reg_read(UC_ARM_REG_R0)
            state.update(cpu=cpu,before=before,constructed=constructed,objects=objects,hook=hook)
            return cpu,get,SimpleNamespace(executed_current=executed)
        env={**original_names.__globals__,'ACTORS':actors,'machine':machine}
        exec(compile(adapter,__file__+'::original-name-consumers','exec'),env)
        result=env['names'](value,b'',b'',{'ordinary_constructor_fixture':True})
        for row in result['rows']:
            wanted=expected[row['actor_ID'],row['consumer']]
            if version=='proposed':
                for field in proposal['fields']:
                    if field['actor']==row['actor_ID']:wanted=wanted.replace(field['current_text'],field['target_text'])
            assert row['text']==wanted,(row['actor_ID'],row['consumer'],row['text'],wanted)
        cpu=state['cpu'];assert bytes(cpu.mem_read(BASE,0x400000))==state['constructed']
        for actor in state['objects']:cpu.mem_write(actor,state['before'][actor-BASE:actor-BASE+4])
        assert bytes(cpu.mem_read(BASE,0x400000))==state['before'];cpu.hook_del(state['hook'])
        versions.append(dict(version=version,ARM9_sha256=sha(value),names=result,
            ordinary_constructor_andname_ring_inverse_recovers_all4MiB=True,no_startup_orhistorical_RAM_overlay=True))
    oracle_env={**expected_pixels.__globals__}
    exec(compile(PROGRESSIVE_ORACLE_SOURCE,__file__+'::independent-font','exec'),oracle_env)
    planes=[];bindings=[];known={};pictures=[]
    for index,(version,value) in enumerate([('current',arm),('proposed',target)]):
        source_style=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':sha(value)})
        styleproof=source_style(value)
        sections=MainCodeFile(value,BASE).sections;payload=bytes(sections[3].data[:-48]);owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
        def machine_for_paint(a):
            assert a==value;cpu=paint_machine(a)
            def exact(u,pc,size,_):
                hit=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
                assert len(hit)==1,hex(pc)
                owner=hit[0];assert bytes(u.mem_read(pc,size))==bytes(owner.data[pc-owner.ramAddress:pc-owner.ramAddress+size])
            cpu.hook_add(UC_HOOK_CODE,exact);return cpu
        for row in versions[index]['names']['rows']:
            raw=bytes.fromhex(row['text_hex'])
            # Style11 is the proven progressive name caller. Style1 is a second
            # native text-plane test; this does not assert an observed catalogue UI.
            for native_style in [11,1]:
                key=(raw,native_style)
                if key in known:
                    bindings.append(dict(version=version,actor=row['actor_ID'],consumer=row['consumer'],style=native_style,plane=known[key],exact_string_style_font_andcode_inverse_reuse=True));continue
                env={**raster.__globals__,'machine':machine_for_paint}
                source=style.NATIVE_NAME_RASTER_SOURCE if native_style==11 else __import__('inspect').getsource(raster)
                exec(compile(source,__file__+'::native-name-plane','exec'),env)
                pixels,events,font=env['raster'](value,raw)
                assert font==parent.read_file('/GRP/KANJI.FNT')
                assert pixels==oracle_env['expected_pixels'](value,font,events)
                visible,flushes=original_name_events(events,raw);assert visible==codes(raw)
                assert all(e['style']==native_style and e['y']==0 and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events)
                if version=='proposed':assert all(e['kind']=='ascii' for e in events)
                number=len(planes);known[key]=number
                plane=args.out/f'name_plane_{number:02d}.bin';plane.write_bytes(pixels)
                pic=Image.new('RGB',(216,64));pic.putdata([(65,53,42) if p else (250,245,223) for p in pixels])
                preview=plane.with_suffix('.png');pic.save(preview);pictures.append((f'{version} A{row["actor_ID"]} S{native_style} '+row['text'],pic))
                planes.append(dict(version=version,text=row['text'],style=native_style,plane=str(plane),plane_sha256=sha(pixels),events=events,
                    source_character_codes=visible,only_native_zero_ink_flushes=flushes,progressive_style_proof=styleproof,
                    preview=str(preview),preview_sha256=sha(preview.read_bytes()),complete_glyphs_bounds_andindependent_pixels_pass=True))
                bindings.append(dict(version=version,actor=row['actor_ID'],consumer=row['consumer'],style=native_style,plane=number))
    sheet=Image.new('RGB',(900,len(pictures)*80),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,pic) in enumerate(pictures):
        draw.text((4,i*80+2),label,fill='white');sheet.paste(pic.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(4,i*80+17))
    sheetpath=args.out/'native_names_review.png';sheet.save(sheetpath)
    negatives=[]
    for kind in ['stale-parent','wrong-source','wrong-clean','adjacent-slot','false-owner','unexpected-pointer','control-target','unreviewed']:
        other=deepcopy(proposal);a,c=arm,clean;f=other['fields'][0]
        if kind=='stale-parent':a=arm[:-1]+bytes([arm[-1]^1])
        elif kind=='wrong-source':f['source_hex']='00'*f['owned_bytes']
        elif kind=='wrong-clean':c=clean[:f['source_clean_component']['offset']]+b'X'+clean[f['source_clean_component']['offset']+1:]
        elif kind=='adjacent-slot':f['following16_hex']='00'*16
        elif kind=='false-owner':f['owners']=[]
        elif kind=='unexpected-pointer':f['aligned_ARM9_references']=[]
        elif kind=='control-target':f['target_hex']='01'+f['target_hex'][2:]
        else:f['review']['source']=False
        try:plan_arm9_name_fields(a,other,c)
        except (ValueError,UnicodeError):negatives.append(kind)
        else:raise AssertionError(kind)
    save(args.out/'native_name_fields_verification.json',dict(proposal=str(args.proposal),proposal_sha256=sha(args.proposal.read_bytes()),
        name_data_plan=proof,proposed_ARM9=str(targetpath),versions=versions,planes=planes,consumer_plane_bindings=bindings,negative_cases_rejected=negatives,
        original_progressive_andfull_name_getters_pass=True,no_historical_RAM_overlay=True,
        offline_constructor_fixture_not_own_coldboot_context=True,actual_header_catalogue_UI_startup_andregistered_deployment_pending=True,
        direct_view_pending=True,review_sheet=dict(path=str(sheetpath),sha256=sha(sheetpath.read_bytes())),
        no_ROM_created=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.proposal,args.names,Path('dk4tool/patch/owned_name_fields_v2.py'),Path(__file__)]}))
    print(dict(getters=sum(len(v['names']['rows']) for v in versions),unique_name_planes=len(planes),consumer_style_bindings=len(bindings),negatives=len(negatives),proposed_ARM9_sha256=sha(target),actual_pending=True))

if __name__=='__main__':main()
