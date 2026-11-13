"""Check stored539 pages and relocated branches with pinned Rafael consumer proofs."""
from pathlib import Path
from scripts import check_rafael_early_tutorial_stored as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
FRESH=Path('work/analysis/Rafael_B61_B80_formatting_20261104/speech_native_resume_v3/compiled_native_pages.json')
OWN=Path('work/analysis/Rafael_B61_B80_formatting_20261104/own_default_macros_andsource_qualification_v1.json')
QUAL=Path('work/analysis/Rafael_B61_B80_latest_runtime_20261104/dependency_qualification.json')

source=checked_text(previous.source,{
    "    adapter=full_native['source_owned_target_page_adapter']":
        """    assert sha(Path(native['previous_native']).read_bytes())==native['previous_native_sha256']
    assert sha(FRESH.read_bytes())==full_native['evidence'][str(FRESH)]
    fresh=load(FRESH);assert fresh['runtime']==runtime
    adapter=fresh['source_owned_target_page_adapter']""",
    "    macros=load(macro_path);assert macros['runtime']==runtime":
        """    macros=load(macro_path);own=load(OWN);qualification=load(QUAL)
    assert own['runtime']==qualification['runtime']==runtime
    assert own['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10)
    assert len(own['own_native_default_macro_cases']['cases'])==4
    assert sha(macro_path.read_bytes())==own['previous_complete_preamble_macro_proof_sha256']
    assert sha(QUAL.read_bytes())==own['source_dispatch_ABI_reused_by_exact_dependency_qualification_sha256']
    assert qualification['native_name_consumers_anddefault_Rafael_macro_dependencies_compatible']""",
    "macros['source_owned_FE_adapter']":"native['source_owned_FE_expected_value_adapter']",
    "[args.reconstruction,args.native,Path(__file__)]":
        "[args.reconstruction,args.native,FRESH,OWN,QUAL,macro_path,Path(previous.__file__),Path(__file__)]",
})
exec(compile(source,__file__+'::same-stored-consumers-andrelative-branches-current-qualified-Rafael','exec'),globals())
