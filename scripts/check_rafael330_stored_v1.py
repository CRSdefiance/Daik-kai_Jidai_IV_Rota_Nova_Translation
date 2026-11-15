"""Reuse complete stored/native guards with current Rafael dependencies and FE child commands."""
from pathlib import Path
from scripts import check_rafael_early_tutorial_stored as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
source=checked_text(previous.source,{
    "    macros=load(macro_path);assert macros['runtime']==runtime":
        """    macros=load(macro_path)
    identity=load(Path('work/analysis/Rafael_B81_B84_formatting_20261105/scoped_names_macro_andconsumer_dependency_qualification_v1.json'))
    assert identity['runtime']==runtime and identity['complete_ARM9_COMMON_font_andactor_array_exact_to_qualified_runtime']
    ownpath=Path(identity['same_Rafael_default_macro_proof']);assert sha(ownpath.read_bytes())==identity['same_Rafael_default_macro_proof_sha256']
    own=load(ownpath);assert own['runtime']['ARM9_sha256']==runtime['ARM9_sha256'] and own['runtime']['COMMON_sha256']==runtime['COMMON_sha256']
    assert own['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10) and len(own['own_native_default_macro_cases']['cases'])==4
    assert sha(macro_path.read_bytes())==own['previous_complete_preamble_macro_proof_sha256']""",
    "macros['source_owned_FE_adapter']":"native['source_owned_FE_expected_value_adapter']",
})
exec(compile(source,__file__+'::same-stored-full-glyph-canary-parity-macro-andfinal-relative-checks','exec'),globals())
