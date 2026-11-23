"""Bind the partial-refill and ratio prompts to complete displayed glyphs."""

from PIL import Image, ImageDraw

from scripts import register_port_supply_dialogue_20261115 as prior
from scripts import replay_port_resupply_options_20261119 as play
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold

base, current, stage = play.base, play.current, prior.stage
PROOF = play.ROOT / "verified_resupply_prompts.json"
SHEET = play.ROOT / "port_resupply_choices.png"
CASES = {
    "poor": (816, (3400, 3550), 3750, "The offer clearly states the shortfall and asks whether to buy a smaller refill."),
    "mix": (817, (3750, 3950), 5000, "The short follow-up specifies which supplies the player can rebalance."),
}


def main():
    assert not PROOF.exists() and not SHEET.exists()
    release = base.load(current.RELEASE)
    assert release["candidate_sha256"] == base.digest(current.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    image = base.NdsImage.open(current.ROM)
    arm, common, kanji = (image.read_file(path) for path in (stage.ARM, stage.COMMON, "/GRP/KANJI.FNT"))
    assert stage.digest(arm) == release["target_ARM9_sha256"]
    assert stage.digest(common) == release["target_COMMON_sha256"]
    records = stage.owned_entries(common, arm, stage.digest(arm[stage.DIRECTORY_OFFSET:stage.TABLE_OFFSET]))
    earlier = {r["message_ID"]: r for r in base.load(prior.REVIEW)["records"]}
    layouts = {r["n"]: r for r in base.load(stage.STORED)["native_cases"]}
    raster, _, _ = stage.font_tools(image)
    evidence = {str(path): base.digest(path) for path in (current.RELEASE, prior.REVIEW, stage.STORED)}
    results, photos = [], []
    for mode, (ident, held_frames, return_frame, note) in CASES.items():
        folder = play.ROOT / mode
        path = folder / "capture/capture_report.json"
        report = base.load(path)
        assert report["ROM_sha256"] == release["candidate_sha256"] and report["cold_boot"]
        assert not report["savestate_loaded"] and not report["callback_errors"]
        assert report["scripted_input_schedule"] == base.load(folder / "inputs.json")
        donor = report["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
        assert {k for k, v in report.items() if k.startswith("synthetic_") and v} == {"synthetic_condition_fixtures"}
        fixture, = report["synthetic_condition_fixtures"]
        assert fixture["mode"] == mode and fixture["frame"] == 3200 and fixture["all_other4MiB_RAM_exact"]
        expected = earlier[ident]
        assert all(expected["review"].values()) and records[ident].text.hex() == expected["staged_hex"]
        layout = layouts[ident]
        lo, hi = layout["caller_span"]
        assert arm[lo:hi].hex() == layout["original_caller_hex"]
        plane, _ = stage.render_portrait(raster, arm, kanji, bytes.fromhex(layout["native_output_hex"]))
        assert stage.digest(plane) == layout["native_plane_sha256"]
        shots = {entry["frame"]: entry for entry in report["frames_captured"] if entry["path"].endswith("_cold_boot.png")}
        holds = []
        for frame in (*held_frames, return_frame):
            ref = shots[frame]
            assert base.digest(ref["path"]) == ref["PNG_sha256"]
            evidence[ref["path"]] = ref["PNG_sha256"]
            with Image.open(ref["path"]) as photo:
                screenshot = photo.convert("RGB")
            if frame in held_frames:
                ink = native_hold(screenshot, plane)
                holds.append(dict(capture=ref, complete_glyph_ink_pixels=ink))
            if frame in (held_frames[0], return_frame):
                photos.append((f"COMMON {ident} · frame {frame}", screenshot.crop((0, 192, 256, 384))))
        evidence[str(path)] = base.digest(path)
        results.append(dict(id=ident, source_reference=expected["source_reference"], source_hex=expected["source_hex"],
            current_reference=stage.reference(records[ident]), current_hex=records[ident].text.hex(),
            wording=expected["english"], decision="retention", localization_note=note, review=expected["review"],
            fixture=fixture, matching_holds=holds, port_menu_return=shots[return_frame]))
    sheet = Image.new("RGB", (1040, 808), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (label, photo) in enumerate(photos):
        x, y = (i % 2)*520, (i//2)*404
        draw.text((x+4, y+3), label, fill="white")
        sheet.paste(photo.resize((512, 384), Image.Resampling.NEAREST), (x+4, y+17))
    sheet.save(SHEET)
    evidence[str(SHEET)] = base.digest(SHEET)
    base.save(PROOF, dict(candidate_sha256=release["candidate_sha256"], cases=results,
                          initialized_Copenhagen_port=True, naturally_earned_preconditions=False,
                          hardware=False, new_editorial_credit=0, evidence=evidence))
    print("Both previously offline-only Port prompts matched complete live glyphs.")


if __name__ == "__main__":
    main()
