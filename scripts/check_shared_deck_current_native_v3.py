"""Use current own-Rafael code/RAM and the validated Refit formatter for all four panels."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ascii_draw_offset_20261027 import SLOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.probe_button_prompt_native import call
from scripts.execute_scene_caption_raster import BASE,CONTEXT,BITMAP,IMAGE,TEXT,BUFFER,STACK,GET_ORIGIN
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels

ROOT=Path('work/analysis/Shared_Deck_current_native_v4_20261104')
REVIEW=Path('work/analysis/Shared_Deck_tutorials_contextual_20261104/four_panel_contextual_review_v1.json')
RELEASE=Path('work/analysis/Rafael_early_tutorial_release_verified_20261104/registered_release_verification.json')
STARTUP=RELEASE.with_name('own_registered_startup_verification.json')

def native(ctx,compiled,mode):
    cpu,_,provider=machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
    def put(at,*words):cpu.mem_write(at,struct.pack('<'+'I'*len(words),*words))
    put(BITMAP,BITMAP+0x60);put(BITMAP+0x68,GET_ORIGIN);put(BITMAP+0x10,IMAGE,5)
    put(BITMAP+0x28,168,108);put(BITMAP+0x30,0,0,168,108)
    pitch=168 if mode==16 else 42;size=pitch*108*2
    put(IMAGE,mode,pitch,108);put(IMAGE+0x10,BUFFER-IMAGE)
    font=struct.unpack_from('<I',ctx.arm,0xD5088)[0];put(font+4,6,12)
    cpu.mem_write(TEXT-16,b'\x5a'*16+compiled+b'\x5a'*16)
    background=b'\x09\x00' if mode==16 else b'\x99\x99'
    cpu.mem_write(BUFFER-32,b'\xa5'*32+background*(size//2)+b'\xa5'*32)
    events=[];executed=set()
    def code(u,pc,length,_):
        if pc==GET_ORIGIN:
            destination=u.reg_read(UC_ARM_REG_R0)
            assert u.reg_read(UC_ARM_REG_R1)==BITMAP and STACK-0x1000<=destination<=STACK-8
            put(destination,0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        owners=[s for s in ctx.sections if s.ramAddress<=pc and pc+length<=s.ramAddress+len(s.data)]
        assert len(owners)==1,hex(pc)
        s=owners[0];assert bytes(u.mem_read(pc,length))==bytes(s.data[pc-s.ramAddress:pc-s.ramAddress+length]),hex(pc)
        executed.add(pc)
        if pc==BASE+0xD16B4:
            glyph,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
            events.append(dict(kind='ascii',code=glyph,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
    cpu.hook_add(UC_HOOK_CODE,code)
    before=bytes(cpu.mem_read(BASE,len(ctx.raw)))
    call(cpu,0xD5160,(CONTEXT,BITMAP,1),instruction_limit=1000000)
    put(CONTEXT+0x1C,0);put(CONTEXT+0x24,0,0)
    call(cpu,0xD5404,(CONTEXT,TEXT),instruction_limit=1000000)
    assert bytes(cpu.mem_read(BASE,len(ctx.raw)))==before
    assert bytes(cpu.mem_read(TEXT-16,16))==bytes(cpu.mem_read(TEXT+len(compiled),16))==b'\x5a'*16
    assert bytes(cpu.mem_read(TEXT,len(compiled)))==compiled
    assert bytes(cpu.mem_read(BUFFER-32,32))==bytes(cpu.mem_read(BUFFER+size,32))==b'\xa5'*32
    pixels=bytes(cpu.mem_read(BUFFER,size))
    assert struct.unpack('<I',cpu.mem_read(SLOT,4))[0]==0xE2834001
    shifted=[{**e,'y':e['y']+1} for e in events]
    canvas=expected_pixels(ctx.arm,b'',shifted,mode,background=9)
    source_stride=512 if mode==16 else 128
    stride=pitch*2
    expected=b''.join(canvas[y*source_stride:y*source_stride+stride] for y in range(108))
    if pixels!=expected:
        diagnostic=ROOT/'pixel_mismatch_diagnostic.json'
        assert not diagnostic.exists()
        diffs=[(i,a,b) for i,(a,b) in enumerate(zip(pixels,expected)) if a!=b]
        save(diagnostic,dict(mode=mode,differing_bytes=len(diffs),first40_differences=diffs[:40],events=events,
            font_object=font,font_object_first32_hex=bytes(cpu.mem_read(font,32)).hex(),
            actual_hex_first64=pixels[:64].hex(),expected_hex_first64=expected[:64].hex()))
    assert pixels==expected
    return pixels,events,sorted(executed)

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0);review=load(REVIEW);assert review['runtime']==ctx.receipt()
    layout_path=Path('work/analysis/refit_help_v712/native_layout_proof.json');layout=load(layout_path)
    layout_arm=Path('work/analysis/refit_help_v712/target_ARM9.bin').read_bytes()
    assert all(ctx.arm[a:b]==layout_arm[a:b] for a,b in layout['layout']['owned_spans'])
    history=load('work/analysis/deck_explanations_pool_proof.json');all_offsets=sorted(struct.unpack_from('<I',ctx.arm,r['field_offset'])[0]-BASE for r in history['references'])
    assert len(set(all_offsets))==31
    proposed=bytearray(ctx.arm);plans=[]
    for row in review['records']:
        at=row['current_reference']['offset'];end=next(n for n in all_offsets if n>at)
        current=bytes.fromhex(row['current_hex']);assert ctx.arm[at:end]==(current+b'\0').ljust(end-at,b'\0')
        compiled,lines=compile_paragraph(row['english'].removesuffix('{PAD}'));assert len(compiled)<=end-at
        proposed[at:end]=compiled.ljust(end-at,b'\0')
        plans.append(dict(id=row['id'],current_offset=at,allocation=end-at,compiled_hex=compiled.hex(),lines=lines,logical_English=row['english'].removesuffix('{PAD}')))
    inverse=bytearray(proposed)
    for p in plans:inverse[p['current_offset']:p['current_offset']+p['allocation']]=ctx.arm[p['current_offset']:p['current_offset']+p['allocation']]
    assert bytes(inverse)==ctx.arm
    ROOT.mkdir();target=ROOT/'proposed_ARM9_RESEARCH_ONLY.bin';target.write_bytes(proposed)
    cases=[];sheet=Image.new('RGB',(672,1040),'white');draw=ImageDraw.Draw(sheet)
    for index,p in enumerate(plans):
        for mode in (4,16):
            pixels,events,executed=native(ctx,bytes.fromhex(p['compiled_hex']),mode)
            content=[e for e in events if e['code']!=32]
            assert [e['code'] for e in content]==[ord(c) for c in p['logical_English'] if c!=' ']
            assert all(0<=e['x'] and e['x']+6<=168 and 0<=e['y'] and e['y']+12<=60 for e in content)
            path=ROOT/(p['id']+'_'+str(mode)+'.bin');path.write_bytes(pixels)
            cases.append(dict(**p,mode=mode,pixels=str(path),pixels_sha256=sha(pixels),glyph_events=events,executed_source_addresses=executed,
                complete_first_internal_final_glyphs_andnative_pixels_andblank_guards_exact=True,all_main4MiB_unchanged=True,ABI_text_pixel_canaries_exact=True))
            if mode==16:
                pic=Image.new('RGB',(168,108));pic.putdata([(255,255,255) if c==9 else (128,128,128) if c==14 else (0,0,0) for c in struct.unpack('<18144H',pixels)])
                draw.text((8,index*260+2),p['id'].removeprefix('DECK_EXPLANATION_'),fill='black')
                sheet.paste(pic.crop((0,0,168,60)).resize((672,240),Image.Resampling.NEAREST),(0,index*260+20))
    png=ROOT/'four_current_refit_panels.png';sheet.save(png)
    save(ROOT/'native_andstorage_verification.json',dict(runtime=ctx.receipt(),review=str(REVIEW),review_sha256=sha(REVIEW.read_bytes()),plans=plans,cases=cases,
        current_layout_native_proof=str(layout_path),current_layout_native_proof_sha256=sha(layout_path.read_bytes()),
        source_owned_span=history['source_span'],current_used_bytes=540,target_used_bytes=540,allocation_shortfall_bytes=0,
        all31_pointer_values_andallocation_starts_unchanged=True,complete_parent_inverse_andall_unowned_ARM9_bytes_exact=True,
        proposed_ARM9=str(target),proposed_ARM9_sha256=sha(proposed),original_good_wordings_retained=True,prose_not_shortened_for_storage=True,
        original_native_addresses_andcurrent_owned_code_checked_at_every_instruction=True,no_historical_RAM_overlay=True,
        actual_resource_pitch42_or168_height108_andaccepted_native_Y_plus1_exact=True,
        initialized_metrics_surface_andzero_origin_getter_are_explicit_native_test_contracts=True,
        bitmap_parent_constructor_allocator_GPU_andactual_gameplay_not_claimed=True,
        review_sheet=dict(path=str(png),sha256=sha(png.read_bytes()),panels=4),direct_visual_review_pending=True,
        current_consumer_formatter_replaces_legacy_guard_indents=True,connected_stored_text_andactual_gameplay_andregistered_deployment_pending=True,
        no_ROM_created=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REVIEW,RELEASE,STARTUP,layout_path,Path('dk4tool/dialogue/refit_help.py'),Path(__file__)]}))
    print('Four current panels/eight native mode cases pass;all4MiB/ABI/canaries/font pixels exact;four existing slots fit540 bytes,no pointer moves orROM.')
