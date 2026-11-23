"""Verify whole Alexandria scenes reached through ordinary port and Square input."""
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_alexandria_dialogue_candidate_20261121 as replay
from scripts import verify_alexandria_dialogue_20261121 as display
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as panel


stage, base, native, town = replay.stage, replay.base, replay.stage.native, panel.town
PROOF = replay.ROOT / "verified_alexandria_v2.json"
NAMES = {174: "Owner", 175: "Cook"}


def check_report(report, donor):
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    battery = report["battery_save_preloaded"]
    assert battery["copied_byte_exact_before_cold_boot"] and battery["source"] == donor["donor"]
    assert battery["source_sha256"] == donor["sha256"] == base.digest(donor["donor"])


def main():
    assert not PROOF.exists()
    proof, source, observed, before, after = map(base.load, (
        display.PROOF, stage.review.OUTPUT, replay.OBSERVED, replay.BASELINE, replay.REPORT))
    candidate = base.digest(stage.ROM)
    assert candidate == after["ROM_sha256"] == proof["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert before["ROM_sha256"] == source["previous_sha256"] == base.digest(stage.parent.ROM)
    assert base.digest(replay.BASELINE) == observed["report_sha256"]
    plan_path = replay.baseline.ROOT / "source_save.json"
    donor = base.load(plan_path)
    assert donor["working_ROM_sha256"] == before["ROM_sha256"]
    for report in (before, after):
        check_report(report, donor)
    assert before["scripted_input_schedule"] == after["scripted_input_schedule"]
    assert before["frames"] == after["frames"] == observed["controls"]["returned"]
    for row in base.load(replay.baseline.ROOT / "capture/navigation_command_journal.json")["commands_received"]:
        assert row["validation_passed"]
    original, fixed = map(base.NdsImage.open, (stage.parent.ROM, stage.ROM))
    arm, font, ev = (fixed.read_file(name) for name in (native.ARM, "/GRP/KANJI.FNT", "/data/EV1.DK4"))
    assert arm == original.read_file(native.ARM) and font == original.read_file("/GRP/KANJI.FNT")
    assert ev == original.read_file("/data/EV1.DK4")
    event_map = base.load(town.events.OUTPUT)["routes"][1]
    assert native.digest(ev) == event_map["archive_sha256"]
    event, = [r for r in event_map["entries"] if (r["town"], r["script_block"], r["facility"]) == (25, 190, 0)]
    calendar = dict(route=1, birthday=[7, 12], final_calendar=observed["final_calendar"])
    original_event, current_event = (panel.event_completion(arm, report, ev, event, calendar) for report in (before, after))
    assert original_event["runtime_event_hex"] == current_event["runtime_event_hex"]

    context = SimpleNamespace(image=fixed, arm=arm)
    paint, fe = town.clipped_renderer(context), town.current_fe_painter(context)
    name_font = panel.GameAsciiFont.from_arm9(arm)
    stored_proof = {row["id"]: row for row in proof["records"] if row["block"] == 190}
    prior_refs = {row["frame"]: row for row in before["frames_captured"] if row["path"].endswith("_navigation.png")}
    revised_refs = {row["frame"]: row for row in after["frames_captured"] if row["path"].endswith("_cold_boot.png")}
    panels = sorted((row for row in source["records"] if row["block"] == 190), key=lambda row: row["ordinal"])
    after_block = native.IlnkContainer.parse(fixed.read_file("/data/SC1.DK4")).blocks[190]
    holds, unchanged, samples = [], [], []
    for row, frame in zip(panels, observed["panels"], strict=True):
        old_shot, old = town.read_frame(prior_refs, frame)
        shot, picture = town.read_frame(revised_refs, frame)
        info = stored_proof[row["id"]]
        at, raw = info["stored_offset"], bytes.fromhex(info["stored_command_hex"])
        assert after_block[at:at + len(raw)] == raw
        if row["decision"] == "retention":
            assert old_shot["framebuffer_sha256"] == shot["framebuffer_sha256"]
        selector = row["source_selector"]
        body = raw[6:raw.index(0, 6)]
        if selector == 254:
            result = fe(body)
            pixels, width = result["physical"], 228
        else:
            result = paint(arm, font, body)
            page, = result["pages"]
            pixels, width = bytes.fromhex(page["native_plane_hex"]), 216
            panel.complete_mask(name_font, NAMES[selector], picture, 16, 277, town.INKS[1])
        assert result["complete_consumed_bytes"] == len(body) and panel.mask_check(pixels, width, picture), row["id"]
        if row["decision"] == "retention":
            unchanged.append(shot)
        else:
            assert native.digest(pixels) == info["plane_sha256"]
            holds.append(dict(id=row["id"], file_path=row["file_path"], frame=frame, before=old_shot, after=shot))
            samples.extend(((row["id"] + " before", old), (row["id"] + " revised", picture)))
    controls = {}
    for name, frame in observed["controls"].items():
        a, _ = town.read_frame(prior_refs, frame)
        b, picture = town.read_frame(revised_refs, frame)
        assert a["framebuffer_sha256"] == b["framebuffer_sha256"], name
        controls[name] = b
        unchanged.append(b)
        samples.append((name, picture))
    assert len(holds) == 2 and len(panels) == 12
    sheets = []
    for pos in range(0, len(samples), 6):
        image = replay.ROOT / f"alexandria_gameplay_{pos // 6 + 1}.png"
        town.sheet(samples[pos:pos + 6], image)
        sheets.append(dict(path=str(image), sha256=base.digest(image)))
    evidence = (replay.BASELINE, replay.REPORT, replay.OBSERVED, display.PROOF, plan_path)
    base.save(PROOF, dict(candidate_sha256=candidate, natural_activation=True, hardware_verified=False,
        original_notice_dismissal_and_Square_return=True, exact_native_glyph_matches=True, holds=holds,
        unchanged_controls=unchanged, full_scene_panels=len(panels), controls=controls, sheets=sheets,
        source_native_event=original_event, staged_native_event=current_event,
        evidence={str(path): base.digest(path) for path in evidence}))
    print(f"Matched the whole Alexandria Square scene, including both revised panels and {len(controls)} transitions.")


if __name__ == "__main__":
    main()
