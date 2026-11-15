"""Replay Janus's signed letter, the spice advice, and the trader's explanation."""

import argparse
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_lil_late_wraps_20261114 as template
from scripts import refine_lil_final_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/lil_final_wraps_20261114_v1')
ROM = ROOT / 'lil_final_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'lil_final_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = template.FRAME_COUNT
EXCERPTS = ((214, 968, 1036), (304, 1022, 1200), (319, 298, 570), (319, 570, 746))
PLAY_ORDER = ('DK4_MES_B214_R0068', 'DK4_MES_B304_R0047', 'DK4_MES_B304_R0051',
              'DK4_MES_B319_R0014', 'DK4_MES_B319_R0018', 'DK4_MES_B319_R0022',
              'DK4_MES_B319_R0026', 'DK4_MES_B319_R0030')
FOLLOWING_IDS = (PLAY_ORDER[1], PLAY_ORDER[3], PLAY_ORDER[5], PLAY_ORDER[6])
REVISED_IDS = tuple(ident for ident in PLAY_ORDER if ident not in FOLLOWING_IDS)
SURROUNDING = {'before': (2200, 6750, 8500), 'after': (2200, 6100, 7850)}

env = template.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.initial_names.bare_tokens})),
}
exec(compile(template.template.prepare_source, __file__ + '::native-Lil-entry-and-original-return', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(template.capture.__code__, template.capture.__globals__ | globals())
startup = FunctionType(template.template.startup.__code__, template.template.startup.__globals__ | globals())
verify_storage = FunctionType(template.verify_storage.__code__, template.verify_storage.__globals__ | globals())
verify_source = checked_text(template.verify_source, {
    'two_pages = set()':
        "two_pages = {'DK4_MES_B304_R0051', 'DK4_MES_B319_R0018'} if side == 'before' else set()",
    'Matched the trader’s reply, the crew assignment advice, and the sail tutorial.':
        'Matched Janus’s signature, the Market Info instruction, and the trader’s two revised pages.',
})
exec(compile(verify_source, __file__ + '::Lil-letter-and-trade-replay', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
