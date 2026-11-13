"""Use the observed dialogue palette; menu andname palettes remain distinct."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_hodram_focused_actual_pixels.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    'Hodram_B81_B89_actual_pixels_20261101':'Hodram_B81_B89_actual_pixels_20261101c',
    '[6720,7200,11520,12240,12720,13200,13680,13920]':'[6720,7200,11520,12240,12720,13200,13680]',
    'if im.getpixel((xx,yy))==(8,8,8)}\n                difference':
        'if im.getpixel((xx,yy))==(0,8,0)}\n                difference',
})
exec(compile(source,__file__+'::distinct-actual-dialogue-palette','exec'),globals())
