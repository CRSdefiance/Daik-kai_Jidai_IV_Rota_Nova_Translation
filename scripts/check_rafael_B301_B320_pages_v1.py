"""Check all compiled pages with the original glyph and pagination consumers."""
from scripts import check_rafael_B281_B300_pages_v1 as previous
from scripts.plan_rafael_B301_B320_v1 import IDENTITY, MACROS
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    "len(qualified['four_logical_macro_records'])==4": "len(qualified['ten_logical_FI_records'])==10",
})

if __name__ == '__main__':
    env = {**previous.previous.native.env, 'IDENTITY': IDENTITY, 'MACRO_QUALIFICATION': MACROS, '__file__': __file__}
    exec(compile(source, __file__ + '::original-native-pages-Rafael3894', 'exec'), env)
    env['main']()
