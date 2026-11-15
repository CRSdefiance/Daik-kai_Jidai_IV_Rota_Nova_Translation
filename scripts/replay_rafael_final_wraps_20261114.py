"""Replay Ian's signed letter, the Arabian Nights reading, and the sword test."""

import argparse
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_quest_wraps_20261114 as previous
from scripts import stage_rafael_final_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_final_wraps_20261114_v1')
ROM = ROOT / 'rafael_final_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_final_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = previous.FRAME_COUNT
EXCERPTS = ((235, 1004, 1084), (318, 662, 882), (318, 886, 1016), (336, 1256, 1422))
PLAY_ORDER = ('DK4_MES_B235_R0048', 'DK4_MES_B318_R0137', 'DK4_MES_B318_R0141',
              'DK4_MES_B318_R0146', 'DK4_MES_B318_R0151',
              'DK4_MES_B336_R0109', 'DK4_MES_B336_R0112', 'DK4_MES_B336_R0116')
REVISED_IDS = (PLAY_ORDER[2], PLAY_ORDER[5], PLAY_ORDER[6])
FOLLOWING_IDS = tuple(ident for ident in PLAY_ORDER if ident not in REVISED_IDS)

env = previous.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': previous.prepare.__globals__['stage'].bare_tokens})),
}
prepare_source = checked_text(previous.prepare_source, {
    'assert 2 <= len(selected) <= 4 and all': 'assert 1 <= len(selected) <= 3 and all',
    'Eight original speech commands': 'Eight original speech commands, including two exact retentions,',
})
exec(compile(prepare_source, __file__ + '::prior-Rafael-opening-fixture', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(previous.capture.__code__, previous.capture.__globals__ | globals()
                       | {'previous': previous.capture.__globals__['previous']})
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | globals()
                       | {'previous': previous.startup.__globals__['previous']})
verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | globals()
                              | {'previous': previous.verify_storage.__globals__['previous']})
verify_source = checked_text(previous.verify_source, {
    "assert len(shown['DK4_MES_B309_R0059']) == 2":
        "assert all(len(holds) == 1 for holds in shown.values())",
    'verified_revised_pages=6': 'verified_revised_pages=3',
    'Matched the Sofala escort, the boy’s recovery and both pages of the hidden-village directions.':
        'Matched Ian’s signature, the formal reading, and the sword-test exchange.',
})
exec(compile(verify_source, __file__ + '::letter-reading-and-sword-test', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
