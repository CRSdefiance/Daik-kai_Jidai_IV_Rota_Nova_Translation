"""Verify the revised sailing guide on the original mode-selection path."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont

from scripts import observe_attack_display_ownership_20261118 as history
from scripts import stage_sailing_mode_prose_20261118 as stage
from scripts.verify_original_latin_cards_native_v197 import native5

base, native, parent = stage.base, stage.native, stage.parent
ROOT = stage.ROOT / "initialized_replay"
IDENTITY = stage.ROOT / "replay_ROM_identity.json"
REPLAY = ROOT / "sailing_prose"
LIVE = ROOT / "verified_panels.json"
SHEET = ROOT / "sailing_mode_panels.png"
FRAMES = ((6220, 0, "Info"), (6320, 1, "Search"),
          (6420, 2, "Declare War before selection"), (6520, 2, "Declare War with Madeira selected"))


def replay():
    assert not IDENTITY.exists()
    release, proof = map(base.load, (parent.RELEASE, stage.PROOF))
    assert proof["predecessor_sha256"] == release["candidate_sha256"]
    assert base.digest(stage.ROM) == proof["candidate_sha256"]
    base.save(IDENTITY, release | dict(candidate=str(stage.ROM),
        candidate_sha256=proof["candidate_sha256"], target_ARM9_sha256=proof["target_ARM9_sha256"]))
    local_parent = type("ReplayIdentity", (), dict(ROM=stage.ROM, RELEASE=IDENTITY))
    run = FunctionType(history.run.__code__, vars(history) | {"parent": local_parent, "ROOT": ROOT})
    run("sailing_prose")


def verify():
    old = history.ROOT / "neutral_v2"
    manifest = base.load(stage.PROOF)
    compiled = manifest["rows"]
    inputs, traces, terminals = [], [], []
    for path in (old, REPLAY):
        terminals.append(base.load(path / "terminal.json"))
        inputs.append(base.load(path / "inputs.json"))
        traces.append(base.load(path / "requests.json"))
        assert not traces[-1]["errors"] and traces[-1]["all_host_slots_restored_and_core_file_exact"]
    assert inputs[0] == inputs[1] and traces[0]["source_requests"] == traces[1]["source_requests"]
    assert terminals[0]["location_fixture"] == terminals[1]["location_fixture"] or (
        terminals[0]["location_fixture"]["changes"] == terminals[1]["location_fixture"]["changes"]
        and terminals[0]["location_fixture"]["frame"] == terminals[1]["location_fixture"]["frame"] == 5000)
    current_path, previous_path = REPLAY / "capture/capture_report.json", old / "capture/capture_report.json"
    current, previous = map(base.load, (current_path, previous_path))
    assert current["ROM_sha256"] == base.digest(stage.ROM) == manifest["candidate_sha256"]
    assert previous["ROM_sha256"] == base.digest(parent.ROM) == manifest["predecessor_sha256"]
    assert current["cold_boot"] and not current["callback_errors"] and not current["savestate_loaded"]

    def capture(report, frame):
        result, = [entry for entry in report["frames_captured"] if entry["frame"] == frame
                   and entry["path"].endswith("_cold_boot.png")]
        assert base.digest(result["path"]) == result["PNG_sha256"]
        with Image.open(result["path"]) as picture:
            return result, picture.convert("RGB")

    image = base.NdsImage.open(stage.ROM)
    font = GameAsciiFont.from_arm9(image.read_file(native.ARM))
    rows, references = [], {}
    sheet = Image.new("RGB", (1024, 768), "#182025")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, panel_index, label) in enumerate(FRAMES):
        before, old_image = capture(previous, frame)
        after, new_image = capture(current, frame)
        assert old_image.crop((0, 176, 256, 384)).tobytes() == new_image.crop((0, 176, 256, 384)).tobytes()
        expected = set()
        panel = compiled[panel_index]
        for glyph in panel["glyphs"]:
            mask = font.decode(glyph["character"])
            x, y = glyph["origin"]
            expected.update((x + dx, y + dy) for dx in range(6) for dy in range(11) if mask.getpixel((dx, dy)))
        actual = {(x, y) for y in range(176) for x in range(256)
                  if native5(new_image.getpixel((x, y))) == (31, 31, 31)}
        assert actual == expected, (frame, panel["id"], len(expected - actual), len(actual - expected))
        assert all(native5(new_image.getpixel((x, y))) == (0, 0, 0)
                   for y in range(176) for x in range(256) if (x, y) not in expected)
        rows.append(dict(id=panel["id"], frame=frame, scope=label, complete_glyphs=len(panel["glyphs"]),
            complete_ink_and_blank_pixels=256*176, text=panel["english"], capture=after))
        references.update({r["path"]:r["PNG_sha256"] for r in (before, after)})
        x, y = i % 2 * 512, i // 2 * 384
        draw.text((x + 8, y + 4), label, fill="white")
        sheet.paste(new_image.crop((0, 0, 256, 176)).resize((512, 352), Image.Resampling.NEAREST), (x, y + 22))

    assert not LIVE.exists() and not SHEET.exists()
    sheet.save(SHEET)
    references.update({str(path):base.digest(path) for path in
        (current_path, previous_path, REPLAY / "requests.json", old / "requests.json", SHEET)})
    base.save(LIVE, dict(candidate_sha256=manifest["candidate_sha256"], native_display_matches=rows, evidence=references,
        located_Madeira_after_existing_position_fixture=True, ordinary_controls=True, actual_emulator=True,
        hardware=False, complete_first_last_glyphs_and_black_space=True,
        requests_and_lower_screen_equal=True, no_new_coverage_credit=True))
    print("Verified complete native glyphs and black space in all four sailing guide holds.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "verify"))
    globals()[parser.parse_args().action]()
