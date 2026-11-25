"""Verify the original post-Trade Deck lesson, its subtitles and its Lisbon return."""

from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_rafael_deck_after_trade_20261119 as ordinary
from scripts import stage_rafael_deck_tutorial_followup_20261122 as staged
from scripts.verify_captain_biographies_v1 import captured, shots


base,native = staged.base,staged.native
ROOT = staged.ROOT/"ordinary_deck"
PROOF,SHEET = ROOT/"verified_gameplay.json",ROOT/"ordinary_deck_lesson.png"
REPORT = ROOT/"after/capture/capture_report.json"
NATIVE = staged.render.PROOF


def verify():
    assert not PROOF.exists() and not SHEET.exists()
    stored,review,offline = map(base.load,(staged.PROOF,staged.compiled.REVIEW,NATIVE))
    sha = base.digest(staged.ROM)
    assert sha == stored["candidate_sha256"] == offline["proposed_ROM_sha256"]
    assert base.digest(staged.compiled.REVIEW)==stored["draft_sha256"]
    current = base.NdsImage.open(staged.ROM)
    arm = current.read_file(native.ARM)
    font = GameAsciiFont.from_arm9(arm)
    cjk = current.read_file(ordinary.FONT)
    paint = staged.render.renderer.inherited.early.prior.precedent.planners(arm)[1]
    target = native.IlnkContainer.parse(current.read_file(staged.ARCHIVE)).blocks[43]
    assert native.digest(target)==stored["compiled_block_sha256"]
    replay = type("Replay",(),dict(ROOT=ROOT,END=staged.ordinary.END))
    load_run = FunctionType(ordinary.load_run.__code__,ordinary.load_run.__globals__|{"replay":replay})
    evidence = {str(path):base.digest(path) for path in (staged.PROOF,staged.compiled.REVIEW,NATIVE)}
    report,trace,returns = load_run("after",sha,stored["compiled_block_sha256"],evidence)
    frames = shots(report)
    rows = {row["id"]:row for row in review["records"]}
    native_displays = {r["id"]:r for r in offline["full_progressive_and_FE_cases"]}
    lessons,panels = [],[]
    for command,returned in zip(stored["commands"],returns,strict=True):
        assert returned["source"]["instruction_offset"]==command["stored_offset"]
        assert returned["source"]["first_word"]==command["word"]
        raw = bytes.fromhex(command["stored"])
        start = command["stored_offset"]
        assert target[start:start+len(raw)]==raw
        if command["word"] != 0x4000:
            assert not command["record_ids"] and command["stored"]==command["current"]
            continue
        ident, = command["record_ids"]
        row = rows[ident]
        selector = raw[5]
        assert selector == row["source_selector"]
        revised = row["decision"]=="revision"
        if revised:
            result = native_displays[ident]
            assert result["target_hex" if selector==254 else "stored_hex"]==raw[5:raw.index(0,6)].hex()
            layouts = result["layouts"]
            rendered = layouts[0]
            if ident.endswith("R0017"):
                assert rendered["names"]=={"FI":"Rafael"} and rendered["scope"]=="offline Rafael default"
            page, = rendered["pages"]
            plane = ordinary.TOOL.prior.masks(bytes.fromhex(page["native_plane_hex"]))
            text = raw[6:raw.index(0,6)].replace(b"FI",b"Rafael")
            if selector == 254:
                # The observed post-Trade system panel uses the Lisbon body
                # composition qualified by the original route replay.
                _,text,page,plane = ordinary.pixel_page(arm,cjk,paint,raw)
        else:
            assert command["current"]==command["stored"]
            _,text,page,plane = ordinary.pixel_page(arm,cjk,paint,raw)
        entered = trace[returned["entry_row"]]
        hold,image = ordinary.match_page(entered,returned,frames,font,selector,plane)
        evidence[hold["capture"]] = hold["sha256"]
        lessons.append(dict(id=ident,revision=revised,body_hex=text.hex(),
            native_plane_sha256=native.digest(bytes.fromhex(page["native_plane_hex"])),
            executed_scope="original_SC0_B43_post_Trade",hold=hold))
        panels.append((ident,image))
    assert len(lessons)==12 and sum(row["revision"] for row in lessons)==6
    assert sum(row["hold"]["speaker"] is not None for row in lessons)==11
    last=lessons[-1]
    assert last["hold"]["speaker"] is None and last["id"].endswith("R0045")
    assert b"Deck View" in bytes.fromhex(last["body_hex"])
    captain, = [row for row in lessons if row["id"].endswith("R0017")]
    text=bytes.fromhex(captain["body_hex"])
    assert text.startswith(b"First up is the captain.") and b"Rafael." in text and text.isascii()

    # The old ordinary replay is the visual reference for the scene's Lisbon return.
    reference = staged.ordinary.ROOT/"corrected/capture/capture_report.json"
    previous_report = base.load(reference)
    assert previous_report["cold_boot"] and previous_report["scripted_input_schedule"]==report["scripted_input_schedule"]
    assert previous_report["battery_save_preloaded"]["source_sha256"]==report["battery_save_preloaded"]["source_sha256"]
    matched = []
    for n in (15961,16261,16561,16800):
        prior = shots(previous_report)[n]
        latest = frames[n]
        if latest["framebuffer_sha256"]==prior["framebuffer_sha256"] and n>returns[-1]["frame"]:
            evidence[latest["path"]]=latest["PNG_sha256"]
            matched.append(latest)
    assert matched and matched[0]["frame"]==15961
    evidence[str(reference)]=base.digest(reference)
    panels.append(("Normal Lisbon return",captured(frames[15961])))
    sheet=Image.new("RGB",(1024,212*((len(panels)+3)//4)),"#263238")
    draw=ImageDraw.Draw(sheet)
    for i,(ident,image) in enumerate(panels):
        x,y=(i%4)*256,(i//4)*212
        draw.text((x+4,y+3),ident,fill="white")
        sheet.paste(image.crop((0,192,256,384)),(x,y+20))
    sheet.save(SHEET)
    evidence[str(SHEET)]=base.digest(SHEET)
    base.save(PROOF,dict(candidate_sha256=sha,ordinary_gameplay_existing_Lisbon_save=True,
        native_lesson_event_after_Trade=True,speakerless_system_page_exact=True,hardware=False,
        twelve_complete_panels=lessons,original_command_count=len(returns),last_command_frame=returns[-1]["frame"],
        ordinary_return_to_Lisbon=True,matched_town_frames=matched,played_captain_given_name="Rafael",
        full_default_capital_F_and_runtime_name=True,
        sheet=str(SHEET),sheet_sha256=base.digest(SHEET),evidence=evidence))
    print(f"Observed all 12 Deck lesson pages and {len(matched)} exact Lisbon return frames.",flush=True)


if __name__=="__main__":
    verify()

