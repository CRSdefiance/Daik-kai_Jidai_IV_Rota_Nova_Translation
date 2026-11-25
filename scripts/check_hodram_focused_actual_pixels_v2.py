"""Correct the sampled speaker membership: frame13920 is Hodram, not Emilio."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_hodram_focused_actual_pixels.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    'Hodram_B81_B89_actual_pixels_20261101':'Hodram_B81_B89_actual_pixels_20261101b',
    '[6720,7200,11520,12240,12720,13200,13680,13920]':'[6720,7200,11520,12240,12720,13200,13680]',
})
exec(compile(source,__file__+'::correct-observed-speaker-membership','exec'),globals())
