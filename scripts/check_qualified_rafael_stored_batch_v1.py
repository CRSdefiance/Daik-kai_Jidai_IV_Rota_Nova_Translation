"""Reuse the complete Rafael stored consumer with an explicit scoped identity proof."""
from scripts import check_rafael330_stored_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows = previous.check_FE_rows
progressive_expand = previous.progressive_expand
FE_expand = previous.FE_expand
source = checked_text(previous.source, {
    "for arg in ('reconstruction','native','out'):": "for arg in ('reconstruction','native','identity','out'):",
    "identity=load(Path('work/analysis/Rafael_B81_B84_formatting_20261105/scoped_names_macro_andconsumer_dependency_qualification_v1.json'))":
        "identity=load(args.identity)",
    "identity['complete_ARM9_COMMON_font_andactor_array_exact_to_qualified_runtime']":
        "identity['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']",
    "[args.reconstruction,args.native,Path(__file__)]":
        "[args.reconstruction,args.native,args.identity,macro_path,ownpath,Path(__file__)]",
})
exec(compile(source, __file__+'::same-complete-stored-page-andbranch-checks-explicit-identity', 'exec'), globals())
