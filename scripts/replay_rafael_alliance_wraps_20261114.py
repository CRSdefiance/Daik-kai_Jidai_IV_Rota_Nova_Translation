"""Replay a page-count change and the core Rafael name-substitution exchanges."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_voyage_wraps_20261114 as previous
from scripts import replay_rafael_name_wraps_20261114 as fixture
from scripts import stage_rafael_alliance_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_alliance_wraps_20261114_v1')
ROM = ROOT / 'rafael_alliance_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_alliance_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof_v2.json'
FRAME_COUNT = 8801
EXCERPTS = ((150, 122, 384), (151, 1748, 1904), (159, 370, 476))
FOLLOWING_IDS = ('DK4_MES_B150_R0017', 'DK4_MES_B151_R0212', 'DK4_MES_B159_R0051')
REVISED_IDS = ('DK4_MES_B150_R0013', 'DK4_MES_B151_R0208', 'DK4_MES_B159_R0047')
PLAY_ORDER = tuple(item for group in zip(REVISED_IDS, FOLLOWING_IDS, strict=True) for item in group)
env = previous.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {
        'previous': SimpleNamespace(bare_tokens=stage.previous.previous_token_scanner),
    })),
    'tools': previous.verify.__globals__['tools'],
}
source = checked_text(getsource(fixture.prepare), {
    'assert len(speeches) == 10 and len(rows) == 21': 'assert len(speeches) == 6 and len(rows) == 17',
    'Ten original speech commands': 'Six original speech commands',
    'stage.bare_tokens(body)': 'stage.previous.bare_tokens(body)',
})
exec(compile(source, __file__ + '::prior-Rafael-opening-fixture', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(previous.capture.__code__, previous.capture.__globals__ | globals()
                       | {'previous': previous.capture.__globals__['previous']})
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | globals()
                       | {'previous': previous.startup.__globals__['previous']})
verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | globals()
                              | {'previous': previous.verify_storage.__globals__['previous']})
source = checked_text(getsource(previous.previous.verify), {
    '    tools = previous.previous.previous.prior\n': '',
    "assert len(shown['DK4_MES_B101_R0068']) == 2":
        "assert len(shown['DK4_MES_B150_R0013']) == (2 if side == 'before' else 1)",
    'verified_revised_pages=5': 'verified_revised_pages=3, previous_revised_pages=4',
    "    assert outside['before'] == outside['after']":
        "    assert outside['before'][0] == outside['after'][0]\n"
        "    # The removed page makes the same scheduled A presses advance one extra tutorial turn.\n"
        "    for side in ('before', 'after'):\n"
        "        report = base.load(ROOT / side / 'capture_report.json')\n"
        "        photos = tools.photos(report)\n"
        "        assert photos[8500][0]['framebuffer_sha256'] == photos[8700][0]['framebuffer_sha256']\n"
        "        for frame in (2200, 8500, 8700):\n"
        "            path = photos[frame][0]['path']\n"
        "            evidence[path] = base.digest(path)\n"
        "    assert outside['before'][1:] != outside['after'][1:]",
    'outside_exact_frames=[2200, 8500, 8700], source_commands_preserved=True':
        'outside_exact_frames=[2200], later_tutorial_frames=[8500, 8700], later_same_frame_hashes=outside, source_commands_preserved=True',
    'Matched the company and full name, the two-page rumor, the charm and three following replies.':
        'Matched the two-to-one page change, both name-substitution lines and all three following replies.',
})
exec(compile(source, __file__ + '::page-reduction-and-name-fixture', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

