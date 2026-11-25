"""Observe both confirmation directions and returns for Sailing Help."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_maria_B18_B20_20261122 as current


ROOT = Path("work/analysis/shared_settings_20261122")
KEYS = (
    (1601, "START"), (2001, "DOWN"), (2401, "A"),
    (2801, "DOWN"), (3201, "DOWN"), (3601, "A"),
    (4001, "A"), (4401, "A"), (4801, "A"),
    (5201, "A"), (5601, "B"), (6001, "B"),
)
FOCUS = {100, 101, 102, 103, 330, 331, 332, 333}


def schedule(case):
    assert case == "sailing_help"
    events = [dict(start=frame, duration=8, buttons=[key]) for frame,key in KEYS]
    return events, [frame+199 for frame,_ in KEYS[2:]], 6250, None, None


def main():
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, FOCUS=FOCUS, observer=trace.scoped_observer,
        get_schedule=schedule, __file__=__file__)
    exec(compile(getsource(playback.main), __file__+"::Sailing Help controls", "exec"), scope)
    scope["main"]("sailing_help")


if __name__ == "__main__":
    main()

