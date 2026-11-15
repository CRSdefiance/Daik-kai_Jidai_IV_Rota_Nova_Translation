"""Render the reviewed Rafael paragraphs on the exact registered runtime."""
from scripts import check_rafael_B166_B167_ordinary_v1 as native
from scripts.plan_rafael_B261_B280_v1 import IDENTITY, MACROS
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(native.source, {
    "identity['exact_unchanged_actor0_macro_dependencies']":
        "identity['all_scoped_getters_fresh_on_registered_ARM9'] and qualified['runtime']==ctx.receipt()",
    "assert qualified['full_name']=='Rafael Castor'":
        "assert len(qualified['three_logical_FI_records'])==3 and all("
        "case['output_hex']==b'Rafael Castor'.hex() "
        "for case in qualified['current_default_expansions']['FU']['cases'])",
})

if __name__ == '__main__':
    env = {**native.env, 'IDENTITY': IDENTITY, 'MACRO_QUALIFICATION': MACROS, '__file__': __file__}
    exec(compile(source, __file__ + '::fresh-native-macro-qualification', 'exec'), env)
    env['main']()
