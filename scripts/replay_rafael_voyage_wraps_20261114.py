"""Replay both tutorials and the urgent rescue exchange in Rafael's route."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_crew_wraps_20261114 as previous
from scripts import stage_rafael_voyage_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_voyage_wraps_20261114_v2')
ROM = ROOT / 'rafael_voyage_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_voyage_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = 8801
EXCERPTS = ((121, 296, 390), (129, 540, 870), (143, 4262, 4548))
FOLLOWING_IDS = ('DK4_MES_B121_R0048', 'DK4_MES_B129_R0039', 'DK4_MES_B143_R0383')
REVISED_IDS = ('DK4_MES_B121_R0045', 'DK4_MES_B129_R0033', 'DK4_MES_B129_R0036', 'DK4_MES_B143_R0380')
PLAY_ORDER = (REVISED_IDS[0], FOLLOWING_IDS[0], REVISED_IDS[1], REVISED_IDS[2],
              FOLLOWING_IDS[1], REVISED_IDS[3], FOLLOWING_IDS[2])
env = previous.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {
        'previous': SimpleNamespace(bare_tokens=stage.previous_token_scanner),
    })),
}
env['tools'] = previous.previous.previous.previous.prior
prepare = FunctionType(previous.prepare.__code__, env)
capture = FunctionType(previous.capture.__code__, previous.capture.__globals__ | globals()
                       | {'previous': previous.previous.previous})
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | globals()
                       | {'previous': previous.previous.previous})
verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | globals()
                              | {'previous': previous.verify_storage.__globals__['previous']})
source = checked_text(getsource(previous.verify), {
    '    tools = previous.previous.previous.prior\n': '',
    'DK4_MES_B101_R0068': 'DK4_MES_B143_R0380',
    'Matched the company and full name, the two-page rumor, the charm and three following replies.':
        'Matched the rescue plea, trade advice, two-page naval tutorial and three following replies.',
})
exec(compile(source, __file__ + '::prior-Rafael-page-replay-contract', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

