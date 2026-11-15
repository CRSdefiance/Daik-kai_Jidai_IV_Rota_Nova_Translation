"""Replay Yifa's advice, Jam's sign-off, and two clues on Maria's route."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops

from scripts import replay_maria_late_wraps_20261114 as template
from scripts import replay_maria_opening_wraps_20261114 as previous
from scripts import refine_maria_final_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/maria_final_wraps_20261114_v2')
ROM = ROOT / 'maria_final_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'maria_final_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
AFTER_INPUTS = ROOT / 'after_inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = 12001
RETURN_FRAMES = (3900, 11450, 11700)
PLAY_ORDER = (
    'DK4_MES_B200_R0012', 'DK4_MES_B200_R0015', 'DK4_MES_B200_R0018',
    'DK4_MES_B209_R0048', 'DK4_MES_B209_R0063',
    'DK4_MES_B212_R0105', 'DK4_MES_B212_R0109', 'DK4_MES_B212_R0112',
    'DK4_MES_B258_R0051', 'DK4_MES_B258_R0054',
    'DK4_MES_B275_R0128', 'DK4_MES_B275_R0131',
)
FOLLOWING_IDS = (PLAY_ORDER[0], PLAY_ORDER[7], PLAY_ORDER[9], PLAY_ORDER[11])
REVISED_IDS = tuple(ident for ident in PLAY_ORDER if ident not in FOLLOWING_IDS)
PAGED_IDS = {PLAY_ORDER[1], PLAY_ORDER[6], PLAY_ORDER[8]}
RECLAIMED_PAGE_ID = PLAY_ORDER[10]
CONDITIONAL_EXCERPTS = {'DK4_MES_B209_R0063': [1088]}


def input_path(side):
    return INPUTS if side == 'before' else AFTER_INPUTS


def verify_port_focus_frame(frame):
    screens = []
    for side in ('before', 'after'):
        report = base.load(ROOT / side / 'capture_report.json')
        receipt = next(row for row in report['frames_captured'] if row['frame'] == frame)
        with Image.open(receipt['path']) as image:
            screens.append(image.convert('RGB'))
    difference = ImageChops.difference(*screens)
    bounds = difference.getbbox()
    assert bounds == (208, 242, 252, 258), bounds
    return dict(frame=frame, port_focus_bounds=list(bounds),
                equal_pixels_outside_focus=True, exact_framebuffer_match=False)


env = previous.prepare.__globals__ | globals()
prepare_source = checked_text(template.prepare_source, {
    "range(4200, 9076, 325)": "range(4200, 10701, 325)",
    '    base.save(INPUTS, schedule)': '    base.save(INPUTS, schedule)\n    base.save(AFTER_INPUTS, schedule[:-1])',
})
exec(compile(prepare_source, __file__ + '::same-Maria-host-and-treasure-clue-inputs', 'exec'), env)
prepare = env['prepare']
capture_source = checked_text(getsource(previous.capture), {
    "range(4350, 8251, 25)": "range(4350, 9901, 25)",
    'str(INPUTS)': 'str(input_path(side))',
})
exec(compile(capture_source, __file__ + '::same-native-Maria-captures-and-longer-schedule', 'exec'), env)
capture = env['capture']

verify_source = checked_text(template.verify_source, {
    'report[\'frames\'] == previous.FRAME_COUNT': 'report[\'frames\'] == FRAME_COUNT',
    '4350 <= frame <= 8250': '4350 <= frame <= 9900',
    "len(planes) == (2 if ident == PAGED_ID else 1)":
        "len(planes) == (2 if ident in PAGED_IDS or (side == 'before' and ident == RECLAIMED_PAGE_ID) else 1)",
    "    assert outside['before'] == outside['after'], outside":
        """    assert outside['before'][:2] == outside['after'][:2], outside
    port_focus = verify_port_focus_frame(RETURN_FRAMES[2])""",
    'outside_exact_frames=list(RETURN_FRAMES)':
        'outside_exact_frames=list(RETURN_FRAMES[:2]), port_focus_frame=port_focus',
    'report[\'scripted_input_schedule\'] == base.load(INPUTS)':
        'report[\'scripted_input_schedule\'] == base.load(input_path(side))',
    'str(INPUTS): base.digest(INPUTS)}': 'str(INPUTS): base.digest(INPUTS), str(AFTER_INPUTS): base.digest(AFTER_INPUTS)}',
    'verified_revised_pages=len(REVISED_IDS) + 1': 'verified_revised_pages=len(REVISED_IDS) + len(PAGED_IDS)',
    'observed_Muramasa_pages_before_after=[2, 2]':
        'observed_two_page_records=sorted(PAGED_IDS), observed_reclaimed_page=RECLAIMED_PAGE_ID',
})
exec(compile(verify_source, __file__ + '::complete-portrait-masks-and-multipage-checks', 'exec'), env)
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

