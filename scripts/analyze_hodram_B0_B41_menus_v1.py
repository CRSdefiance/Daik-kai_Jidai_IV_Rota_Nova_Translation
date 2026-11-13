"""Keep source-key and ordered-call attribution for the three residual menus."""
from pathlib import Path
from scripts.analyze_hodram_B211_B230_menus_v1 import source,menu_scopes

BODY=Path('work/Hodram_B0_B41_clean_20261107/bounded_pixels_1_v1/focused_actual_pixels.json')
if __name__=='__main__':exec(compile(source,__file__+'::same-exact-source-occurrence-native-menu-checks','exec'),globals())
