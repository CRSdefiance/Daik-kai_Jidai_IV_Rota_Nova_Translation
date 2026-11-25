"""Check the final native layout changes and carry forward inspected unchanged pages."""
import sys
from types import FunctionType

from scripts import verify_rafael_B281_B300_visual_delta_v1 as previous
from scripts.verify_rafael_B301_B320_flow_delta_v1 import FINAL as INSPECTED, ROOT
from scripts.refine_rafael_B301_B320_plan_v1 import MANUSCRIPT


DELTA = ROOT / 'visual_delta_inputs_v1'
FRESH = ROOT / 'visual_delta_native_v1/compiled_native_pages.json'
FINAL = ROOT / 'final_native_pages_v2.json'
PLAN = ROOT / 'visual_plan_v1/automatic_plans.json'
SHEETS = ROOT / 'visual_delta_sheets_v1'
env = {
    **vars(previous), '__file__': __file__, 'ORIGINAL': ROOT / 'flow_plan_v2/automatic_plans.json',
    'PLAN': PLAN, 'FORMATTING': MANUSCRIPT, 'FIRST_NATIVE': INSPECTED,
    'DELTA': DELTA, 'DELTA_MANUSCRIPT': DELTA / 'manuscript.json',
    'DELTA_PLAN': DELTA / 'automatic_plans.json', 'FRESH': FRESH, 'FINAL': FINAL, 'SHEETS': SHEETS,
}
env['inputs'] = FunctionType(previous.inputs.__code__, env)


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        FunctionType(previous.prepare.__code__, env)()
    else:
        assert not sys.argv[1:]
        FunctionType(previous.combine.__code__, env)()
