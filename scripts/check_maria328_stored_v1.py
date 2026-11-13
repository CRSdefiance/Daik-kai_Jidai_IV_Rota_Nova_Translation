"""Keep every stored native guard and check FE rows on the exact328-object rebuild."""
from scripts import check_editorial_stored_explicit_captain_v1 as previous
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '                    rendered=painter(expanded)':
        "                    rendered=painter(expanded)\n                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
})
if __name__=='__main__':
    env={**vars(previous),**globals()}
    exec(compile(source,__file__+'::same-stored-compound-glyph-bounds-parity-branch-guards-plus-FE-rows','exec'),env)
