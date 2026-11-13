"""Run the qualified Rafael planner on the final 187 ordinary layouts."""
import inspect
import sys
from types import FunctionType

from scripts import check_rafael_B166_B167_ordinary_v1 as native
from scripts import plan_rafael_B166_B167_ordinary_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B170_B176_contextual_v1 import CURRENT, IDENTITY, OUT as PROSE, ROOT, STAGED as HEADINGS


FORMATTING = ROOT / 'ordinary_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v1.json'
STAGED = ROOT / 'source_staged_FE_inputs_v1.json'
MACROS = previous.MACROS
TOKEN = previous.TOKEN
PLAIN_FE = {241, 244, 64}

prepare_source = checked_text(inspect.getsource(previous.prepare), {
    'if row[\'source_record_index\'] not in PLAIN_FE:': "if row['id'] in HEADINGS:",
    '                staged.append(row)': "                row['FE_layout_finding'] = 'Keep every source patron heading on its own structural row above the response.'\n                staged.append(row)",
    "            row['source_FE_presentation_kind']='Ordinary FE prose within a source-qualified exchange'":
        "            assert row['source_record_index'] in PLAIN_FE\n            row['source_FE_presentation_kind']='Source modal prose or applause without a separate heading'",
    '==(164,22)': '==(187,3)',
    'ordinary+staged)==12': 'ordinary+staged)==2',
    "'physical_speech_objects':164": "'physical_speech_objects':187",
    "'complete_contextual_batch_records':186": "'complete_contextual_batch_records':190",
    '164 ordinary records ready for fresh wrapping and 22 source-staged FE inputs isolated for layout checks.':
        '187 ordinary records and three source-staged patron panels ready for fresh display checks.',
})
exec(compile(prepare_source, __file__+'::same-logical-and-macro-preparation', 'exec'), {**vars(previous), **globals()}, globals())

scope = checked_text(inspect.getsource(previous.qualify_source), {
    "doc['blocks']==[166,167]": "doc['blocks']==list(range(170,177))",
    'len(bindings)==164': 'len(bindings)==187',
})
scope_env = {**previous.qualify_source.__globals__, 'CURRENT': CURRENT, 'IDENTITY': IDENTITY}
exec(compile(scope, __file__+'::exact-source-and-current-scope', 'exec'), scope_env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1] == '--native':
        del sys.argv[1]
        FunctionType(native.env['main'].__code__, {**native.env, 'IDENTITY': IDENTITY, '__file__': __file__})()
    else:
        FunctionType(previous.env['main'].__code__,
                     {**previous.env, 'qualify_source': scope_env['qualify_source'], '__file__': __file__})()
