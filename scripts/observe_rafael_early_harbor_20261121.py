"""Observe Rafael's full early harbor exchange on the current testing ROM."""
from pathlib import Path
from types import FunctionType

from scripts import observe_opening_scene_labels_20261115 as history
from scripts import observe_online_gallery_common_v1 as replay
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_stockholm_dialogue_followup_20261121 as active


base = active.base
ROOT = Path("out/rafael_early_harbor_gameplay_20261121")
END = 9300


def schedule(_case):
    first, representative, _, input_file, donor = history.schedule("rafael")
    assert donor is None
    keys = [dict(start=n,duration=8,buttons=["A"]) for n in range(3361,END-230,310)]
    frames = sorted(set(representative) | set(range(2300,END,110)) |
                    {row["start"]+250 for row in keys})
    return first+keys,frames,END,input_file,None


if __name__ == "__main__":
    release=base.load(active.RELEASE)
    assert base.digest(active.ROM)==release["candidate_sha256"] and base.digest(base.REGISTRY)==release["registry_sha256"]
    run=FunctionType(replay.main.__code__,vars(replay)|dict(ROOT=ROOT,parent=active,
        observer=trace.scoped_observer,get_schedule=schedule,FOCUS={3393,3394,3395,3396,3397,3398},__file__=__file__))
    run("rafael")
