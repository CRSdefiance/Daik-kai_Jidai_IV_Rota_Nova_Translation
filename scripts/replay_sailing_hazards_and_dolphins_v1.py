"""Cold-boot the candidate and replay the native dolphin log exchange."""

from inspect import getsource
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_sailing_reactions_v1 as precedent
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_sailing_hazards_and_dolphins_v1 as candidate
from scripts import verify_oasis_and_whale_reports_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base = candidate.review.parent.base
stage = SimpleNamespace(ROOT=candidate.ROOT, ROM=candidate.ROM, PROOF=candidate.PROOF,
    ARM=candidate.ARM, CLEAN=candidate.review.CLEAN, BASE=candidate.BASE,
    NdsImage=base.NdsImage, base=base)
STARTUP = stage.ROOT / 'own_startup'
DOLPHINS = stage.ROOT / 'dolphin_log'
END = 12800
COMMANDS = (
    dict(until=8750, condition_fixture={'event': 'dolphins'}, buttons=['UP'], duration=400),
    dict(until=8950, buttons=['A'], duration=8),
    dict(until=9150, buttons=['A'], duration=8),
    dict(until=10450, buttons=['UP'], duration=950),
    dict(until=11200, buttons=['UP'], duration=700),
    dict(until=11950, buttons=['UP'], duration=700),
    dict(until=12200, buttons=['A'], duration=8),
    dict(until=12500, buttons=['A'], duration=8),
    dict(until=END, buttons=[], duration=8),
    dict(stop=True),
)


def cold_boot():
    environment = vars(startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP,
                                      PRIOR=previous.replay.STARTUP)
    FunctionType(startup.main.__code__, environment)()


def set_condition(arm, raw, request):
    source = checked_text(getsource(precedent.set_condition), {
        "event in ('wind', 'whale')": "event == 'dolphins'",
        "{'wind': 24, 'whale': 11}[event]": "{'dolphins': 12}[event]",
    })
    environment = vars(precedent) | {'stage': stage}
    exec(compile(source, __file__ + '::focused-dolphin-condition', 'exec'), environment)
    return environment['set_condition'](arm, raw, request)


def gameplay():
    source = checked_text(getsource(precedent.gameplay), {
        'from scripts.replay_sailing_reactions_v1 import set_condition':
            'from scripts.replay_sailing_hazards_and_dolphins_v1 import set_condition',
    })
    environment = vars(precedent) | dict(stage=stage, ROOT=DOLPHINS, END=END, COMMANDS=COMMANDS)
    exec(compile(source, __file__ + '::dolphin-log-replay', 'exec'), environment)
    environment['gameplay']()


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
