"""Exercise Aziza's interrupted thought, the company name, and the Calicut page."""

import argparse
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_hodram_final_wraps_20261114 as template
from scripts import stage_lil_opening_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/lil_opening_wraps_20261114_v1')
ROM = ROOT / 'lil_opening_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'lil_opening_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof_phase_matched.json'
FRAME_COUNT = template.FRAME_COUNT
EXCERPTS = ((12, 712, 854), (12, 3196, 3390), (17, 18, 202))
PLAY_ORDER = ('DK4_MES_B12_R0060', 'DK4_MES_B12_R0064', 'DK4_MES_B12_R0233',
              'DK4_MES_B12_R0236', 'DK4_MES_B12_R0240', 'DK4_MES_B17_R0009',
              'DK4_MES_B17_R0012')
FOLLOWING_IDS = (PLAY_ORDER[1], PLAY_ORDER[3], PLAY_ORDER[5])
REVISED_IDS = tuple(ident for ident in PLAY_ORDER if ident not in FOLLOWING_IDS)
SURROUNDING = {'before': (2200, 6100, 8325), 'after': (2200, 5775, 8000)}

env = template.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.opening.initial_names.bare_tokens})),
}
prepare_source = checked_text(template.template.template.prepare_source, {
    'host = bank.blocks[42]': 'host = bank.blocks[22]',
    'blocks[42]': 'blocks[22]',
    'host[:42], host[host_end - 6:host_end]': 'host[:56], host[host_end - 14:host_end]',
    'initial[8:] == clean_host[8:42]': 'initial[8:] == clean_host[8:56]',
    "clean_host[clean_end - 6:clean_end] == bytes.fromhex('00c200000000')":
        "clean_host[clean_end - 14:clean_end] == bytes.fromhex('00c200a0ffff2c081b8200000000')",
    'len(rows) == 17': 'len(rows) == 19',
    'initialized Hodram opening': 'initialized Lil opening',
})
exec(compile(prepare_source, __file__ + '::native-Lil-entry-and-return', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(template.capture.__code__, template.capture.__globals__ | globals())
startup = FunctionType(template.startup.__code__, template.startup.__globals__ | globals())
storage_source = checked_text(template.template.template.storage_source, {
    ' Hodram command boundaries': ' Lil command boundaries',
})
storage_env = template.verify_storage.__globals__ | globals()
exec(compile(storage_source, __file__ + '::Lil-command-boundaries', 'exec'), storage_env)
verify_storage = storage_env['verify_storage']
verify_source = checked_text(template.verify_source, {
    """        two_pages = {'DK4_MES_B213_R0027', 'DK4_MES_B213_R0030'}
        if side == 'before':
            two_pages.add('DK4_MES_B324_R0013')""":
        """        two_pages = {'DK4_MES_B17_R0012'} if side == 'before' else set()""",
    'verified_revised_pages=6': 'verified_revised_pages=4',
    'initialized_excerpts_at_Hodram_entry': 'initialized_excerpts_at_Lil_entry',
    'Matched the Muramasa letter, both name substitutions, and the village account.':
        'Matched the company substitution, Aziza’s interrupted account, and the Calicut page.',
})
exec(compile(verify_source, __file__ + '::Lil-exchange-replay', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
