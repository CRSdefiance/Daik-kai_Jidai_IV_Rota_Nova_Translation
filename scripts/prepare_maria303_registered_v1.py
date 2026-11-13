"""Freeze303 completed reviews over the exact713-entry cumulative parent."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_maria301_registered_v1.py').read_text(encoding='utf-8'), {
    'maria301_release_v1': 'maria303_release_v1',
    'Maria_B0_B32_clean_20261109': 'Maria_B58_B70_clean_20261109',
    'maria_B0_B32_final_review_v1': 'maria_B58_B70_final_review_v1',
    'maria301_editorial_release_v1': 'maria303_editorial_release_v1',
    'work/hodram_residual_release_v1/registered_release_verification.json': 'work/maria310_release_v1/registered_release_verification.json',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'": "ROOT/'reconstruction_v2/reconstruction.json'",
    '(708,114,43)': '(713,114,48)',
    'translations/maria_B0_B32_scoped_names_final_v1.json': 'translations/maria_B58_B70_scoped_names_final_v1.json',
    "extra = dict(research_completion=str(ready_path),sealed_inputs=str(sealed))":
        "extra = dict(research_completion=str(ready_path),sealed_inputs=str(sealed),source_alignment_qualification=str(ROOT/'source_alignment_qualification_v1.json'))",
    'record_count=301,speech_count=299,typed_choice_count=2,menu_count=1': 'record_count=303,speech_count=299,typed_choice_count=4,menu_count=2',
    'style_count=7,scoped_name_count=36,native_pages=303,relative_cases=635,FE_count=0,captain=3,actual_frames=42683': 'style_count=0,scoped_name_count=20,native_pages=299,relative_cases=120,FE_count=12,captain=3,actual_frames=48322',
    "format='dk4-reviewed-maria301-release-v1'": "format='dk4-reviewed-maria303-release-v1'",
    "    dependencies += [r['run_plan'] for r in load(evidence['actual'])['runs']]":
        "    dependencies += [r['run_plan'] for r in load(evidence['actual'])['runs']]\n    dependencies += [Path('dk4tool/script/maria303_source_alignment_v1.py'),Path('scripts/qualify_maria303_source_alignment_v1.py')]",
    "len(proof['changed_records']) == 301": "len(proof['changed_records']) == 303",
    'Qualified301 reviewed records over the708-entry cumulative parent': 'Qualified303 reviewed records over the713-entry cumulative parent',
})
exec(compile(source, __file__+'::same-sealed-source-current-native-branch-loader-gameplay-contract303', 'exec'), globals())
