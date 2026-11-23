"""Replay the ordinary Alexandria approach through the revised Listen path."""
from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_rafael_first_market_20261121 as template
from scripts import stage_hodram_alexandria_tutorial_20261121 as stage


base = stage.base
ROOT = stage.ROOT / "voyage"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
BASELINE = stage.review.arrival.REPORT
MENU, RETURN, STEP = 20640, 28120, 340


def voyage():
    stored, draft, original, coverage = map(base.load, (stage.PROOF, stage.review.OUTPUT,
                                                       BASELINE, stage.review.arrival.OUTPUT))
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    assert base.digest(BASELINE) == coverage["report_sha256"]
    assert original["ROM_sha256"] == coverage["candidate_sha256"]
    assert base.digest(stage.parent.ROM) == stored["predecessor_sha256"] == draft["previous_sha256"]
    assert original["cold_boot"] and not original["savestate_loaded"] and not original["callback_errors"]
    assert not any(value for key, value in original.items() if key.startswith("synthetic_"))
    donor = original["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    observed = {row["id"]: row for row in coverage["full_body_matches"]}
    rows = {row["id"]: row for row in draft["records"]}
    changes = {}
    for group in stored["groups"]:
        for ident, plan in group["plans"].items():
            new, old = plan["expected_native_pages"], observed[ident]["stored_pages"]
            if rows[ident]["block"] == 51 or rows[ident]["source_record_index"] < 92:
                assert new == old == 1
            changes[ident] = new - old
    returned = RETURN + STEP * sum(changes.values())
    former = [row for row in original["scripted_input_schedule"] if MENU < row["start"] <= RETURN]
    assert former == [dict(start=n, duration=8, buttons=["A"]) for n in range(MENU + 1, RETURN, STEP)]
    shared = [row for row in original["scripted_input_schedule"] if row["start"] <= MENU]
    later = [dict(start=n, duration=8, buttons=["A"]) for n in range(MENU + 1, returned, STEP)]
    frames = sorted({8980, 11020, MENU, *range(MENU + STEP, returned + 1, STEP)}
        | {row["frame"] for item in observed.values() for row in item["actual_complete_pages"] if row["frame"] < MENU})
    ROOT.mkdir()
    inputs = ROOT / "inputs.json"
    base.save(inputs, shared + later)
    base.save(ROOT / "replay_scope.json", dict(predecessor_report_sha256=base.digest(BASELINE),
        unmodified_donor_sha256=donor["source_sha256"], original_inputs_through_menu=len(shared),
        changed_pages=changes, expected_menu=MENU, expected_return=returned, horizon_adjusted_only_after_listen=True))
    harness = template.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(REPORT.parent), "--frames", str(returned),
                "--inputs-json", str(inputs), "--battery-save", donor["source"], "--press-start", "-1", "--touchscreen",
                "--dump-ram", "--capture-every", "999999", "--capture-at", *map(str, frames)]
    harness.main()
    assert base.digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("voyage", "startup", "patch"))
    case = parser.parse_args().case
    if case == "voyage":
        voyage()
    else:
        common = template.template
        action = common.common.startup if case == "startup" else common.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=common.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
