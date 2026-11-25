"""Replay established Search outcomes and check complete count glyphs."""

from argparse import ArgumentParser
from io import StringIO
from json import dumps
from pathlib import Path
from struct import unpack_from
import sys
from unicodedata import normalize

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_crew_and_shore_reports_v1 as history
from scripts import stage_search_supply_and_fatigue_digits_20261121 as stage


base, shared = stage.base, stage.shared
ROOT = stage.ROOT
PROOF, SHEET = ROOT / "verified_gameplay.json", ROOT / "search_counts_live.png"
END = 10433
HOLDS = {5500: (309, (15,)), 10433: (308, (3,))}
RECAPTURES = (7401, 8652, 8682)


def replay(version, extend=False):
    plan, prior_path, _, donor, inputs, commands, _ = history.history("attack")
    selected = [cmd for cmd in commands if cmd.get("until", END + 1) <= END]
    assert selected[-1]["until"] == END
    fixture = "coherent_source_region2_fleet_and_mobile_shore"
    assert all(c["battle_fixture"] == {"fatigue_search_context": fixture}
               for c in selected if "battle_fixture" in c)
    last = END
    if extend:
        last = END + 200
        selected.append(dict(until=last, buttons=["A"], duration=4))
        for _ in range(3):
            selected.extend((
                dict(until=last + 140, buttons=["Y"], duration=12),
                dict(until=last + 280, buttons=["Y"], duration=12),
                dict(until=last + 310, duration=1, battle_fixture={"fatigue_search_context": fixture}),
                dict(until=last + 540, buttons=["A"], duration=4),
                dict(until=last + 565, duration=1),
                dict(until=last + 745, buttons=["A"], duration=4),
                dict(until=last + 925, buttons=["A"], duration=4),
            ))
            last += 925
    selected.append({"stop": True})
    directory = ROOT / (f"{version}_extra" if extend else version)
    directory.mkdir(exist_ok=False)
    stable = base.load(stage.parent.RELEASE if version == "before" else stage.PROOF)
    rom = stage.parent.ROM if version == "before" else stage.ROM
    assert base.digest(rom) == stable["candidate_sha256"]
    assert base.digest(donor) == plan["source_donor_sha256"]
    base.save(directory / "commands.json", selected)
    old = sys.argv, sys.stdin, history.dispatch.apply_fixture
    try:
        sys.argv = [__file__, "--rom", str(rom), "--out", str(directory / "capture"), "--frames", str(last + 1),
                    "--inputs-json", str(inputs), "--battery-save", str(donor), "--touchscreen",
                    "--capture-every", "999999", "--pause-at", str(plan["initial_pause_frame"]),
                    "--capture-at", *map(str, HOLDS), "--dump-capture-ram", "--dump-ram", "--allow-battle-fixtures"]
        sys.stdin = StringIO("".join(dumps(cmd) + "\n" for cmd in selected))
        history.dispatch.apply_fixture = history.fixtures(stable["target_ARM9_sha256"])
        history.harness.main()
    finally:
        sys.argv, sys.stdin, history.dispatch.apply_fixture = old
    report = base.load(directory / "capture/capture_report.json")
    assert report["frames"] == last and not report["callback_errors"] and report["ROM_sha256"] == stable["candidate_sha256"]
    base.save(directory / "run.json", dict(historical_report=str(prior_path), historical_report_sha256=base.digest(prior_path),
                                          normal_inputs=True, held_frames=list(HOLDS), final_frame=last))


def picture_mask(raster, arm, kanji, raw, spoken):
    if spoken:
        pixels, glyphs = stage.render_portrait(raster, arm, kanji, raw)
    else:
        pixels, glyphs = stage.common.discovery.mixed.render(raster, arm, kanji, raw)
    return pixels, glyphs


def verify():
    assert not PROOF.exists()
    stage_proof = base.load(stage.PROOF)
    folders = [ROOT / v / "capture" for v in ("before", "after")]
    paths = [folder / "capture_report.json" for folder in folders]
    cases = [base.NdsImage.open(p) for p in (stage.parent.ROM, stage.ROM)]
    arms = [img.read_file(shared.ARM) for img in cases]
    prior, after = reports = list(map(base.load, paths))
    assert [r["ROM_sha256"] for r in reports] == [stage_proof["parent_sha256"], stage_proof["candidate_sha256"]]
    assert all(r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"] and r["frames"] == END for r in reports)
    for key in ("core_DLL_sha256", "core_options", "scripted_input_schedule", "exact_requested_capture_frames"):
        assert prior[key] == after[key]
    for key in ("source_sha256", "copied_byte_exact_before_cold_boot"):
        assert prior["battery_save_preloaded"][key] == after["battery_save_preloaded"][key]
    fixture_key = "synthetic_battle_recovery_proximity_fixtures"
    before_fixtures, after_fixtures = [r[fixture_key] for r in reports]
    for old, new in zip(before_fixtures, after_fixtures, strict=True):
        assert old["frame"] == new["frame"] and old["owned_bytes"] == new["owned_bytes"]
        assert old["changes"] == new["changes"] and len(new["owned_bytes"]) == 48
    assert len(before_fixtures) == 5
    snapshot_key = "read_only_capture_RAM_snapshots"
    snapshots = [{r["frame"]: r for r in report[snapshot_key]} | {END: report["read_only_RAM_snapshot"]}
                 for report in reports]
    assert all(set(HOLDS) <= set(shot) for shot in snapshots)
    frames = [{r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
              for report in reports]
    assert frames[0].keys() == frames[1].keys() and END in frames[0]
    sheet = Image.new("RGB", (1024, 224 * len(HOLDS)), "#263238")
    labels = ImageDraw.Draw(sheet)
    rasters = [stage.common.discovery.mixed.font_tools(image)[0] for image in cases]
    kanji = cases[1].read_file("/GRP/KANJI.FNT")
    assert kanji == cases[0].read_file("/GRP/KANJI.FNT")
    changed, unaffected = [], []
    expected = {row["message_ID"]: row["english"] for row in stage_proof["records"]}
    for frame, old in frames[0].items():
        new = frames[1][frame]
        for row in (old, new):
            assert base.digest(row["path"]) == row["PNG_sha256"]
        if old["framebuffer_sha256"] == new["framebuffer_sha256"]:
            unaffected.append(frame)
            continue
        # Consecutive paused captures of the same notice can share the held page.
        anchor = 5500 if frame in RECAPTURES else frame if frame in HOLDS else None
        assert anchor is not None, frame
        if frame != anchor:
            continue
        n, amounts = HOLDS[anchor]
        spoken = n in stage.FORAGE_IDS
        texts, pixels = [], []
        panels = [Image.open(r["path"]).convert("RGB") for r in (old, new)]
        for ras, arm, shot, panel in zip(rasters, arms, snapshots, panels, strict=True):
            receipt = shot[anchor]
            assert receipt["read_only_export"] and base.digest(receipt["path"]) == receipt["sha256"]
            raw = Path(receipt["path"]).read_bytes()
            offset = unpack_from("<I", arm, 0x54450 if spoken else 0x54894)[0] - stage.number.BASE
            display = raw[offset:offset + 512].split(b"\0", 1)[0]
            assert " ".join(normalize("NFKC", display.decode("cp932")).split()) == expected[n] % tuple(map(str, amounts))
            texts.append(display.hex())
            plane, glyphs = picture_mask(ras, arm, kanji, display, spoken)
            pixels.append(plane)
        box = (16, 296, 244, 360 if spoken else 344)
        assert bytes(c == (0, 8, 0) for c in panels[1].crop(box).get_flattened_data()) == pixels[1], (anchor, texts)
        delta = ImageChops.difference(*panels).getbbox()
        assert delta and 16 <= delta[0] < delta[2] <= 244 and 294 <= delta[1] < delta[3] <= 361, (anchor, delta)
        changed.append(dict(frame=frame, message_ID=n, source_amounts=amounts, original_display_hex=texts[0],
                            current_display_hex=texts[1], complete_ASCII_ink=True, difference_bounds=delta))
        for i, panel in enumerate(panels):
            left, top = i * 512, (len(changed) - 1) * 224
            labels.text((left + 5, top + 5), f"COMMON {n} " + ("before" if i == 0 else "corrected"), fill="white")
            cropped = panel.crop((0, 280, 256, 384)).resize((512, 208), Image.Resampling.NEAREST)
            sheet.paste(cropped, (left, top + 16))
    assert [row["frame"] for row in changed] == list(HOLDS) and 7621 in unaffected
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=stage_proof["candidate_sha256"], parent_sha256=stage_proof["parent_sha256"],
        original_search_outcomes=True, position_fixture_count=len(before_fixtures), held_results=changed,
        unchanged_frames=unaffected, return_to_sailing=7621, exact_same_return_frame=True,
        foraging_actual_current_replay=False, hardware_verified=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence={str(path): base.digest(path) for path in paths}))
    print("Both fatigue notices match their complete regular-width glyphs in gameplay.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("before", "after", "verify"))
    parser.add_argument("--extend", action="store_true", help="Try three more normal Search attempts from the final notice.")
    args = parser.parse_args()
    verify() if args.action == "verify" else replay(args.action, extend=args.extend)
