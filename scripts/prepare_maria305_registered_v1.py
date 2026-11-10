"""Freeze305 complete mixed reviews over the exact719-entry registered predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_maria337_registered_v1.py').read_text(encoding='utf-8'), {
    'dk4tool.patch.maria337_release_v1':'dk4tool.patch.maria305_release_v1',
    'from scripts.meaning_maria337_clean_v1 import ROOT':"ROOT=Path('work/Maria_B176_B195_clean_20261110')",
    'maria_B125_B136':'maria_B176_B195',
    'translations/maria337_editorial_release_v1.json':'translations/maria305_editorial_release_v1.json',
    'work/maria330_release_v1/registered_release_verification.json':'work/maria390_B152_B175_release_v1/registered_release_verification.json',
    '==(716,114,51)':'==(719,114,54)',
    'stored_catalogue_all_v1/all335_stored_effective_body_bindings.json':'stored_catalogue_all_v1/all_stored_effective_body_bindings.json',
    "ROOT/'display_run_menu1_v1/run_plan.json',":"ROOT/'display_run_menu1_v1/run_plan.json',ROOT/'display_run_menu2_v1/run_plan.json',",
    'dk4tool/patch/maria337_release_v1.py':'dk4tool/patch/maria305_release_v1.py',
    "Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path(__file__)":
        "Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('scripts/finalize_maria305_research_v1.py'),Path(__file__)",
    "format='dk4-reviewed-maria337-release-v1',record_count=337,speech_count=335,ordinary_count=335,style_count=0,typed_choice_count=2,menu_count=1":
        "format='dk4-reviewed-maria305-release-v1',record_count=305,speech_count=294,ordinary_count=272,style_count=22,typed_choice_count=11,menu_count=5",
    'scoped_name_count=21,native_pages=339,relative_cases=430,FE_count=6':'scoped_name_count=27,native_pages=302,relative_cases=170,FE_count=16',
    'actual_frames=33202':'actual_frames=63843',
    "len(proof['changed_records'])==337":"len(proof['changed_records'])==305",
    'source_records=337,physical_body_candidates=335,native_pages=339':'source_records=305,physical_body_candidates=294,native_pages=302',
    'Qualified337 reviews over716-entry Maria330':'Qualified305 reviews over719-entry Maria390',
})
exec(compile(source,__file__+'::same-frozen-inputs-pure-complete-transaction-andparent-inverse','exec'),globals())
