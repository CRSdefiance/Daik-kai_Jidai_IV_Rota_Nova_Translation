"""Observe revised harbor and loan dialogue through the regular New Game entry."""

from argparse import ArgumentParser
import sys

from scripts import check_rafael_B84_training_gameplay_20261122 as visual
from scripts import headless_desmume_v193 as harness
from scripts import replay_rafael_preparation_gameplay_20261121 as prior
from scripts import stage_rafael_proof_and_financing_20261122 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "ordinary_lisbon_opening"
REPORT = ROOT / "capture/capture_report.json"
OUTPUT = ROOT / "verified_opening.json"
PRIOR_REPORT = prior.ROOT / "capture/capture_report.json"
PRIOR_REVIEW = prior.ROOT / "verified_preparation.json"
END = 14301
FRAMES = tuple(range(4500, 13601, 100)) + (13690, 13790, 13890, 13990, 14090, 14190, 14290)
SELECTED = tuple(f"DK4_MES_B44_R{number:04d}" for number in (13, 17, 103, 163))


def replay():
    source, evidence, stored = map(base.load, (PRIOR_REPORT, PRIOR_REVIEW, stage.PROOF))
    assert base.digest(PRIOR_REPORT) == evidence["report_sha256"]
    assert evidence["candidate_sha256"] == source["ROM_sha256"] and evidence["ordinary_new_game"]
    assert stored["candidate_sha256"] == base.digest(stage.ROM)
    assert source["cold_boot"] and not source.get("battery_save_preloaded")
    assert not source["savestate_loaded"] and not source["callback_errors"]
    inputs = [row for row in source["scripted_input_schedule"] if row["start"] < END]
    ROOT.mkdir()
    plan = ROOT / "inputs.json"
    base.save(plan, inputs)
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(REPORT.parent),
        "--frames", str(END), "--inputs-json", str(plan), "--press-start", "-1",
        "--capture-every", "999999", "--capture-at", *map(str, FRAMES)]
    harness.main()


def verify():
    report, display, draft = map(base.load, (REPORT, stage.NATIVE, stage.REVIEW))
    candidate = base.digest(stage.ROM)
    assert report["ROM_sha256"] == display["candidate_sha256"] == candidate
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and not any(
        value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(ROOT / "inputs.json")
    names = visual.GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(native.ARM))
    labels = {r["id"]: r["speaker"] for r in draft["records"]}
    stored = {r["id"]: r for r in display["records"] if r["id"] in SELECTED}
    captures = [(frame, *visual.screen(report, frame)) for frame in FRAMES]
    matched, missed, pictures = [], [], []
    for ident in SELECTED:
        check = stored[ident]
        page, = check["layouts"][0]["pages"]
        for frame, receipt, pixels in captures:
            try:
                if not visual.mask_check(bytes.fromhex(page["native_plane_hex"]), 216, pixels):
                    continue
                visual.glyphs(names, pixels, labels[ident], (16,277), visual.LABEL_COLOR, 226)
            except AssertionError:
                continue
            matched.append(dict(id=ident, frame=frame, capture=receipt, speaker=labels[ident],
                exact_candidate_command_hex=check["exact_command_hex"]))
            pictures.append((ident+" / "+labels[ident], pixels))
            break
        else:
            missed.append(ident)
    assert matched
    assert [r["frame"] for r in matched] == sorted(r["frame"] for r in matched)
    path, digest = visual.make_sheet(ROOT / "ordinary_opening_review.png", pictures)
    base.save(OUTPUT, dict(candidate_sha256=candidate, ordinary_new_game=True, synthetic_fixture=False,
        report=str(REPORT), report_sha256=base.digest(REPORT), observations=matched, unobserved=missed,
        focused_show_all_elsewhere=True, hardware=False, sheets=[dict(path=path, sha256=digest)]))
    print(f"Observed {len(matched)} revised native panels in regular New Game play. Unobserved: {missed}")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay","verify"))
    globals()[cli.parse_args().action]()
