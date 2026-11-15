"""Verify the Sofala escort, recovery reply, and hidden-village directions."""

import argparse
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_history_wraps_20261114 as previous
from scripts import stage_rafael_quest_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_quest_wraps_20261114_v1')
ROM = ROOT / 'rafael_quest_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_quest_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = previous.FRAME_COUNT
EXCERPTS = ((266, 840, 1192), (308, 218, 358), (309, 660, 940))
PLAY_ORDER = ('DK4_MES_B266_R0049', 'DK4_MES_B266_R0053', 'DK4_MES_B266_R0056',
              'DK4_MES_B308_R0030', 'DK4_MES_B308_R0034', 'DK4_MES_B309_R0050',
              'DK4_MES_B309_R0054', 'DK4_MES_B309_R0059')
FOLLOWING_IDS = ('DK4_MES_B266_R0049', 'DK4_MES_B308_R0034', 'DK4_MES_B309_R0054')
REVISED_IDS = tuple(ident for ident in PLAY_ORDER if ident not in FOLLOWING_IDS)

env = previous.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': previous.prepare.__globals__['stage'].bare_tokens})),
}
prepare_source = checked_text(previous.prepare_source, {
    'assert len(speeches) == 9 and len(rows) == 20': 'assert len(speeches) == 8 and len(rows) == 19',
    'Nine original speech commands': 'Eight original speech commands',
})
exec(compile(prepare_source, __file__ + '::prior-Rafael-opening-fixture', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(previous.capture.__code__, previous.capture.__globals__ | globals()
                       | {'previous': previous.capture.__globals__['previous']})
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | globals()
                       | {'previous': previous.startup.__globals__['previous']})
verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | globals()
                              | {'previous': previous.verify_storage.__globals__['previous']})
verify_source = checked_text(previous.previous.source, {
    'DK4_MES_B221_R0027': 'DK4_MES_B309_R0059',
    'Matched both Muramasa pages, the family-name substitution, and Ian’s exchange.':
        'Matched the Sofala escort, the boy’s recovery and both pages of the hidden-village directions.',
})
exec(compile(verify_source, __file__ + '::quest-and-village-page-turns', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
