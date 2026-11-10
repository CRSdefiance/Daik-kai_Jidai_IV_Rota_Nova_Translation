"""Preserve the exact44-byte command while terminating B164R99 before its padding."""
from scripts.amend_maria390_FE_storage_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load

source=checked_text(previous,{
    'from dk4tool.script.reviewed_FE_storage_padding_v1 import remove_FE_text_parity_space':
        'from dk4tool.script.reviewed_FE_storage_padding_v2 import replace_FE_text_parity_space_with_NUL as remove_FE_text_parity_space',
    "Path('dk4tool/script/reviewed_FE_storage_padding_v1.py')":"Path('dk4tool/script/reviewed_FE_storage_padding_v2.py')",
})
if __name__=='__main__':
    proof=load('work/Maria_B152_B175_clean_20261109/FE_storage_diagnostic_v1.json')
    assert proof['exact_stored_alignment_space_causes_extra_row'] and proof['unpadded_compiled_plane_matches_directly_viewed_native_plane']
    exec(compile(source,__file__+'::odd-length-FE-owned-single-byte-NUL-full-extent-andinverse-guards','exec'),globals())
