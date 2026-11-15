"""Use the measured story ink RGB; menu and name palettes remain distinct."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_hodram_B91_B110_actual_pixels.py').read_text(encoding='utf-8'),{
    'work/analysis/Hodram_B91_B110_actual_pixels_20261101':
    'work/analysis/Hodram_B91_B110_actual_pixels_20261101b',
    'origin=match(im,ink,(8,8,8),range(12,21),range(298,307))':
    'origin=match(im,ink,(0,8,0),range(12,21),range(298,307))',
    "            bounded_framebuffer_alignment_only_no_backing_owner_claim=True))":
    "            measured_story_ink_RGB=[0,8,0],bounded_framebuffer_alignment_only_no_backing_owner_claim=True))",
})
exec(compile(source,__file__+'::measured-story-palette','exec'),globals())
