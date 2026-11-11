"""Freeze the approved Lil261 review against the exact registered predecessor."""

from scripts.prepare_lil254_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "Freeze 254 complete reviews over the exact 729-entry registered predecessor.": "Freeze 261 complete reviews over the exact 730-entry registered predecessor.",
    "Lil254_B312_B319_clean_20261110": "Lil261_B323_B335_clean_20261110",
    "lil_B312_B319_": "lil_B323_B335_",
    "work/lil278_B299_B311_release_v1": "work/lil254_B312_B319_release_v1",
    "(729,114,64)": "(730,114,65)",
    "lil254_release_v1": "lil261_release_v1",
    "lil254_editorial_release_v1": "lil261_editorial_release_v1",
    "dk4-reviewed-lil254-release-v1": "dk4-reviewed-lil261-release-v1",
    "finalize_lil254_research_v1": "finalize_lil261_research_v1",
    "approve_lil254_actual_v1": "approve_lil261_actual_v1",
    "record_count=254,speech_count=246,ordinary_count=88,style_count=158,typed_choice_count=8,menu_count=3": "record_count=261,speech_count=255,ordinary_count=136,style_count=119,typed_choice_count=6,menu_count=3",
    "scoped_name_count=10,native_pages=251,relative_cases=330,FE_count=7,FE_owner_IDs=[],captain=2,actual_frames=25841": "scoped_name_count=9,native_pages=258,relative_cases=455,FE_count=13,FE_owner_IDs=[],captain=2,actual_frames=26561",
    "len(proof['changed_records'])==254": "len(proof['changed_records'])==261",
    "source_records=254,physical_body_candidates=246,native_pages=251": "source_records=261,physical_body_candidates=255,native_pages=258",
    "Qualified 254 reviews over the 729-entry Lil278 release": "Qualified 261 reviews over the 730-entry Lil254 release",
})
exec(compile(source, __file__, 'exec'), globals())
