"""Verify full Trade labels and isolate their pixel changes in Local and Cargo."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_trade_labels_20261119 as game
from scripts.finish_refit_display_v712 import load as load_capture
from scripts.verify_commodity_private_market_live_v354 import exact_label

stage,base = game.stage,game.stage.base
FOCUS = (10400,11600)


def rectangle(row):
    x,y,_,_,width,height = row
    return (x,y,x+width,y+height)


def verify():
    assert not game.PLAYBACK.exists()
    staged = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate==staged["candidate_sha256"]
    runs = [load_capture(game.replay.ROOT/name,digest,11600) for name,digest in
            (("baseline",staged["parent_sha256"]),("corrected",candidate))]
    (before,old,prior_ref),(current,new,current_ref) = runs
    trace_report = base.load(stage.TRACE/"capture/capture_report.json")
    trace_frames = {r["frame"]:r["framebuffer_sha256"] for r in trace_report["frames_captured"]}
    for report in (before,current):
        assert report["core_options"]==before["core_options"] and report["scripted_input_schedule"]==before["scripted_input_schedule"]
        assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
        donor = report["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"])==donor["source_sha256"]
    assert before["battery_save_preloaded"]["source_sha256"]==current["battery_save_preloaded"]["source_sha256"]
    assert all(r["framebuffer_sha256"]==trace_frames[r["frame"]] for r in before["frames_captured"] if r["frame"] in FOCUS)
    assert old.keys()==new.keys()
    changed = [frame for frame in old if old[frame].tobytes()!=new[frame].tobytes()]
    assert set(FOCUS)<=set(changed) and {9200,9600}.isdisjoint(changed)

    image = base.NdsImage.open(stage.ROM)
    font = GameAsciiFont.from_arm9(image.read_file(stage.ARM))
    rows = staged["records"]
    rectangles = [rectangle(row[key]) for row in rows if row["display_changed"] for key in ("original_geometry","staged_geometry")]
    changed_mask = {(x,y) for x0,y0,x1,y1 in rectangles for x in range(x0,x1) for y in range(y0,y1)}
    for frame in changed:
        difference = ImageChops.difference(old[frame],new[frame])
        box = difference.getbbox()
        assert box is not None and box[3]<192
        for y in range(box[1],box[3]):
            for x in range(box[0],box[2]):
                assert difference.getpixel((x,y))==(0,0,0) or (x,y) in changed_mask,(frame,x,y)
    holds = []
    for frame in FOCUS:
        captions = []
        for row in rows:
            before_text = "Stat" if row["previous_English"]=="Status" else row["previous_English"]
            text = row["english"]
            before_box = rectangle(row["original_geometry"])
            after_box = rectangle(row["staged_geometry"])
            before_mask = exact_label(old[frame],font,before_text,(before_box[0],before_box[1]+1),before_box,advance=6)
            after_mask = exact_label(new[frame],font,text,(after_box[0],after_box[1]+1),after_box,advance=6)
            captions.append(dict(id=row["id"],previous=before_mask,current=after_mask))
        for shots in (old,new):
            mask = exact_label(shots[frame],font,"Olive Oil\n  Cond. 100%",(144,127),(144,126,256,162))
            assert mask["exact_ink_pixels"]==224
        holds.append(dict(frame=frame,view="Local" if frame==10400 else "Cargo",captions=captions))
    canvas = Image.new("RGB",(1024,804),"#263238")
    draw = ImageDraw.Draw(canvas)
    for i,frame in enumerate(FOCUS):
        for j,(shots,label) in enumerate(((old,"before"),(new,"corrected"))):
            x,y = j*512,i*402
            draw.text((x+5,y+5),f"{holds[i]['view']}  {label}",fill="white")
            panel = shots[frame].crop((0,0,256,192)).resize((512,384),Image.Resampling.NEAREST)
            canvas.paste(panel,(x,y+18))
    sheet = stage.ROOT/"trade_label_comparison.png"
    canvas.save(sheet)
    evidence = {r["report"]:r["sha256"] for r in (prior_ref,current_ref)}
    evidence.update({str(p):base.digest(p) for p in (sheet,Path(__file__),stage.TRACE/"capture/capture_report.json")})
    for report in (before,current):
        evidence.update({r["path"]:r["PNG_sha256"] for r in report["frames_captured"] if r["frame"] in changed})
    base.save(game.PLAYBACK,dict(candidate_sha256=candidate,ordinary_input=True,hardware=False,
        local_and_cargo_holds=holds,visible_status_glyphs_complete=True,sampled_changed_frames=changed,
        exact_other_frames=sorted(set(old)-set(changed)),pixels_outside_changed_text_exact=True,
        registered_Goods_Info_complete_in_both_views=True,original_trade_amounts_icons_controls_exact=True,
        sheets=[dict(path=str(sheet),sha256=base.digest(sheet))],evidence=evidence))
    print("Verified all 12 captions in Local and Cargo and matching pixels outside the four revised labels.")


if __name__=="__main__":
    verify()
