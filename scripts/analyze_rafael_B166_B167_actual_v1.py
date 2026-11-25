"""Match the exact CP932 shadow mask on four retained ellipses, keeping all pixel guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

BASE=Path('scripts/analyze_reviewed_scene_fixture.py')
source=checked_text(BASE.read_text(encoding='utf-8'),{
    "    exec(compile(source,__file__+'::same-ordered-calls-complete-pixels-andblank-guards','exec'),globals())":
        """    source=checked_text(source,{
        "        if sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata())) != page['pixel_mask_sha256']:\\n            continue":
        "        if not exact_color_masks(page,crop):\\n            continue",
        "        all_selected_pages_observed_in_exact_fixture_order=True,":
        "        exact_black_and_CP932_shadow_masks_for_four_source_ellipses=True,all_selected_pages_observed_in_exact_fixture_order=True,",
    })
    exec(compile(source,__file__+'::same-ordered-calls-complete-black-gray-andblank-guards','exec'),globals())""",
})
SPECIAL={
    'DK4_MES_B166_R0225':(1,15),
    'DK4_MES_B166_R0519':(1,15),
    'DK4_MES_B166_R0265':(15,14),
    'DK4_MES_B166_R0273':(15,14),
}


def exact_color_masks(page,crop):
    colors=list(crop.get_flattened_data())
    black=bytes(v==(0,8,0) for v in colors)
    if page['id'] not in SPECIAL:
        return sha(black)==page['pixel_mask_sha256']
    plane=Path(page['native_plane']).read_bytes()
    assert sha(plane)==page['native_plane_sha256'] and page['page']==1
    assert bytes.fromhex(page['text_hex']).rstrip(b' ').endswith(bytes.fromhex('8163'))
    ink,shadow=SPECIAL[page['id']]
    assert set(plane)=={0,ink,shadow}
    expected_ink=bytes(v==ink for v in plane)
    expected_shadow=bytes(v==shadow for v in plane)
    assert sum(expected_ink)==sum(expected_shadow)==6
    return black==expected_ink and bytes(v==(197,198,197) for v in colors)==expected_shadow


if __name__=='__main__':
    exec(compile(source,__file__+'::same-analyzer-with-exact-retained-ellipsis-colors','exec'),globals())
