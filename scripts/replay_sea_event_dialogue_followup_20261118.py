"""Replay the known Maria startup and original foam dialogue on the staged ROM."""

import argparse
from inspect import getsource
from pathlib import Path
from shutil import copyfile
import subprocess
import sys
from types import FunctionType

from scripts import run_sea_event_bubbles_focused_v2 as historical
from scripts import stage_sea_event_dialogue_followup_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base = stage.base
STARTUP = stage.ROOT / "startup_fixture"
LIVE = Path("work/sea_wrap_bubbles_v3")
set_condition = FunctionType(historical.set_condition.__code__, vars(historical) | {"ROM": stage.ROM})


def gameplay():
    staged = base.load(stage.PROOF)
    alias = LIVE / "SeaWrap.nds"
    LIVE.mkdir()
    copyfile(stage.ROM, alias)
    assert base.digest(alias) == staged["candidate_sha256"]
    source = checked_text(getsource(historical.main), {
        "staged['research_ROM_sha256']": "staged['candidate_sha256']",
        "    OUT.mkdir()\n": "",
        "    first = dict(until=8727, condition_fixture={'mode': 'choose-bubbles'}, buttons=['UP'], duration=400)\n"
        "    navigation.write_text(json.dumps(first) + '\\n', encoding='utf-8')":
        "    navigation.write_bytes(HISTORICAL_COMMANDS.read_bytes())",
        "'from scripts.run_sea_event_bubbles_focused_v2 import set_condition'":
        "'from scripts.replay_sea_event_dialogue_followup_20261118 import set_condition'",
    })
    env = vars(historical) | dict(OUT=LIVE, ROM=alias, EVIDENCE=stage.PROOF,
        HISTORICAL_COMMANDS=historical.OUT / "commands.jsonl")
    exec(compile(source, __file__ + "::gameplay", "exec"), env)
    env["main"]()


def startup():
    release = base.load(stage.parent.RELEASE)
    before = base.load(release["own_registered_startup"])
    parent_capture = Path(before["read_only_snapshot"]["path"]).parent
    old = parent_capture / "capture_report.json"
    prior = base.load(old)
    assert prior["ROM_sha256"] == release["candidate_sha256"] and prior["frames"] == 31000
    prior_args = base.load(parent_capture.parent / "worker_argv.json")
    args = prior_args[:]
    flag = "--gallery-save-fixture-manifest"
    fixture_path = Path(args[args.index(flag) + 1])
    fixture = base.load(fixture_path)
    assert fixture["production_ROM_sha256"] == release["candidate_sha256"]
    assert base.digest(fixture["fixture_save"]) == fixture["fixture_save_sha256"]
    STARTUP.mkdir()
    manifest = STARTUP / "system_unlock_manifest.json"
    base.save(manifest, fixture | dict(production_ROM=str(stage.ROM),
        production_ROM_sha256=base.digest(stage.ROM),
        current_test_scope="Maria startup with the established system-only unlock."))
    for key, path in (("--rom", stage.ROM), ("--out", STARTUP / "capture"), (flag, manifest)):
        args[args.index(key) + 1] = str(path)
    base.save(STARTUP / "worker_argv.json", args)
    subprocess.run([sys.executable, "-m", "scripts.headless_desmume_v193", *args], check=True)
    assert base.digest(fixture["fixture_save"]) == fixture["fixture_save_sha256"]
    base.save(STARTUP / "basis.json", dict(previous_report=str(old), previous_report_sha256=base.digest(old),
        manifest=str(manifest), manifest_sha256=base.digest(manifest)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
