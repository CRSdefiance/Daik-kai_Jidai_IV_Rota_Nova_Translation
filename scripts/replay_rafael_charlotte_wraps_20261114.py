"""Verify representative revised speeches and transitions on the current cumulative build."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_early_wraps_20261111 as previous
from scripts import stage_rafael_charlotte_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_charlotte_wraps_20261114_v1')
ROM = ROOT / 'rafael_charlotte_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_charlotte_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
EXCERPTS = (
    (63, 88, 254, (0x4000,) * 4),
    (63, 962, 1174, (0x4000,) * 2),
    (70, 1442, 1548, (0x4000,) * 2),
)
REVISED_IDS = ('DK4_MES_B63_R0014', 'DK4_MES_B63_R0092', 'DK4_MES_B70_R0174')
FOLLOWING_IDS = ('DK4_MES_B63_R0018', 'DK4_MES_B63_R0095', 'DK4_MES_B70_R0178')
PLAY_ORDER = tuple(item for group in zip(REVISED_IDS, FOLLOWING_IDS, strict=True) for item in group)
fixture_env = vars(previous) | globals()
read_excerpts = FunctionType(previous.read_excerpts.__code__, fixture_env)
fixture_env['read_excerpts'] = read_excerpts
capture = FunctionType(previous.capture.__code__, fixture_env)


def derived(function, changes, values=None):
    env = fixture_env | (values or {})
    source = checked_text(getsource(function), changes)
    exec(compile(source, __file__ + '::existing-native-replay-contract', 'exec'), env)
    return env[function.__name__]


prepare = derived(previous.prepare, {
    'Original command excerpts placed at initialized Lil entry. B60 branch body is replayed without its outer condition.':
        'Original Rafael speech commands placed at initialized Lil entry. Natural story triggers are outside this replay.',
})
verify = derived(previous.verify, {
    "    assert [len(observed[side]['DK4_MES_B52_R0018']) for side in ('before','after')] == [2, 1]\n"
    "    assert [len(observed[side]['DK4_MES_B60_R0399']) for side in ('before','after')] == [2, 2]":
        "    assert all(len(shown[key]) == 1 for shown in observed.values() for key in PLAY_ORDER)",
    'verified_albuquerque_pages=[2,1], verified_pereira_pages=[2,2], evidence=evidence':
        'verified_revised_pages=len(REVISED_IDS), verified_following_pages=len(FOLLOWING_IDS), evidence=evidence',
    'Matched B42’s revised questions, the B52 two-to-one page change, B60’s two pages, and both following replies.':
        'Matched three revised speeches and their original following replies.',
})
startup = derived(previous.startup, {
    "PRIOR=parent_replay.ROOT / 'own_startup'": "PRIOR=stage.parent.stage.ROOT / 'own_startup'",
    'BIOGRAPHIES=parent_replay.ROOT': 'BIOGRAPHIES=stage.parent.stage.ROOT',
})


def verify_storage():
    draft = base.load(stage.REVIEW)
    expected_count = len(draft['records'])
    adapter = SimpleNamespace(**(vars(stage.prior) | vars(stage)))
    source = checked_text(getsource(previous.storage.main), {
        'assert len(matches)==12': f'assert len(matches)=={expected_count}',
        '12 unchanged native boundaries and before/after catalog misses on all four routes verified.':
            f'{expected_count} Rafael command boundaries and before/after catalogue misses verified.',
    })
    env = vars(previous.storage) | dict(stage=adapter, replay=SimpleNamespace(SETUP=SETUP, ROM=ROM),
                                    PROOF=PROOF, __file__=__file__)
    exec(compile(source, __file__ + '::existing-boundary-and-catalogue-proof', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

