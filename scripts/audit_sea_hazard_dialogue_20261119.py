"""Bind hazard replay screens to the staged dialogue and the original portraits."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from scripts import replay_sea_hazard_dialogue_20261119 as play
from scripts import stage_sea_hazard_dialogue_20261119 as build
from scripts.audit_fleet_encounter_dialogue_20261119 import page, record_frame, snapshot
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold

base = build.base
PROOF = build.ROOT / "verified_hazard_replays_capture.json"
SIGHTING = {
    9627: b"Oh! Admiral! Whirlpool!",
    9827: b"Let's steer clear of it! All hands to your stations!",
    10027: b"Admiral, we've spotted a port!",
}


def audit(folder, image, staged, evidence, observations, required_contact):
    path = folder / "terminal.json"
    terminal = base.load(path)
    assert terminal["candidate_sha256"] == staged["candidate_sha256"]
    evidence[str(path)] = base.digest(path)
    for key in ("report", "commands"):
        assert base.digest(terminal[key]) == terminal[key + "_sha256"]
        evidence[terminal[key]] = terminal[key + "_sha256"]
    report = base.load(terminal["report"])
    assert report["ROM_sha256"] == staged["candidate_sha256"] and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    captures = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
    ram = {r["frame"]: r for r in report["read_only_pause_RAM_snapshots"]}
    fixtures = report["synthetic_condition_fixtures"]
    assert [r["mode"] for r in fixtures] == (["choose", "restore", "place_first_contact_zone"]
                                           if required_contact else ["choose", "restore"])
    arm = image.read_file(build.ARM)
    for receipt in fixtures:
        ident = receipt["frame"]
        data = snapshot(ram[ident])
        request = {k: receipt[k] for k in ("event", "mode")}
        _, reconstructed = play.set_condition(arm, data, request)
        # JSON storage canonicalizes coordinate tuples to lists.
        for field in ("old_position", "ship_position"):
            if field in reconstructed:
                reconstructed[field] = list(reconstructed[field])
        assert reconstructed | {"frame": ident} == receipt
        evidence[ram[ident]["path"]] = ram[ident]["sha256"]

    relative = play.encounter.earlier.BASE
    plain, wrapped = [unpack_from("<I", arm, i)[0] - relative for i in (0x5444C, 0x54450)]
    selector = play.encounter.earlier.FIELD - relative
    raster, _, _ = build.workflow.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    rows = {bytes.fromhex(r["staged_hex"]): r for r in staged["records"] if 2409 <= r["message_ID"] <= 2412}
    panels, observed = [], {}
    for n, capture in captures.items():
        if n < 9627:
            continue
        raw = snapshot(ram[n])
        if n > 9627:
            assert raw[selector:selector+4] == play.encounter.earlier.ORIGINAL
        stored = raw[plain:plain+256].split(b"\0", 1)[0]
        row = rows.get(stored)
        display = raw[wrapped:wrapped+256].split(b"\0", 1)[0]
        if n in observations:
            assert b" ".join(display.split()) == observations[n], (n, display)
        if n not in observations and (row is None or row["message_ID"] in observed):
            continue
        pixels, glyphs = build.render_portrait(raster, arm, kanji, display)
        photographed = page(image, capture)
        ink = native_hold(photographed, pixels)
        label = f"{n}: {display.decode('ascii').strip().splitlines()[0]}"
        panels.append((photographed, label))
        evidence[capture["path"]] = capture["PNG_sha256"]
        evidence[ram[n]["path"]] = ram[n]["sha256"]
        if row:
            assert row["display_hex"] == display.hex()
            assert build.native.digest(pixels) == row["formatting_evidence"]["ink_sha256"]
            assert len(glyphs) == row["formatting_evidence"]["glyph_count"]
            observed[row["message_ID"]] = dict(message_ID=row["message_ID"], frame=n,
                complete_visible_ink_pixels=ink, original_display_hex=display.hex(), capture=capture)
    assert len(panels) >= len(observations)
    if required_contact:
        assert observed, "The seed needs a native contact frame before coverage can be credited."
    sheet = Image.new("RGB", (1040, 208*((len(panels)+1)//2)), "#263238")
    draw = ImageDraw.Draw(sheet)
    for index, (photo, label) in enumerate(panels):
        record_frame(draw, sheet, photo, index, label)
    path = folder / ("whirlpool_contact.png" if required_contact else "whirlpool_sighting.png")
    sheet.save(path)
    evidence[str(path)] = base.digest(path)
    return (dict(event="whirlpool_contact" if required_contact else "whirlpool_sighting",
                 observed=list(observed.values()), original_warning_frames=list(observations),
                 selector_restored=True, fixture_receipts=fixtures),
            dict(path=str(path), sha256=evidence[str(path)]))


def main():
    assert not PROOF.exists()
    staged = base.load(build.PROOF)
    sha = base.digest(build.ROM)
    assert staged["candidate_sha256"] == sha
    image = base.NdsImage.open(build.ROM)
    evidence = {str(build.PROOF): base.digest(build.PROOF)}
    outcomes, sheets = [], []
    for folder, observations, contact in (("replays", SIGHTING, False),
                                          ("replays_contact", {}, True)):
        outcome, sheet = audit(build.ROOT / folder / "whirlpool", image, staged, evidence, observations, contact)
        outcomes.append(outcome)
        sheets.append(sheet)
    base.save(PROOF, dict(candidate_sha256=sha, outcomes=outcomes, sheets=sheets, evidence=evidence,
        original_sequences_initialized=True, natural_random_selection_verified=False, hardware=False))
    print("Verified the original whirlpool warning and native collision portrait.")


if __name__ == "__main__":
    main()
