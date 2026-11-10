"""Freeze335 complete reviews over the exact717-entry registered predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria337_registered_v1.py').read_text(encoding='utf-8'),{
    'dk4tool.patch.maria337_release_v1':'dk4tool.patch.maria335_B137_B151_release_v1',
    'scripts.meaning_maria337_clean_v1':'scripts.meaning_maria335_B137_B151_v1',
    'maria_B125_B136':'maria_B137_B151',
    'translations/maria337_editorial_release_v1.json':'translations/maria335_B137_B151_editorial_release_v1.json',
    'work/maria330_release_v1/registered_release_verification.json':'work/maria337_release_v1/registered_release_verification.json',
    'reconstruction_v1/reconstruction.json':'reconstruction_v2/reconstruction.json',
    '==(716,114,51)':'==(717,114,52)',
    'all335_stored_effective_body_bindings.json':'all333_stored_effective_body_bindings.json',
    "extra=dict(research_completion=str(readypath),sealed_inputs=str(sealed))":
        "extra=dict(research_completion=str(readypath),sealed_inputs=str(sealed),inherited_alignment_qualification=str(ROOT/'inherited_alignment_guard_v1.json'))",
    'dk4tool/patch/maria337_release_v1.py':'dk4tool/patch/maria335_B137_B151_release_v1.py',
    "Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path(__file__)":
        "Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('scripts/rebuild_maria335_B137_B151_reviewed_v1.py'),Path('scripts/rebuild_maria335_B137_B151_reviewed_v2.py'),Path(__file__)",
    "format='dk4-reviewed-maria337-release-v1',record_count=337,speech_count=335,ordinary_count=335":
        "format='dk4-reviewed-maria335-b137-b151-release-v1',record_count=335,speech_count=333,ordinary_count=333",
    'scoped_name_count=21,native_pages=339,relative_cases=430,FE_count=6':'scoped_name_count=26,native_pages=333,relative_cases=100,FE_count=18',
    'actual_frames=33202':'actual_frames=31522',
    "len(proof['changed_records'])==337":"len(proof['changed_records'])==335",
    'source_records=337,physical_body_candidates=335,native_pages=339':'source_records=335,physical_body_candidates=333,native_pages=333',
    'Qualified337 reviews over716-entry Maria330':'Qualified335 reviews over717-entry Maria337',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-frozen-inputs-complete-parent-target-inverse-contract','exec'),globals())
