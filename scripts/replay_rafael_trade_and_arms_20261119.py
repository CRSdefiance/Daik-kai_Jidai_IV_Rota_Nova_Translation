"""Run both trade-lesson choices and the Arms lesson in initialized emulator fixtures."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import check_rafael_voyage_ceuta_20261119 as checks
from scripts import replay_rafael_sail_controls_20261119 as prior
from scripts import review_rafael_trade_and_arms_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base = stage.base
ROOT = stage.STAGED / 'initialized_lessons'
CASES = {'trade-advice': (129, 9401), 'trade-confident': (129, 6501), 'town-arms': (140, 6501)}
STARTUP_DIR = stage.STAGED / 'own_startup'
STARTUP = stage.STAGED / 'own_startup_verification.json'


def fixture_paths(block):
    root = ROOT / f'B{block}'
    return root, root / f'Rafael_B{block}_QA_ONLY.nds', root / 'fixture.json'


def prepare():
    source = checked_text(getsource(prior.prepare), {
        "group, = staged['groups']": "group, = (row for row in staged['groups'] if row['block'] == BLOCK)",
        "group['block'] == 128": "group['block'] == BLOCK",
        'bank.blocks[128]': 'bank.blocks[BLOCK]',
        "len(speeches) == 45 and len(parsed) == 78": "len(speeches) == SPEECHES and len(parsed) == len(group['commands']) + 10",
        'ROOT.mkdir()': 'ROOT.mkdir(parents=True)',
        'stage.workflow.logical_end(lesson)': 'stage.earlier.workflow.logical_end(lesson)',
        'original_block_128_sha256': 'lesson_block_sha256',
        "print('Prepared the complete B128 interpreter path with the original Rafael initialization.')":
            "print(f'Prepared the complete B{BLOCK} path behind the original Rafael prelude.')",
    })
    for block, speeches in ((129, 14), (140, 4)):
        root, rom, manifest = fixture_paths(block)
        scope = vars(prior) | dict(ROOT=root, FIXTURE=rom, MANIFEST=manifest, stage=stage,
            BLOCK=block, SPEECHES=speeches)
        exec(compile(source, __file__ + '::prepare', 'exec'), scope)
        scope['prepare']()


def capture(name):
    block, limit = CASES[name]
    _, rom, manifest = fixture_paths(block)
    root = ROOT / name
    assert not root.exists()
    recipe = checked_text(getsource(prior.capture), {
        "    inputs = ROOT / 'ordinary_inputs.json'":
            "    if SECOND_CHOICE:\n        schedule.append(dict(start=4100, duration=5, buttons=['DOWN']))\n        schedule.sort(key=lambda row: row['start'])\n"
            "    ROOT.mkdir()\n    inputs = ROOT / 'ordinary_inputs.json'",
    })
    scope = vars(prior) | dict(ROOT=root, FIXTURE=rom, MANIFEST=manifest, FRAMES=limit,
        SECOND_CHOICE=name == 'trade-confident')
    exec(compile(recipe, __file__ + '::capture', 'exec'), scope)
    scope['capture']()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'patch', 'capture-startup', 'startup', *CASES))
    action = parser.parse_args().action
    if action == 'prepare':
        prepare()
    elif action in CASES:
        capture(action)
    else:
        scope = vars(checks) | dict(stage=stage, STARTUP=STARTUP, STARTUP_DIR=STARTUP_DIR)
        if action == 'patch':
            FunctionType(checks.patch.__code__, scope)()
        else:
            FunctionType(checks.startup.__code__, scope)(action == 'capture-startup')
