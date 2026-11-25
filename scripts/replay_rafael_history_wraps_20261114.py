"""Replay Rafael's taunt, Gerhard's artifact story and Samwell's reply."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_port_wraps_20261114 as previous
from scripts import stage_rafael_history_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_history_wraps_20261114_v2')
BEFORE = Path('out/rafael_history_wraps_20261114_v1/before')
ROM = ROOT / 'rafael_history_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_history_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_verified.json'
FRAME_COUNT = previous.FRAME_COUNT
SURROUNDING = {'before': (2200, 7050, 7350), 'after': (2200, 6750, 7050)}
EXCERPTS = ((1, 440, 556), (234, 838, 1122), (242, 518, 732))
PLAY_ORDER = ('DK4_MES_B1_R0058', 'DK4_MES_B1_R0063',
              'DK4_MES_B234_R0042', 'DK4_MES_B234_R0046', 'DK4_MES_B234_R0051', 'DK4_MES_B234_R0055',
              'DK4_MES_B242_R0042', 'DK4_MES_B242_R0047', 'DK4_MES_B242_R0051')
REVISED_IDS = tuple(PLAY_ORDER[index] for index in (0, 2, 5, 6, 7))
FOLLOWING_IDS = tuple(ident for ident in PLAY_ORDER if ident not in REVISED_IDS)

env = previous.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': previous.prepare.__globals__['stage'].bare_tokens})),
}
prepare_source = checked_text(getsource(previous.fixture.prepare), {
    'assert len(selected) == 2 and all': 'assert 2 <= len(selected) <= 4 and all',
    'first, last = selected': 'first, last = selected[0], selected[-1]',
    "assert first['offset'] + first['native_extent'] == last['offset']":
        "assert all(a['offset'] + a['native_extent'] == b['offset'] for a, b in zip(selected, selected[1:]))",
    'assert len(speeches) == 10 and len(rows) == 21': 'assert len(speeches) == 9 and len(rows) == 20',
    "page, = painter(arm, font, body)['pages']": "pages = painter(arm, font, body)['pages']",
    "transition[ident] = page['native_plane_hex']": "transition[ident] = [page['native_plane_hex'] for page in pages]",
    'Ten original speech commands': 'Nine original speech commands',
})
exec(compile(prepare_source, __file__ + '::prior-Rafael-opening-fixture', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(previous.capture.__code__, previous.capture.__globals__ | globals()
                       | {'previous': previous.capture.__globals__['previous']})
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | globals()
                       | {'previous': previous.startup.__globals__['previous']})
verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | globals()
                              | {'previous': previous.verify_storage.__globals__['previous']})
verify_source = checked_text(previous.source, {
    "report_path = ROOT / side / 'capture_report.json'":
        "report_path = (BEFORE if side == 'before' else ROOT / side) / 'capture_report.json'",
    "assert len(shown['DK4_MES_B221_R0027']) == 2":
        "assert len(shown['DK4_MES_B234_R0042']) == (2 if side == 'before' else 1)",
    "        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in (2200, 8500, 8700)]":
        "        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in SURROUNDING[side]]\n"
        "        evidence.update({photos[frame][0]['path']: base.digest(photos[frame][0]['path']) for frame in SURROUNDING[side]})",
    'outside_exact_frames=[2200, 8500, 8700]':
        "outside_exact_frames=list(zip(SURROUNDING['before'], SURROUNDING['after'], strict=True))",
    'verified_revised_pages=6': 'verified_revised_pages=5',
    'Matched both Muramasa pages, the family-name substitution, and Ian’s exchange.':
        'Matched Clau’s cabin joke, the condensed page sequence in Gerhard’s story and Samwell’s exchange.',
})
exec(compile(verify_source, __file__ + '::dialogue-page-turns', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
