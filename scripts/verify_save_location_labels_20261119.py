"""Verify Save and Load list text against native glyphs and paired frames."""

from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_save_location_labels_20261119 as replay
from scripts import verify_save_dialogue_followup_20261119 as prior

stage, base = replay.stage, replay.base
STARTUP = stage.ROOT / "own_startup_verification.json"
GAME = stage.ROOT / "verified_slot_lists.json"
SHEET = stage.ROOT / "save_load_comparison.png"
OFFLINE = stage.ROOT / "stock_sea_area_labels.png"
WHITE = (230,230,230)
SEA = (108,236,215,255)
DOCKED = (108,208,227,227)
HEADING = (32,0,224,15)


def glyph_points(font,text):
    points = {(6*i+x,y) for i,ch in enumerate(text)
              for cell in (font.decode(ch),) for x in range(6) for y in range(11) if cell.getpixel((x,y))}
    assert points and len(text)>1
    assert any(x<6 for x,_ in points) or text.startswith(" ")
    assert any(x>=6*(len(text)-1) for x,_ in points)
    return points


def exact_mask(image,font,text,rect):
    left,top,right,bottom = rect
    current = {(x,y) for x in range(left,right) for y in range(top,bottom)
               if image.getpixel((x,y)) == WHITE}
    expected = glyph_points(font,text)
    origin = (min(x for x,_ in current)-min(x for x,_ in expected),
              min(y for _,y in current)-min(y for _,y in expected))
    assert left <= origin[0] and origin[0]+len(text)*6 <= right
    assert top <= origin[1] and origin[1]+11 <= bottom
    assert {(origin[0]+x,origin[1]+y) for x,y in expected} == current, (text,origin)
    return dict(text=text,rect=rect,origin=origin,complete_white_pixels=len(current))


def startup():
    scope = vars(prior.startup_workflow) | dict(stage=stage,replay=replay,STARTUP=STARTUP,__file__=__file__)
    FunctionType(prior.startup_workflow.startup.__code__,scope)()
    boot = base.load(STARTUP)
    snapshot = boot["read_only_snapshot"]
    assert base.digest(snapshot["path"]) == snapshot["sha256"]
    live = Path(snapshot["path"]).read_bytes()
    stored = base.load(stage.PROOF)
    for at,span in stored["slots_changed"].items():
        offset = int(at)
        arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
        assert live[offset:offset+span] == arm[offset:offset+span]


def gameplay():
    assert not any(p.exists() for p in (GAME,SHEET,OFFLINE))
    staged = base.load(stage.PROOF)
    parent = base.load(stage.parent.RELEASE)
    assert base.digest(stage.ROM) == staged["candidate_sha256"]
    assert base.digest(stage.parent.ROM) == parent["candidate_sha256"] == staged["parent_sha256"]
    sides, evidence = [], {}
    for label, sha in (("before",parent["candidate_sha256"]),("after",staged["candidate_sha256"])):
        term_path = stage.ROOT / label / "terminal.json"
        terminal = base.load(term_path)
        assert base.digest(terminal["report"]) == terminal["report_sha256"]
        report, _ = prior.checked_report(terminal["report"],sha,replay.FRAMES[-1])
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
        assert base.digest(report["battery_save_preloaded"]["source"]) == terminal["donor_sha256"]
        assert not any(value for k,value in report.items() if k.startswith("synthetic_"))
        captures = {r["frame"]:r for r in report["frames_captured"]}
        assert set(replay.FRAMES) <= set(captures)
        sides.append((report,captures))
        evidence.update({str(term_path):base.digest(term_path),terminal["report"]:terminal["report_sha256"]})
    fields = ("scripted_input_schedule","core_options","exact_requested_capture_frames")
    assert all(sides[0][0][k] == sides[1][0][k] for k in fields)

    arm_old,arm = (base.NdsImage.open(p).read_file(stage.ARM) for p in (stage.parent.ROM,stage.ROM))
    font = GameAsciiFont.from_arm9(arm)
    assert font == GameAsciiFont.from_arm9(arm_old)
    rows,stable = [],[]
    sheet = Image.new("RGB",(1024,408),"#2a3741")
    draw = ImageDraw.Draw(sheet)
    for frame in replay.FRAMES:
        old_shot,new_shot = (captures[frame] for _,captures in sides)
        old,new = (Image.open(shot["path"]).convert("RGB") for shot in (old_shot,new_shot))
        if frame not in (6200,7400):
            assert old.tobytes() == new.tobytes()
            stable.append(frame)
            continue
        is_save = frame == 6200
        old_title = "Select a save slot." if is_save else "Select data to load."
        new_title = old_title if is_save else "Select a save to load."
        full = ("N. SeaAt Sea","N. Sea At Sea","Stockholm Docked")
        mask_a = [exact_mask(old,font,full[0],SEA),exact_mask(old,font,old_title,HEADING),
                  exact_mask(old,font,full[2],DOCKED)]
        mask_b = [exact_mask(new,font,full[1],SEA),exact_mask(new,font,new_title,HEADING),
                  exact_mask(new,font,full[2],DOCKED)]
        assert mask_a[0]["origin"] == mask_b[0]["origin"] and mask_a[2] == mask_b[2]
        allowed = (SEA,) if is_save else (SEA,HEADING)
        differences = [(i%256,i//256) for i,(a,b) in enumerate(zip(
            old.get_flattened_data(),new.get_flattened_data(),strict=True)) if a!=b]
        assert differences and all(any(l<=x<r and t<=y<bot for l,t,r,bot in allowed) for x,y in differences)
        for i,(photo,label) in enumerate(((old,"Before"),(new,"After"))):
            x,y = i*512,0 if is_save else 204
            draw.text((x+6,y+3),f'{"Save" if is_save else "Load"} · {label}',fill="white")
            band = Image.new("RGB",(256,88),"#2a3741")
            band.paste(photo.crop((0,0,256,16)),(0,0))
            band.paste(photo.crop((0,200,256,256)),(0,20))
            sheet.paste(band.resize((512,176),Image.Resampling.NEAREST),(x,y+20))
        rows.append(dict(frame=frame,menu="Save" if is_save else "Load",original_capture=old_shot,
            revised_capture=new_shot,before=mask_a,after=mask_b,pixels_changed=len(differences),
            every_pixel_outside_verified_rectangles_matches=True))
    assert stable == [5400,5800,6600,7000] and len(rows)==2
    sheet.save(SHEET)

    spans = staged["stock_and_fallback_painter_arguments"]
    assert len(spans)==18
    rows_by_code = {row["region"]:row for row in spans if row["consumer"]=="Save"}
    assert all(rows_by_code[r["region"]]["combined"]==r["combined"] for r in spans)
    offline = Image.new("RGB",(480,264),"#2a3741")
    pen = ImageDraw.Draw(offline)
    for i,code in enumerate([*range(7),7]):
        row = rows_by_code[code]
        assert row["maximum_width_px"]<=96
        text = row["combined"]
        offset = 33*i
        pen.text((8,offset+5),str(code) if code<7 else "No area",fill="white")
        points = glyph_points(font,text)
        assert max(x for x,_ in points) < row["maximum_width_px"]
        bar = Image.new("RGB",(144,13),"#19333d")
        for x,y in points:
            bar.putpixel((x,y),WHITE)
        offline.paste(bar.resize((288,26),Image.Resampling.NEAREST),(104,offset+2))
    offline.save(OFFLINE)
    evidence.update({str(p):base.digest(p) for p in (stage.PROOF,SHEET,OFFLINE,Path(__file__))})
    base.save(GAME,dict(candidate_sha256=staged["candidate_sha256"],ordinary_emulator_controls=True,
        both_menus_observed=rows,other_paired_complete_frames=stable,hardware=False,
        exact_stock_and_fallback_painter_inputs=len(spans),observed_stock_area="N. Sea",
        other_stock_areas_checked_offline=True,evidence=evidence))
    print("Both slot lists and headings match complete glyph masks. Four control frames and all outside pixels match.")


if __name__ == "__main__":
    gameplay()
    startup()

