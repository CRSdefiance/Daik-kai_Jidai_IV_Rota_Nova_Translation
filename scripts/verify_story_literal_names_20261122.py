"""Check actual Hodram replay screens, focus fixture, and story transitions."""

from pathlib import Path
from types import SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_story_literal_names_20261122 as replay
from scripts import stage_story_literal_names_20261122 as stage
from scripts import verify_hodram_custom_names_20261122 as captured
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as system_display
from scripts.audit_captain_name_latin_20261119 import BODY_COLOR, EDITOR_COLOR, LABEL_COLOR, glyphs


base, native = stage.base, stage.native
ROOT, PROOF = stage.ROOT, stage.ROOT / "verified_gameplay.json"
REPORTS = {name: ROOT / name / "capture/capture_report.json" for name in ("previous","fixed","system")}
BODY = 0x0218EDC8


def rows(font, image, entries):
    result = []
    for line, (value, x) in enumerate(entries):
        y = 297 + line * 16
        assert not any(image.getpixel((left, row)) == BODY_COLOR
                       for left in range(16, x) for row in range(y, y+11))
        result.append(glyphs(font, image, value, (x,y), BODY_COLOR, 238))
    return result


def make_sheet(path, pictures):
    sheet = Image.new("RGB", (1024, 410 * ((len(pictures)+1)//2)), "#263238")
    label = ImageDraw.Draw(sheet)
    for i, (caption, image) in enumerate(pictures):
        x,y = (i%2)*512,(i//2)*410
        label.text((x+4,y+3),caption,fill="white")
        sheet.paste(image.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+20))
    sheet.save(path)
    return str(path),base.digest(path)


def verify():
    assert not PROOF.exists()
    stored, defect = map(base.load,(stage.PROOF,stage.trace.FINDING))
    fixture_path = ROOT / "system/fixture.json"
    fixture = base.load(fixture_path)
    previous, current, system = (base.load(REPORTS[key]) for key in REPORTS)
    candidate = base.digest(stage.ROM)
    assert previous["ROM_sha256"] == stored["predecessor_sha256"] == base.digest(stage.parent.ROM)
    assert current["ROM_sha256"] == fixture["candidate_sha256"] == stored["candidate_sha256"] == candidate
    assert system["ROM_sha256"] == fixture["fixture_sha256"] == base.digest(replay.FOCUSED_ROM)
    assert fixture["exact_candidate_inverse"] and not fixture["natural_activation"]
    for report in (previous,current,system):
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not report.get("battery_save_preloaded") and not any(v for k,v in report.items() if k.startswith("synthetic_"))
    schedule = previous["scripted_input_schedule"]
    assert schedule == current["scripted_input_schedule"]
    assert system["scripted_input_schedule"] == [e for e in schedule if e["start"] < system["frames"]]
    rom = base.NdsImage.open(stage.ROM)
    arm = rom.read_file(native.ARM)
    font = GameAsciiFont.from_arm9(arm)
    assert font == GameAsciiFont.from_arm9(base.NdsImage.open(stage.parent.ROM).read_file(native.ARM))
    first = captured.MAX
    _,last,company = captured.EXPECTED_FIELDS
    confirmation = []
    for report in (previous,current,system):
        raw,shot,evidence = captured.hold(report,14520)
        names = captured.confirm_fields(raw,first)
        for value,y in zip((first,*captured.EXPECTED_FIELDS),(221,243,265,287),strict=True):
            glyphs(font,shot,value.decode("ascii"),(89,y),EDITOR_COLOR,202)
        confirmation.append(dict(fields=names,evidence=evidence))
    _,context_before,context_before_capture = captured.hold(previous,23970)
    _,context,context_capture = captured.hold(current,23970)
    assert context_before.tobytes() == context.tobytes()
    expanded = bytes.fromhex(defect["first_expanded_hex"])
    raw,bad,bad_capture = captured.hold(previous,24320)
    native_before = captured.require_string(raw,BODY,expanded)
    corruption = b"Bergstrom"+first+last+company+b"F"
    old_rows = rows(font,bad,(
        ("One of your speeches,",16), ("Admiral "+corruption[:28].decode("ascii"),16),
        (corruption[28:].decode("ascii")+",",16), ("was the first thing that ever made",22)))
    raw,extra,extra_capture = captured.hold(previous,24670)
    captured.require_string(raw,BODY,expanded)
    rows(font,extra,(("me shake with eagerness for battle.",22),("",16),("",16),("",16)))
    raw,fixed,fixed_capture = captured.hold(current,24320)
    native_after = captured.require_string(raw,BODY,expanded)
    fixed_rows = rows(font,fixed,(
        ("One of your speeches,",16), ("Admiral BergstromFIFAFOF,",16),
        ("was the first thing that ever made",22), ("me shake with eagerness for battle.",22)))
    plate = glyphs(font,fixed,"Charles Rochefort",(16,277),LABEL_COLOR,130)
    raw,reply,reply_capture = captured.hold(current,24670)
    captured.require_string(raw,0x022A4F78,first+b" "+last)
    reply_plate = glyphs(font,reply,(first+b" "+last).decode("ascii"),(16,277),LABEL_COLOR,226)
    reply_rows = rows(font,reply,(("Enough of that. Few duties",16),("are as painful",16),("as giving a speech. Anyway...",16),("",16)))
    _,old_reply,old_reply_capture = captured.hold(previous,25020)
    assert old_reply.crop((0,192,256,357)).tobytes() == reply.crop((0,192,256,357)).tobytes()
    _,next_page,next_capture = captured.hold(current,25020)
    _,old_next,old_next_capture = captured.hold(previous,25370)
    assert old_next.crop((0,192,256,357)).tobytes() == next_page.crop((0,192,256,357)).tobytes()
    _,manuel,manuel_capture = captured.hold(current,25370)
    glyphs(font,manuel,"Manuel Almeida",(16,277),LABEL_COLOR,112)
    rows(font,manuel,(("Great!",16),("",16),("",16),("",16)))
    sheets = dict((make_sheet(ROOT/"ordinary_comparison.png",(
        ("Before / Gerhard's lead-in",context_before),("After / same lead-in",context),
        ("Before / nested surname substitutions",bad),("After / literal surname and complete speech",fixed),
        ("Before / unintended extra page",extra),("After / following reply",reply),
        ("After / Hodram continues",next_page),("After / Manuel replies",manuel))),))

    _,notification,notification_capture = captured.hold(system,15220)
    expected = first+b": Charm +1!"
    layout = system_display.town.current_fe_painter(SimpleNamespace(image=rom,arm=arm))(expected)
    assert layout["complete_consumed_bytes"] == len(expected)
    plane = layout["physical"]
    assert system_display.mask_check(plane,228,notification)
    system_rows = rows(font,notification,((expected.decode("ascii"),16),("",16),("",16),("",16)))
    _,departure,departure_capture = captured.hold(system,15570)
    assert departure.tobytes() != notification.tobytes()
    sheets.update((make_sheet(ROOT/"focused_system_comparison.png",(
        ("Focused system notification / complete custom first name",notification),
        ("Next input / ordinary Stockholm port screen",departure))),))
    evidence = {str(p):base.digest(p) for p in (*REPORTS.values(),fixture_path,stage.PROOF,stage.trace.FINDING)}
    base.save(PROOF,dict(candidate_sha256=candidate,predecessor_sha256=previous["ROM_sha256"],
        ordinary=dict(actual_original_opening=True, same_controls_and_names=True, formerly_extra_page_removed=True,
            confirmation=confirmation, before_story_holds=[context_before_capture,bad_capture,extra_capture,old_reply_capture,old_next_capture],
            fixed_story_holds=[context_capture,fixed_capture,reply_capture,next_capture,manuel_capture],
            charles_panel=dict(first_pass_before=native_before,first_pass_after=native_after,
                nameplate=plate,incorrect_before=old_rows,complete_after=fixed_rows),
            following_reply=dict(nameplate=reply_plate,body=reply_rows,
                source_retention_reference=defect["nameplate_and_neighbor_refs"][1]["source_ref"],
                wrap_followup_pending=True)),
        focused_system=dict(fixture=fixture,system_body_mask_exact=True,body_masks=system_rows,
            screenshot=notification_capture,transition_to_town=departure_capture,natural_activation=False),
        offline_fallback_check=True,evidence=evidence,sheets=sheets))


if __name__ == "__main__":
    verify()
