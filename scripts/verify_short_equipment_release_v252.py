"""Exact combined inheritance and expanded, deliberately incomplete plaque audit."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.short_equipment_paper import ROOT
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROM=Path("out/all_routes_combined_v252_candidate.nds")
CAPTURE=Path("work/emulation_v193/short_equipment_v252")


def frame(folder,number,digest):
    report=json.loads((CAPTURE/folder/"capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"]==digest and report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    row=next(r for r in report["frames_captured"] if r["frame"]==number and ("final" in r["path"] if number in (12600,17500,11600) else "cold_boot" in r["path"]))
    assert sha(Path(row["path"]).read_bytes())==row["PNG_sha256"]
    return Image.open(row["path"]).convert("RGB"),row


def numeric_field(font,image,x,y,width=3,color=(230,230,230)):
    text=""
    for index in range(width):
        found=[]
        for char in " 0123456789":
            try:complete_mask(font,char,image,x+index*6,y,color);found.append(char)
            except ValueError:pass
        assert len(found)==1,(x,y,index,found)
        text+=found[0]
    return int(text)


def right_aligned_number(font,image,right):
    matches=[]
    for color in ((230,230,230),(98,97,98)):
        for length in (1,2,3):
            x=right-length*6
            try:
                value=numeric_field(font,image,x,211,length,color)
                if len(str(value))!=length:
                    continue
                complete_mask(font,str(value),image,x,211,color)
                matches.append({"value":value,"bounds":[x,211,x+length*6,222],"color":color})
            except (AssertionError,ValueError):
                pass
    assert matches
    longest=max((r["bounds"][2]-r["bounds"][0]) for r in matches)
    full=[r for r in matches if r["bounds"][2]-r["bounds"][0]==longest]
    assert len(full)==1,full
    return full[0]


def main():
    prior=Path("out/all_routes_combined_v251_candidate.nds")
    assert (ROOT/"v251_reproduction.nds").read_bytes()==prior.read_bytes()
    before,after=NdsImage.open(prior),NdsImage.open(ROM);digest=sha(ROM.read_bytes())
    a={p:bytes(d) for _,p,d in before.iter_files()};b={p:bytes(d) for _,p,d in after.iter_files()}
    assert a==b and before.rom.arm7==after.rom.arm7 and before.rom.arm9OverlayTable==after.rom.arm9OverlayTable
    assert after.read_file("/__arm9__.bin")== (ROOT/"research_arm9.bin").read_bytes()
    old=json.loads(prior.with_suffix(".manifest.json").read_text(encoding="utf-8"));m=json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    norm=lambda p:p.replace("\\","/")
    assert [norm(p) for p in m["batches"]]==[norm(p) for p in old["batches"]] and len(m["batches"])==467
    assert m["required_batches"]==old["required_batches"]
    for p,ids in old["changed_records"].items():assert set(ids)<=set(m["changed_records"][p])
    assert m["candidate_sha256"]==digest and m["release_stack_sha256"]==sha(Path("translations/release_stack.json").read_bytes())
    patch=ROM.with_suffix(".xdelta");clean=Path("work/clean.nds")
    assert sha(clean.read_bytes())=="f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,ROOT/"exact_patch_reconstruction.nds")
    assert (ROOT/"exact_patch_reconstruction.nds").read_bytes()==ROM.read_bytes()
    person_batch=json.loads(Path("translations/person_info_graphics_v3.json").read_text(encoding="utf-8"));person_art=PxlImage.from_bytes(after.read_file(person_batch["file_path"]))
    crew_batch=json.loads(Path("translations/assign_sailors_graphics_v5.json").read_text(encoding="utf-8"));crew_art=PxlImage.from_bytes(after.read_file(crew_batch["file_path"]))
    font=GameAsciiFont.from_arm9(after.read_file("/__arm9__.bin"));cases=[];screens=[]
    for folder,number,label in [("town",16600,"Captain, displayed Raphael Castor"),("town",16900,"Janus"),("town",17200,"Claudio"),("town",17500,"Julio"),("lil_items",10500,"Lil")]:
        image,row=frame(folder,number,digest);screens.append((label,image))
        for record in person_batch["records"]:
            x0,y0,x1,y1=record["plaque_box"]
            for y in range(y0,y1):
                for x in range(x0,x1):assert native5(image.getpixel((x,y)))==native5(person_art.palette[person_art.indices[y*256+x]])
        abilities=[]
        for name,x,y in [("Command",16,272),("Sailing",96,272),("Survey",176,272),("Finance",16,296),("Observe",96,296),("Vigor",176,296),("Aim",16,320),("Swords",96,320),("Speech",176,320),("Guile",16,344)]:
            value=numeric_field(font,image,x+42,y);assert 0<=value<=500
            ink,bounds=complete_mask(font,f"{name:>7}{value:3d}",image,x,y,(230,230,230))
            abilities.append({"name":name,"value":value,"full_bounds":bounds,"full_line_ink":ink})
        cases.append({"character_context":label,"capture":row,"all10_complete_plaque_areas_exact":True,"all10_complete_skill_label_number_lines":abilities,"fully_completed":False})
    hints=[]
    for text,number,x0,x1,runpath in [("Equipped Items",10500,136,224,"work/analysis/plaque_style_v247/tooltip_runs.bin"),("Armor",12000,64,98,str(ROOT/"armor_paper_runs.bin")),("Weapon",12600,16,56,str(ROOT/"weapon_paper_runs.bin"))]:
        image,row=frame("lil_items",number,digest);ink,bounds=complete_mask(font,text,image,x0+2,210,(0,8,0));paper=0;data=Path(runpath).read_bytes()
        for offset in range(0,len(data),20):
            x,y,w,h,color=struct.unpack_from("<5I",data,offset);assert h==1
            expected=(color&31,color>>5&31,color>>10&31)
            for col in range(w):
                actual=image.getpixel((x0+x+col,208+y))
                if actual!=(0,8,0):assert native5(actual)==expected;paper+=1
        assert paper==(x1-x0)*16-ink
        hints.append({"text":text,"capture":row,"complete_glyph_bounds":bounds,"all_native_font_ink_pixels":ink,"paper_pixels_exact":paper,"full_texture_and_bevel_exact":True,"fully_completed":False})
        screens.append((text,image))
    crew=[]
    for number,label in [(10000,"initial assignment"),(10500,"after Lo"),(11000,"after Hi"),(11600,"after one decrease")]:
        image,row=frame("crew_trimmed",number,digest)
        for record in crew_batch["records"]:
            x0,y0,x1,y1=record["plaque_box"]
            for y in range(y0,y1):
                for x in range(x0,x1):assert native5(image.getpixel((x,y)))==native5(crew_art.palette[crew_art.indices[y*256+x]])
        values={key:right_aligned_number(font,image,right) for key,right in [("need",160),("now",196),("max",232)]}
        crew.append({"state":label,"capture":row,"all7_complete_plaque_areas_exact":True,"observed_displayed_crew_values":values,"inventory_arithmetic_not_inferred":True,"fully_completed":False})
        screens.append((label,image))
    # Record complete older frames outside the short-hint changes as regression evidence.
    unchanged=0
    for folder,oldfolder in [("lil_items","lil_items"),("town","town"),("crew_trimmed","crew_trimmed")]:
        prior_dir=Path("work/emulation_v193/plaque_coverage_v252")/oldfolder
        old_report=json.loads((prior_dir/"capture_report.json").read_text(encoding="utf-8"));new_report=json.loads((CAPTURE/folder/"capture_report.json").read_text(encoding="utf-8"))
        lookup={r["frame"]:r["PNG_sha256"] for r in old_report["frames_captured"] if "cold_boot" in r["path"]}
        for row in new_report["frames_captured"]:
            assert sha(Path(row["path"]).read_bytes())==row["PNG_sha256"]
            if "cold_boot" in row["path"] and (folder!="lil_items" or row["frame"]<11600):
                assert lookup[row["frame"]]==row["PNG_sha256"];unchanged+=1
    sheet=Image.new("RGB",(1024,((len(screens)+3)//4)*410),"#333");draw=ImageDraw.Draw(sheet)
    for n,(label,image) in enumerate(screens):
        x=n%4*256;y=n//4*410;draw.text((x+4,y+4),label,fill="white");sheet.paste(image,(x,y+24))
    sheet.save(ROOT/"expanded_live_audit.png")
    proof={"format":"dk4-expanded-plaque-audit-v252","candidate":str(ROM),"candidate_sha256":digest,"patch":str(patch),"patch_sha256":sha(patch.read_bytes()),"profile":m["profile"],"base_sha256":m["base_sha256"],
           "all467_prior_batches_required_layers_stages_and_records_retained":True,"all_ROM_files_routes_art_and_prior43_fringe_pixels_unchanged":True,"only_ARM9_changed":True,
           "complete_V251_reproduction_exact":True,"exact_clean_patch_reconstruction":True,"sailor_cases":cases,"hint_cases":hints,"crew_cases":crew,"unchanged_regression_frames":unchanged,
           "occupied_item_name_dimensions_other_health_mood_states_and_full_route_coverage_pending":True,
           "displayed_Raphael_spelling_still_differs_from_locked_Rafael_policy":True,"all18_base_plaque_hint_audit_entries_remain_incomplete":True,"new_Armor_Weapon_variants_incomplete":True,"experimental_user_acceptance_pending":True,"full_goal_complete":False}
    (ROOT/"saved_live_proof.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"candidate_sha256":digest,"patch_sha256":proof["patch_sha256"],"sailor_cases":len(cases),"hint_cases":len(hints),"crew_cases":len(crew),"unchanged_regression_frames":unchanged}))


if __name__=="__main__":
    main()
