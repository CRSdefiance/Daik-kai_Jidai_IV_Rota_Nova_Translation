"""Verify the entire ordinary sound-panel replay and both complete footer labels."""

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts import observe_sound_play_stop_20261123 as replay
from scripts import stage_sound_play_stop_20261123 as stage
from scripts.reconcile_editorial_acceptance_20261123 import digest, read, reference
from scripts.verify_plaque_release_v247 import find_mask


OUTPUT, SHEET = stage.ROOT / "verified_sound_controls.json", stage.ROOT / "sound_controls.png"
FOOTER = (226, 370, 255, 384)
EXPECTED_BOUNDS = [229, 371, 253, 382]
OLD_DOTS = {(231, 370), (236, 370), (246, 370)}
RETAINED_DOT_CASES = {3900, 4150, 4850, 5100, 5490, 5800}


def replay_evidence(case, candidate):
    root = replay.ROOT / case
    path = root / "capture/capture_report.json"
    trace = root / "requests.json"
    contract = root / "source_contract.json"
    data, observer = read(path), read(trace)
    assert data["ROM_sha256"] == candidate and digest(data["ROM"]) == candidate
    assert data["cold_boot"] and not data["savestate_loaded"] and not data["callback_errors"]
    assert not data.get("battery_save_preloaded") and not any(v for k,v in data.items() if k.startswith("synthetic_"))
    assert data["scripted_input_schedule"] == replay.schedule(case)[0]
    assert data["frames"] == replay.FRAMES[-1]
    assert not observer["errors"] and not observer["mismatches"] and not observer["source_requests"]
    assert observer["all_host_slots_restored_and_core_file_exact"] and observer["source_contract_sha256"] == digest(contract)
    assert {row["PC"] for row in read(contract)["targets"]} == replay.TARGETS
    rows = observer["rows"]
    assert [r["PC"] for r in rows] == [replay.PLAY, replay.STOP, replay.PLAY, replay.STOP, replay.PLAY]
    assert [r["playing"] for r in rows] == [0, 1, 0, 1, 1]
    frames = {r["frame"]: r for r in data["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    assert set(replay.FRAMES) <= frames.keys()
    return data, rows, frames, {str(f): digest(f) for f in (path, trace, contract)}


def picture(row):
    assert digest(row["path"]) == row["PNG_sha256"]
    with Image.open(row["path"]) as image:
        assert image.size == (256, 384)
        return image.convert("RGB")


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    stored = read(stage.PROOF)
    before, after = (replay_evidence(case, stored[key]) for case, key in (
        ("current", "predecessor_sha256"), ("staged", "candidate_sha256")))
    assert before[0]["core_options"] == after[0]["core_options"]
    assert before[0]["core_DLL_sha256"] == after[0]["core_DLL_sha256"]
    assert digest(replay.ROOT / "current/terminal.json") == stored["current_replay_sha256"]
    arm = NdsImage.open(stage.ROM).read_file(stage.ARM)
    assert arm[stage.SLOT:stage.SLOT + 16] == stage.STOP_ENGLISH + stage.PLAY_ENGLISH
    for prior, installed in zip(before[1], after[1], strict=True):
        old_bytes = stage.STOP_JAPANESE if prior["PC"] == replay.STOP else stage.PLAY_ENGLISH
        new_bytes = stage.STOP_ENGLISH if prior["PC"] == replay.STOP else stage.PLAY_ENGLISH
        assert prior["text_hex"] == old_bytes[:4].hex()
        assert installed == prior | {"text_hex": new_bytes[:4].hex()}

    font = GameAsciiFont.from_arm9(arm)
    masks, holds, images, retired_dots = {}, {}, {}, {}
    for frame in replay.FRAMES:
        old, new = (picture(result[2][frame]) for result in (before, after))
        difference = ImageChops.difference(old, new).getbbox()
        if 2801 < frame < 5301:
            selected = next(row for row in reversed(before[1]) if row["frame"] <= frame)
            text = "Stop" if selected["PC"] == replay.STOP else "Play"
            mask = find_mask(font, text, new, FOOTER)
            assert mask["bounds"] == EXPECTED_BOUNDS
            if text == "Stop":
                x0, y0, x1, y1 = difference
                assert FOOTER[0] <= x0 < x1 <= FOOTER[2] and FOOTER[1] <= y0 < y1 <= FOOTER[3]
            else:
                assert mask == find_mask(font, text, old, FOOTER)
            masks[frame] = mask
        if frame in RETAINED_DOT_CASES:
            shift = -12 if frame >= 5301 else 0
            dots = {(x + shift, y) for x, y in OLD_DOTS}
            assert difference == (min(x for x, _ in dots), 370, max(x for x, _ in dots) + 1, 371)
            assert {pos for pos in ((x, 370) for x in range(difference[0], difference[2]))
                    if old.getpixel(pos) != new.getpixel(pos)} == dots
            assert all(old.getpixel(pos) == (230, 230, 230) and new.getpixel(pos) == (123, 141, 180) for pos in dots)
            retired_dots[frame] = sorted(dots)
        elif frame not in masks or masks[frame]["text"] == "Play":
            assert difference is None
        holds[frame] = difference
        images[frame] = (old, new)

    assert [frame for frame, value in masks.items() if value["text"] == "Stop"] == [3500, 4510, 4650]
    assert all(images[3500][0].getpixel(pos) == (230, 230, 230) and
               images[3500][1].getpixel(pos) == (123, 141, 180) for pos in OLD_DOTS)
    assert masks[3900]["text"] == masks[5100]["text"] == "Play"
    sheets = Image.new("RGB", (552, 569), "#26313a")
    labels = ImageDraw.Draw(sheets)
    for i, pic in enumerate(images[3500]):
        x = 10 + 276 * i
        labels.text((x, 8), ("Previous ROM · Music playing", "Staged ROM · Music playing")[i], fill="white")
        sheets.paste(pic, (x, 25))
    for j, (frame, state) in enumerate(((3200, "BGM off"), (3500, "BGM on"), (3900, "BGM stopped"), (5100, "SFX selected"))):
        x = 10 + j * 137
        labels.text((x, 426), state, fill="white")
        strip = images[frame][1].crop((214, 369, 256, 384)).resize((126, 45), Image.Resampling.NEAREST)
        sheets.paste(strip, (x, 446))
    labels.text((10, 508), "Stop also clears three old Japanese pixels that survived a return to Play.", fill="white")
    sheets.save(SHEET)
    rows = [row | dict(review=row["review"] | dict(formatting=True)) for row in stored["records"]]
    result = dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        translation_policy=stored["translation_policy"], encoder=stored["encoder"], target_locale=stored["target_locale"],
        review_gates=stored["review_gates"], records=rows, all_full_frame_differences=holds,
        exact_play_and_stop_glyphs=masks, native_state_trace=after[1], retired_Japanese_glyph_residue=retired_dots,
        ordinary_controller_replay=True, audio_output_assessed=False, hardware=False,
        sheet=reference(SHEET), evidence=before[3] | after[3] | {str(stage.PROOF):digest(stage.PROOF)})
    validate_natural_dialogue_batch(result)
    stage.base.save(OUTPUT, result)
    print("Verified complete Play and Stop lettering and the removal of three residual pixels across six later holds.")


if __name__ == "__main__":
    main()
