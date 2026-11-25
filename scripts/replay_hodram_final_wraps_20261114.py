"""Replay the signed-letter dialogue, town lead, artifact rumor and village account."""

import argparse
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_hodram_rumor_wraps_20261114 as template
from scripts import stage_hodram_final_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/hodram_final_wraps_20261114_v1')
ROM = ROOT / 'hodram_final_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'hodram_final_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof_phase_matched.json'
FRAME_COUNT = template.FRAME_COUNT
EXCERPTS = ((213, 300, 630), (257, 8, 96), (314, 28, 262), (324, 58, 274))
PLAY_ORDER = ('DK4_MES_B213_R0027', 'DK4_MES_B213_R0030', 'DK4_MES_B257_R0006',
              'DK4_MES_B314_R0010', 'DK4_MES_B314_R0014', 'DK4_MES_B324_R0013', 'DK4_MES_B324_R0016')
FOLLOWING_IDS = (PLAY_ORDER[1], PLAY_ORDER[-1])
REVISED_IDS = tuple(ident for ident in PLAY_ORDER if ident not in FOLLOWING_IDS)
SURROUNDING = {'before': (2200, 6725, 8325), 'after': (2200, 6425, 8000)}

env = template.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.previous.initial_names.bare_tokens})),
    'previous': template.capture.__globals__['previous'],
}
exec(compile(template.template.prepare_source, __file__ + '::same-Hodram-opening-and-exit', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(template.capture.__code__, template.capture.__globals__ | globals()
                       | {'previous': template.capture.__globals__['previous']})
startup = FunctionType(template.startup.__code__, template.startup.__globals__ | globals()
                       | {'previous': template.startup.__globals__['previous']})
verify_storage = FunctionType(template.verify_storage.__code__, template.verify_storage.__globals__ | globals()
                              | {'previous': template.verify_storage.__globals__['previous']})
verify_source = checked_text(template.verify_source, {
    "report_path = (BEFORE if side == 'before' else ROOT / side) / 'capture_report.json'":
        "report_path = ROOT / side / 'capture_report.json'",
    '        assert all(len(shown[ident]) == (2 if ident in TWO_PAGE_IDS else 1) for ident in PLAY_ORDER)':
        """        two_pages = {'DK4_MES_B213_R0027', 'DK4_MES_B213_R0030'}
        if side == 'before':
            two_pages.add('DK4_MES_B324_R0013')
        assert all(len(shown[ident]) == (2 if ident in two_pages else 1) for ident in PLAY_ORDER)""",
    'verified_revised_pages=7': 'verified_revised_pages=6',
    'Matched Maria’s reply, the reassurance and name substitution, and the stern-sail advice.':
        'Matched the Muramasa letter, both name substitutions, and the village account.',
})
exec(compile(verify_source, __file__ + '::Hodram-letter-and-town-page-turns', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
