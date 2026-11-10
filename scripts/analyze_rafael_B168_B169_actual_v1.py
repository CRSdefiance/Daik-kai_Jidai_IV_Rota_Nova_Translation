"""Compare CP932 punctuation using ink and shadow as separate exact masks."""
from collections import Counter
from pathlib import Path
import sys

from scripts.source_locked_derivation_v5118 import checked_text


BASE = Path('scripts/analyze_reviewed_scene_fixture.py')
SOURCE = checked_text(BASE.read_text(encoding='utf-8'), {
    "    exec(compile(source,__file__+'::same-ordered-calls-complete-pixels-andblank-guards','exec'),globals())":
        "    source=checked_text(source,{\n"
        "        \"        if sha(bytes(rgb == (0, 8, 0) for rgb in crop.getdata())) != page['pixel_mask_sha256']:\\n            continue\":\n"
        "        \"        if not exact_masks(page,crop):\\n            continue\",\n"
        "        '        all_selected_pages_observed_in_exact_fixture_order=True,':\n"
        "        '        exact_CP932_punctuation_ink_and_shadow_masks=True,all_selected_pages_observed_in_exact_fixture_order=True,',\n"
        "    })\n"
        "    exec(compile(source,__file__+'::ordered-body-and-header-with-exact-native-punctuation-masks','exec'),globals())",
})
SPECIAL = {
    'DK4_MES_B169_R0055': '81638163',
    'DK4_MES_B169_R0161': '8149',
    'DK4_MES_B169_R0169': '8163',
    'DK4_MES_B169_R0212': '8163',
}
PIXEL_COUNTS = dict(zip(SPECIAL, (12, 9, 6, 6), strict=True))
PROBE = '--probe-mask' in sys.argv
if PROBE:
    sys.argv.remove('--probe-mask')


def exact_masks(page, crop):
    pixels = list(crop.get_flattened_data())
    black = bytes(v == (0, 8, 0) for v in pixels)
    ident = page['id']
    if ident not in SPECIAL:
        return sha(black) == page['pixel_mask_sha256']
    plane = Path(page['native_plane']).read_bytes()
    assert sha(plane) == page['native_plane_sha256'] and page['page'] == 1
    assert bytes.fromhex(page['text_hex']).rstrip(b' ').hex() == SPECIAL[ident]
    if PROBE:
        visible = Counter((native, rgb) for native, rgb in zip(plane, pixels, strict=True) if native)
        print(ident, sorted(visible.items()), flush=True)
        return False
    ink, shadow = 1, 15
    assert set(plane) == {0, ink, shadow} and plane.count(ink) == plane.count(shadow) == PIXEL_COUNTS[ident]
    return black == bytes(v == ink for v in plane) and bytes(v == (197, 198, 197) for v in pixels) == bytes(v == shadow for v in plane)


if __name__ == '__main__':
    exec(compile(SOURCE, __file__+'::same-analysis-with-source-bound-CP932-masks', 'exec'), globals())
