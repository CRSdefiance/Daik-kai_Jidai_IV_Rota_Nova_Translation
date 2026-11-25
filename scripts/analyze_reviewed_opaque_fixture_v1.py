"""Preserve exact body/header/order checks and compare two source-bound CP932 shadows."""
from pathlib import Path
from scripts.analyze_reviewed_dynamic_fixture_v1 import dynamic_headers
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
NATIVE=ROOT/'storage_inputs_v2/native_pages.json'
bindings={r['id']:r for r in load(NATIVE)['records'] if r['id'] in ['DK4_MES_B40_R0088','DK4_MES_B40_R0092']}

def body_colors_exact(crop,page):
    ident=page['id']
    if ident not in bindings:
        return sha(bytes(rgb==(0,8,0) for rgb in crop.get_flattened_data()))==page['pixel_mask_sha256']
    row=bindings[ident];native=row['complete_native_English_display']['pages'][0]
    assert page['page']==1 and page['text_hex']==row['expanded_native_hex']
    assert page['native_plane_sha256']==native['native_plane_sha256']
    assert row['source_selector']==78 and row['compiled_hex'].startswith('4e')
    plane=Path(native['native_plane']).read_bytes();assert sha(plane)==native['native_plane_sha256']
    assert set(plane)=={0,1,15} and crop.size==(216,64)
    actual=list(crop.get_flattened_data())
    # Independent native font proof includes style1 ink and the CP932 style15 shadow.
    # Both complete color masks, including every blank position, must match separately.
    return all(bytes(rgb==color for rgb in actual)==bytes(v==value for v in plane)
        for value,color in [(1,(0,8,0)),(15,(197,198,197))])

source=checked_text(Path('scripts/analyze_reviewed_scene_fixture.py').read_text(encoding='utf-8'),{
    "exec(compile(source,__file__+'::same-ordered-calls-complete-pixels-andblank-guards','exec'),globals())":
    "source=checked_text(source,{\"if sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata())) != page['pixel_mask_sha256']:\":\"if not body_colors_exact(crop,page):\"})\n    exec(compile(dynamic_headers(source),__file__+'::same-pixels-order-guards-and-two-exact-native-shadow-bindings','exec'),globals())",
})
exec(compile(source,__file__+'::complete-source-bound-CP932-color-masks','exec'),globals())
