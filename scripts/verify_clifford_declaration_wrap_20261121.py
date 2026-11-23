"""Replay the declaration and compare complete current and corrected portrait masks."""

from argparse import ArgumentParser
from inspect import getsource
from types import SimpleNamespace

from PIL import Image

from scripts import stage_clifford_declaration_wrap_20261121 as stage
from scripts.verify_shipyard_gameplay_v760 import independent_font


base, replay = stage.base, stage.gameplay.replay
ROOT = stage.ROOT / "playback"
RUN = ROOT / "attack"
PROOF = stage.ROOT / "verified_gameplay.json"
INK = (0, 8, 0)
HOLD = 6120


def playback():
    draft, original = map(base.load, (stage.PROOF, stage.parent.RELEASE))
    for key in ("candidate_sha256", "target_ARM9_sha256", "target_COMMON_sha256"):
        original[key] = draft[key]
    release = stage.ROOT / "playback_binding.json"
    base.save(release, original)
    overrides = vars(replay) | dict(ROOT=ROOT, current=SimpleNamespace(ROM=stage.ROM, RELEASE=release),
                                   __file__=__file__)
    exec(compile(getsource(replay.main), __file__ + "::paired-replay", "exec"), overrides)
    overrides["main"]()


def verify():
    assert not PROOF.exists()
    draft = base.load(stage.PROOF)
    before, after = (folder / "capture/capture_report.json" for folder in (stage.gameplay.ROOT, RUN))
    reports = list(map(base.load, (before, after)))
    assert [r["ROM_sha256"] for r in reports] == [draft["parent_sha256"], draft["candidate_sha256"]]
    assert base.digest(stage.ROM) == draft["candidate_sha256"]
    for key in ("core_DLL_sha256", "core_options", "scripted_input_schedule", "exact_requested_capture_frames"):
        assert reports[0][key] == reports[1][key], key
    fixture = "synthetic_battle_recovery_proximity_fixtures"
    before_fixture, after_fixture = [r[fixture][0] for r in reports]
    individual_ram_hashes = {"before_RAM_sha256", "after_RAM_sha256", "fixture_sha256"}
    assert {k: v for k, v in before_fixture.items() if k not in individual_ram_hashes} == {
        k: v for k, v in after_fixture.items() if k not in individual_ram_hashes}
    for key in ("source", "source_sha256", "copied_byte_exact_before_cold_boot"):
        assert reports[0]["battery_save_preloaded"][key] == reports[1]["battery_save_preloaded"][key], key
    assert all(r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"] for r in reports)
    assert base.digest(stage.gameplay.ROOT / "inputs.json") == base.digest(RUN / "inputs.json")
    requests = [base.load(folder / "requests.json") for folder in (stage.gameplay.ROOT, RUN)]
    for folder, trace in zip((stage.gameplay.ROOT, RUN), requests, strict=True):
        assert trace["source_contract_sha256"] == base.digest(folder / "source_contract.json")
        assert not trace["errors"] and not trace["mismatches"] and trace["callbacks"] == 44
    assert requests[0]["source_requests"] == requests[1]["source_requests"]
    stills = [{r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
              for report in reports]
    assert stills[0].keys() == stills[1].keys()
    changed, unchanged = [], []
    for frame, old in stills[0].items():
        new = stills[1][frame]
        assert all(base.digest(r["path"]) == r["PNG_sha256"] for r in (old, new)), frame
        (unchanged if old["framebuffer_sha256"] == new["framebuffer_sha256"] else changed).append(frame)
    assert changed == [HOLD]
    rom = base.NdsImage.open(stage.ROM)
    arm, kanji = (rom.read_file(path) for path in (stage.shared.ARM, "/GRP/KANJI.FNT"))
    view = next(r for r in draft["native_views"] if r["message_ID"] == stage.N)
    masks, pictures = [], []
    for side, stills_by_frame in zip(("before_hex", "after_hex"), stills, strict=True):
        row = stills_by_frame[HOLD]
        words = [line.strip() for line in bytes.fromhex(view[side]).decode("ascii").splitlines()]
        font_mask = independent_font(arm, kanji, words)
        expected = {(16 + i % 228, 297 + i // 228) for i, ink in enumerate(font_mask) if ink}
        image = Image.open(row["path"]).convert("RGB")
        actual = {(x, y) for y in range(294, 366) for x in range(16, 244) if image.getpixel((x, y)) == INK}
        assert actual == expected, (side, len(actual ^ expected))
        masks.append(expected)
        pictures.append(image)
    differences = {(i % 256, i // 256) for i, (old, new) in enumerate(
        zip(pictures[0].get_flattened_data(), pictures[1].get_flattened_data(), strict=True)) if old != new}
    assert differences == (masks[0] ^ masks[1])
    terminal = [stage.gameplay.ROOT / "requests.json", RUN / "requests.json", before, after]
    base.save(PROOF, dict(candidate_sha256=draft["candidate_sha256"], parent_sha256=draft["parent_sha256"],
        original_fleet_inputs_and_40_byte_location_fixture=True, hardware_verified=False,
        exact_unchanged_framebuffers=unchanged, changed_frame=HOLD, changed_text_pixels=len(differences),
        total_ink=list(map(len, masks)), original_text_retained=True, before=stills[0][HOLD], after=stills[1][HOLD],
        report_evidence={str(path): base.digest(path) for path in terminal}))
    print(f"All {len(unchanged)} control frames unchanged. Clifford’s live page matches the complete glyph mask.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="Verify a completed paired capture.")
    if not parser.parse_args().verify_only:
        playback()
    verify()
