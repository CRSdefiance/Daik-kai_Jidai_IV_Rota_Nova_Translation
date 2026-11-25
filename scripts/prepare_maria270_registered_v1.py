"""Freeze completed Maria270 research over the registered market-corrected parent."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_maria301_registered_v1.py').read_text(encoding='utf-8'),{
    'maria301_release_v1':'maria270_release_v1','Maria_B0_B32_clean_20261109':'Maria_B37_B50_clean_20261109',
    'maria_B0_B32_final_review_v1':'maria_B37_B49_final_review_v1',
    'maria301_editorial_release_v1':'maria270_editorial_release_v1',
    'work/hodram_residual_release_v1/registered_release_verification.json':'work/market_goods_info_terminator_release_v1/registered_release_verification.json',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'stored270_reconstruction_v1/reconstruction.json'",
    '(708,114,43)':'(710,114,45)',
    "ROOT/'stored_v1/stored_native_verification.json'":"ROOT/'stored270_v1/stored_native_verification.json'",
    "ROOT/'stored_catalogue_all_v1/all299_stored_effective_body_bindings.json'":"ROOT/'stored270_catalogue_v1/all266_stored_effective_body_bindings.json'",
    "ROOT/'loaders_v1/verification.json'":"ROOT/'loaders270_v1/verification.json'",
    "ROOT/'offline_display_approval_v1.json'":"ROOT/'offline270_display_approval_v2.json'",
    "ROOT/'gameplay_review_v1.json'":"ROOT/'gameplay270_review_v1.json'",
    'translations/maria_B0_B32_scoped_names_final_v1.json':'translations/maria_B37_B49_scoped_names_final_v1.json',
    "extra = dict(research_completion=str(ready_path),sealed_inputs=str(sealed))":
        "extra = dict(research_completion=str(ready_path),sealed_inputs=str(sealed),market_parent_qualification=str(ROOT/'market_parent_qualification_v1.json'))",
    'record_count=301,speech_count=299,typed_choice_count=2,menu_count=1':'record_count=270,speech_count=266,typed_choice_count=4,menu_count=2',
    'style_count=7,scoped_name_count=36,native_pages=303,relative_cases=635,FE_count=0,captain=3,actual_frames=42683':
        'style_count=0,scoped_name_count=28,native_pages=272,relative_cases=480,FE_count=1,captain=3,actual_frames=41924',
    "len(proof['changed_records']) == 301":"len(proof['changed_records']) == 270",
    'Qualified301 reviewed records over the708-entry cumulative parent':'Qualified270 reviewed records over the710-entry market-corrected cumulative parent',
})
exec(compile(source,__file__+'::same-sealed-research-preparation-exact-registered-market-parent','exec'),globals())
