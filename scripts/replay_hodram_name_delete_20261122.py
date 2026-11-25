"""Replay the exact ordinary Hodram editor controls on the deletion candidate."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from scripts import observe_hodram_custom_names_20261122 as original
from scripts import stage_captain_name_delete_20261122 as staged


base = original.base
ROOT = staged.ROOT/"ordinary_editor"
REPORT=ROOT/"capture/capture_report.json"
FRAMES=(2050,2790,3870,6270,6570,6690,7170,7410,8900,12260,14300,14520)
END = FRAMES[-1] + 1


def main():
    assert not ROOT.exists()
    proof,baseline=map(base.load,(staged.PROOF,staged.BASELINE))
    assert base.digest(staged.ROM)==proof["candidate_sha256"]
    assert baseline["ROM_sha256"]==proof["predecessor_sha256"]==base.digest(original.current.ROM)
    assert baseline["cold_boot"] and not baseline["savestate_loaded"] and not baseline.get("battery_save_preloaded")
    assert not baseline["callback_errors"] and not any(v for k,v in baseline.items() if k.startswith("synthetic_"))
    recorded = [e for e in baseline["scripted_input_schedule"] if e["start"]<END]
    ROOT.mkdir()
    inputs=ROOT/"inputs.json"
    base.save(inputs,recorded)
    argv=sys.argv
    try:
        sys.argv=[original.harness.__file__,"--rom",str(staged.ROM),"--out",str(REPORT.parent),"--frames",str(END),
            "--inputs-json",str(inputs),"--press-start","-1","--touchscreen","--capture-every","999999",
            "--dump-capture-ram","--capture-at",*map(str,FRAMES)]
        original.harness.main()
    finally:
        sys.argv=argv


if __name__=="__main__":
    main()

