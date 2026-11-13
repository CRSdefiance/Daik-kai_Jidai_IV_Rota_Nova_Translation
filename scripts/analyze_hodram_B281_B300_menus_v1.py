"""Use exact source-key occurrence windows and the qualified native cursor-band model."""
from scripts.analyze_hodram_B251_B280_menus_v1 import source,menu_scopes,background_band
from scripts.approve_hodram_B281_B300_display_v5 import ROOT

BODY=ROOT/'actual_pixels_v1/focused_actual_pixels.json'
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-live-menu-pixels-and-source-occurrences','exec'),globals())
