"""Visit the empty Gallery collections using the ordinary save from V307."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_alexandria_cooking_20261114 as current


base = current.base
ROOT = Path("work/gallery_empty_common_20261114_v1")
HISTORY = Path("work/emulation_v193/gallery_menu_v307/capture_report.json")
DONOR = HISTORY.parent / "saves/all_routes_combined_v307_candidate.dsv"
OWNER = Path("work/analysis/gallery_access_v306/access_proof.json")
FOCUS = {98, 99, 287, 336}


def schedule(case):
    assert case == "gallery_empty"
    prior = base.load(HISTORY)
    donor = base.load(OWNER)
    assert prior["cold_boot"] and not prior["savestate_loaded"] and not prior["callback_errors"]
    assert not prior.get("battery_save_preloaded")
    assert donor["normal_new_save_enables_title_Gallery_without_unlock_patch"]
    plan = [dict(start=1601, duration=8, buttons=["START"])]
    for frame, key in (
        (2201, "DOWN"), (2501, "DOWN"), (2801, "DOWN"), (3101, "DOWN"), (3401, "DOWN"),
        (3701, "A"), (4101, "A"), (4501, "A"), (4901, "DOWN"), (5301, "A"),
        (5701, "A"), (6101, "B"),
    ):
        plan.append(dict(start=frame, duration=8, buttons=[key]))
    return plan, [row["start"]+199 for row in plan], 6400, HISTORY, dict(source=str(DONOR),source_sha256=base.digest(DONOR))


def main():
    env = vars(playback) | dict(ROOT=ROOT, parent=current, FOCUS=FOCUS,
        observer=trace.scoped_observer, get_schedule=schedule, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary-save-and-empty-collections", "exec"), env)
    env["main"]("gallery_empty")


if __name__ == "__main__":
    main()

