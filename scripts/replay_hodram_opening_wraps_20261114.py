"""Replay the confrontation, shorter diplomatic speech, and Hodram's name expansion."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_final_wraps_20261114 as template
from scripts import stage_hodram_opening_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/hodram_opening_wraps_20261114_v2')
ROM = ROOT / 'hodram_opening_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'hodram_opening_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_verified.json'
FRAME_COUNT = template.FRAME_COUNT
SURROUNDING = {'before': (2200, 7025, 7675), 'after': (2200, 6700, 7350)}
EXCERPTS = ((44, 164, 234), (72, 1390, 1580), (72, 1590, 1682), (84, 1612, 1708))
PLAY_ORDER = ('DK4_MES_B44_R0021', 'DK4_MES_B44_R0025', 'DK4_MES_B72_R0088',
              'DK4_MES_B72_R0091', 'DK4_MES_B72_R0098', 'DK4_MES_B84_R0165', 'DK4_MES_B84_R0169')
REVISED_IDS = (PLAY_ORDER[0], PLAY_ORDER[3], PLAY_ORDER[5])
FOLLOWING_IDS = tuple(ident for ident in PLAY_ORDER if ident not in REVISED_IDS)

env = template.prepare.__globals__ | globals() | {
    'stage': SimpleNamespace(**(vars(stage) | {'bare_tokens': stage.initial_names.bare_tokens})),
    'previous': template.capture.__globals__['previous'],
}
prepare_source = checked_text(template.prepare_source, {
    'assert len(speeches) == 8 and len(rows) == 19': 'assert len(speeches) == 7 and len(rows) == 17',
    'initial = bank.blocks[44][:40]': '''host = bank.blocks[42]
        host_end = 8 + unpack_from('<H', host, 4)[0]
        clean = base.NdsImage.open(stage.CLEAN)
        clean_host = stage.IlnkContainer.parse(clean.read_file(stage.FILE)).blocks[42]
        clean_end = 8 + unpack_from('<H', clean_host, 4)[0]
        initial, exit_bytes = host[:42], host[host_end - 6:host_end]
        assert initial[8:] == clean_host[8:42]
        assert exit_bytes == clean_host[clean_end - 6:clean_end] == bytes.fromhex('00c200000000')''',
    """        last = bank.blocks[EXCERPTS[-1][0]]
        end = 8 + unpack_from('<H', last, 4)[0]
        assert last[end - 4:end] == bytes(4)
        logical.extend(bytes(4))""": '        logical.extend(exit_bytes)',
    'bank.blocks[44] = body': 'bank.blocks[42] = body',
    'Eight original speech commands, including two exact retentions, at the initialized Rafael opening.':
        'Seven original speech commands at the initialized Hodram opening, with its original exit.',
})
exec(compile(prepare_source, __file__ + '::original-Hodram-opening-fixture', 'exec'), env)
prepare = env['prepare']
capture_source = checked_text(getsource(template.capture), {
    '*range(2850, 7701, 25), 8500, 8700': '*range(2850, 8776, 25)',
})
exec(compile(capture_source, __file__ + '::opening-and-departure-capture', 'exec'), env)
capture = env['capture']
startup = FunctionType(template.startup.__code__, template.startup.__globals__ | globals()
                       | {'previous': template.startup.__globals__['previous']})
storage_env = template.verify_storage.__globals__ | globals() | {'previous': template.verify_storage.__globals__['previous']}
storage_source = checked_text(getsource(template.verify_storage), {' Rafael command boundaries': ' Hodram command boundaries'})
exec(compile(storage_source, __file__ + '::Hodram-command-boundaries', 'exec'), storage_env)
verify_storage = storage_env['verify_storage']
verify_source = checked_text(template.verify_source, {
    'assert all(len(holds) == 1 for holds in shown.values())':
        """assert len(shown['DK4_MES_B72_R0091']) == (2 if side == 'before' else 1)
        assert all(len(shown[ident]) == 1 for ident in PLAY_ORDER if ident != 'DK4_MES_B72_R0091')""",
    'initialized_excerpts_at_Rafael_entry': 'initialized_excerpts_at_Hodram_entry',
    "        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in (2200, 8500, 8700)]":
        """        assert last_frame < SURROUNDING[side][1]
        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in SURROUNDING[side]]
        evidence.update({photos[frame][0]['path']: base.digest(photos[frame][0]['path']) for frame in SURROUNDING[side]})""",
    'outside_exact_frames=[2200, 8500, 8700]':
        "outside_exact_frames=list(zip(SURROUNDING['before'], SURROUNDING['after'], strict=True))",
    'Matched Ian’s signature, the formal reading, and the sword-test exchange.':
        'Matched Lil’s question, the diplomacy page transition, and Hodram’s full name.',
})
exec(compile(verify_source, __file__ + '::Hodram-page-turns-and-name', 'exec'), env)
verify = env['verify']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()
