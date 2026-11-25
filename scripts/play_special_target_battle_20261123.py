"""Cold-boot the registered ROM with an existing sea target and recorded controls."""

import argparse
import sys
from inspect import getsource
from json import dumps
from pathlib import Path

from scripts import replay_current_sea_targets_20261123 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, sha256


RELEASE = Path("releases/all_routes_editorial_20261123_sea_inspection_prose_candidate/verification/registered_release_verification.json")
PREDECESSOR = Path("releases/all_routes_editorial_20261123_cartridge_title_candidate/verification/registered_release_verification.json")
ROOT = Path("E:/Rota Nova translations/Generated/work/special_target_battle_20261123")


def play(case, label, replay=None, control=None):
    assert label.isascii() and label.replace("_", "").isalnum()
    source, release = map(previous.read, (previous.HISTORY, RELEASE))
    rom = Path(release["candidate"])
    assert previous.digest(rom) == release["candidate_sha256"]
    assert previous.digest(previous.REGISTRY) == release["registry_sha256"]
    donor = source["battery_save_preloaded"]
    assert previous.digest(donor["source"]) == donor["source_sha256"]
    model, _ = previous.CASES[case]
    approved = previous.read(previous.REGISTERED_NAMES)
    name, = [row for row in approved["records"] if row["model_ID"] == model]
    candidate_sha, arm_sha = release["candidate_sha256"], release["target_ARM9_sha256"]
    encoded = name["english"].encode("ascii")
    if control == "predecessor":
        parent = previous.read(PREDECESSOR)
        rom, candidate_sha = Path(parent["candidate"]), parent["candidate_sha256"]
        assert replay is not None and previous.digest(rom) == candidate_sha
        assert release["predecessor"]["candidate_sha256"] == candidate_sha
        assert parent["target_ARM9_sha256"] == arm_sha
    if control == "clean":
        assert replay is not None and previous.digest(CLEAN) == release["clean_input_sha256"]
        rom, candidate_sha = CLEAN, release["clean_input_sha256"]
        arm_sha = sha256(NdsImage.open(CLEAN).read_file("/__arm9__.bin")).hexdigest()
        encoded = name["clean_Japanese"].encode("cp932")
    body = checked_text(getsource(previous.prior.special_target), {
        "model in (149, 153)": "149 <= model <= 153",
        "34 if model == 149 else 38": "model - 115",
        "'化魚'.encode('cp932') if model == 149 else b'Ghost'": "INSTALLED_LABEL",
    })
    env = vars(previous.prior) | dict(INSTALLED_LABEL=encoded, __file__=__file__)
    exec(compile(body, __file__ + "::stock-model-scope", "exec"), env)
    work = ROOT / label
    work.mkdir(parents=True)
    commands, inputs = work / "controller.jsonl", work / "startup_inputs.json"
    initial = (replay.read_text(encoding="utf-8") if replay is not None else
               dumps(dict(until=6750, condition_fixture=previous.prior.previous.REQUEST)) + "\n")
    commands.write_text(initial, encoding="utf-8")
    inputs.write_text(dumps(source["scripted_input_schedule"]), encoding="utf-8")
    harness = previous.prior.harness
    stream = previous.prior.GrowingCommands(commands)
    old_argv, old_stdin, old_fixture = sys.argv, sys.stdin, previous.prior.adapter.set_condition
    try:
        sys.stdin = stream
        previous.prior.adapter.set_condition = lambda arm, raw, request: env["special_target"](
            rom, arm_sha, model, arm, raw, request)
        sys.argv = [harness.__file__, "--rom", str(rom), "--out", str(work / "capture"),
            "--frames", "90000", "--inputs-json", str(inputs), "--press-start", "-1", "--touchscreen",
            "--battery-save", donor["source"], "--capture-every", "999999", "--pause-at", "4800",
            "--dump-pause-ram", "--allow-condition-fixtures"]
        harness.main()
    finally:
        sys.argv, sys.stdin, previous.prior.adapter.set_condition = old_argv, old_stdin, old_fixture
        stream.close()
    report = previous.read(work / "capture/capture_report.json")
    fixtures = [key for key, value in report.items() if key.startswith("synthetic_") and value]
    assert fixtures == ["synthetic_condition_fixtures"]
    fixture, = report[fixtures[0]]
    assert fixture["frame"] == 4800 and fixture["original_existing_model_ID"] == model
    assert report["ROM_sha256"] == candidate_sha and not report["callback_errors"]
    assert previous.digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", choices=tuple(previous.CASES))
    parser.add_argument("run_label")
    parser.add_argument("--replay", type=Path)
    controls = parser.add_mutually_exclusive_group()
    controls.add_argument("--clean-control", dest="control", action="store_const", const="clean")
    controls.add_argument("--predecessor-control", dest="control", action="store_const", const="predecessor")
    args = parser.parse_args()
    play(args.model, args.run_label, args.replay, args.control)
