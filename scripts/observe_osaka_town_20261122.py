"""Navigate a copy of the original Nagasaki battery save on the current cumulative ROM."""

from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_rafael_deck_tutorial_followup_20261122 as current
from scripts.run_activity_special_live_v989 import GrowingCommands


base=current.base
ROOT=Path("work/analysis/osaka_town_gameplay_20261122")
DONOR_RECORD=Path("work/analysis/japan_facilities_v517/saved_checkpoint.json")
INPUT_REFERENCE=DONOR_RECORD.with_name("reload_inputs.json")
JOURNAL=ROOT/"navigation.jsonl"


def main():
    assert not ROOT.exists()
    latest=base.load(current.RELEASE)
    assert base.digest(current.ROM)==latest["candidate_sha256"] and base.digest(base.REGISTRY)==latest["registry_sha256"]
    save=base.load(DONOR_RECORD)
    assert save["production_cold_reload_verified_on_V518"] and base.digest(save["save"])==save["sha256"]
    inputs=base.load(INPUT_REFERENCE)[:4]
    assert [row["start"] for row in inputs]==[1601,2001,2401,2801]
    ROOT.mkdir(parents=True)
    prefix=ROOT/"inputs.json"
    base.save(prefix,inputs)
    base.save(ROOT/"source_save.json",dict(candidate_sha256=latest["candidate_sha256"],
        source=str(DONOR_RECORD),source_sha256=base.digest(DONOR_RECORD),save=save["save"],save_sha256=save["sha256"],
        input_reference=str(INPUT_REFERENCE),input_sha256=base.digest(prefix),preloaded_real_Nagasaki_battery=True))
    JOURNAL.touch(exist_ok=False)
    stream=GrowingCommands(JOURNAL)
    old_argv,old_stdin=sys.argv,sys.stdin
    try:
        sys.stdin=stream
        sys.argv=[harness.__file__,"--rom",str(current.ROM),"--out",str(ROOT/"capture"),
            "--frames","100000","--inputs-json",str(prefix),"--press-start","-1","--touchscreen",
            "--battery-save",save["save"],"--capture-every","999999","--pause-at","3650",
            "--dump-pause-ram","--dump-ram"]
        harness.main()
    finally:
        sys.argv,sys.stdin=old_argv,old_stdin
        stream.close()
    assert base.digest(save["save"])==save["sha256"]


if __name__=="__main__":
    main()

