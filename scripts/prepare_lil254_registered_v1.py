"""Freeze the approved Lil254 review against the exact registered predecessor."""

from scripts.prepare_lil278_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Freeze 278 complete reviews over the exact 728-entry registered predecessor.':
        'Freeze 254 complete reviews over the exact 729-entry registered predecessor.',
    'Lil278_B299_B311_clean_20261110': 'Lil254_B312_B319_clean_20261110',
    'lil_B299_B311_': 'lil_B312_B319_',
    'lil361_B283_B298_release_v1': 'lil278_B299_B311_release_v1',
    '(728,114,63)': '(729,114,64)',
    'lil278': 'lil254',
    'record_count=278,speech_count=272,ordinary_count=133,style_count=139,typed_choice_count=6,menu_count=3':
        'record_count=254,speech_count=246,ordinary_count=88,style_count=158,typed_choice_count=8,menu_count=3',
    'scoped_name_count=10,native_pages=280,relative_cases=670,FE_count=8,FE_owner_IDs=[],captain=2,actual_frames=25121':
        'scoped_name_count=10,native_pages=251,relative_cases=330,FE_count=7,FE_owner_IDs=[],captain=2,actual_frames=25841',
    "len(proof['changed_records'])==278": "len(proof['changed_records'])==254",
    'source_records=278,physical_body_candidates=272,native_pages=280':
        'source_records=254,physical_body_candidates=246,native_pages=251',
    'Qualified 278 reviews over the 728-entry Lil361 release': 'Qualified 254 reviews over the 729-entry Lil278 release',
})

exec(compile(source, __file__, 'exec'), globals())
