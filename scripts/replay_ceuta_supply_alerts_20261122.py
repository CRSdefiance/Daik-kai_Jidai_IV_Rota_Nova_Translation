"""Verify both natural shortage alerts on the registered predecessor and staged ROM."""

from argparse import ArgumentParser
import sys

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_ceuta_sea_encounters_20261122 as voyage
from scripts import stage_ceuta_supply_alerts_20261122 as stage
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.verify_mutiny_release_inputs_v1 import portrait_ink


base,native = stage.base,stage.native
ROOT = stage.ROOT / "ordinary_replay"
BASELINE = voyage.ROOT / "capture/capture_report.json"
REPORT = ROOT / "capture/capture_report.json"
LIVE, SHEET = ROOT / "verified_gameplay.json", ROOT / "supply_alert_comparison.png"
CONTROL = (3200,4300,8310,8876,9476,10100)
AT = {9076:("Water","water"),9276:("Food","food")}
FRAMES = (*CONTROL,*AT)
BODY_BOX = (16,296,244,360)


def replay():
    assert not ROOT.exists()
    old,proof = map(base.load,(BASELINE,stage.PROOF))
    assert old["ROM_sha256"] == proof["predecessor_sha256"] == base.digest(stage.parent.ROM)
    donor = old["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    assert old["frames"]==10101 and old["cold_boot"] and not old["savestate_loaded"]
    assert not old["callback_errors"] and not any(v for k,v in old.items() if k.startswith("synthetic_"))
    ROOT.mkdir()
    inputs = ROOT/"inputs.json"
    base.save(inputs,old["scripted_input_schedule"])
    argv = sys.argv
    try:
        sys.argv = [voyage.harness.__file__, "--rom", str(stage.ROM),"--out",str(REPORT.parent),"--frames","10101",
            "--inputs-json",str(inputs),"--press-start","-1","--touchscreen","--battery-save",donor["source"],
            "--capture-every","999999","--dump-ram","--capture-at",*map(str,sorted(FRAMES))]
        voyage.harness.main()
    finally:
        sys.argv = argv
    assert base.digest(donor["source"]) == donor["source_sha256"]


def verify():
    assert not LIVE.exists()
    before,after,proof,offline = map(base.load,(BASELINE,REPORT,stage.PROOF,stage.NATIVE))
    assert base.digest(stage.ROM)==after["ROM_sha256"]==offline["candidate_sha256"]==proof["candidate_sha256"]
    assert before["ROM_sha256"]==base.digest(stage.parent.ROM)==proof["predecessor_sha256"]
    assert before["scripted_input_schedule"]==after["scripted_input_schedule"] and before["frames"]==after["frames"]==10101
    for run in (before,after):
        assert run["cold_boot"] and not run["callback_errors"] and not run["savestate_loaded"]
        assert not any(v for k,v in run.items() if k.startswith("synthetic_"))
        donor = run["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"])==donor["source_sha256"]
    assert all(before["battery_save_preloaded"][k]==after["battery_save_preloaded"][k] for k in ("source","source_sha256"))
    pictures = [{r["frame"]:r for r in run["frames_captured"] if r["path"].endswith("_cold_boot.png")} for run in (before,after)]
    im = base.NdsImage.open(stage.ROM)
    render,_,_ = font_tools(im)
    arm,kanji = (im.read_file(id) for id in (stage.ARM,"/GRP/KANJI.FNT"))
    presentations,cells = [],[]
    for frame,(old,new) in AT.items():
        row, = [r for r in offline["all_supply_modes_and_voice_cases"] if r["message_ID"]==601 and r["arguments"]==[new]]
        complete = []
        for label,frames,arg in (("Before",pictures[0],old),("After",pictures[1],new)):
            hit = frames[frame]
            assert base.digest(hit["path"])==hit["PNG_sha256"]
            text = f"No {arg} left!"
            pixels,glyphs = render_portrait(render,arm,kanji,b" "+text.encode("ascii"))
            assert portrait_ink(hit["path"],BODY_BOX) == bytes(v==1 for v in pixels)
            if label=="After":
                assert row["lines"]==[text] and native.digest(pixels)==row["native_plane_sha256"]
            with Image.open(hit["path"]) as shot:
                snapshot = shot.convert("RGB")
            cells.append((f"{label} / {text}",snapshot))
            complete.append(dict(capture=hit,text=text,glyph_count=len(glyphs),exact_native_ink=True))
        a,b = (img for _,img in cells[-2:])
        difference = ImageChops.difference(a,b).getbbox()
        assert difference and 16<=difference[0]<difference[2]<=244 and 296<=difference[1]<difference[3]<=312
        presentations.append(dict(frame=frame,message_ID=601,before=complete[0],after=complete[1],diff_rectangle=difference))

    controls = []
    for frame in CONTROL:
        a,b = (run[frame] for run in pictures)
        assert base.digest(a["path"])==a["PNG_sha256"] and base.digest(b["path"])==b["PNG_sha256"]
        assert a["framebuffer_sha256"]==b["framebuffer_sha256"],frame
        controls.append(b)
    for text, number in (("Before supply depletion at sea",8876),("Return to sailing after both alerts",9476)):
        with Image.open(pictures[1][number]["path"]) as im:
            cells.append((text,im.convert("RGB")))
    sheet = Image.new("RGB",(1024,412*3),"#263238")
    title = ImageDraw.Draw(sheet)
    for i,(text,picture) in enumerate(cells):
        x,y = (i%2)*512,(i//2)*412
        title.text((x+4,y+2),text,fill="white")
        sheet.paste(picture.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+19))
    sheet.save(SHEET)
    base.save(LIVE,dict(candidate_sha256=after["ROM_sha256"],predecessor_sha256=before["ROM_sha256"],
        normal_sailing_inputs=True,no_supplied_encounter_or_resource_conditions=True,ordinary_alerts=presentations,
        matched_control_frames=controls,older_foam_event_not_triggered=True,
        ordinary_automatic_travel_cancellation_unvisited=True,hardware=False,
        sheet=str(SHEET),sheet_sha256=base.digest(SHEET),
        evidence={str(p):base.digest(p) for p in (BASELINE,REPORT,stage.NATIVE,ROOT/"inputs.json")}))


if __name__ == "__main__":
    cli=ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("replay","verify"))
    globals()[cli.parse_args().action]()

