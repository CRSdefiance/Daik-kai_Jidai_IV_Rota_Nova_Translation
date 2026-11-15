"""Replay Mivor's reversal, Maria's two-page appeal, and the tablet joke at Lil's entry."""

import argparse
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_lil_opening_wraps_20261114 as template
from scripts import refine_lil_midroute_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/lil_midroute_wraps_20261114_v1')
ROM = ROOT / 'lil_midroute_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'lil_midroute_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = template.FRAME_COUNT
EXCERPTS = ((73, 1750, 1958), (115, 1638, 1876), (136, 216, 410))
PLAY_ORDER = ('DK4_MES_B73_R0139', 'DK4_MES_B73_R0142', 'DK4_MES_B73_R0145',
              'DK4_MES_B115_R0128', 'DK4_MES_B115_R0131',
              'DK4_MES_B136_R0022', 'DK4_MES_B136_R0025', 'DK4_MES_B136_R0029')
FOLLOWING_IDS = (PLAY_ORDER[1], PLAY_ORDER[4], PLAY_ORDER[6])
REVISED_IDS = tuple(ident for ident in PLAY_ORDER if ident not in FOLLOWING_IDS)
SURROUNDING = {'before': (2200, 8500, 8700), 'after': (2200, 8500, 8700)}

env = template.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.initial_names.bare_tokens})),
}
prepare_source = checked_text(template.prepare_source, {
    "len(speeches) == 7 and len(rows) == 19": "len(speeches) == 8 and len(rows) == 20",
    "Seven original speech commands at the initialized Lil opening":
        "Eight original speech commands at the initialized Lil opening",
})
exec(compile(prepare_source, __file__ + '::native-Lil-entry-and-original-return', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(template.capture.__code__, template.capture.__globals__ | globals())
startup = FunctionType(template.startup.__code__, template.startup.__globals__ | globals())
verify_storage = FunctionType(template.verify_storage.__code__, template.verify_storage.__globals__ | globals())
verify_source = checked_text(template.verify_source, {
    "two_pages = {'DK4_MES_B17_R0012'} if side == 'before' else set()":
        "two_pages = {'DK4_MES_B115_R0128'}",
    'verified_revised_pages=4': 'verified_revised_pages=6',
    'Matched the company substitution, Aziza’s interrupted account, and the Calicut page.':
        'Matched Mivor’s reversal, Maria’s two-page appeal, and the tablet conversation.',
})
exec(compile(verify_source, __file__ + '::Lil-midroute-exchange-replay', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
