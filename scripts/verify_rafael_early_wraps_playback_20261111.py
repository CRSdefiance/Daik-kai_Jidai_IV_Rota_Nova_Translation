"""Compare both emulator replays at the same scene state after the page count changes."""

from inspect import getsource
from pathlib import Path

from scripts import replay_rafael_early_wraps_20261111 as replay
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(getsource(replay.verify), {
        "for frame in (2100, 7800, 8000)": "for frame in equivalent_frames[side]",
        "outside_exact_frames=[2100,7800,8000]":
            'outside_exact_frames=equivalent_frames, post_scene_input_schedule_diverges=True',
        "{str(SETUP): base.digest(SETUP)}":
            "{str(path): base.digest(path) for path in (SETUP, Path(__file__), Path(replay.__file__))}",
    })
    # One fewer text page returns to town one A press earlier.
    # Compare the actual town return before later A presses select other menus.
    env = vars(replay) | dict(equivalent_frames={'before': (2100, 6270, 6330), 'after': (2100, 6010, 6070)},
                              __file__=__file__, replay=replay, Path=Path)
    exec(compile(source, __file__ + '::equivalent-town-state', 'exec'), env)
    env['verify']()


if __name__ == '__main__':
    main()
