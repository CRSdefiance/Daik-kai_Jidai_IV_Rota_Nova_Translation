"""Verify changed ship tutorials in Rafael's initialized opening."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_homecoming_wraps_20261114 as previous
from scripts import replay_rafael_crew_wraps_20261114 as crew
from scripts import replay_rafael_name_wraps_20261114 as fixture
from scripts import stage_rafael_seamanship_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_seamanship_wraps_20261114_v2')
ROM = ROOT / 'rafael_seamanship_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_seamanship_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = 8801
EXCERPTS = ((177, 2514, 2662), (179, 2098, 2302), (180, 616, 1044))
FOLLOWING_IDS = ('DK4_MES_B177_R0187', 'DK4_MES_B179_R0125', 'DK4_MES_B180_R0079')
REVISED_IDS = ('DK4_MES_B177_R0183', 'DK4_MES_B179_R0122', 'DK4_MES_B180_R0072', 'DK4_MES_B180_R0076')
PLAY_ORDER = (REVISED_IDS[0], FOLLOWING_IDS[0], REVISED_IDS[1], FOLLOWING_IDS[1],
              REVISED_IDS[2], REVISED_IDS[3], FOLLOWING_IDS[2])
env = previous.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.previous.previous.previous.previous_token_scanner})),
    'tools': previous.verify.__globals__['tools'],
}
source = checked_text(getsource(fixture.prepare), {
    'assert len(selected) == 2 and all': 'assert len(selected) in (2, 3) and all',
    'first, last = selected': 'first, last = selected[0], selected[-1]',
    "assert first['offset'] + first['native_extent'] == last['offset']":
        "assert all(a['offset'] + a['native_extent'] == b['offset'] for a, b in zip(selected, selected[1:]))",
    'assert len(speeches) == 10 and len(rows) == 21': 'assert len(speeches) == 7 and len(rows) == 18',
    'Ten original speech commands': 'Seven original speech commands',
    "page, = painter(arm, font, body)['pages']":
        "pages = painter(arm, font, body)['pages']",
    "transition[ident] = page['native_plane_hex']":
        "transition[ident] = [page['native_plane_hex'] for page in pages]",
})
exec(compile(source, __file__ + '::prior-Rafael-opening-fixture', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(previous.capture.__code__, previous.capture.__globals__ | globals()
                       | {'previous': previous.capture.__globals__['previous']})
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | globals()
                       | {'previous': previous.startup.__globals__['previous']})
verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | globals()
                              | {'previous': previous.verify_storage.__globals__['previous']})
source = checked_text(getsource(crew.verify), {
    '    tools = previous.previous.previous.prior\n': '',
    'DK4_MES_B101_R0068': 'DK4_MES_B179_R0122',
    'verified_revised_pages=5': 'verified_revised_pages=6',
    'verified_following_pages=3': 'verified_following_pages=sum(len(shown[ident]) for ident in FOLLOWING_IDS)',
    'planes = [transition] if transition else': 'planes = transition if transition else',
    'Matched the company and full name, the two-page rumor, the charm and three following replies.':
        'Matched the ship-buying advice, both repair and square-sail pages, and their following lines.',
})
exec(compile(source, __file__ + '::ship-tutorial-page-turns', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
