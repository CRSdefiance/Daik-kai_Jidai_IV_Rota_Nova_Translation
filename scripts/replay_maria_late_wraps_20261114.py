"""Replay the grouped prices and both signed letters at Maria's initialized entry."""

import argparse
import sys
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import replay_maria_midroute_wraps_20261114 as midroute
from scripts import replay_maria_opening_wraps_20261114 as previous
from scripts import refine_maria_late_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/maria_late_wraps_20261114_v2')
ROM = ROOT / 'maria_late_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'maria_late_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
RETURN_FRAMES = (3900, 9750, 10000)
PLAY_ORDER = (
    'DK4_MES_B169_R0061', 'DK4_MES_B169_R0073', 'DK4_MES_B174_R0028',
    'DK4_MES_B182_R0026', 'DK4_MES_B182_R0029', 'DK4_MES_B182_R0032', 'DK4_MES_B182_R0064',
    'DK4_MES_B187_R0067', 'DK4_MES_B187_R0074', 'DK4_MES_B187_R0086',
)
REVISED_IDS = (PLAY_ORDER[0], PLAY_ORDER[2], PLAY_ORDER[3], PLAY_ORDER[5], PLAY_ORDER[7], PLAY_ORDER[8])
FOLLOWING_IDS = tuple(ident for ident in PLAY_ORDER if ident not in REVISED_IDS)
PAGED_ID = PLAY_ORDER[3]
CONDITIONAL_EXCERPTS = {
    'DK4_MES_B169_R0073': [436],
    'DK4_MES_B182_R0064': [1244],
    'DK4_MES_B187_R0086': [1266],
}

env = previous.prepare.__globals__ | globals()
prepare_source = checked_text(midroute.prepare_source, {
    "assert group['existing_extra_FE_commands'] == ([630, 1026] if block == 116 else [])":
        "assert not group['existing_extra_FE_commands']",
    "range(4200, 8701, 325)": "range(4200, 9076, 325)",
})
exec(compile(prepare_source, __file__ + '::same-Maria-host-and-letter-page-inputs', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(previous.capture.__code__, previous.capture.__globals__ | globals())

verify_source = checked_text(getsource(midroute.verify), {
    "len(planes) == (2 if side == 'before' and ident == PAGED_ID else 1)":
        "len(planes) == (2 if ident == PAGED_ID else 1)",
    "assert cursor < RETURN_FRAMES[side][1]": "assert cursor < RETURN_FRAMES[1]",
    """        outside_photos = photos
        if side == 'before':
            retry_path = RETRY_DIRECTORY / 'capture_report.json'
            retry = base.load(retry_path)
            previous.validate_capture(retry)
            assert retry['ROM_sha256'] == report['ROM_sha256'] and retry['frames'] == report['frames']
            assert retry['scripted_input_schedule'] == report['scripted_input_schedule'] + [
                dict(start=8750, duration=16, buttons=['A'])]
            outside_photos = tools.photos(retry)
            assert outside_photos[3900][0]['framebuffer_sha256'] == photos[3900][0]['framebuffer_sha256']
            evidence[str(retry_path)] = base.digest(retry_path)
        outside[side] = [outside_photos[frame][0]['framebuffer_sha256'] for frame in RETURN_FRAMES[side]]
        for frame in RETURN_FRAMES[side]:
            receipt = outside_photos[frame][0]""":
        """        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in RETURN_FRAMES]
        for frame in RETURN_FRAMES:
            receipt = photos[frame][0]""",
    'outside_exact_frames=list(zip(*RETURN_FRAMES.values(), strict=True))':
        'outside_exact_frames=list(RETURN_FRAMES)',
    'source_commands_preserved=True, additional_baseline_page_turn_frame=8750,':
        'source_commands_preserved=True,',
    'verified_revised_pages=len(REVISED_IDS),':
        'verified_revised_pages=len(REVISED_IDS) + 1, verified_revised_utterances=len(REVISED_IDS),',
    'observed_Ian_pages_before_after=[2, 1]': 'observed_Muramasa_pages_before_after=[2, 2]',
})
exec(compile(verify_source, __file__ + '::existing-portrait-mask-and-two-page-letter-verification', 'exec'), env)
verify = env['verify']
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | {
    'base': base, 'ROOT': ROOT, 'ROM': ROM, 'STARTUP': STARTUP, 'SETUP': SETUP, 'stage': stage,
})
verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | {
    'base': base, 'ROOT': ROOT, 'ROM': ROM, 'PROOF': PROOF, 'SETUP': SETUP, 'stage': stage,
})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'verify', 'verify_storage', 'startup'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

