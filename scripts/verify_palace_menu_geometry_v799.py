"""Every actual menu glyph placed from original descriptor geometry,not pixels."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch import palace_label_boundaries as labels
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import save

ROOT=labels.ROOT
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/palace_v799_expanded_menu')


def main():
    rom=NdsImage.open('out/all_routes_combined_v799_candidate.nds');arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x51F4C,0x5210C),(0x52D8C,0x52F28),(0x5D4FC,0x5D518),(0xCF348,0xCF3A0))
    assert all(arm[lo:hi]==clean[lo:hi] for lo,hi in spans)
    vtable=struct.unpack_from('<I',arm,0x525D8)[0]
    descriptor_vtable=struct.unpack_from('<I',arm,0x51FB4)[0]
    expected_pointers=tuple(labels.blobs()[0][s] for s in labels.LABELS)
    frames=[];all_labels=set()
    for frame in (4400,7400,11800):
        rp=CAP/f'frame_{frame:06d}_arm9_ram.bin';raw=rp.read_bytes();assert len(raw)==0x400000
        cpu=machine(arm);cpu.mem_write(BASE,raw)
        def get(fn,args=()):call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
        def word(p):return struct.unpack('<I',cpu.mem_read(p,4))[0]
        candidates=[];at=0
        while (at:=raw.find(struct.pack('<I',vtable),at))>=0:
            obj=BASE+at;at+=1;desc=word(obj+4)
            if not BASE<=desc<BASE+len(raw)-32 or word(desc)!=descriptor_vtable:continue
            count=get(word(descriptor_vtable)-BASE,(desc,))
            if count!=6:continue
            pointers=tuple(get(word(descriptor_vtable+4)-BASE,(desc,i)) for i in range(count))
            if pointers==expected_pointers:candidates.append((obj,desc))
        assert len(candidates)==1,candidates
        obj,desc=candidates[0];visible=[]
        for i,pointer in enumerate(expected_pointers):
            if get(word(descriptor_vtable+12)-BASE,(desc,i)):
                text=bytes(cpu.mem_read(pointer,64)).split(b'\0')[0].decode('ascii')
                width=get(0xCF348,(pointer,0,0));assert width==len(text)
                visible.append((i,text,width))
        get(word(descriptor_vtable+0x28)-BASE,(0x02470020,desc))
        margin_x,margin_y=struct.unpack('<2i',cpu.mem_read(0x02470020,8))
        assert (margin_x,margin_y)==(0,4)
        get(word(descriptor_vtable+0x2C)-BASE,(0x02470040,desc,max(w for _,_,w in visible),len(visible)))
        rect=struct.unpack('<4i',cpu.mem_read(0x02470040,16));left,top,right,bottom=rect
        ui_offset=struct.unpack_from('<i',arm,vtable-BASE-16)[0]
        assert tuple(struct.unpack('<4i',cpu.mem_read(obj+ui_offset+0x40,16)))==rect
        assert right-left==6*max(w for _,_,w in visible)+2*margin_x+32
        assert bottom-top==(12+2*margin_y)*len(visible)+24
        png=CAP/f'frame_{frame:06d}_navigation.png';image=Image.open(png).convert('RGB');rows=[]
        for n,(index,text,width) in enumerate(visible):
            plane=raster(arm,b' '+text.encode(),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
            assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),[text])
            x=(left+right-width*6)//2
            row_top=top+192+12+n*(12+2*margin_y);y=row_top+margin_y
            expected={(x-6+i%228,y+i//228) for i,p in enumerate(plane) if p==1}
            actual={(px,py) for py in range(row_top,row_top+12+2*margin_y)
                for px in range(left+12,right-12) if image.getpixel((px,py))==(8,8,8)}
            assert expected==actual,(frame,text,len(expected-actual),len(actual-expected))
            assert all(left+12<=px<right-12 and row_top<=py<row_top+12+2*margin_y for px,py in expected)
            all_labels.add(text)
            rows.append({'source_menu_index':index,'english':text,'source_width_units':width,
                'text_origin_from_native_geometry':[x,y],'complete_glyphs_and_blank_row_exact':True,
                'no_dropped_first_or_last_letters_no_neighbor_text_or_bounds_loss':True})
        frames.append({'frame':frame,'RAM_sha256':sha(raw),'PNG_sha256':sha(png.read_bytes()),
            'actual_menu_object':obj,'source_typed_descriptor':desc,'original_UI_base_offset':ui_offset,
            'original_virtual_geometry_method':word(descriptor_vtable+0x2C),'native_rectangle':rect,
            'rows':rows})
    assert all_labels==set(labels.LABELS)
    save(ROOT/'actual_menu_geometry_verification.json',{'candidate_sha256':sha(Path('out/all_routes_combined_v799_candidate.nds').read_bytes()),
        'frames':frames,'all_six_labels_complete_in_actual_menus':True,'total_actual_rows':sum(len(r['rows']) for r in frames),
        'positions_from_original_virtual_width_margin_rectangle_and_live_object_not_observed_glyphs':True,
        'actual_UI_ink_RGB':[8,8,8],'source_geometry_code_exact_to_clean':list(spans),
        'no_gameplay_fixture_outcome_or_whole_game_completion_claim':True,
        'producer_sha256':sha(Path('scripts/verify_palace_menu_geometry_v799.py').read_bytes()),'full_goal_complete':False})
    print('Twelve actual menu rows cover all6 labels;independent glyphs,bounds and blank rows match original native geometry exactly.',flush=True)


if __name__=='__main__':main()
