"""Apply the verified formatter to this batch's complete, source-bound prose."""
import inspect
from pathlib import Path
import sys
from types import FunctionType

from scripts import plan_rafael_B261_B280_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B281_B300_contextual_v1 import BLOCKS, INPUTS, OUT, ROOT


_, CURRENT, OBJECTS, GETTERS, ROLES = INPUTS
IDENTITY = ROOT/'scoped_runtime_v1.json'
FORMATTING = ROOT/'ordinary_formatting_manuscript_v1.json'
PREFERENCES = ROOT/'ordinary_visual_preferences_v1.json'
STAGED = ROOT/'source_staged_layouts_v1.json'
MACROS = ROOT/'native_macro_measurements_v1.json'

source = checked_text(inspect.getsource(previous.prepare), {
    "release['all_preceding_eight_stages_and_exclusive_field_preserved']":
        "release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']",
    "        assert row['native_literal_tokens'] == ['FI']":
        "        token, = row['native_literal_tokens']\n        assert token in ('FI', 'FA', 'FO')",
    "row['english'].replace('FI', measured['FI'])": "row['english'].replace(token, measured[token])",
    "    assert len(checks) == 3": "    assert len(checks) == 4",
    'three_logical_FI_records=checks': 'four_logical_macro_records=checks',
    "'physical_speech_objects': 130, 'style_physical_speech_objects': 16":
        "'physical_speech_objects': 240, 'style_physical_speech_objects': 76",
    "'style_command_objects': 2": "'style_command_objects': 11",
    'Measured four default substitutions and all three FI-bearing logical paragraphs on Rafael3514.':
        'Measured four default substitutions and the four FA, FI and FO paragraphs on Rafael3649.',
})
env = {**vars(previous), **globals()}
exec(compile(source, __file__+'::current-registered-macros-and-paragraphs', 'exec'), env)
prepare = env['prepare']
qualify_source = FunctionType(previous.qualify_source.__code__, env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        planner = previous.planner
        FunctionType(planner.main.__code__, {**planner.env, 'qualify_source': qualify_source, '__file__': __file__})()
