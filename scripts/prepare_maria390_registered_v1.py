"""Freeze390 completed reviews over the exact718-entry registered predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria337_registered_v1.py').read_text(encoding='utf-8'),{
    'dk4tool.patch.maria337_release_v1':'dk4tool.patch.maria390_release_v1',
    'from scripts.meaning_maria337_clean_v1 import ROOT':"ROOT=Path('work/Maria_B152_B175_clean_20261109')",
    'maria_B125_B136':'maria_B152_B175',
    'translations/maria337_editorial_release_v1.json':'translations/maria390_editorial_release_v1.json',
    'work/maria330_release_v1/registered_release_verification.json':'work/maria335_B137_B151_release_v1/registered_release_verification.json',
    'reconstruction_v1/reconstruction.json':'reconstruction_v3/reconstruction.json',
    '==(716,114,51)':'==(718,114,53)',
    'stored_v1/stored_native_verification.json':'stored_v3/stored_native_verification.json',
    'stored_catalogue_all_v1/all335_stored_effective_body_bindings.json':'stored_catalogue_all_v2/all373_stored_effective_body_bindings.json',
    'loaders_v1/verification.json':'loaders_v3/verification.json',
    'offline_display_approval_v1.json':'offline_display_approval_v2.json',
    "extra=dict(research_completion=str(readypath),sealed_inputs=str(sealed))":
        "extra=dict(research_completion=str(readypath),sealed_inputs=str(sealed),owned_FE_padding_qualification=str(ROOT/'reconstruction_v2/FE_storage_alignment.json'))",
    "ROOT/'display_run_menu1_v1/run_plan.json',":
        "ROOT/'display_run_menu1_v1/run_plan.json',ROOT/'display_run_menu2_v1/run_plan.json',ROOT/'wine_display_run_v1/run_plan.json',",
    'dk4tool/patch/maria337_release_v1.py':'dk4tool/patch/maria390_release_v1.py',
    "Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path(__file__)":
        "Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('dk4tool/script/reviewed_FE_storage_padding_v2.py'),Path(__file__)",
    "format='dk4-reviewed-maria337-release-v1',record_count=337,speech_count=335,ordinary_count=335,style_count=0,typed_choice_count=2,menu_count=1":
        "format='dk4-reviewed-maria390-release-v1',record_count=390,speech_count=373,ordinary_count=373,style_count=0,typed_choice_count=17,menu_count=8",
    'scoped_name_count=21,native_pages=339,relative_cases=430,FE_count=6':'scoped_name_count=47,native_pages=373,relative_cases=610,FE_count=32',
    'actual_frames=33202':'actual_frames=63284',
    "len(proof['changed_records'])==337":"len(proof['changed_records'])==390",
    'source_records=337,physical_body_candidates=335,native_pages=339':'source_records=390,physical_body_candidates=373,native_pages=373',
    'Qualified337 reviews over716-entry Maria330':'Qualified390 reviews over718-entry Maria335 B137-B151',
})
exec(compile(source,__file__+'::same-frozen-inputs-pure-complete-transaction-andparent-inverse-contract','exec'),globals())
