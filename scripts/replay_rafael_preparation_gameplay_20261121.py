"""Play through Rafael's loan, appointment and preparation choice from New Game."""
from pathlib import Path
import sys

from scripts import register_rafael_harbor_exchange_20261121 as active
from scripts import replay_rafael_harbor_exchange_20261121 as opening
from scripts.replay_amsterdam_bread_20261121 import GrowingCommands
from scripts import headless_desmume_v193 as harness


base=active.base
ROOT=Path("out/rafael_preparation_gameplay_20261121")
ADVANCE=tuple(9450+230*i for i in range(85))
PAUSE=ADVANCE[-1]+215


def main():
    assert not ROOT.exists()
    release=base.load(active.RELEASE)
    assert base.digest(active.ROM)==release["candidate_sha256"] and base.digest(base.REGISTRY)==release["registry_sha256"]
    previous=base.load(opening.REPORT)
    verified=base.load(opening.ROOT/"verified_harbor.json")
    assert base.digest(opening.REPORT)==verified["evidence"][str(opening.REPORT)]
    assert previous["ROM_sha256"]==verified["candidate_sha256"]==release["candidate_sha256"]
    events=previous["scripted_input_schedule"]+[dict(start=n,duration=8,buttons=["A"]) for n in ADVANCE]
    ROOT.mkdir()
    timeline,commands=ROOT/"inputs.json",ROOT/"navigation.jsonl"
    base.save(timeline,events)
    commands.touch(exist_ok=False)
    channel=GrowingCommands(commands)
    argv,stdin=sys.argv,sys.stdin
    try:
        sys.stdin=channel
        frames=[9191,*[n+200 for n in ADVANCE]]
        sys.argv=[harness.__file__,"--rom",str(active.ROM),"--out",str(ROOT/"capture"),
            "--frames","45000","--inputs-json",str(timeline),"--press-start","-1",
            "--capture-every","999999","--dump-ram","--capture-at",*map(str,frames),"--pause-at",str(PAUSE)]
        harness.main()
    finally:
        channel.close()
        sys.argv,sys.stdin=argv,stdin


if __name__=="__main__":
    main()
