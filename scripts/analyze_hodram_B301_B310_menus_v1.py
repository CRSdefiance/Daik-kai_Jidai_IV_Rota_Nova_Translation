"""Bind all four live menu occurrences to exact source keys and native pixels."""
from scripts.analyze_hodram_B281_B300_menus_v1 import source,menu_scopes,background_band
from scripts.approve_hodram_B301_B310_display_v6 import ROOT

BODY=ROOT/'actual_pixels_v1/focused_actual_pixels.json'
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-source-scoped-menu-pixels-and-cursor-bands','exec'),globals())
