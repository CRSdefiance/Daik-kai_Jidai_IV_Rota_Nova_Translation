"""Replay the verified Cristina Deck fixture on the staged Lounge wording."""

from argparse import ArgumentParser
from inspect import getsource
from io import StringIO
from pathlib import Path
import sys
from types import FunctionType

from scripts import native_battle_fixture_v620 as dispatch
from scripts import native_physical_fatigue_fixture_v963 as early
from scripts import native_physical_fatigue_fixture_v964 as late
from scripts import native_physical_fatigue_standoff_v963 as approach
from scripts import run_physical_fatigue_adapter_v964 as adapter
from scripts import stage_ship_room_names_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base,native=stage.base,stage.native
HISTORICAL=Path("work/analysis/physical_fatigue_v964")
ROOT=stage.ROOT/"deck_gameplay_retry"
REPORT=ROOT/"capture/capture_report.json"
PROOF=ROOT/"verified_deck_gameplay.json"


def play():
    assert not ROOT.exists()
    source=base.load(HISTORICAL/"CristinaFatigue_run_plan.json")
    donor=source["source_donor"]
    assert base.digest(donor)==source["source_donor_sha256"]
    assert base.digest(source["inputs"])==source["inputs_sha256"]
    commands=HISTORICAL/"CristinaFatigue_navigation.jsonl"
    proof=base.load(stage.PROOF)
    assert proof["candidate_sha256"]==base.digest(stage.ROM)
    arm=base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    assert proof["stored_components"][stage.ARM]==native.digest(arm)
    expected="translations/physical_fatigue_editorial_release_v1.json"

    def config(path):
        assert path==expected
        return {"target_arm9_sha256":native.digest(arm)}

    ROOT.mkdir()
    base.save(ROOT/"replay_inputs.json",dict(source_plan=str(HISTORICAL/"CristinaFatigue_run_plan.json"),
        donor=donor,donor_sha256=source["source_donor_sha256"],instructions=str(commands),instructions_sha256=base.digest(commands),
        original_input_prefix=source["inputs"],input_prefix_sha256=source["inputs_sha256"],candidate_sha256=proof["candidate_sha256"]))
    original=[early.assign,late.assign,dispatch.apply_fixture,sys.argv,sys.stdin]
    early.assign=FunctionType(early.assign.__code__,early.assign.__globals__|{"read":config})
    late.assign=FunctionType(late.assign.__code__,late.assign.__globals__|{"read":config})
    diagnostic=base.load(stage.ROOT/"deck_replay_fleet_identity/fleet_identity.json")
    assert diagnostic["candidate_sha256"]==proof["candidate_sha256"] and diagnostic["frame"]==4801
    hodram,speyer=diagnostic["original_getters"]
    assert (hodram["fleet"],hodram["player_owned"],speyer["fleet"],speyer["player_owned"])==(1,1,5,0)
    assert (hodram["full_name"],speyer["full_name"])==("Hodram Fleet","Speyer Co. Fleet １")
    current_fixture=checked_text(getsource(approach.source.apply_fixture),{
        'names[1].startswith(\'Speyer Co.Fleet \')':'names[1].startswith(\'Speyer Co. Fleet \')',
    })
    current_approach=checked_text(getsource(approach.apply_fixture),{
        "text=inspect.getsource(source.apply_fixture)":"text=CURRENT_FLEET_PRODUCER",
    })
    scope=approach.apply_fixture.__globals__|{"read":config,"ROM":stage.ROM,"CURRENT_FLEET_PRODUCER":current_fixture}
    exec(compile(current_approach,__file__+"::observed-fleet-spellings","exec"),scope)
    dispatch.apply_fixture=scope["apply_fixture"]
    try:
        sys.stdin=StringIO(commands.read_text(encoding="utf-8"))
        sys.argv=["headless_desmume_v193.py","--rom",str(stage.ROM),"--out",str(ROOT/"capture"),"--frames","16901",
            "--inputs-json",source["inputs"],"--touchscreen","--capture-every","999999","--capture-at","15300","16300","16500","16700","16900",
            "--battery-save",donor,"--pause-at","4800","--dump-capture-ram","--allow-battle-fixtures","--allow-physical-fatigue-fixtures"]
        adapter.main()
    finally:
        early.assign,late.assign,dispatch.apply_fixture,sys.argv,sys.stdin=original
    assert base.digest(donor)==source["source_donor_sha256"]


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("play",))
    globals()[parser.parse_args().action]()

