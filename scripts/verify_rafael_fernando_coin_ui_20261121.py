"""Verify a complete round of the original coin interface on the staged runtime."""
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from scripts import replay_rafael_fernando_coin_game_20261121 as replay
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_rafael_refit_sailing_gameplay_20261121 import panel, town


stage, base, native = replay.stage, replay.base, replay.native
ROOT = replay.COIN_ROUND
REPORT = ROOT / "capture/capture_report.json"
PROOF = ROOT / "verified_coin_ui.json"
PROMPT_INK = (0, 8, 0)
FRAMES = (3900, 4510, 4800, 5205, 5440, 6620, 6975, 7210, 7335, 7800)
ACTUAL_COUNTS = {4800: 10, 5205: 9, 5440: 6, 6620: 3, 6975: 1, 7210: 1}
RETURN = "Hmm... That's hard to answer..."


def occupied(picture):
    def gold(pixel):
        red, green, blue = pixel
        return red >= 119 and green >= 104 and green >= red - 32 and blue < red - 15

    return [i for i, (x, y) in enumerate(replay.COIN_CENTERS) if
            sum(gold(picture.getpixel((x + dx, 192 + y + dy))) for dx in range(-4, 5) for dy in range(-4, 5)) >= 40]


def main():
    assert not PROOF.exists()
    fixture_path, inputs = ROOT / "fixture.json", ROOT / "inputs.json"
    fixture, report = map(base.load, (fixture_path, REPORT))
    candidate = base.digest(stage.ROM)
    assert candidate == fixture["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert fixture["exact_candidate_inverse"] and fixture["source_opcode"] == "01c1" and fixture["source_offset"] == 388
    assert not fixture["natural_activation"] and not fixture["original_recruitment_branch_present"]
    assert base.digest(fixture["fixture"]) == report["ROM_sha256"] == fixture["fixture_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    schedule = base.load(inputs)
    assert report["frames"] == replay.ROUND_END and report["scripted_input_schedule"] == schedule
    assert [(r["start"], r.get("touch"), r["buttons"]) for r in schedule if 5000 < r["start"] < 5440] == [
        (5060, [48, 67], []), (5125, None, ["A"]), (5255, None, ["X"])]
    rom, prior = map(base.NdsImage.open, (stage.ROM, stage.parent.ROM))
    arm = rom.read_file(native.ARM)
    board_asset = "/_pxl/slackimg11.pxl"
    assert arm == prior.read_file(native.ARM)
    board = PxlImage.from_bytes(rom.read_file(board_asset))
    assert rom.read_file(board_asset) == prior.read_file(board_asset)
    captures = {e["frame"]: e for e in report["frames_captured"] if e["path"].endswith("_cold_boot.png")}
    pictures = {frame: town.read_frame(captures, frame)[1] for frame in FRAMES}
    opener = pictures[3900]
    assert all(native5(board.palette[board.indices[y * 256 + x]]) == native5(opener.getpixel((x, y + 192)))
               for y in range(72) for x in range(80, 256))
    font = panel.GameAsciiFont.from_arm9(arm)
    for frame, line in ((3900, "Let's decide who goes first."), (4510, "I'll go first."), (7800, RETURN)):
        _, bounds = panel.complete_mask(font, line, pictures[frame], 16, 297, PROMPT_INK)
        assert not any(pictures[frame].getpixel((x, y)) == PROMPT_INK
                       for x in range(bounds[2], 240) for y in range(297, 308))
    truth = {t: occupied(pictures[t]) for t in ACTUAL_COUNTS}
    assert {t: len(v) for t, v in truth.items()} == ACTUAL_COUNTS
    assert set(truth[4800]) - set(truth[5205]) == {0}
    assert all(set(truth[b]).issubset(truth[a]) for a, b in zip(truth, list(truth)[1:]))
    transition = pictures[7335]
    assert not occupied(transition) and transition.getpixel((80, 235))[0] > 0
    assert set(transition.crop((0, 280, 256, 384)).get_flattened_data()) == {(0, 0, 0)}
    opening = native.IlnkContainer.parse(rom.read_file(replay.PATH)).blocks[44]
    assert RETURN.encode("ascii") in opening and b"\x00\x49" == opening[26:28]
    panel.complete_mask(font, "Rafael Castor", pictures[7800], 16, 277, town.INKS[1])
    previews = [(title, pictures[frame]) for title, frame in (("Deciding who goes first", 3900),
        ("Fernando goes first", 4510), ("Board with ten coins", 4800), ("Board with six coins", 5440),
        ("Board with one coin", 6975), ("Original opening resumes", 7800))]
    sheet = ROOT / "coin_ui_round.png"
    town.sheet(previews, sheet)
    evidence = {str(path): base.digest(path) for path in (REPORT, fixture_path, inputs, Path(fixture["fixture"]))}
    base.save(PROOF, dict(candidate_sha256=candidate, original_coin_opcode="01c1", round_completed=True,
        original_opening_resumed=True, lower_screen_board_matches_registered_asset=True, natural_activation=False,
        no_recruitment_outcome_claim=True, live_coin_occupancy=truth,
        captured_frames=[captures[t] for t in FRAMES], evidence=evidence,
        sheets=[dict(path=str(sheet), sha256=base.digest(sheet))]))
    print("Verified native starting prompts, board changes from ten coins to one, and the return to the original opening.")


if __name__ == "__main__":
    main()
