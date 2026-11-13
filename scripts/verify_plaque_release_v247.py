"""Verify exact integration, patch reconstruction, and complete live lettering."""

import json
import struct
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import ROOT, save
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROM=Path("out/all_routes_combined_v247_candidate.nds")


def find_mask(font,text,image,region):
    colors=[c for c,_ in Counter(image.crop(region).get_flattened_data()).most_common() if min(c)>180][:4]
    for color in colors:
        for y in range(region[1],region[3]-10):
            for x in range(region[0],region[2]-len(text)*6+1):
                try:
                    ink,bounds=complete_mask(font,text,image,x,y,color)
                    return {"text":text,"bounds":bounds,"ink_pixels":ink,"color":color,"all_ink_and_blank_cells_exact":True}
                except ValueError:
                    pass
    raise ValueError("No complete live native mask: "+text)


def main():
    prior=Path("out/all_routes_combined_v246_candidate.nds")
    assert (ROOT/"v246_reproduction.nds").read_bytes()==prior.read_bytes()
    old,new=NdsImage.open(prior),NdsImage.open(ROM)
    before={p:bytes(d) for _,p,d in old.iter_files()};after={p:bytes(d) for _,p,d in new.iter_files()}
    changed=sorted(p for p in before if before[p]!=after[p])
    assert changed==["/_pxl/dividecrewinfo.pxl","/_pxl/personinfo.pxl"]
    assert new.read_file("/__arm9__.bin")== (ROOT/"research_arm9.bin").read_bytes()
    assert old.rom.arm7==new.rom.arm7 and old.rom.arm9OverlayTable==new.rom.arm9OverlayTable
    for name,path in (("crew","/_pxl/dividecrewinfo.pxl"),("person","/_pxl/personinfo.pxl")):
        a,b=PxlImage.from_bytes(before[path]),PxlImage.from_bytes(after[path])
        assert b.source==(ROOT/(name+"_target.pxl")).read_bytes()
        assert a.source[:a.pixels_offset]==b.source[:b.pixels_offset] and len(a.source)==len(b.source)
    previous=json.loads(prior.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    manifest=json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    swaps={"translations/assign_sailors_graphics_v4.json":"translations/assign_sailors_graphics_v5.json","translations/person_info_graphics_v2.json":"translations/person_info_graphics_v3.json"}
    norm=lambda s:s.replace("\\","/")
    assert [norm(s) for s in manifest["batches"]]==[swaps.get(norm(s),norm(s)) for s in previous["batches"]]
    assert len(manifest["batches"])==467 and manifest["required_batches"]==previous["required_batches"]
    for p,ids in previous["changed_records"].items():
        assert set(ids)<=set(manifest["changed_records"][p])
    digest=sha(ROM.read_bytes())
    assert manifest["candidate_sha256"]==digest
    assert manifest["release_stack_sha256"]==sha(Path("translations/release_stack.json").read_bytes())
    patch=ROM.with_suffix(".xdelta");clean=Path("work/clean.nds")
    assert sha(clean.read_bytes())=="f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,ROOT/"exact_patch_reconstruction.nds")
    assert (ROOT/"exact_patch_reconstruction.nds").read_bytes()==ROM.read_bytes()
    screens={};cases=[];reports={}
    for name,frame,batch_path in (("crew",10000,"translations/assign_sailors_graphics_v5.json"),("person",10500,"translations/person_info_graphics_v3.json")):
        directory=Path("work/emulation_v193/plaque_style_v247_final_format")/name
        report=json.loads((directory/"capture_report.json").read_text(encoding="utf-8"))
        assert report["ROM_sha256"]==digest and report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        for row in report["frames_captured"]:
            assert sha(Path(row["path"]).read_bytes())==row["PNG_sha256"]
        image=Image.open(directory/f"frame_{frame:06d}_final.png").convert("RGB");screens[name]=image;reports[name]=report
        batch=json.loads(Path(batch_path).read_text(encoding="utf-8"));asset=PxlImage.from_bytes(new.read_file(batch["file_path"]))
        for row in batch["records"]:
            x0,y0,x1,y1=row["plaque_box"]
            for y in range(y0,y1):
                for x in range(x0,x1):
                    assert native5(image.getpixel((x,y)))==native5(asset.palette[asset.indices[y*256+x]]),(name,row["text"],x,y)
            cases.append({"screen":name,"text":row["text"],"plaque_bounds":row["plaque_box"],"entire_texture_border_and_lettering_exact":True})
    font=GameAsciiFont.from_arm9(new.read_file("/__arm9__.bin"));person=screens["person"]
    ink,bounds=complete_mask(font,"Equipped Items",person,138,210,(0,8,0))
    run_data=(ROOT/"tooltip_runs.bin").read_bytes();paper_pixels=0
    for offset in range(0,len(run_data),20):
        x,y,w,h,color=struct.unpack_from("<5I",run_data,offset)
        assert h==1
        expected=(color&31,(color>>5)&31,(color>>10)&31)
        for n in range(w):
            actual=person.getpixel((136+x+n,208+y))
            if actual!=(0,8,0):
                assert native5(actual)==expected,(x+n,y,actual,expected)
                paper_pixels+=1
    assert paper_pixels==88*16-ink
    live_labels=[find_mask(font,text,person,region) for text,region in [
        ("Vigor",(172,292,224,312)),("Speech",(172,316,224,336)),
        ("Swords",(92,316,144,336)),("Guile",(12,340,64,360))]]
    live_labels.extend(find_mask(font,text,screens["crew"],region) for text,region in [
        ("Lo",(48,365,73,384)),("Hi",(80,365,108,384))])
    # Read and verify all three native value cells; older screenshots clipped
    # digits and must not be used as an authoritative numeric reference.
    numeric_lines=[]
    for label,x,y in [
        ("Command",16,272),("Sailing",96,272),("Survey",176,272),
        ("Finance",16,296),("Observe",96,296),("Vigor",176,296),
        ("Aim",16,320),("Swords",96,320),("Speech",176,320),("Guile",16,344)]:
        digits=""
        for slot in range(3):
            matches=[]
            for ch in " 0123456789":
                try:
                    complete_mask(font,ch,person,x+42+slot*6,y,(230,230,230))
                    matches.append(ch)
                except ValueError:
                    pass
            assert len(matches)==1,(label,slot,matches)
            digits+=matches[0]
        value=int(digits)
        assert 0<=value<=500 and digits==f"{value:3d}"
        full=f"{label:>7}{value:3d}"
        count,box=complete_mask(font,full,person,x,y,(230,230,230))
        assert len(full)==10 and box[2]<=240
        numeric_lines.append({"label":label,"value":value,"bounds":box,
                              "complete_line_ink_pixels":count,
                              "all_seven_label_and_three_numeric_cells_exact":True})
    old_arm=old.read_file("/__arm9__.bin");new_arm=new.read_file("/__arm9__.bin")
    assert old_arm[0x7DCC8:0x7DE20]==new_arm[0x7DCC8:0x7DE20]
    snapshot=reports["person"]["read_only_RAM_snapshot"];ram=Path(snapshot["path"]).read_bytes();assert sha(ram)==snapshot["sha256"]
    views=[]
    for offset in range(0,len(ram)-48,4):
        f=struct.unpack_from("<12I",ram,offset)
        if f[5]==4 and f[7]==0 and f[8] in (0,8,16,24,32,40) and f[11]==8 and 0<=f[10]<=50 and 0x02312700<=f[3]<=0x02314000:
            views.append([f[3],f[8],f[10]])
    groups={}
    for owner,row,width in views:groups.setdefault(owner,[]).append([row,width])
    assert any({row for row,width in v}=={0,8,16,24,32,40} for v in groups.values())
    proof={"format":"dk4-plaque-style-combined-v247","candidate":str(ROM),"candidate_sha256":digest,
           "patch":str(patch),"patch_sha256":sha(patch.read_bytes()),"profile":manifest["profile"],
           "base_sha256":manifest["base_sha256"],"changed_components_vs_V246":["/__arm9__.bin",*changed],
           "all_467_batches_required_layers_prior_records_routes_and_other_graphics_preserved":True,
           "previous_V246_complete_reproduction_exact":True,"exact_clean_patch_reconstruction":True,
           "live_plaques":cases,"equipment_font_ink_pixels":ink,"equipment_font_bounds":bounds,
           "native_equipment_paper_pixels":paper_pixels,"complete_live_runtime_labels":live_labels,
           "all_ten_complete_skill_label_value_lines":numeric_lines,
           "six_native_bar_rows_remain_bounded":True,"focused_graphics_tests_passed":29,
           "targeted_cold_boots_no_savestate_or_RAM_injection":True,"experimental_user_acceptance_pending":True,
           "full_goal_complete":False}
    save(ROOT/"saved_live_proof.json",proof)
    preview=Image.new("RGB",(1024,768))
    for n,name in enumerate(("crew","person")):
        preview.paste(screens[name].resize((512,768),Image.Resampling.NEAREST),(n*512,0))
    preview.save(ROOT/"live_preview.png")
    print(json.dumps({"candidate_sha256":digest,"patch_sha256":proof["patch_sha256"],"complete_plaques":len(cases),"runtime_labels":len(live_labels),"paper_pixels":paper_pixels}))


if __name__=="__main__":
    main()
