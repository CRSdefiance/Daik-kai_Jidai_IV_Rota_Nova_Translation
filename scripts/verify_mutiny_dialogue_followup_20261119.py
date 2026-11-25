"""Verify initialized mutiny dialogue, the Quell Mutiny choice, and the cumulative boot."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import replay_mutiny_dialogue_followup_20261119 as replay
from scripts import verify_mutiny_release_inputs_v1 as historical
from scripts import verify_sea_event_dialogue_followup_20261118 as sea
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import render_portrait

stage, base = replay.stage, replay.base
STARTUP = stage.ROOT / "own_startup_verification.json"
GAME = stage.ROOT / "verified_quell_v2.json"
SHEET = stage.ROOT / "quell_gameplay_v2.png"
HISTORICAL = Path("releases/all_routes_editorial_20261111_mutiny_candidate/verification/stored_mutiny_verification.json")
SPEECHES = ((516, 9627), (517, 9827), (541, 10327))
RETURN_FRAME = 10527


def startup():
    check = FunctionType(sea.startup.__code__, vars(sea) | dict(stage=stage, replay=replay, STARTUP=STARTUP, __file__=__file__))
    check()


def gameplay():
    assert not GAME.exists() and not SHEET.exists()
    staged, terminal = map(base.load, (stage.PROOF, replay.OUT / "terminal.json"))
    sha = base.digest(stage.ROM)
    assert sha == staged["candidate_sha256"] == terminal["candidate_sha256"]
    assert terminal["donor_unchanged"] and base.digest(terminal["report"]) == terminal["report_sha256"]
    assert base.digest(terminal["commands"]) == terminal["commands_sha256"]
    report, final = checked_report(terminal["report"], sha, 11527)
    assert not any(report[k] for k in report if k.startswith("synthetic_") and k != "synthetic_condition_fixtures")
    assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    frames = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("navigation.png")}
    snapshots = {row["frame"]: row for row in report["read_only_pause_RAM_snapshots"]}

    def snapshot(frame):
        row = snapshots[frame]
        assert row["read_only_export"] and base.digest(row["path"]) == row["sha256"]
        return Path(row["path"]).read_bytes()

    rom = base.NdsImage.open(stage.ROM)
    arm = rom.read_file(stage.ARM)
    kanji = rom.read_file("/GRP/KANJI.FNT")
    raster, _, _ = font_tools(rom)
    fixtures = []
    for frame, mode in ((8327, "select-mutiny"), (9627, "restore-mutiny-selection")):
        _, receipt = replay.set_condition(arm, snapshot(frame), {"mode": mode})
        fixtures.append(receipt | {"frame": frame})
    assert report["synthetic_condition_fixtures"] == fixtures
    field = historical.FIELD - historical.BASE
    assert final[field:field + 4] == historical.ORIGINAL
    assert snapshot(RETURN_FRAME)[field:field + 4] == historical.ORIGINAL
    expand, output = (unpack_from("<I", arm, p)[0] - historical.BASE for p in (0x5444C, 0x54450))
    rows = {r["message_ID"]: r for r in staged["records"]}
    observed = []
    crop = (16, 296, 244, 360)
    for n, frame in SPEECHES:
        raw = snapshot(frame)
        plain, display = (raw[at:at + 256].split(b"\0", 1)[0] for at in (expand, output))
        row = rows[n]
        assert plain.hex() == row["staged_hex"] and display.hex() == row["display_hex"]
        plane, glyphs = render_portrait(raster, arm, kanji, display)
        assert bytes(value == 1 for value in plane) == historical.portrait_ink(frames[frame]["path"], crop)
        observed.append(dict(message_ID=n, frame=frame, glyphs=len(glyphs), capture=frames[frame],
            complete_native_ink=True, visible_lines=row["visible_lines"]))

    history = base.load(HISTORICAL)
    menu = history["native_menu"]
    original = getsource(historical.menu_masks)
    source = checked_text(original, {"(10127, (1, 15, 1))": "(10127, (15, 1, 1)), (10527, (1, 1, 1))"})
    local = dict(vars(historical))
    exec(compile(source, __file__ + "::quell-choice-masks", "exec"), local)
    masks = local["menu_masks"](menu, frames)
    assert [row["english"] for row in masks if row["style"] == 15] == ["Quell Mutiny"]
    for frame in (10027, 10127, RETURN_FRAME):
        raw = snapshot(frame)
        for row in history["menu_allocation"]["changes"]:
            assert unpack_from("<I", raw, row["field"])[0] == row["target_pointer"]
    journal = replay.OUT / "capture/navigation_command_journal.json"
    commands = base.load(journal)["commands_received"]
    assert all(row["validation_passed"] for row in commands)
    by_frame = {row["frame"]: row["command"] for row in commands}
    assert "buttons" not in by_frame[10027]
    assert by_frame[10127]["buttons"] == by_frame[10327]["buttons"] == ["A"]
    assert not any(c.get("buttons") == ["DOWN"] for c in by_frame.values())
    assert historical.portrait_ink(frames[RETURN_FRAME]["path"], crop) != historical.portrait_ink(frames[10327]["path"], crop)

    sheet = Image.new("RGB", (1024, 624), "#28343e")
    painter = ImageDraw.Draw(sheet)
    samples = ((9627, "Threat to force a port call"), (9827, "Revised warning"),
        (10027, "Three original choices"), (10127, "Quell Mutiny selected"),
        (10327, "Missing Boarding Leader"), (RETURN_FRAME, "Return to the response menu"))
    for i, (frame, label) in enumerate(samples):
        x, y = (i % 2) * 512, (i // 2) * 208
        painter.text((x + 8, y + 3), label, fill="white")
        with Image.open(frames[frame]["path"]) as screen:
            lower = screen.convert("RGB").crop((0, 288, 256, 384)) if frame not in (10027, 10127, RETURN_FRAME) else (
                screen.convert("RGB").crop((0, 242, 256, 338)))
        sheet.paste(lower.resize((512, 192), Image.Resampling.NEAREST), (x, y + 15))
    sheet.save(SHEET)
    base.save(GAME, dict(candidate_sha256=sha, actual_emulator=True, hardware=False, selector_word_restored=True,
        observed=observed, observed_revised_records=[517], offline_only_revised_records=sorted(set(stage.REVISIONS) - {517}),
        choice_masks=masks, original_A_selects_quell=True, absent_boarding_leader_warning=True,
        response_menu_return=frames[RETURN_FRAME], natural_mutiny_occurrence_verified=False, fixture=fixtures,
        evidence={str(p): base.digest(p) for p in (
            stage.PROOF, replay.OUT / "terminal.json", terminal["report"], journal, HISTORICAL,
            menu["sheet"]["path"], SHEET, Path(__file__))}))
    print("Verified three dialogue masks, nine menu masks, the missing-role branch and return to the response menu.")


if __name__ == "__main__":
    gameplay()
    startup()
