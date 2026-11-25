"""Use the original native glyph and pagination checks for every residual speech."""
from scripts import check_rafael_B281_B300_pages_v1 as previous
from scripts.plan_rafael_B0_B34_v1 import IDENTITY, MACROS
from scripts.source_locked_derivation_v5118 import checked_text


source=checked_text(previous.source,{
    "len(qualified['four_logical_macro_records'])==4":"len(qualified['sixteen_logical_macro_records'])==16",
})


if __name__=='__main__':
    env={**previous.previous.native.env,'IDENTITY':IDENTITY,'MACRO_QUALIFICATION':MACROS,'__file__':__file__}
    exec(compile(source,__file__+'::same-native-glyph-and-page-checks','exec'),env)
    env['main']()
