"""Exact native caption masks, inherited behavior and private-storage guards."""

import argparse
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, target
from dk4tool.patch.square_caption_cells import fixed_transform, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute

ROOT = Path('work/analysis/square_caption_cells_v483')


def native(arm, text, width=64, origin=(0,0)):
    u=machine(arm)
    pool=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48])
    u.mem_write(POOL,pool)
    header,view,ctx,string=0x02450000,0x02453000,0x02454000,0x02455000
    count=width*12//2
    initial=struct.pack('<5I',4,width//4,12,0x02452000-header,20)
    u.mem_write(header-16,b'\xA5'*(20+count+32))
    u.mem_write(header,initial+bytes(count))
    call(u,0xD3D80,(view,))
    u.mem_write(STACK,struct.pack('<4I',width,12,0,0))
    call(u,0xD3AFC,(view,header,0,0))
    view_before=bytes(u.mem_read(view,48))
    font=struct.unpack_from('<I',arm,0xD5088)[0]
    u.mem_write(font+4,struct.pack('<2I',6,12))
    call(u,0xD5160,(ctx,view,1))
    u.mem_write(ctx+36,struct.pack('<2I',*origin))
    u.mem_write(string,text.encode()+b'\0')
    call(u,target(arm,0x5FDC4)-BASE,(ctx,string))
    assert u.reg_read(UC_ARM_REG_R0)-string==len(text)
    assert bytes(u.mem_read(view,48))==view_before
    assert bytes(u.mem_read(header,20))==initial
    assert bytes(u.mem_read(header-16,16))==bytes(u.mem_read(header+20+count,16))==b'\xA5'*16
    assert struct.unpack('<4I',u.mem_read(ctx+4,16))==(0,0,width,12)
    assert bytes(u.mem_read(string,len(text)+1))==text.encode()+b'\0'
    assert bytes(u.mem_read(font+4,8))==struct.pack('<2I',6,12)
    assert struct.unpack('<i',u.mem_read(ctx+28,4))[0]==-1
    packed=bytes(u.mem_read(header+20,count))
    indices=[n for b in packed for n in (b&15,b>>4)]
    return bytes(indices),bytes(u.mem_read(ctx,72)),u


def names(arm):
    u=machine(arm)
    u.mem_write(POOL,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]))
    names=[]
    for category in range(18):
        call(u,target(arm,0x5FDA8)-BASE,(category,))
        p=u.reg_read(UC_ARM_REG_R0)
        names.append(bytes(u.mem_read(p,64)).split(b'\0')[0].decode('ascii'))
    return names


def main():
    global ROOT
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixed',action='store_true',help='Verify V484 fixed-extent variant')
    args=parser.parse_args()
    if args.fixed:
        ROOT=Path('work/analysis/square_caption_cells_v484')
    parent=NdsImage.open('out/all_routes_combined_v474_candidate.nds')
    before=parent.read_file('/__arm9__.bin')
    after,plan=(fixed_transform(before) if args.fixed else transform(before))
    assert (ROOT/'research_arm9.bin').read_bytes()==after
    old_names,new_names=names(before),names(after)
    assert new_names[2]=='Delicacy' and all(old_names[i]==new_names[i] for i in range(18)if i!=2)
    font=GameAsciiFont.from_arm9(after)
    assert font.glyphs==GameAsciiFont.from_arm9(before).glyphs
    cases=[]
    for i,name in enumerate(new_names):
        text=name+' Shop'
        pixels,ctx,u=native(after,text)
        expected=bytearray(64*12)
        for n,c in enumerate(text):
            for y in range(11):
                for x in range(6):
                    if font.decode(c).getpixel((x,y)):
                        assert n*5+x<64
                        expected[y*64+n*5+x]=1
        assert pixels==bytes(expected),(i,text)
        if i!=2:
            old_pixels,old_ctx,_=native(before,text)
            assert pixels==old_pixels and ctx==old_ctx
        pool=bytes(MainCodeFile(after,BASE).sections[3].data[:-48])
        actual=bytes(u.mem_read(POOL,len(pool)))
        if args.fixed:
            assert actual==pool
            section=bytes(MainCodeFile(after,BASE).sections[4].data)
            active=bytes(u.mem_read(0x01FFC000,len(section)))
            start=plan['private_buffer']-0x01FFC000
            assert active[:start]==section[:start] and active[start+448:]==section[start+448:]
            assert active[start+428:start+448]==bytes(20)
        else:
            start=plan['private_buffer']-POOL
            assert actual[:start]==pool[:start] and actual[start+448:]==pool[start+448:]
            assert actual[start+428:start+448]==bytes(20)
        cases.append({'category':i,'complete_caption':text,'all_768_pixels_exact':True,
                      'first_and_final_glyphs_exact':True,'ink_pixels':sum(expected),'original_view_and_header_restored':True})
    rejected=[]
    for width,origin in ((48,(0,0)),(64,(1,0)),(64,(0,1)),(80,(0,0))):
        old_pixels,old_ctx,_=native(before,'Food Shop',width,origin)
        new_pixels,new_ctx,_=native(after,'Food Shop',width,origin)
        assert old_pixels==new_pixels and old_ctx==new_ctx
        rejected.append({'width':width,'origin':origin,'original_fallback_pixels_and_context_exact':True})
    for i in range(18):
        a,b=machine(before),machine(after)
        call(a,0xC5BA0,(i,));call(b,0xC5BA0,(i,))
        assert bytes(a.mem_read(a.reg_read(UC_ARM_REG_R0),64))==bytes(b.mem_read(b.reg_read(UC_ARM_REG_R0),64))
    boot=execute(after,bytes(parent.rom.arm7),parent.rom.arm7RamAddress,
                 repair_entry=plan['cache']['entry'],expected_pool=bytes(MainCodeFile(after,BASE).sections[3].data[:-48]))
    proof={'target_arm9_sha256':sha(after),'plan':plan,'all18_complete_captions':cases,
           'all17_unchanged_caption_rasters_and_contexts_exact':True,'all18_shared_category_getters_preserved':True,
           'native_fallbacks':rejected,'boot':boot,'arena':initialize(after),'actual_GPU_pending':True}
    (ROOT/'native_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('All18 complete captions;17 unchanged masks;four fallbacks;startup/cache/arena passed.')


if __name__=='__main__':
    main()
