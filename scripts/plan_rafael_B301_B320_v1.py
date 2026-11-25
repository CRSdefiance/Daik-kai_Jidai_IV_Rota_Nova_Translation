"""Measure the ten source name substitutions and plan native-width paragraphs."""
from pathlib import Path
import sys
from types import FunctionType

from scripts import plan_rafael_B281_B300_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B301_B320_contextual_v1 import BLOCKS, CURRENT, NAMES as GETTERS, OBJECTS, OUT, ROLES, ROOT


IDENTITY = ROOT / 'scoped_runtime_v1.json'
FORMATTING = ROOT / 'ordinary_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v1.json'
STAGED = ROOT / 'source_staged_layouts_v1.json'
MACROS = ROOT / 'native_macro_measurements_v1.json'
SOURCE = ROOT / 'initial_plan_v1/automatic_plans.json'

source = checked_text(previous.source, {
    "release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']":
        "release['all_predecessor_stage_dependencies_preserved'] and release['owned_Zaganos_surname_verified']",
    "assert token in ('FI', 'FA', 'FO')": "assert token == 'FI'",
    "assert len(checks) == 4": "assert len(checks) == 10",
    'four_logical_macro_records=checks': 'ten_logical_FI_records=checks',
    "'physical_speech_objects': 240, 'style_physical_speech_objects': 76":
        "'physical_speech_objects': 442, 'style_physical_speech_objects': 145",
    "'style_command_objects': 11": "'style_command_objects': 19",
    'Measured four default substitutions and the four FA, FI and FO paragraphs on Rafael3649.':
        'Measured four default substitutions and ten FI paragraphs on Rafael3894.',
})
env = {**previous.env, **globals()}
exec(compile(source, __file__ + '::registered-runtime-macro-bindings', 'exec'), env)
prepare = env['prepare']
qualify_source = FunctionType(previous.qualify_source.__code__, env)


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        planner = previous.previous.planner
        FunctionType(planner.main.__code__, {**planner.env, 'qualify_source': qualify_source, '__file__': __file__})()
