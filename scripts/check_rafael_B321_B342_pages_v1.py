"""Check every new page with the original native glyph and pagination consumers."""
from scripts import check_rafael_B281_B300_pages_v1 as previous
from scripts.plan_rafael_B321_B342_v1 import IDENTITY, MACROS
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    "len(qualified['four_logical_macro_records'])==4": "len(qualified['eleven_logical_macro_records'])==11",
    "identity['all_scoped_getters_fresh_on_registered_ARM9']":
        "identity['exact_prior_ARM9_COMMON_actor_root_and_font']",
})


if __name__ == '__main__':
    env = {**previous.previous.native.env, 'IDENTITY': IDENTITY, 'MACRO_QUALIFICATION': MACROS, '__file__': __file__}
    exec(compile(source, __file__ + '::same-native-glyph-and-page-guards-Rafael4347', 'exec'), env)
    env['main']()
