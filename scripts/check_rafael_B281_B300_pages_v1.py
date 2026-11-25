"""Verify complete glyphs, native bounds and pages for Rafael B281–B300."""
from scripts import check_rafael_B261_B280_pages_v1 as previous
from scripts.plan_rafael_B281_B300_v1 import IDENTITY, MACROS
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    "len(qualified['three_logical_FI_records'])==3": "len(qualified['four_logical_macro_records'])==4",
})

if __name__ == '__main__':
    env = {**previous.native.env, 'IDENTITY': IDENTITY, 'MACRO_QUALIFICATION': MACROS, '__file__': __file__}
    exec(compile(source, __file__+'::same-native-guards-registered-Rafael3649', 'exec'), env)
    env['main']()
