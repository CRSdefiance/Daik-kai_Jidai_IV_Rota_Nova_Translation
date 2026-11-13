"""Use existing native proofs for this prose-only input; check exact FE glyph rows too."""
from scripts import check_editorial_compiled_pages_v3 as previous
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '                rendered=painter(expected)':
        "                rendered=painter(expected)\n                rendered['planned_native_row_comparison']=check_FE_rows(expected,rendered)",
    '        FE_factory_calibration=calibration,':
        '        FE_actual_glyph_row_membership_checked=True,FE_factory_calibration=calibration,',
})
exec(compile(source,__file__+'::same-native-proof-plus-FE-row-membership','exec'),globals())
