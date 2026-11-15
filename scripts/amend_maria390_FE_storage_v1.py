"""Reuse the qualified reversible FE storage amendment for the exact B164R99 owner."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/amend_maria310_FE_storage_v2.py').read_text(encoding='utf-8'),{
    'from scripts.meaning_maria_B51_B52_clean_v1 import ROOT':
        "ROOT=Path('work/Maria_B152_B175_clean_20261109')",
    'work/maria_B50_release_v1/registered_release_verification.json':'work/maria335_B137_B151_release_v1/registered_release_verification.json',
    "g['block']==54":"g['block']==164",
    "r['id']=='DK4_MES_B54_R0507'":"r['id']=='DK4_MES_B164_R0099'",
    "row['source_reference']['offset']==4509":"row['source_reference']==load(ROOT/'FE_storage_diagnostic_v1.json')['source_reference']",
    'blocks[54]':'blocks[164]',
    "out/'B54_RESEARCH_ONLY.bin'":"out/'B164_RESEARCH_ONLY.bin'",
    'inverse[54]':'inverse[164]',
    'all318_compiled_native_pages_unchanged':'all373_compiled_native_pages_unchanged',
    "new['producers'].update":"new['evidence'].update",
    'Preserve Maria310 native FE storage alignment research and all original318 compiled pages.':'Preserve Maria390 exact B164R99 FE padding repair and all373 compiled pages.',
    'Qualified source-bound FE storage alignment;604 commands/132 relative sites and318 compiled pages preserved;':'Qualified B164R99 storage alignment;all679 commands/122 relative sites and373 compiled pages preserved;',
})
if __name__=='__main__':
    proof=load('work/Maria_B152_B175_clean_20261109/FE_storage_diagnostic_v1.json')
    assert proof['exact_stored_alignment_space_causes_extra_row'] and proof['unpadded_compiled_plane_matches_directly_viewed_native_plane']
    exec(compile(source,__file__+'::same-scoped-padding-removal-four-negative-controls-andcomposed-full-inverses','exec'),globals())
