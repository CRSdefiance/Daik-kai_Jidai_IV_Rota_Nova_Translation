"""Verify the registered Rafael preparation scene during ordinary New Game play."""
from types import SimpleNamespace
import re

from scripts import replay_rafael_preparation_gameplay_20261121 as run
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as panel


active, base, native, town = run.active, run.base, panel.native, panel.town
REPORT = run.ROOT / "capture/capture_report.json"
PROOF = run.ROOT / "verified_preparation.json"
SPEAKERS = {0: "Rafael Castor", 4: "Janus Pasar", 5: "Claudio Manaus", 6: "Julio Erneco"}
NAMES = {b"FI": b"Rafael", b"FA": b"Castor", b"FO": b"Castor Co."}
ANCHORS = {264, 285, 308, 316, 327, 355, 398, 432, 446, 449, 464, 469}


def main():
    candidate = base.digest(active.ROM)
    report, release, earlier = map(base.load, (REPORT, active.RELEASE, run.opening.ROOT / "verified_harbor.json"))
    assert candidate == report["ROM_sha256"] == earlier["candidate_sha256"] == release["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and not any(
        value for key, value in report.items() if key.startswith("synthetic_")
    )
    initial = base.load(run.ROOT / "inputs.json")
    assert report["scripted_input_schedule"][:len(initial)] == initial
    current, original = map(base.NdsImage.open, (active.ROM, native.CLEAN))
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    arm, font = (current.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    context = SimpleNamespace(image=current, arm=arm)
    paint, paint_notice = town.clipped_renderer(context), town.current_fe_painter(context)
    name_font = panel.GameAsciiFont.from_arm9(arm)
    scenario = "/data/SC0.DK4"
    source, stored = (native.IlnkContainer.parse(rom.read_file(scenario)).blocks[44] for rom in (original, current))
    shots = {frame["frame"]: frame for frame in report["frames_captured"] if frame["frame"] >= 9650}
    pictures = {frame: town.read_frame(shots, frame)[1] for frame in shots}
    live_masks = {}
    for width in (216, 228):
        for frame, picture in pictures.items():
            pixels = picture.crop((16, 296, 16 + width, 360)).get_flattened_data()
            live_masks[width, frame] = bytes(pixel == town.INKS[0] for pixel in pixels)
    previous = {row["id"] for row in earlier["holds"]}
    matches, missed = [], []
    review = base.load(active.REVIEW)
    for row in review["records"]:
        number, ident, selector = row["source_record_index"], row["id"], row["source_selector"]
        if ident in previous or (number not in ANCHORS and row["decision"] != "revision"):
            continue
        source_ref, current_ref = row["source_reference"], row["registered_reference"]
        assert row["file_path"] == scenario and all(row["review"].values())
        assert native.digest(source) == source_ref["block_sha256"]
        assert native.digest(stored) == current_ref["block_sha256"]
        offset = source_ref["offset"]
        japanese = bytes.fromhex(source_ref["exact_hex"])
        assert source[offset:offset + len(japanese)] == japanese
        offset = current_ref["offset"]
        command = bytes.fromhex(current_ref["exact_command_hex"])
        assert stored[offset:offset + len(command)] == command
        assert command[:6] == b"\0\x40\xff\xff\0" + bytes([selector])
        if row["decision"] == "revision":
            layout = row["native_formatting_evidence"]["layouts"][0]
            body = bytes.fromhex(layout["expanded_hex"])
        else:
            body = re.sub(rb"\b(FI|FA|FO)\b", lambda token: NAMES[token[0]], command[6:].split(b"\0", 1)[0])
        if selector == 254:
            layout_result = paint_notice(body)
            plane, width = layout_result["physical"], 228
        else:
            layout_result = paint(arm, font, body)
            page, = layout_result["pages"]
            assert page["native_independent_plane_equal"]
            plane, width = bytes.fromhex(page["native_plane_hex"]), 216
        assert len(body) == layout_result["complete_consumed_bytes"]
        if row["decision"] == "revision":
            assert native.digest(plane) == layout["plane_sha256"]
        found = None
        expected_mask = bytes(bool(pixel) for pixel in plane)
        for frame, picture in sorted(pictures.items()):
            if live_masks[width, frame] != expected_mask:
                continue
            assert panel.mask_check(plane, width, picture)
            if selector != 254:
                try:
                    panel.complete_mask(name_font, SPEAKERS[selector], picture, 16, 277, town.INKS[1])
                except ValueError:
                    continue
            found = shots[frame]
            break
        evidence = dict(id=ident, english=row["english"], decision=row["decision"], gates=row["review"],
                        source=source_ref, registered=current_ref, expected_layout_sha256=native.digest(plane))
        if found is None:
            missed.append(evidence)
        else:
            matches.append(evidence | {"observed": found})
    menu_frame, _ = town.read_frame(shots, 32225)
    choices = []
    for menu_row in [r for r in review["records"] if r["kind"] == "typed-choice-label"]:
        ref = menu_row["registered_reference"]
        command = bytes.fromhex(ref["exact_command_hex"])
        assert stored[ref["offset"]:ref["offset"] + len(command)] == command
        choices.append(dict(caption=menu_row["english"], source=menu_row["source_reference"], registered=ref))
    assert [choice["caption"] for choice in choices] == ["Ask him.", "Prepare alone."]
    observed = {row["id"]: row["observed"]["frame"] for row in matches}
    assert observed["DK4_MES_B44_R0449"] < 32225 < observed["DK4_MES_B44_R0464"] < observed["DK4_MES_B44_R0469"]
    ordered = sorted(matches, key=lambda row: row["observed"]["frame"])
    sheets = []
    for start in range(0, len(ordered), 6):
        frames = [(row["id"], pictures[row["observed"]["frame"]]) for row in ordered[start:start + 6]]
        target = run.ROOT / f"verified_preparation_{start // 6 + 1}.png"
        town.sheet(frames, target)
        sheets.append(dict(path=str(target), sha256=base.digest(target)))
    base.save(PROOF, dict(candidate_sha256=candidate, report=str(REPORT), report_sha256=base.digest(REPORT),
        ordinary_new_game=True, exact_native_dialogue_pixel_masks=matches, unobserved=missed, sheets=sheets,
        preparation_menu=dict(observed=menu_frame, exact_captions=choices, selected="Ask him.",
            branch_observed_only="Ask him."), earlier_revised_matches=len(previous), hardware_verified=False))
    print(f"Verified {len(matches)} complete native masks, including "
          f"{sum(row['decision'] == 'revision' for row in matches)} revised panels. "
          f"Unmatched: {', '.join(row['id'] for row in missed) or 'none'}.")


if __name__ == "__main__":
    main()
