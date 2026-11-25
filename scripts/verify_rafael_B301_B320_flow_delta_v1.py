"""Rerender changed layout bytes and pack the complete final pages for visual QA."""
from pathlib import Path
import sys
from types import FunctionType

from scripts import verify_rafael_B281_B300_visual_delta_v1 as previous
from scripts.refine_rafael_B301_B320_flow_v1 import MANUSCRIPT, PRIOR, ROOT


DELTA = ROOT / 'flow_delta_inputs_v1'
FRESH = ROOT / 'flow_delta_native_v1/compiled_native_pages.json'
FINAL = ROOT / 'final_native_pages_v1.json'
FINAL_SHEETS = ROOT / 'body_review_sheets_v1'
env = {
    **vars(previous), '__file__': __file__,
    'ORIGINAL': PRIOR, 'PLAN': ROOT / 'flow_plan_v2/automatic_plans.json',
    'FORMATTING': MANUSCRIPT, 'FIRST_NATIVE': ROOT / 'native_pages_v1/compiled_native_pages.json',
    'DELTA': DELTA, 'DELTA_MANUSCRIPT': DELTA / 'manuscript.json',
    'DELTA_PLAN': DELTA / 'automatic_plans.json', 'FRESH': FRESH,
    'FINAL': FINAL, 'SHEETS': ROOT / 'flow_delta_sheets_v1',
}
env['inputs'] = FunctionType(previous.inputs.__code__, env)


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        FunctionType(previous.prepare.__code__, env)()
    else:
        assert not sys.argv[1:]
        FunctionType(previous.combine.__code__, env)()
        pack = FunctionType(previous.body.__code__, {
            **previous.body.__globals__,
            'read_image': lambda path, expected: previous.read_image(Path(path), expected),
        })
        pack(FINAL_SHEETS, FINAL)
