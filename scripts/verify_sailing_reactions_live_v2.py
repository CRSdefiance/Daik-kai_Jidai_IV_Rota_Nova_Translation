"""Verify the complete focused sailing replay on the exact staged ROM."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_sailing_reactions_v3 as fixture
from scripts import verify_sailing_reactions_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    replay = SimpleNamespace(ROOT=fixture.DISMISS_ROOT, END=fixture.DISMISS_END,
        COMMANDS=fixture.DISMISS_COMMANDS, PAUSE=fixture.precedent.PAUSE, set_condition=fixture.set_condition)
    source = checked_text(getsource(prior.verify_live), {
        '    wind, first, second = observed':
            '    wind, first, second = observed\n'
            '    assert (first["frame"], second["frame"]) == (11600, 11800)\n'
            '    assert applied[1]["fixture_initial_age_ticks"] == 120',
        'journal_path, QA, Path(__file__))':
            'journal_path, QA, Path(prior.__file__), replay_driver, Path(__file__))',
    })
    env = vars(prior) | globals() | {'replay': replay, 'replay_driver': Path(fixture.__file__)}
    exec(compile(source, __file__ + '::complete-live-verification', 'exec'), env)
    env['verify_live']()


if __name__ == '__main__':
    main()
