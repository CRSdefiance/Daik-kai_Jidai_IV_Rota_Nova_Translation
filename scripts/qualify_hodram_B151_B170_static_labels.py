"""Exercise source city87 selection and the original Elysion override/copy/getter, with glyph proofs."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R5,UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.hodram_static_labels_v1 import plan_static_labels,CODE_SPANS
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.probe_button_prompt_native import machine,call,STACK,STOP
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.shady_man_font_oracles_v6263 import PROGRESSIVE_ORACLE_SOURCE
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events

ROOT=Path('work/analysis/Hodram_B151_B170_static_labels_20261102')
PROPOSAL=Path('work/analysis/Hodram_B151_B170_clean_20261102/two_static_text_slots_proposal_v1.json')
RELEASE=Path('work/analysis/Hodram_B131_B150_release_verified_20261102/registered_release_verification.json')

def bounded_machine(arm):
    cpu=machine(arm);sections=MainCodeFile(arm,BASE).sections
    payload=bytes(sections[3].data[:-48]) if len(sections)>3 else b''
    if len(payload)==123264:cpu.mem_write(POOL,payload)
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)] if len(payload)==123264 else sections
    executed=set()
    def exact(u,pc,size,_):
        hits=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)];assert len(hits)==1,hex(pc)
        s=hits[0];assert bytes(u.mem_read(pc,size))==bytes(s.data[pc-s.ramAddress:pc-s.ramAddress+size]);executed.add(pc)
    cpu.hook_add(UC_HOOK_CODE,exact);return cpu,executed

if __name__=='__main__':
    assert not ROOT.exists() or {p.name for p in ROOT.iterdir()}=={'proposed_static_labels_ARM9_RESEARCH_ONLY.bin'}
    proposal=load(PROPOSAL);ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'))
    assert sha(Path(proposal['parent_ROM']).read_bytes())==proposal['parent_ROM_sha256']==ctx.receipt()['candidate_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');target,plan=plan_static_labels(ctx.arm,proposal,clean)
    # Exact source struct: strb at +1B follows the name at +8, hence19 owned bytes.
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);ctor={i.address:i for i in cs.disasm(clean[0xA43C0:0xA443C],BASE+0xA43C0)}
    assert ctor[0x20A43FC].op_str=='r0, r6, #8' and ctor[0x20A4434].op_str=='r0, [r1, #0x1b]'
    assert 0x1B-8==19
    city_index=(0x124CCC-struct.unpack_from('<I',clean,0xCD6C8)[0]+BASE)//0x74;assert city_index==87
    city_root=struct.unpack_from('<I',clean,0xCB180)[0];city_object=city_root+4+city_index*108
    # The startup has the original initialized city object, not a fabricated town.
    assert len(ctx.raw[city_object-BASE:city_object-BASE+108])==108
    ROOT.mkdir(parents=True,exist_ok=True)
    target_path=ROOT/'proposed_static_labels_ARM9_RESEARCH_ONLY.bin'
    if target_path.exists():assert target_path.read_bytes()==target
    else:target_path.write_bytes(target)
    results=[];strings=[]
    for version,arm,city,ship in [('clean',clean,'アブハーズ','エリュシオン'),('current',ctx.arm,'Abhaz','エリュシオン'),('proposed',target,'Abkhaz','Elysion')]:
        cpu,executed=bounded_machine(arm);before=bytes(cpu.mem_read(BASE,0x400000))
        call(cpu,0xB5600,(city_object,));assert cpu.reg_read(UC_ARM_REG_R0)==87
        call(cpu,0xB5690,(city_object,));assert cpu.reg_read(UC_ARM_REG_R0)==BASE+0x124CCC
        call(cpu,0xB5630,(city_object,));city_pointer=cpu.reg_read(UC_ARM_REG_R0)
        city_raw=bytes(cpu.mem_read(city_pointer,32)).split(b'\0')[0];assert city_pointer==BASE+0x15CF74 and city_raw.decode('cp932')==city
        assert bytes(cpu.mem_read(BASE,0x400000))==before
        obj=0x02460020;sentinel=b'\xA5'*(0x8C+32);cpu.mem_write(obj-16,sentinel);writes=[]
        hook=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(address=address,size=size,value=value)),begin=obj-16,end=obj+0x8C+15)
        # Original command suffix: ldr literal; mov object; bl setter. Stops at
        # the actual next instruction, with no replacement return or condition.
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP);cpu.reg_write(UC_ARM_REG_R5,obj)
        cpu.emu_start(BASE+0x2BA08,BASE+0x2BA14,count=10000);assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x2BA14
        cpu.hook_del(hook);ship_raw=ship.encode('cp932');wanted=bytearray(sentinel);wanted[24:24+len(ship_raw)+1]=ship_raw+b'\0'
        assert bytes(cpu.mem_read(obj-16,len(sentinel)))==bytes(wanted)
        assert all(obj+8<=w['address'] and w['address']+w['size']<=obj+8+len(ship_raw)+1 for w in writes)
        call(cpu,0x1A4E0,(obj,));pointer=cpu.reg_read(UC_ARM_REG_R0);assert pointer==obj+8
        assert bytes(cpu.mem_read(pointer,19)).split(b'\0')[0]==ship_raw and bytes(cpu.mem_read(BASE,0x400000))==before
        results.append(dict(version=version,ARM9_sha256=sha(arm),city_index=87,city_object_address=city_object,city_record=BASE+0x124CCC,
            original_city_getter=BASE+0xB5630,city_pointer=city_pointer,city_text=city,city_readonly_all4MiB_exact=True,
            ship_text=ship,ship_command_suffix=[BASE+0x2BA08,BASE+0x2BA14],original_setter=BASE+0xA48F8,original_getter=BASE+0x1A4E0,
            ship_struct_bytes=0x8C,name_field_offset=8,name_field_capacity_with_NUL=19,original_writes=writes,
            all_own_input_strings_original_code_object_neighbors_andunowned4MiB_unchanged=True,
            isolated_native_ship_object_fixture_not_live_ship_orfull_command_activation=True,executed_exact_original_instruction_count=len(executed)))
        strings.extend([(version,'city',city),(version,'ship',ship)])
    oracle=dict(expected_pixels.__globals__);exec(compile(PROGRESSIVE_ORACLE_SOURCE,__file__+'::same-font-oracle','exec'),oracle)
    planes=[];seen={};pictures=[]
    for version,consumer,text in strings:
        raw=text.encode('cp932')
        if raw in seen:continue
        arm=target if version=='proposed' else ctx.arm
        env={**raster.__globals__,'machine':lambda value:bounded_machine(value)[0]}
        exec(compile(__import__('inspect').getsource(raster),__file__+'::existing-native-font-plane','exec'),env)
        pixels,events,font=env['raster'](arm,raw);assert font==ctx.image.read_file('/GRP/KANJI.FNT') and pixels==oracle['expected_pixels'](arm,font,events)
        emitted,flushes=original_name_events(events,raw);assert emitted==codes(raw)
        assert all(e['y']==0 and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events)
        path=ROOT/f'{version}_{consumer}.bin';path.write_bytes(pixels);pic=Image.new('RGB',(216,64));pic.putdata([(0,8,0) if v else (239,232,201) for v in pixels]);png=path.with_suffix('.png');pic.save(png)
        row=dict(source_text_version=version,renderer_ARM9_sha256=sha(arm),consumer=consumer,text=text,plane=str(path),plane_sha256=sha(pixels),events=events,zero_ink_flushes=flushes,
            preview=str(png),preview_sha256=sha(png.read_bytes()),complete_glyphs_bounds_andindependent_font_pixels_pass=True,
            font_plane_not_actual_city_or_ship_widget_geometry_observation=True);planes.append(row);seen[raw]=row;pictures.append((version+' '+consumer+' '+text,pic))
    sheet=Image.new('RGB',(900,len(pictures)*80),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,pic) in enumerate(pictures):
        draw.text((4,i*80+2),label.encode('ascii','replace').decode(),fill='white');sheet.paste(pic.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(4,i*80+18))
    sheetpath=ROOT/'static_labels_native_review.png';sheet.save(sheetpath)
    negatives=[]
    for case in ['stale-parent','wrong-clean','wrong-owner','missing-label','changed-current-slot','oversize-target','changed-target','changed-source-NUL','wrong-capacity','control-target']:
        p=deepcopy(proposal);a=ctx.arm;c=clean
        if case=='stale-parent':a=a[:-1]+bytes([a[-1]^1])
        elif case=='wrong-clean':c=c[:-1]+bytes([c[-1]^1])
        elif case=='wrong-owner':p['fields'][0]['pointer_field_offset']+=4
        elif case=='missing-label':p['fields'].pop()
        elif case=='changed-current-slot':p['fields'][0]['current_full_slot_hex']='00'*11
        elif case=='oversize-target':p['fields'][0]['target_span_hex']=(b'X'*12+b'\0').hex()
        elif case=='changed-target':p['fields'][0]['english']='Abkhazia'
        elif case=='changed-source-NUL':p['fields'][0]['clean_slot_hex']=p['fields'][0]['clean_slot_hex'][:-2]+'20'
        elif case=='wrong-capacity':p['fields'][1]['source_slot_capacity']+=1
        else:p['fields'][1]['target_span_hex']='01'+p['fields'][1]['target_span_hex'][2:]
        try:plan_static_labels(a,p,c)
        except (ValueError,UnicodeError):negatives.append(case)
        else:raise AssertionError(case)
    save(ROOT/'native_static_labels_qualification.json',dict(proposal=str(PROPOSAL),proposal_sha256=sha(PROPOSAL.read_bytes()),runtime=ctx.receipt(),
        complete_owned_data_plan=plan,native_versions=results,planes=planes,review_sheet=dict(path=str(sheetpath),sha256=sha(sheetpath.read_bytes())),
        negative_cases_rejected=negatives,all_native_getter_copy_full_characters_bounds_canaries_andparent_inverse_pass=True,
        city_owner_is_table_record87_original_getter=True,ship_owner_is_original_index3_name_override=True,
        source_name_slot19_bytes_matches_existing18byte_editor_cap_without_replaying_editor=True,
        direct_visual_review_pending=True,actual_label_widgets_andEnglish_gameplay_andregistered_deployment_pending=True,
        new_ROM=False,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PROPOSAL,Path('dk4tool/patch/hodram_static_labels_v1.py'),Path(__file__)]}))
    print('Two fixed labels:15 owned prefix bytes/12 changed bytes;three source/current/proposed native versions,five glyph planes,ten rejected mutations. No ROM created;visual/gameplay/deployment pending.')
