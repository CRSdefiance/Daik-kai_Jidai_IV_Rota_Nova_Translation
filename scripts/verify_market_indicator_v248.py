"""Resolve remaining market-icon pixels to complete native frame digits."""

import json
import struct
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R1,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R9,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_title_display_v229 as resources
from scripts.probe_button_prompt_native import STACK, call
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT=Path("work/analysis/market_indicator_v248")
CAPTURE=Path("work/emulation_v193/market_indicator_v248")
ROM=Path("out/all_routes_combined_v247_candidate.nds")


def native_fragments(rom):
    # Retain the unchanged helper's machine for subsequent native fragments.
    # The factory delegates to its original implementation, without state changes.
    machines=[];factory=resources.machine
    def retain(arm):
        u=factory(arm);machines.append(u);return u
    with patch.object(resources,"machine",side_effect=retain):
        loaded=resources.native_views(rom,expected_paths={"/_pxl/__frame.pxl"},owner_range=(0x02313F60,0x02313F74))
    u=machines[0];parent=0x02440020;span=0x2CDC+240
    u.mem_write(parent-16,b"\xa5"*(span+32))
    for n in range(5):call(u,0xD3BD4,(parent+0x2CDC+n*48,))
    u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R9,parent);u.reg_write(UC_ARM_REG_R6,0)
    u.emu_start(0x02085430,0x02085488,count=100000)
    assert u.reg_read(UC_ARM_REG_PC)==0x02085488 and u.reg_read(UC_ARM_REG_SP)==STACK
    assert bytes(u.mem_read(parent-16,16))==b"\xa5"*16
    assert bytes(u.mem_read(parent+span,16))==b"\xa5"*16
    views=[]
    for n in range(5):
        f=list(struct.unpack("<12I",u.mem_read(parent+0x2CDC+n*48,48)))
        assert f[3]==loaded["cases"][0]["owner"] and f[7:9]==[80+n*8,216]
        # Native view initialization writes only the low palette-bank halfword.
        assert f[9]&0xFFFF==9 and f[10:12]==[8,8]
        views.append({"digit":n+1,"source_origin":f[7:9],"extent":f[10:12],"palette_bank":f[9]&0xFFFF,"native_fields":f})
    widget=0x02460020;call(u,0x85E84,(widget,))
    u.mem_write(widget+0xA0,struct.pack("<4I",84,94,108,118))
    selected=[]
    for grade in range(1,6):
        u.mem_write(widget+0x61,bytes([grade]))
        u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R5,widget)
        u.reg_write(UC_ARM_REG_R6,parent);u.reg_write(UC_ARM_REG_R4,resources.VIEW)
        u.emu_start(0x02085AE4,0x02085B50,count=100000)
        assert u.reg_read(UC_ARM_REG_PC)==0x02085B50 and u.reg_read(UC_ARM_REG_SP)==STACK
        assert u.reg_read(UC_ARM_REG_R1)==parent+0x2CDC+(grade-1)*48
        point=list(struct.unpack("<4I",u.mem_read(u.reg_read(UC_ARM_REG_R3),16)))
        assert point==[104,90,84,94]
        selected.append({"grade_input":grade,"native_selected_view":u.reg_read(UC_ARM_REG_R1),"native_destination_point":point[:2],"original_icon_origin":point[2:]})
    arm=rom.read_file("/__arm9__.bin");clean=NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    ranges=[(0x85430,0x85488),(0x85AE4,0x85B54)]
    assert all(arm[lo:hi]==clean[lo:hi] for lo,hi in ranges)
    return {"resource":loaded,"native_source_views":views,"selection_cases":selected,
            "original_code_ranges":[{"start":0x02000000+lo,"end":0x02000000+hi,"sha256":sha(arm[lo:hi])} for lo,hi in ranges],
            "preceding_parent_widget_grade_and_geometry_are_explicit_research_inputs":True,
            "stopped_before_virtual_GPU_draw":True,"actual_market_dispatch_not_claimed":True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);rom=NdsImage.open(ROM);digest=sha(ROM.read_bytes())
    report=json.loads((CAPTURE/"capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"]==digest and report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    for row in report["frames_captured"]:assert sha(Path(row["path"]).read_bytes())==row["PNG_sha256"]
    capture=next(r for r in report["frames_captured"] if r["frame"]==19700 and "final" in r["path"])
    image=Image.open(capture["path"]).convert("RGB");font=GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    atlas=PxlImage.from_bytes(rom.read_file("/_pxl/itemtrade.pxl"));raw=rom.read_file("/_pxl/__frame.pxl");frame=PxlImage.from_bytes(raw)
    ps,px=struct.unpack_from("<2I",raw,12);assert px-ps==83*32
    palette=[native5(bgr555(v)) for v, in struct.iter_unpack("<H",raw[ps+9*32:ps+10*32])]
    original=PxlImage.from_bytes(NdsImage.open("work/clean.nds").read_file("/_pxl/__frame.pxl"))
    assert original.source[ps+9*32:ps+10*32]==raw[ps+9*32:ps+10*32]
    assert all(original.indices[y*256+x]==frame.indices[y*256+x] for y in range(216,224) for x in range(80,120))
    native=native_fragments(rom)
    assert atlas.source==NdsImage.open("work/clean.nds").read_file("/_pxl/itemtrade.pxl")
    cases=[];sheet=Image.new("RGB",(1000,220),"#404040");draw=ImageDraw.Draw(sheet)
    for pos,(index,x0,quantity) in enumerate([(13,84,"3"),(14,116,"5"),(27,148,"8"),(78,180,"7"),(86,212,"5")]):
        candidates=[]
        for view in native["native_source_views"]:
            sx,sy=view["source_origin"]
            ink=[(x,y,palette[frame.indices[(sy+y)*256+sx+x]]) for y in range(8) for x in range(8) if frame.indices[(sy+y)*256+sx+x]!=0]
            if all(native5(image.getpixel((x0+20+x,282+y)))==color for x,y,color in ink):candidates.append((view,ink))
        assert len(candidates)==1
        view,ink=candidates[0]
        expected=[native5(atlas.palette[v]) for v in atlas.indices[index*576:(index+1)*576]]
        mask=font.decode(quantity)
        for y in range(11):
            for x in range(6):
                if mask.getpixel((x,y)):expected[(y+13)*24+x+3]=(0,1,0)
        for y in range(11):
            for x in range(6):
                if mask.getpixel((x,y)):expected[(y+12)*24+x+2]=(28,28,28)
        old_expected=expected[:];overlay=[]
        for x,y,color in ink:
            dx,dy=x+20,y-4
            if 0<=dx<24 and 0<=dy<24:
                expected[dy*24+dx]=color;overlay.append([dx,dy])
        actual=[native5(image.getpixel((x0+x,286+y))) for y in range(24) for x in range(24)]
        assert expected==actual and len(overlay)==5
        differences=[[n%24,n//24] for n,(a,b) in enumerate(zip(old_expected,actual,strict=True)) if a!=b]
        assert differences==sorted(overlay,key=lambda p:(p[1],p[0]))
        draw.text((pos*200+8,5),f"Goods {index}; indicator {view['digit']}",fill="white")
        sheet.paste(image.crop((x0,278,x0+32,310)).resize((192,192),Image.Resampling.NEAREST),(pos*200+4,25))
        cases.append({"atlas_index":index,"quantity":quantity,"indicator_digit":view["digit"],
                      "indicator_source_origin":view["source_origin"],"indicator_palette_bank":view["palette_bank"],
                      "indicator_screen_origin":[x0+20,282],"complete_indicator_ink_pixels_exact":len(ink),
                      "all_first_last_glyph_rows_checked":True,"source_plus_quantity_plus_indicator_pixels_exact":576,
                      "previous_unmapped_pixels_independently_predicted":overlay,"unexplained_icon_rectangle_pixels":0,
                      "complete_24_by_24_icon_composition_exact":True})
    sheet.save(ROOT/"live_review.png")
    proof={"format":"dk4-market-indicator-composition-v248","ROM":str(ROM),"ROM_sha256":digest,
           "capture":capture,"source_frame_sha256":sha(raw),"source_trade_atlas_sha256":sha(atlas.source),
           "native":native,"cases":cases,"complete_icon_composition_pixels":5*576,
           "full_indicator_ink_pixels":sum(c["complete_indicator_ink_pixels_exact"] for c in cases),
           "previous_unmapped_icon_pixels_resolved":25,"unexplained_icon_rectangle_pixels":0,
           "no_savestate_RAM_injection_or_fixture_ROM":True,"quantity_arithmetic_and_gameplay_grade_meaning_not_proved":True,
           "actual_market_widget_dispatch_and_all_icons_still_open":True,"ROM_modified":False,"full_goal_complete":False}
    (ROOT/"proof.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"complete_icon_pixels":2880,"full_indicator_ink_pixels":proof["full_indicator_ink_pixels"],"unmapped_icon_pixels":0,"ROM_changed":False}))


if __name__=="__main__":
    main()
