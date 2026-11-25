"""Cold-boot the candidate and replay the native whale warning and departure."""

from inspect import getsource
from json import loads
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_crew_and_shore_reports_v1 as prior
from scripts import replay_sailing_reactions_v1 as original
from scripts import replay_sailing_reactions_v3 as aged
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_oasis_and_whale_reports_v1 as candidate
from scripts.source_locked_derivation_v5118 import checked_text


base = prior.base
stage = SimpleNamespace(ROOT=candidate.ROOT, ROM=candidate.ROM, PROOF=candidate.PROOF,
    ARM=candidate.review.ARM, CLEAN=candidate.review.CLEAN, BASE=candidate.review.BASE,
    NdsImage=base.NdsImage, base=base)
STARTUP = stage.ROOT / 'own_startup'
RUNS = {'warning': (original.ROOT, 11400), 'escape': (aged.DISMISS_ROOT, aged.DISMISS_END)}


def cold_boot():
    env = vars(startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=prior.STARTUP)
    FunctionType(startup.main.__code__, env)()


def set_condition(arm, raw, request):
    return FunctionType(original.set_condition.__code__, vars(original) | {'stage': stage})(arm, raw, request)


def set_aged_condition(arm, raw, request):
    env = vars(aged) | dict(stage=stage, precedent=SimpleNamespace(set_condition=set_condition))
    return FunctionType(aged.set_condition.__code__, env)(arm, raw, request)


def gameplay(scenario):
    old_root, end = RUNS[scenario]
    terminal = base.load(old_root / 'terminal.json')
    previous_commands, report_path = Path(terminal['commands']), Path(terminal['report'])
    assert base.digest(previous_commands) == terminal['commands_sha256']
    assert base.digest(report_path) == terminal['report_sha256']
    old_report = base.load(report_path)
    assert old_report['cold_boot'] and not old_report['savestate_loaded'] and not old_report['callback_errors']
    commands = [loads(line) for line in previous_commands.read_text(encoding='utf-8').splitlines()]
    commands = [row for row in commands if row.get('until', end + 1) <= end] + [dict(stop=True)]
    assert commands[-2]['until'] == end
    method = 'set_condition' if scenario == 'warning' else 'set_aged_condition as set_condition'
    source = checked_text(getsource(original.gameplay), {
        'from scripts.replay_sailing_reactions_v1 import set_condition':
            f'from scripts.replay_oasis_and_whale_reports_v1 import {method}',
    })
    env = vars(original) | dict(stage=stage, ROOT=stage.ROOT / f'whale_{scenario}', END=end, COMMANDS=commands)
    exec(compile(source, __file__ + '::verified-whale-inputs', 'exec'), env)
    env['gameplay']()


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['warning'], ['escape'])
    if sys.argv[1] == 'startup':
        cold_boot()
    else:
        gameplay(sys.argv[1])
