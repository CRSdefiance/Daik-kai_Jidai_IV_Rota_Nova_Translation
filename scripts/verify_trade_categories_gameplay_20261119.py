"""Verify the longer Goods Info category in ordinary Local and Cargo gameplay."""

from pathlib import Path

from PIL import Image,ImageChops,ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_trade_categories_20261119 as game
from scripts.finish_refit_display_v712 import load as load_capture
from scripts.verify_commodity_private_market_live_v354 import exact_label

stage,base = game.stage,game.stage.base
FOCUS = ((10400,"Local"),(11600,"Cargo"))


def main():
    assert not game.PLAYBACK.exists()
    staged = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate==staged["candidate_sha256"]
    (baseline,old,prior_ref),(current,new,current_ref) = [load_capture(folder,digest,11600) for folder,digest in (
        (game.replay.ROOT/"corrected",staged["parent_sha256"]),(game.CAPTURE,candidate))]
    for report in (baseline,current):
        assert report["core_options"]==baseline["core_options"]
        assert report["scripted_input_schedule"]==baseline["scripted_input_schedule"]
        assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
        donor = report["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"])==donor["source_sha256"]
    assert old.keys()==new.keys()
    changed = [frame for frame in old if old[frame].tobytes()!=new[frame].tobytes()]
    assert changed==[10000,10400,10800,11200,11600]
    for frame in changed:
        difference = ImageChops.difference(old[frame],new[frame]).getbbox()
        assert difference and 144<=difference[0]<difference[2]<=256 and 139<=difference[1]<difference[3]<=150
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    holds = []
    sheet = Image.new("RGB",(840,266),"#263238")
    draw = ImageDraw.Draw(sheet)
    for index,(frame,view) in enumerate(FOCUS):
        old_mask = exact_label(old[frame],font,"Olive Oil\n  Cond. 100%",(144,127),(144,126,256,162))
        new_mask = exact_label(new[frame],font,"Olive Oil\n  Seasonings 100%",(144,127),(144,126,256,162))
        holds.append(dict(frame=frame,view=view,previous=old_mask,registered=new_mask))
        for column,(shots,label) in enumerate(((old,"previous"),(new,"revised"))):
            x,y = column*420,index*133
            draw.text((x+5,y+3),f"{view}   {label}",fill="white")
            crop = shots[frame].crop((128,121,256,163)).resize((384,110),Image.Resampling.NEAREST)
            sheet.paste(crop,(x+5,y+19))
    path = stage.ROOT/"seasonings_local_and_cargo.png"
    sheet.save(path)
    evidence = {r["report"]:r["sha256"] for r in (prior_ref,current_ref)}
    evidence.update({str(p):base.digest(p) for p in (path,Path(__file__))})
    for report in (baseline,current):
        evidence.update({r["path"]:r["PNG_sha256"] for r in report["frames_captured"] if r["frame"] in changed})
    base.save(game.PLAYBACK,dict(candidate_sha256=candidate,ordinary_input=True,hardware=False,
        local_and_cargo_holds=holds,sampled_changed_frames=changed,exact_other_frames=sorted(set(old)-set(changed)),
        only_category_and_shifted_percentage_pixels_changed=True,goods_name_and_suffix_masks_complete=True,
        sheets=[dict(path=str(path),sha256=base.digest(path))],evidence=evidence))
    print("Both Trade views show the complete Seasonings label and percentage with the original panel layout.")


if __name__=="__main__":
    main()
