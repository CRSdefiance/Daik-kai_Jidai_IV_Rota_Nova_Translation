"""Check all three source-qualified menus with the existing strict cursor-band model."""
from scripts.analyze_hodram_B211_B230_menus_v1 import source as previous, menu_scopes
from scripts.analyze_hodram_B231_B250_menu_v1 import background_band
from scripts.approve_hodram_B251_B280_display_v5 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text

BODY = ROOT / 'actual_pixels_v2/focused_actual_pixels.json'
source = checked_text(previous, {
    "                    cyan={point for point in blank if im.getpixel(point)==(0,165,172)}\n                    assert not cyan or cyan==blank\n                    if cyan:selected.append(option)\n                    else:assert all(im.getpixel(point)==(205,198,180) for point in blank)":
        "                    if background_band(im,blank):selected.append(option)",
    'numeric_modal_return_register_original_story_branches_andcancellation_unvisited=True,':
        "cursor_band_model_reused_exact_from='scripts/analyze_hodram_B231_B250_menu_v1.py', numeric_modal_return_register_original_story_branches_andcancellation_unvisited=True,",
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-source-scoped-menu-pixels-and-qualified-cursor-band', 'exec'), globals())
