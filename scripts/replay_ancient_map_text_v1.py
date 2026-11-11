"""Replay the native Old Dagger document on the revised cumulative ROM."""

from inspect import getsource
import sys
from types import FunctionType

from scripts import probe_ancient_map_documents_v1 as original
from scripts import probe_ancient_map_documents_v4 as prior
from scripts import replay_arrival_month_labels_v1 as parent_replay
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_ancient_map_text_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
STARTUP, DISPLAY = stage.ROOT / 'own_startup', stage.ROOT / 'ancient_map'


def cold_boot():
    environment = vars(startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP,
                                       PRIOR=parent_replay.STARTUP)
    FunctionType(startup.main.__code__, environment)()


def set_condition(arm, raw, request):
    source = checked_text(getsource(original.set_condition), {
        '(item_number, map_route) == (189, 7)': '(item_number, map_route) == (189, 18)',
        'changed=changed, original_clue_getter=': 'changes=changed, original_clue_getter=',
    })
    environment = vars(original) | dict(ROM=stage.ROM)
    exec(compile(source, __file__ + '::same-four-clue-bits', 'exec'), environment)
    return environment['set_condition'](arm, raw, request)


def gameplay():
    previous = base.load(prior.ROOT / 'terminal.json')
    assert base.digest(previous['report']) == previous['report_sha256']
    assert base.digest(previous['commands']) == previous['commands_sha256']
    source = checked_text(getsource(original.main), {
        "assert base.digest(ROM) == release['candidate_sha256']":
            "assert base.digest(ROM) == expected['research_ROM_sha256']",
        "observed['ROM_sha256'] == release['candidate_sha256']":
            "observed['ROM_sha256'] == expected['research_ROM_sha256']",
        'from scripts.probe_ancient_map_documents_v1 import set_condition':
            'from scripts.replay_ancient_map_text_v1 import set_condition',
    })
    expected = base.load(stage.PROOF)
    assert expected['registered_input']['candidate_sha256'] == base.load(stage.parent.RELEASE)['candidate_sha256']
    environment = vars(original) | dict(ROOT=DISPLAY, ROM=stage.ROM, COMMANDS=prior.COMMANDS,
                                        expected=expected, __file__=__file__)
    exec(compile(source, __file__ + '::revised-ancient-map', 'exec'), environment)
    environment['main']()
    assert base.digest(DISPLAY / 'commands.jsonl') == previous['commands_sha256']


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
