"""Replay Maria's answer, Hodram's reassurance and the sail tutorial."""

import argparse
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_hodram_opening_wraps_20261114 as template
from scripts import stage_hodram_rumor_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/hodram_rumor_wraps_20261114_v3')
BEFORE = Path('out/hodram_rumor_wraps_20261114_v1/before')
ROM = ROOT / 'hodram_rumor_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'hodram_rumor_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = template.FRAME_COUNT
EXCERPTS = ((123, 1402, 1654), (142, 44, 198), (142, 2870, 2950), (171, 1468, 1756))
PLAY_ORDER = ('DK4_MES_B123_R0103', 'DK4_MES_B123_R0107', 'DK4_MES_B123_R0110',
              'DK4_MES_B142_R0008', 'DK4_MES_B142_R0233', 'DK4_MES_B171_R0098', 'DK4_MES_B171_R0101')
FOLLOWING_IDS = (PLAY_ORDER[0], PLAY_ORDER[-1])
REVISED_IDS = tuple(ident for ident in PLAY_ORDER if ident not in FOLLOWING_IDS)
TWO_PAGE_IDS = {'DK4_MES_B142_R0008', 'DK4_MES_B171_R0098'}
SURROUNDING = {'before': (2200, 8500, 8700), 'after': (2200, 8500, 8700)}

env = template.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.previous.initial_names.bare_tokens})),
    'previous': template.capture.__globals__['previous'],
}
exec(compile(template.prepare_source, __file__ + '::same-Hodram-opening-and-exit', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(template.capture.__code__, template.capture.__globals__ | globals()
                       | {'previous': template.capture.__globals__['previous']})
startup = FunctionType(template.startup.__code__, template.startup.__globals__ | globals()
                       | {'previous': template.startup.__globals__['previous']})
verify_storage = FunctionType(template.verify_storage.__code__, template.verify_storage.__globals__ | globals()
                              | {'previous': template.verify_storage.__globals__['previous']})
verify_source = checked_text(template.verify_source, {
    "report_path = ROOT / side / 'capture_report.json'":
        "report_path = (BEFORE if side == 'before' else ROOT / side) / 'capture_report.json'",
    """        assert len(shown['DK4_MES_B72_R0091']) == (2 if side == 'before' else 1)
        assert all(len(shown[ident]) == 1 for ident in PLAY_ORDER if ident != 'DK4_MES_B72_R0091')""":
        '        assert all(len(shown[ident]) == (2 if ident in TWO_PAGE_IDS else 1) for ident in PLAY_ORDER)',
    'verified_revised_pages=3': 'verified_revised_pages=7',
    'Matched Lil’s question, the diplomacy page transition, and Hodram’s full name.':
        'Matched Maria’s reply, the reassurance and name substitution, and the stern-sail advice.',
})
exec(compile(verify_source, __file__ + '::Hodram-and-sail-page-turns', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
