"""Keep all stored native assertions and add the qualified FE row-membership check."""
from scripts.check_editorial_stored_explicit_captain_v1 import source as previous,compound_storage
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    '                    rendered=painter(expanded)':
        "                    rendered=painter(expanded)\n                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-stored-ordinary-compound-branch-andFE-row-guards','exec'),globals())
