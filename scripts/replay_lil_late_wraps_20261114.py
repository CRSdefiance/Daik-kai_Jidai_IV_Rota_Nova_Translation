"""Replay the shop closure, crew assignment advice, and sail tutorial at Lil's entry."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_lil_midroute_wraps_20261114 as template
from scripts import stage_lil_late_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/lil_late_wraps_20261114_v2')
ROM = ROOT / 'lil_late_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'lil_late_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = template.FRAME_COUNT
EXCERPTS = ((157, 680, 830), (166, 2220, 2438), (167, 1244, 1480), (167, 1480, 1636))
PLAY_ORDER = ('DK4_MES_B157_R0055', 'DK4_MES_B157_R0058', 'DK4_MES_B166_R0153',
              'DK4_MES_B166_R0157', 'DK4_MES_B167_R0095', 'DK4_MES_B167_R0098',
              'DK4_MES_B167_R0101', 'DK4_MES_B167_R0105')
FOLLOWING_IDS = (PLAY_ORDER[0], PLAY_ORDER[2], PLAY_ORDER[5], PLAY_ORDER[7])
REVISED_IDS = tuple(ident for ident in PLAY_ORDER if ident not in FOLLOWING_IDS)
SURROUNDING = template.SURROUNDING

env = template.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.initial_names.bare_tokens})),
}
exec(compile(template.prepare_source, __file__ + '::native-Lil-entry-and-original-return', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(template.capture.__code__, template.capture.__globals__ | globals())
verify_storage = FunctionType(template.verify_storage.__code__, template.verify_storage.__globals__ | globals())
verify_source = checked_text(template.verify_source, {
    "two_pages = {'DK4_MES_B115_R0128'}": 'two_pages = set()',
    'verified_revised_pages=6': 'verified_revised_pages=4',
    'Matched Mivor’s reversal, Maria’s two-page appeal, and the tablet conversation.':
        'Matched the trader’s reply, the crew assignment advice, and the sail tutorial.',
})
exec(compile(verify_source, __file__ + '::Lil-shop-and-sailing-replay', 'exec'), env)
verify = env['verify']


def startup():
    setup = base.load(SETUP)
    assert setup['candidate_sha256'] == base.digest(ROM)
    inputs = ROOT / 'startup_input.json'
    base.save(inputs, dict(research_ROM_sha256=setup['candidate_sha256'],
                          registered_input=dict(candidate_sha256=setup['parent_sha256'])))
    boot = template.startup.__globals__['previous'].previous.prior.prior.boot
    parent_output = stage.parent.replay.ROOT
    parent_capture = parent_output / 'startup_retry_v2/own_startup'
    FunctionType(boot.startup_replay.main.__code__, vars(boot.startup_replay) | dict(
        EVIDENCE=inputs, ROM=ROM, STARTUP=ROOT / 'own_startup', PRIOR=parent_capture))()
    source = checked_text(getsource(boot.startup_check.verify_startup), {
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'":
            "PARENT_CAPTURE / 'capture/capture_report.json'",
    })
    startup_env = vars(boot.startup_check) | dict(ROOT=ROOT, ROM=ROM, PROOF=inputs,
        BIOGRAPHIES=parent_output, BOOT=STARTUP, PARENT_CAPTURE=parent_capture)
    exec(compile(source, __file__ + '::registered-parent-startup-retry', 'exec'), startup_env)
    startup_env['verify_startup']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
