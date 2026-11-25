"""Verify the Lisbon Purser's extra-stock advice against ordinary controls."""

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_lisbon_extra_stock_20261124 as play
from scripts import verify_lisbon_purchase_variants_20261124 as comparison
from scripts import verify_riga_trade_deck_20261124 as evidence
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = evidence.OUT.with_name("lisbon_extra_stock_current_20261124.json")
SHEET = OUT.with_suffix(".png")
PRIOR = Path("releases/all_routes_editorial_20261115_market_trade_dialogue_candidate/verification/registered_review.json")
panels = evidence.panels
KEY = 758
AFTER_OPEN, AFTER_DISMISS = 37700, 38100


def reports(release):
    capture = play.ROOT / "capture/capture_report.json"
    journal = capture.with_name("navigation_command_journal.json")
    provenance = play.ROOT / "runner.json"
    ordinary = play.prior.ROOT / "capture/capture_report.json"
    initial = read(play.prior.BOOK)["evidence"]["capture"]
    report, guide, control, previous, runner = map(read, (capture, journal, ordinary, initial["path"], provenance))
    assert digest(initial["path"]) == initial["sha256"]
    assert report["ROM_sha256"] == control["ROM_sha256"] == guide["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == guide["last_command_frame"] == 40500
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert control["cold_boot"] and not control["savestate_loaded"] and not control["callback_errors"]
    assert not any(value for key, value in control.items() if key.startswith("synthetic_"))
    assert [key for key, value in report.items() if key.startswith("synthetic_") and value] == [
        "synthetic_market_finance_prerequisite"]
    exp, = report["synthetic_market_finance_prerequisite"]
    assert exp["frame"] == play.PAUSE and exp["message"] == KEY and exp["actor"] == 6
    assert not report["earned_finance_prerequisite_verified"] and exp["finance_before"] == 115 and exp["finance_after"] == 160
    assert (exp["native_predicate_before"], exp["native_predicate_after"]) == (0, 1)
    assert report["scripted_input_schedule"][:len(previous["scripted_input_schedule"])] == previous["scripted_input_schedule"]
    expected = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert expected == list(play.ACTIONS)
    assert expected == [row["command"] for row in guide["commands_received"]]
    assert all(row["validation_passed"] for row in guide["commands_received"])
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and not donor["savestate_loaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == control["battery_save_preloaded"]["source_sha256"]
    assert donor["source_sha256"] == runner["original_donor_sha256"]
    frames, controls = [panels.shots(run, "_navigation.png") for run in (report, control)]
    assert frames[play.PAUSE]["framebuffer_sha256"] == controls[play.PAUSE]["framebuffer_sha256"]
    assert frames[AFTER_OPEN]["framebuffer_sha256"] != controls[AFTER_OPEN]["framebuffer_sha256"]
    start_ram, = [row for row in report["read_only_pause_RAM_snapshots"] if row["frame"] == play.PAUSE]
    before = Path(start_ram["path"]).read_bytes()
    assert start_ram["read_only_export"] and len(before) == start_ram["bytes"] == 0x400000
    assert sha256(before).hexdigest() == start_ram["sha256"] == exp["full_RAM_before_sha256"]
    after = bytearray(before)
    offsets = set()
    for change in exp["changes"]:
        offset = change["address"] - play.BASE
        assert 0 <= offset < len(before) and offset not in offsets and before[offset] == change["before"]
        after[offset] = change["after"]
        offsets.add(offset)
    assert len(offsets) == 3 and max(offsets) - min(offsets) == 2
    assert sha256(after).hexdigest() == exp["full_RAM_after_sha256"]
    refs = (capture, journal, provenance, ordinary, initial["path"], donor["source"], play.CONTROLLER, PRIOR, start_ram["path"])
    return frames, controls, exp, list(map(reference, refs))


def check_text(release, screen):
    clean, current = map(NdsImage.open, (CLEAN, play.prior.current.ROM))
    arm = current.read_file(play.prior.current.ARM)
    path = play.prior.current.COMMON
    archive = current.read_file(path)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = evidence.base.common_message_entries(clean.read_file(path), clean.read_file(play.prior.current.ARM))
    installed = evidence.base.common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)
    previous = {row["message_ID"]: row for row in read(PRIOR)["records"] if 754 <= row["message_ID"] <= 760}
    assert set(previous) == set(range(754, 761))
    for key, formerly in previous.items():
        assert formerly["source_hex"] == source[key].text.hex() and formerly["staged_hex"] == installed[key].text.hex()
    ja, en, former = source[KEY], installed[KEY], previous[KEY]
    lines = former["layout_cases"][0]["native_lines"]
    english = " ".join(lines)
    assert english == en.text.decode("ascii").strip() and b"%" not in ja.text + en.text
    observation = dict(body=panels.exact_body(font, lines, screen), lines=lines,
                       nameplate=panels.nameplate(font, "Julio Erneco", screen))
    record = dict(id=f"COMMON_MESSAGE_{KEY}", message_ID=KEY, file_path=path, speaker="Julio Erneco",
        english=english, clean_Japanese=ja.text.decode("cp932"), source_meaning=former["source_meaning"],
        context=("The assigned Purser advises Rafael when opening Trade. Acknowledging the advice opens the usual "
                 "ledger. The Salt within the ordinary quota still stages at its regular price. Back abandons the deal "
                 "and reopening repeats the advice."),
        localization_note=("It seems suits Julio’s measured advice and makes the offer tentative. This time limits "
                           "the claim to the present visit, and certain goods preserves the limited selection."),
        decision="retention", review=dict.fromkeys(GATES, True), source_reference=evidence.source_ref(ja),
        current_reference=evidence.source_ref(en), installed_reference=evidence.source_ref(en), focused_hold=observation)
    return record, list(previous), font


def main():
    release = read(play.prior.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.prior.current.ROM) == release["candidate_sha256"]
    frames, ordinary, expense, refs = reports(release)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    ordinary_entry, ordinary_staged = (panels.picture(ordinary[f]) for f in (AFTER_OPEN, 38500))
    focused_entry, trade = screens[AFTER_OPEN], screens[AFTER_DISMISS]
    record, earlier, font = check_text(release, focused_entry)
    focused_funds = comparison.ledger.exact_ledger(font, trade, (26995, 0, 0, 26995))
    ordinary_funds = comparison.ledger.exact_ledger(font, ordinary_entry, (26995, 0, 0, 26995))
    staged_funds = comparison.ledger.exact_ledger(font, screens[38900], (26995, 0, 577, 26418))
    after_back = panels.find_mask(font, "26995", screens[39700], (55, 348, 139, 366))
    assert ImageChops.difference(trade, ordinary_entry).getbbox() == (82, 230, 110, 258)
    assert (screens[38900].tobytes() == screens[39300].tobytes() == ordinary_staged.tobytes())
    assert focused_entry.tobytes() == screens[40100].tobytes()
    assert trade.tobytes() == screens[40500].tobytes()
    receipt = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), records=[record], clean_rom_sha256=release["clean_input_sha256"],
        candidate_sha256=release["candidate_sha256"], ordinary_control=dict(start=ordinary[play.PAUSE], trade=ordinary[AFTER_OPEN],
            opening_ledger=ordinary_funds),
        focused_prerequisite=expense, focused_gameplay=dict(advice=frames[AFTER_OPEN], after_dismiss=frames[AFTER_DISMISS],
            opening_ledger=focused_funds, staged=frames[38900], staged_ledger=staged_funds, staged_price=577,
            staged_equals_ordinary_play=True, back=frames[39700], wallet_after_back=after_back,
            advice_repeated=frames[40100], reopened_trade=frames[40500], repeat_frames_identical=True),
        exact_earlier_advisory_body_bindings=earlier,
        unvisited=["Ordinarily gained Finance 160", "Purchase beyond the regular stock quota", "Physical hardware"],
        ROM_changed=False, new_editorial_credit=0, evidence=refs + [reference(play.prior.current.RELEASE)])
    validate_natural_dialogue_batch(receipt)
    sheet = Image.new("RGB", (768, 808), "#263238")
    draw = ImageDraw.Draw(sheet)
    selected = ((ordinary_entry, "Ordinary Trade, Finance 115"),
                (focused_entry, "Julio's advice, Finance 160 fixture"),
                (trade, "Dismiss advice and open Trade"),
                (screens[38900], "Stage Salt at the ordinary price"),
                (screens[39700], "Back preserves the balance"),
                (screens[40100], "Reopening repeats the advice"))
    for index, (image, label) in enumerate(selected):
        x, y = index % 3 * 256, index // 3 * 404
        draw.text((x + 4, y + 4), label, fill="white")
        sheet.paste(image, (x, y + 20))
    sheet.save(SHEET)
    receipt["contact_sheet"] = reference(SHEET)
    write(OUT, receipt)
    print("Verified the ordinary Trade control, the complete native extra-stock advice, and the Trade return.")


if __name__ == "__main__":
    main()
