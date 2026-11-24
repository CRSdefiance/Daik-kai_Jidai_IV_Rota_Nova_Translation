"""Compare the staged recruiting page and unchanged neighboring frames in ordinary play."""

import io
import sys
from types import FunctionType, SimpleNamespace

from scripts import stage_stockholm_recruiting_20261124 as build
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


run, panels = build.review.run, build.panels
ROOT = build.ROOT / "gameplay"
BASELINE = run.ROOT.with_name("riga_auto_dock_upper_20261124")
PAIRED = build.ROOT / "paired_stockholm_recruiting.json"
SHEET = build.ROOT / "stockholm_recruiting_paired_1_20261123.png"
CHANGED = 9550


def replay():
    stored, release = read(build.STORED), read(build.parent.RELEASE)
    assert digest(build.ROM) == stored["candidate"]["sha256"]
    assert stored["previous"]["sha256"] == release["candidate_sha256"] == digest(build.parent.ROM)
    assert stored["whole_parent_inverse"] and stored["unchanged_archive_directory"]
    proof = read(build.review.OUT)
    baseline = proof["evidence"][1]
    assert reference(BASELINE / "terminal.json") == baseline["terminal"]
    journal = read(baseline["journal"]["path"])
    assert reference(BASELINE / "capture/navigation_command_journal.json") == baseline["journal"]
    commands = (BASELINE / "controller.jsonl").read_bytes()
    assert [row["command"] for row in journal["commands_received"]][-1] == {"stop": True}
    baseline_capture = read(baseline["capture"]["path"])
    assert reference(BASELINE / "capture/capture_report.json") == baseline["capture"]
    donor = baseline_capture["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    ROOT.mkdir()
    (ROOT / "controller.jsonl").write_bytes(commands)
    inputs = ROOT / "inputs.json"
    initial = BASELINE / "inputs.json"
    terminal = read(baseline["terminal"]["path"])
    assert digest(initial) == terminal["evidence"][str(initial)]
    inputs.write_bytes(initial.read_bytes())
    harness = run.replay.harness
    with io.TextIOWrapper(io.BytesIO(commands), encoding="utf-8") as stream:
        original, argv = sys.stdin, sys.argv
        try:
            sys.stdin = stream
            sys.argv = [harness.__file__, "--rom", str(build.ROM), "--out", str(ROOT / "capture"),
                "--frames", "90000", "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--battery-save", donor["source"], "--touchscreen", "--pause-at", str(run.FIRST_PAUSE)]
            harness.main()
        finally:
            sys.stdin, sys.argv = original, argv
    assert digest(donor["source"]) == donor["source_sha256"]


def verify():
    stored, release = read(build.STORED), read(build.parent.RELEASE)
    candidate = stored["candidate"]["sha256"]
    old, _, before, _ = build.review.run_capture(BASELINE, release)
    capture, journal = [ROOT / "capture" / filename for filename in ("capture_report.json", "navigation_command_journal.json")]
    report, nav = map(read, (capture, journal))
    assert digest(build.ROM) == report["ROM_sha256"] == nav["ROM_sha256"] == candidate
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert report["battery_save_preloaded"]["source_sha256"] == read(before["capture"]["path"])["battery_save_preloaded"]["source_sha256"]
    assert report["scripted_input_schedule"] == read(before["capture"]["path"])["scripted_input_schedule"]
    baseline_nav = read(before["journal"]["path"])
    assert nav["commands_received"] == baseline_nav["commands_received"]
    assert nav["last_command_frame"] == baseline_nav["last_command_frame"] == report["frames"]
    new = {shot["frame"]: shot for shot in report["frames_captured"] if shot["path"].endswith("_navigation.png")}
    unchanged = []
    for frame in (8000, 8310, 8640, 8950, 9260, 9820, 10130, 10430):
        assert old[frame]["framebuffer_sha256"] == new[frame]["framebuffer_sha256"]
        unchanged.append(dict(predecessor=old[frame], candidate=new[frame]))
    assert old[CHANGED]["framebuffer_sha256"] != new[CHANGED]["framebuffer_sha256"]
    earlier, revised = [panels.picture(r[CHANGED]) for r in (old, new)]

    rom = NdsImage.open(build.ROM)
    arm, font = rom.read_file(build.ARM), rom.read_file("/GRP/KANJI.FNT")
    archive = rom.read_file(build.STORY)
    block = panels.IlnkContainer.parse(archive).blocks[build.BLOCK]
    assert sha256(archive).hexdigest() == stored["target_SC1_sha256"]
    assert sha256(block).hexdigest() == stored["target_block_sha256"]
    edit = stored["edit"]
    at, command = edit["command_offset"], bytes.fromhex(edit["after_hex"])
    assert block[at:at + len(command)] == command
    paint = panels.town.clipped_renderer(SimpleNamespace(image=rom, arm=arm))
    text = panels.bytes_for(command)
    display = paint(arm, font, text)
    page, = display["pages"]
    plane = bytes.fromhex(page["native_plane_hex"])
    assert display["complete_consumed_bytes"] == len(text) and page["native_independent_plane_equal"]
    assert sha256(plane).hexdigest() == edit["page_sha256"] and panels.mask_check(plane, 216, revised)
    plate = panels.nameplate(build.review.auto.GameAsciiFont.from_arm9(arm), "Gerhard Adernkatz", revised)
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": PAIRED})
    sheet, = sheets("stockholm_recruiting_paired", [("Earlier advice", earlier), ("Revised advice", revised)], (0, 273, 256, 374))
    assert sheet == reference(SHEET)
    write(PAIRED, dict(candidate_sha256=candidate, previous_sha256=release["candidate_sha256"],
        ordinary_saved_game=True, same_choice_and_tavern_return=True, before=before,
        after=dict(capture=reference(capture), journal=reference(journal)),
        stored=reference(build.STORED), revised=new[CHANGED], earlier=old[CHANGED], complete_nameplate=plate,
        unchanged_frames=unchanged, complete_page_sha256=edit["page_sha256"], visual=sheet))
    print("Verified the complete revised page and Gerhard's nameplate, plus eight unchanged gameplay holds.")


if __name__ == "__main__":
    replay()
    verify()
