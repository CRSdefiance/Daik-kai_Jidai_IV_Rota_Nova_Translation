"""Exercise the stock Hodram name editor and its original opening through ordinary inputs."""

from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_ceuta_supply_alerts_20261122 as current
from scripts.run_activity_special_live_v989 import GrowingCommands


base = current.base
ROOT = Path("work/analysis/hodram_custom_name_display_20261122")
REFERENCE = Path("work/analysis/papal_trade_route_runs_v7625/route1/ordinary_NewGame_inputs.json")
FIRST_PAUSE = 2050


def main():
    assert not ROOT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM)==release["candidate_sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(current.MANIFEST)==release["manifest_sha256"]
    initial = [e for e in base.load(REFERENCE) if e["start"] <= FIRST_PAUSE]
    assert [r["buttons"] for r in initial]==[["START"],["A"],["RIGHT"],["A"]]
    ROOT.mkdir(parents=True)
    inputs = ROOT/"inputs.json"
    base.save(inputs,initial)
    base.save(ROOT/"candidate_binding.json",dict(candidate_sha256=release["candidate_sha256"],
        manifest_sha256=release["manifest_sha256"],history=str(REFERENCE),history_sha256=base.digest(REFERENCE),
        initial_input_sha256=base.digest(inputs),real_cartridge_controls_only=True))
    journal = ROOT/"navigation.jsonl"
    journal.touch(exist_ok=False)
    previous_argv, previous_stdin = sys.argv, sys.stdin
    commands = GrowingCommands(journal)
    try:
        sys.stdin = commands
        sys.argv = [harness.__file__,"--rom",str(current.ROM),"--out",str(ROOT/"capture"),
            "--frames","40000","--inputs-json",str(inputs),"--press-start","-1","--touchscreen",
            "--capture-every","999999","--pause-at",str(FIRST_PAUSE),"--dump-pause-ram","--dump-ram"]
        harness.main()
    finally:
        sys.argv, sys.stdin = previous_argv, previous_stdin
        commands.close()


if __name__=="__main__":
    main()

