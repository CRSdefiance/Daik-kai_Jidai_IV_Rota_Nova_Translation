"""Observe COMMON requests on a mixed purchase and sale that is cancelled in Syracuse."""

from types import FunctionType

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as native
from scripts import register_lisbon_roster_galley_20261124 as current
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read
from scripts.verify_syracuse_local_purchase_20261124 import OUT as PREVIOUS


ROOT = current.build.ROOT.with_name("editorial_20261124_syracuse_mixed_trade")
CASE = "mixed_cancel"
SPLIT = 16900
FRAMES = (16100, 16500, 16900, 17340, 17700, 18100, 18500, 18900, 19300)
END = FRAMES[-1] + 1


def schedule(case):
    assert case == CASE
    refs = read(PREVIOUS)["evidence"]
    before = refs["capture"]
    assert digest(before["path"]) == before["sha256"]
    report = read(before["path"])
    donor = report["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == refs["donor"]["sha256"]
    events = [row for row in report["scripted_input_schedule"] if row["start"] <= SPLIT]
    # Keep the staged sale and select Wheat from the Local grid directly.
    events.extend(dict(start=frame, duration=8, buttons=[], touch=position)
                  for frame, position in ((17301, [96, 105]), (17309, [128, 54])))
    events.extend(dict(start=frame, duration=8, buttons=[key])
                  for frame, key in ((17701, "X"), (18101, "B"), (18501, "B"), (18901, "A")))
    return events, FRAMES, END, PREVIOUS, donor


if __name__ == "__main__":
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    settings = vars(playback) | dict(ROOT=ROOT, parent=current, observer=native.scoped_observer,
                                    get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    FunctionType(playback.main.__code__, settings)(CASE)
