"""Verify the royal address and an ordinary tavern exchange in Rafael's opening."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_alliance_wraps_20261114 as previous
from scripts import replay_rafael_crew_wraps_20261114 as crew
from scripts import replay_rafael_name_wraps_20261114 as fixture
from scripts import stage_rafael_homecoming_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_homecoming_wraps_20261114_v2')
ROM = ROOT / 'rafael_homecoming_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_homecoming_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = 8801
EXCERPTS = ((165, 90, 478), (166, 1048, 1206), (169, 976, 1048))
FOLLOWING_IDS = ('DK4_MES_B165_R0019', 'DK4_MES_B166_R0103', 'DK4_MES_B169_R0106')
REVISED_IDS = ('DK4_MES_B165_R0013', 'DK4_MES_B165_R0016', 'DK4_MES_B166_R0100', 'DK4_MES_B169_R0102')
PLAY_ORDER = (REVISED_IDS[0], REVISED_IDS[1], FOLLOWING_IDS[0], REVISED_IDS[2],
              FOLLOWING_IDS[1], REVISED_IDS[3], FOLLOWING_IDS[2])
env = previous.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.previous.previous.previous_token_scanner})),
    'tools': previous.verify.__globals__['tools'],
}
source = checked_text(getsource(fixture.prepare), {
    'assert len(selected) == 2 and all': 'assert len(selected) in (2, 3) and all',
    'first, last = selected': 'first, last = selected[0], selected[-1]',
    "assert first['offset'] + first['native_extent'] == last['offset']":
        "assert all(a['offset'] + a['native_extent'] == b['offset'] for a, b in zip(selected, selected[1:]))",
    'assert len(speeches) == 10 and len(rows) == 21': 'assert len(speeches) == 7 and len(rows) == 18',
    'Ten original speech commands': 'Seven original speech commands',
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
    'DK4_MES_B101_R0068': 'DK4_MES_B165_R0016',
    'Matched the company and full name, the two-page rumor, the charm and three following replies.':
        'Matched both royal pages, the appointment, Ian’s dismissal exchange and all three following replies.',
})
exec(compile(source, __file__ + '::royal-page-turn-and-tavern-fixture', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

