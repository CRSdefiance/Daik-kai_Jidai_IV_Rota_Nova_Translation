"""Native source bevels, 17 full labels, eight hints, ABI and exact patch."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.direct_equipment_paper import FRAMEBUFFER, ORIGIN_X, ORIGIN_Y
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.source_plaque_bevels import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.native_inventory_fixture_v481 import transfer
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_equipment_long_names_v536 import CASES
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path("out/all_routes_combined_v546_candidate.nds")
ROOT = Path("work/analysis/plaque_borders_v546")
CAPTURES = Path("E:/Rota Nova translations/Generated/work/emulation_v193")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def report(name, digest):
    folder = CAPTURES / f"plaque_borders_v546_{name}"
    r = read(folder / "capture_report.json")
    assert r["ROM_sha256"] == digest and r["cold_boot"] and not r["savestate_loaded"]
    assert not r["callback_errors"]
    for s in r["frames_captured"]:
        assert sha(Path(s["path"]).read_bytes()) == s["PNG_sha256"]
    return r, {s["frame"]: s for s in r["frames_captured"]}


def hint(font, tile, image, text, slot):
    width = len(text) * 6 + 4
    left = min(slot, 224 - width)
    ink, bounds = complete_mask(font, text, image, left + 2, 210, (0, 8, 0))
    expected = {(left + 2 + n * 6 + x, 210 + y) for n, c in enumerate(text)
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    for y in range(16):
        for x in range(width):
            dx = x if x < 2 else 42 + x - width + 2 if x >= width - 2 else 2 + (x - 2) % 40
            color = struct.unpack_from("<H", tile, (y * 44 + dx) * 2)[0]
            rgb = (0, 1, 0) if (left + x, 208 + y) in expected else (
                color & 31, (color >> 5) & 31, (color >> 10) & 31)
            assert native5(image.getpixel((left + x, 208 + y))) == rgb, (text, x, y)
    return {"english": text, "all_grain_bevel_letters_exact": width * 16,
            "complete_font_pixels": ink, "font_bounds": bounds}


def renderer_cases(arm, tile, plan):
    u = machine(arm)
    u.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    manager = 0x02450000
    u.mem_write(ORIGIN_X, bytes(4)); u.mem_write(ORIGIN_Y, bytes(4))
    seed = b"\xA5" * 0x30000
    cases = []
    for screen in (0, 1):
        for width in range(10, 245):
            u.mem_write(FRAMEBUFFER - 16, b"\xA5" * (0x30000 + 32))
            u.mem_write(plan["state_pointer"], struct.pack("<I", manager))
            u.mem_write(manager + 0x18, struct.pack("<I", screen))
            u.mem_write(manager + 0x20, struct.pack("<4I", 6, 12, 6 + width, 28))
            call(u, plan["entry"] - BASE, (manager, 0, 255, 255))
            expected = bytearray(seed)
            for y in range(16):
                for x in range(width):
                    dx = x if x < 2 else 42 + x - width + 2 if x >= width - 2 else 2 + (x - 2) % 40
                    value = struct.unpack_from("<H", tile, (y * 44 + dx) * 2)[0]
                    struct.pack_into("<H", expected, screen * 0x18000 + ((12 + y) * 256 + 6 + x) * 2, value)
            assert bytes(u.mem_read(FRAMEBUFFER, 0x30000)) == expected
            assert bytes(u.mem_read(FRAMEBUFFER - 16, 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(FRAMEBUFFER + 0x30000, 16)) == b"\xA5" * 16
            cases.append({"screen": screen, "width": width, "all_bytes_bounds_and_saved_register_stack_ABI_exact": True})
    fallbacks = []

    def catch(uc, address, _size, _data):
        if address == plan["old_dispatcher"]:
            fallbacks.append(address)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, catch)
    for width, height, screen, x, y, active in [(9,16,0,6,12,True),(245,16,0,0,12,True),
        (130,15,0,6,12,True),(130,17,0,6,12,True),(130,16,2,6,12,True),
        (130,16,0,0xFFFFFFFF,12,True),(130,16,0,127,12,True),(130,16,0,6,177,True),
        (130,16,0,6,12,False)]:
        u.mem_write(FRAMEBUFFER, seed)
        u.mem_write(plan["state_pointer"], struct.pack("<I", manager if active else 0))
        u.mem_write(manager + 0x18, struct.pack("<I", screen))
        u.mem_write(manager + 0x20, struct.pack("<4I", x,y,(x+width)&0xFFFFFFFF,y+height))
        count = len(fallbacks)
        call(u, plan["entry"] - BASE, (manager,0,255,255))
        assert len(fallbacks) == count + 1 and bytes(u.mem_read(FRAMEBUFFER,0x30000)) == seed
    u.hook_del(hook)
    return cases


def main():
    current = NdsImage.open(ROM); parent = NdsImage.open("out/all_routes_combined_v545_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes()); manifest = read(ROM.with_suffix(".manifest.json"))
    prior_manifest = read("out/all_routes_combined_v545_candidate.manifest.json")
    assert manifest["candidate_sha256"] == digest and manifest["profile"] == "all-routes-unified-v546"
    assert manifest["batches"] == prior_manifest["batches"] and len(manifest["batches"]) == 470
    assert len(read("translations/release_stack.json")["accepted_layers"]) == 114
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    old = {p:d for _,p,d in parent.iter_files()} | dict(parent.iter_components())
    new = {p:d for _,p,d in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys()
    assert sorted(p for p in old if old[p] != new[p]) == ["/__arm9__.bin","/_pxl/dividecrewinfo.pxl","/_pxl/personinfo.pxl"]
    expected, stage = apply_release(parent, clean, "translations/source_plaque_bevels_v1.json")
    assert all(new[path] == data for path,data in expected.items())
    config = read("translations/source_plaque_bevels_v1.json")
    arm = new["/__arm9__.bin"]; font = GameAsciiFont.from_arm9(arm)
    plan = read("work/analysis/direct_equipment_v270/runtime_plan.json")
    pool = bytes(MainCodeFile(arm,BASE).sections[3].data)
    tile = pool[plan["tile_pointer"]-POOL:plan["tile_pointer"]-POOL+1408]
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    # Independent coordinate checks against the clean frame, not old paper().
    for y in range(16):
        for x in range(44):
            if 2 <= x < 42 and 2 <= y < 14: continue
            sx = 8+x if x<2 else 46+x-42 if x>=42 else 10+(x-2)%36
            rgb = native5(donor.palette[donor.indices[(20+y)*256+sx]])
            value = struct.unpack_from("<H",tile,(y*44+x)*2)[0]
            assert rgb == (value&31,(value>>5)&31,(value>>10)&31)
    renderer = renderer_cases(arm,tile,plan)
    native = []
    for name, group, selections in zip(("crew","person"),config["files"],
                                       ((10000,10300,10600),(10500,12600,13500,14400)),strict=True):
        _, frames = report(name,digest)
        asset = PxlImage.from_bytes(new[group["file_path"]])
        for frame in selections:
            shot = Image.open(frames[frame]["path"]).convert("RGB")
            for row in group["records"]:
                l,t,r,b = row["plaque_box"]
                assert all(native5(shot.getpixel((x,y))) == native5(asset.palette[asset.indices[y*256+x]])
                           for y in range(t,b) for x in range(l,r))
                dl,dt,dr,db = row["draw_box"]
                tx,ty = dl+(dr-dl-len(row["english"])*5)//2,dt+(db-dt-11)//2
                wanted = {(tx+n*5+x,ty+y) for n,c in enumerate(row["english"])
                          for y in range(11) for x in range(6) if font.decode(c).getpixel((x,y))}
                found = {(x,y) for y in range(t,b) for x in range(l,r)
                         if native5(shot.getpixel((x,y))) == native5(asset.palette[row["ink_palette_index"]])}
                assert found == wanted
                native.append({"english":row["english"],"frame":frame,"all_native_pixels_and_full_letters_exact":True})
    run, frames = report("slots",digest)
    raw = (CAPTURES/"plaque_borders_v546_slots/frame_003000_arm9_ram.bin").read_bytes()
    _, fixture = transfer(arm,raw,[40,71,92,98,126])
    assert run["synthetic_inventory_fixtures"] == [dict(fixture,frame=3000)]
    displays=[]
    for text,frame,slot in [(name,f,slot) for _,name,f,slot in CASES] + [
                           ("Weapon",6200,16),("Armor",7000,64),("Equipped Items",12000,208)]:
        shot=Image.open(frames[frame]["path"]).convert("RGB")
        displays.append({"frame":frame,"display":hint(font,tile,shot,text,slot),"capture":frames[frame]["path"]})
    save=read(ROOT/"save_copy_manifest.json")
    assert sha(Path(save["source"]).read_bytes()) == save["source_sha256"]
    assert sha(Path(save["test_copy"]).read_bytes()) == save["test_copy_sha256"]
    fresh,_=report("fresh",digest)
    previous=read(CAPTURES/"treasure_texture_v545_fresh/capture_report.json")
    assert fresh["scripted_input_schedule"] == previous["scripted_input_schedule"]
    assert fresh["core_options"] == previous["core_options"]
    a,b=[{s["frame"]:s["PNG_sha256"] for s in r["frames_captured"]} for r in (fresh,previous)]
    assert a==b and len(a)==56
    preservation=read("work/analysis/treasure_texture_v545/preservation_proof.json")
    assert len(preservation["entries"])==921
    for path in ("/_pxl/dividecrewinfo.pxl","/_pxl/personinfo.pxl"):
        src,dst=PxlImage.from_bytes(clean.read_file(path)),PxlImage.from_bytes(new[path])
        assert src.source[:src.pixels_offset]==dst.source[:dst.pixels_offset] and len(src.indices)==len(dst.indices)
    assert all(old[r["path"]]==new[r["path"]] for r in preservation["entries"]
               if r["path"] not in ("/_pxl/dividecrewinfo.pxl","/_pxl/personinfo.pxl"))
    preservation.update(candidate=str(ROM),candidate_sha256=digest,parent_proof="work/analysis/treasure_texture_v545/preservation_proof.json")
    (ROOT/"preservation_proof.json").write_text(json.dumps(preservation,indent=2)+"\n",encoding="utf-8")
    make_xdelta(Path("work/clean.nds"),ROM,ROM.with_suffix(".xdelta"))
    apply_xdelta(Path("work/clean.nds"),ROM.with_suffix(".xdelta"),ROOT/"reconstructed.nds")
    assert (ROOT/"reconstructed.nds").read_bytes()==ROM.read_bytes()
    plaques=read("translations/graphics_completion_campaign_v1.json")["plaque_style_v247"]["ongoing_plaque_inventory"]
    assert len(plaques)==18 and all(not p["fully_completed"] for p in plaques)
    assert len(read("translations/graphics_completion_requirements_v313.json")["historical_pending_items_retained"])==22
    proof={"candidate":str(ROM),"candidate_sha256":digest,"profile":manifest["profile"],
           "base":manifest["base_rom"],"base_sha256":manifest["base_sha256"],
           "patch_sha256":sha(ROM.with_suffix(".xdelta").read_bytes()),"exact_clean_patch_reconstruction":True,
           "stage":stage,"native_painter_cases":renderer,"nine_invalid_contracts_delegate_without_writes":True,
           "native_plaque_cases":native,"native_equipment_hints":displays,"all56_regression_frames_exact_V545":True,
           "all_instructions_heap_startup_cache_layout_and_fine_grain_interiors_preserved":True,
           "all470_batches114_layers921_preservation_entries_retained":True,
           "source_and_test_saves_unchanged_temporary_inventory_only":True,"all18_entries_remain_incomplete":True,
           "experimental":True,"canonical_promoted":False,"full_goal_complete":False}
    (ROOT/"release_proof.json").write_text(json.dumps(proof,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("V546: 61 full plaques, eight full hints, 470 renderer cases, 56 regression frames and exact patch pass.")


if __name__ == "__main__":
    main()
