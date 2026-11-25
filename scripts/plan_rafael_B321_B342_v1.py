"""Use the proven Rafael formatter for the complete final-SC0 manuscript."""
from pathlib import Path
import linecache
import sys
from types import FunctionType

from scripts import plan_rafael_B281_B300_v1 as previous
from scripts import check_rafael_compiled_pages_v2 as native_tools
from scripts.checkpoint_rafael_B321_B331_contextual_v1 import INPUTS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B321_B342_contextual_v1 import BLOCKS, OUT, ROOT


_, CURRENT, OBJECTS, GETTERS, ROLES = INPUTS
IDENTITY = ROOT / 'scoped_runtime_v1.json'
FORMATTING = ROOT / 'ordinary_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v1.json'
STAGED = ROOT / 'source_staged_layouts_v1.json'
MACROS = ROOT / 'native_macro_measurements_v1.json'

source = checked_text(previous.source, {
    "release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']":
        "release['all_predecessor_stage_dependencies_preserved'] and release['all_other_files_components_graphics_names_andruntime_exact_to_parent']",
    'assert len(checks) == 4': 'assert len(checks) == 11',
    'four_logical_macro_records=checks': 'eleven_logical_macro_records=checks',
    "    expand = env['expand']": """    expand = env['expand']
    fe_adapter = checked_text(load(ADAPTERS)['source_owned_FE_adapter'], {
        "b'Hodram'": "b'Rafael'", "b'Bergstrom'": "b'Castor'",
        "b'Bergstrom Fleet'": "b'Castor Co.'",
    })
    fe_env = dict(native_tools.FE_expand.__globals__)
    exec(compile(fe_adapter, __file__ + '::original-null-actor-system-wrapper', 'exec'), fe_env)
    expand_fe = fe_env['expand']""",
    "        native = ctx.execute(expand, row['english'].encode('ascii'), row['source_selector'])":
        """        if row['kind'] == 'system-FE':
            assert row['source_selector'] == 254
            native = ctx.execute(expand_fe, row['english'].encode('ascii'))
        else:
            native = ctx.execute(expand, row['english'].encode('ascii'), row['source_selector'])""",
    'source_owned_progressive_adapter=adapter,': 'source_owned_progressive_adapter=adapter, source_owned_FE_adapter=fe_adapter,',
    "'physical_speech_objects': 240, 'style_physical_speech_objects': 76":
        "'physical_speech_objects': 540, 'style_physical_speech_objects': 298",
    "'style_command_objects': 11": "'style_command_objects': 48",
    'Measured four default substitutions and the four FA, FI and FO paragraphs on Rafael3649.':
        'Measured four default substitutions and all eleven FI or FA paragraphs on Rafael4347.',
})
env = {**previous.env, **globals()}
exec(compile(source, __file__ + '::same-native-macro-and-paragraph-preparation', 'exec'), env)
prepare = env['prepare']
qualify_source = FunctionType(previous.qualify_source.__code__, env)


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        planner = previous.previous.planner
        planned_source = checked_text(planner.source, {
            "assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077']":
                "assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077','DK4_MES_B336_R0084']",
            "result['lines'][0 if row['id']=='DK4_MES_B56_R0077' else 3]":
                "result['lines'][{'DK4_MES_B56_R0077': 0, 'DK4_MES_B336_R0084': 1}.get(row['id'], 3)]",
        })
        planned_env = {**planner.env, 'qualify_source': qualify_source, '__file__': __file__}
        filename = __file__ + '::same-planner-with-exact-sentence-ending-retention'
        linecache.cache[filename] = (len(planned_source), None, planned_source.splitlines(keepends=True), filename)
        exec(compile(planned_source, filename, 'exec'), planned_env)
        planned_env['main']()
