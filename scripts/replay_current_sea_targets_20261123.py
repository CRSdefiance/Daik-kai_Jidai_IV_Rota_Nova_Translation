"""Exercise each installed sea-inspection variant through the original controls."""

import sys
from argparse import ArgumentParser
from inspect import getsource
from json import dumps
from pathlib import Path

from scripts import replay_special_target_labels_20261115 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read


RELEASE = Path("releases/all_routes_editorial_20261123_cartridge_title_candidate/verification/registered_release_verification.json")
REGISTERED_NAMES = Path("releases/all_routes_editorial_20261121_stock_encounter_names_candidate/verification/registered_review.json")
HISTORY = Path("work/stock_encounter_names_20261121/ghost_settled/capture/capture_report.json")
ROOT = Path("E:/Rota Nova translations/Generated/work/current_sea_target_inspections_20261123")
CASES = {"fish": (149, "Monster Fish"), "squid": (150, "Giant Squid"), "shark": (151, "Shark"),
         "whale": (152, "Whale"), "ghost": (153, "Ghost Ship")}
FRAMES = (4800, 5400, 5600, 5700, 5950, 6300, 6750)


def replay(case, staged=False):
    model, _ = CASES[case]
    release, source, history = map(read, (RELEASE, REGISTERED_NAMES, HISTORY))
    rom = Path(release["candidate"])
    expected_sha = release["candidate_sha256"]
    assert digest(rom) == expected_sha and digest(REGISTRY) == release["registry_sha256"]
    folder = ROOT / case
    if staged:
        proof = read(ROOT / "stage/stored_proof.json")
        assert proof["predecessor"]["sha256"] == expected_sha and proof["exact_old_parent_inverse"]
        rom = Path(proof["candidate"]["path"])
        expected_sha = proof["candidate"]["sha256"]
        assert digest(rom) == expected_sha and proof["target_ARM9_sha256"] == release["target_ARM9_sha256"]
        folder = ROOT / "stage/focused" / case
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert history["frames"] == FRAMES[-1] and history["ROM_sha256"] == source["candidate_sha256"]
    donor = history["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    row, = (entry for entry in source["records"] if entry["model_ID"] == model)
    label = row["english"].encode("ascii")
    assert row["class_ID"] == model - 115 and row["review"]["formatting"]
    body = checked_text(getsource(prior.special_target), {
        "model in (149, 153)": "149 <= model <= 153",
        "34 if model == 149 else 38": "model - 115",
        "'化魚'.encode('cp932') if model == 149 else b'Ghost'": "INSTALLED_LABEL",
    })
    env = vars(prior) | dict(INSTALLED_LABEL=label, __file__=__file__)
    exec(compile(body, __file__ + "::stock-model-scope", "exec"), env)
    folder.mkdir(parents=True)
    inputs, commands = folder / "inputs.json", folder / "commands.jsonl"
    schedule = history["scripted_input_schedule"]
    inputs.write_text(dumps(schedule), encoding="utf-8")
    commands.write_text("".join(dumps(entry) + "\n" for entry in (
        dict(until=5700, condition_fixture=prior.previous.REQUEST), dict(until=FRAMES[-1]), dict(stop=True)
    )), encoding="utf-8")
    args = [prior.harness.__file__, "--rom", str(rom), "--out", str(folder / "capture"),
        "--frames", str(FRAMES[-1] + 1), "--inputs-json", str(inputs), "--press-start", "-1", "--touchscreen",
        "--battery-save", donor["source"], "--capture-every", "999999", "--capture-at", *map(str, FRAMES),
        "--pause-at", "4800", "--dump-pause-ram", "--allow-condition-fixtures"]
    stream = prior.GrowingCommands(commands)
    stdin, argv, fixture = sys.stdin, sys.argv, prior.adapter.set_condition
    try:
        sys.stdin, sys.argv = stream, args
        prior.adapter.set_condition = lambda arm, raw, request: env["special_target"](
            rom, release["target_ARM9_sha256"], model, arm, raw, request)
        prior.harness.main()
    finally:
        sys.stdin, sys.argv, prior.adapter.set_condition = stdin, argv, fixture
        stream.close()
    report = read(folder / "capture/capture_report.json")
    assert report["ROM_sha256"] == expected_sha and report["frames"] == FRAMES[-1]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == schedule
    result, = report["synthetic_condition_fixtures"]
    assert result["original_existing_model_ID"] == model and result["original_class_ID"] == model - 115
    assert result["all_other4MiB_bytes_exact"] and result["target_model_link_fixture"] == (model != 149)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("model", choices=tuple(CASES))
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    replay(args.model, args.staged)
