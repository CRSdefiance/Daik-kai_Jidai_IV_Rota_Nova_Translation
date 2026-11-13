"""Keep complete stored-page andbranch checks with qualified current macro/renderer reuse."""
from pathlib import Path
from scripts import check_rafael_early_tutorial_stored as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
QUAL=Path('work/analysis/Rafael_B51_B60_current_runtime_20261104/dependency_qualification.json')

source=checked_text(previous.source,{
    "    adapter=full_native['source_owned_target_page_adapter']":
        """    qualification=load(QUAL)
    assert qualification['runtime']==runtime and qualification['previously_rendered253_body_pages_andfour_captions_qualify_for_exact_reuse']
    adapter=checked_text(full_native['source_owned_target_page_adapter'],{
        qualification['previous_runtime']['ARM9_sha256']:runtime['ARM9_sha256'],
    })""",
    "    macros=load(macro_path);assert macros['runtime']==runtime":
        """    macros=load(macro_path)
    assert macros['runtime']['ARM9_sha256']==qualification['previous_runtime']['ARM9_sha256']
    assert macros['runtime']['COMMON_sha256']==runtime['COMMON_sha256']
    assert len(qualification['own_captain0_default_macro_alignments']['cases'])==4""",
    "[args.reconstruction,args.native,Path(__file__)]":
        "[args.reconstruction,args.native,QUAL,Path(__file__)]",
})
exec(compile(source,__file__+'::same-parity-native-pages-and76-relocated-branches-current-qualified-Rafael','exec'),globals())
