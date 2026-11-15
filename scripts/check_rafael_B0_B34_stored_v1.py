"""Reuse complete stored speech/page/branch checks with this batch's native macro proof."""
from scripts import check_qualified_rafael_stored_with_fu_v1 as previous
from scripts.plan_rafael_B0_B34_v1 import MACROS
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "identity['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']":
        "identity['exact_unchanged_actor0_macro_dependencies'] and identity['all_scoped_getters_fresh_on_registered_ARM9']",
    "ownpath=Path(identity['same_Rafael_default_macro_proof']);assert sha(ownpath.read_bytes())==identity['same_Rafael_default_macro_proof_sha256']":
        "ownpath=MACROS;assert sha(ownpath.read_bytes())==identity['evidence'][str(MACROS)]",
    "assert own['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10) and len(own['own_native_default_macro_cases']['cases'])==4":
        "assert own['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10,FU=13) and len(own['sixteen_logical_macro_records'])==16 and len(own['current_default_expansions']['FU']['cases'])==4",
    "own['previous_complete_preamble_macro_proof_sha256']":"own['evidence'][str(macro_path)]",
    "identity['macro_widths']['FU']==78":"6*identity['macro_ascii_lengths']['FU']==78",
})
env={**vars(previous),'MACROS':MACROS,'__file__':__file__}
exec(compile(source,__file__+'::same-stored-glyph-pagination-andbranch-guards','exec'),env)

if __name__=='__main__':env['main']()
