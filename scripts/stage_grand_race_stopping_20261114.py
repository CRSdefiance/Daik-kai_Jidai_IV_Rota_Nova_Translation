"""Stage and replay the revised stopping rule in its original Grand Race descriptor."""

import argparse
from pathlib import Path
from struct import pack
import sys

from PIL import Image, ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.grand_race_help import format_page
from scripts import checkpoint_race_quit_common_20261114 as review
from scripts import headless_desmume_v193 as harness
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_release_baseline import files


run,base,parent=review.run,review.base,review.current
ROOT=run.ROOT/"stopping_revision"
ROM=ROOT/"Grand_Race_stopping_RESEARCH_ONLY.nds"
RECEIPT=ROOT/"staged.json"
LIVE=ROOT/"actual_stop_page.json"
DRAFT=("You can't drop out on your own mid-race. To stop the race, turn off your DS. "
       "Turning off even one DS ends the race for everyone.")
FRAMES=(2400,5200,8400,8800,9200,10000)
FRAME_COUNT=10001


def stage():
    assert not ROOT.exists()
    published=base.load(parent.RELEASE)
    old=base.load(review.OUTPUT)
    assert base.digest(parent.ROM)==published["candidate_sha256"]==old["candidate_sha256"]
    assert base.digest(parent.MANIFEST)==published["manifest_sha256"]
    assert base.digest(base.REGISTRY)==published["registry_sha256"]
    row=next(item for item in old["records"] if item["title"]=="Stopping a Race")
    ref=row["current_reference"]
    at=ref["body_pointer"]-0x02000000
    original=bytes.fromhex(ref["exact_hex"])
    _,body,lines,_=format_page(DRAFT)
    assert ' '.join(lines)==DRAFT and len(lines)==4
    assert lines[:2]==["You can't drop out on your own mid-race.","To stop the race, turn off your DS."]
    assert len(body)+1 < len(original)
    assert (at, len(original))==(0x137D7D,174)
    image=base.NdsImage.open(parent.ROM)
    prior=files(image)
    arm=prior[review.ARM]
    assert arm[at:at+len(original)]==original and arm[at-1]==0
    assert [i for i in range(0,len(arm)-3,4) if arm[i:i+4]==pack("<I",ref["body_pointer"])] == [ref["descriptor_offset"]+4]
    for other in old["records"]:
        if other is row:
            continue
        other_ref=other["current_reference"]
        other_at=other_ref["body_pointer"]-0x02000000
        assert other_at+len(bytes.fromhex(other_ref["exact_hex"]))<=at or at+len(original)<=other_at
    slot=(body+b"\0").ljust(len(original),b"\0")
    refined=arm[:at]+slot+arm[at+len(original):]
    verify_runtime(refined,published)
    image.replace_file(review.ARM,refined)
    target=files(image)
    assert target.keys()==prior.keys() and {p for p in prior if prior[p]!=target[p]}=={review.ARM}
    ROOT.mkdir()
    image.save(ROM)
    image.replace_file(review.ARM,arm)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    schedule=[event for event in run.schedule("race")[0] if event["start"]<=9601]
    base.save(ROOT/"inputs.json",schedule)
    base.save(RECEIPT,dict(input_ROM_sha256=published["candidate_sha256"],research_ROM_sha256=base.digest(ROM),
        source_review=str(review.OUTPUT),source_review_sha256=base.digest(review.OUTPUT),
        ARM9_offset=at,original_slot_hex=original.hex(),refined_slot_hex=slot.hex(),actual_proposed_lines=lines,
        target_ARM9_sha256=parent.assets.edit.digest(refined),complete_parent_inverse=True,
        descriptor_and_all_other_components_exact=True,gate_requires_display_replay=True))


def capture():
    receipt=base.load(RECEIPT)
    assert base.digest(ROM)==receipt["research_ROM_sha256"]
    donor=run.schedule("race")[-1]
    args=[sys.argv[0],"--rom",str(ROM),"--battery-save",donor["source"],"--touchscreen",
        "--inputs-json",str(ROOT/"inputs.json"),"--out",str(ROOT/"capture"),"--frames",str(FRAME_COUNT),
        "--capture-every","999999","--capture-at",*map(str,FRAMES)]
    original=sys.argv
    try:
        sys.argv=args
        harness.main()
    finally:
        sys.argv=original


def verify():
    assert not LIVE.exists()
    source_path=run.ROOT/"race/capture/capture_report.json"
    here_path=ROOT/"capture/capture_report.json"
    source,here=map(base.load,(source_path,here_path))
    receipt=base.load(RECEIPT)
    assert source["ROM_sha256"]==receipt["input_ROM_sha256"]
    assert here["ROM_sha256"]==receipt["research_ROM_sha256"]==base.digest(ROM)
    assert here["cold_boot"] and not here["savestate_loaded"] and not here["callback_errors"]
    assert not any(v for k,v in here.items() if k.startswith("synthetic_"))
    assert here["scripted_input_schedule"]==base.load(ROOT/"inputs.json")
    assert here["battery_save_preloaded"]["source_sha256"]==source["battery_save_preloaded"]["source_sha256"]
    old,new=({shot["frame"]:shot for shot in report["frames_captured"]} for report in (source,here))
    controls=[frame for frame in FRAMES if frame!=8800]
    assert all(old[n]["framebuffer_sha256"]==new[n]["framebuffer_sha256"] for n in controls)
    a,b=[review.checks.screen(value[8800]) for value in (old,new)]
    diff=ImageChops.difference(a,b).getbbox()
    assert diff and 4<=diff[0]<diff[2]<=256 and 216<=diff[1]<diff[3]<=344
    arm=base.NdsImage.open(ROM).read_file(review.ARM)
    font=GameAsciiFont.from_arm9(arm)
    shot=b.point(lambda n:n>>3)
    header,bounds=complete_mask(font,"Stopping a Race",shot,4,193,(0,31,0))
    expected=Image.new("1",(252,128))
    lines=[]
    for i,text in enumerate(receipt["actual_proposed_lines"]):
        count,rect=complete_mask(font,text,shot,4,217+i*16,(28,28,28))
        lines.append(dict(text=text,count=count,bounds=rect))
        for column,letter in enumerate(text):
            expected.paste(font.decode(letter),(column*6,1+i*16))
    pixels=shot.load()
    assert all((pixels[x+4,y+216]==(28,28,28))==bool(expected.getpixel((x,y)))
               for x in range(252) for y in range(128))
    viewed=ROOT/"revised_page.png"
    b.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST).save(viewed)
    base.save(LIVE,dict(research_ROM_sha256=receipt["research_ROM_sha256"],tested_without_savestate_or_fixture=True,
        complete_revised_body_mask=True,source_title_and_enabled_navigation_preserved=True,header_pixels=header,
        title_bounds=bounds,body_lines=lines,changed_pixel_bounds=diff,
        unchanged_framebuffer_controls=[new[n] for n in controls],review_image=str(viewed),
        review_image_sha256=base.digest(viewed),human_visual_review_pending=True,
        evidence={str(p):base.digest(p) for p in (source_path,here_path,RECEIPT,Path(__file__))}))


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step",choices=("stage","capture","verify"))
    globals()[parser.parse_args().step]()

