"""Match measured body placement and disclose the sampled partial initial highlight."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_hodram_B91_B110_actual_pixels.py').read_text(encoding='utf-8'),{
    'work/analysis/Hodram_B91_B110_actual_pixels_20261101':
    'work/analysis/Hodram_B91_B110_actual_pixels_20261101d',
    'origin=match(im,ink,(8,8,8),range(12,21),range(298,307))':
    'origin=match(im,ink,(0,8,0),range(12,21),range(292,307))',
    "            bounded_framebuffer_alignment_only_no_backing_owner_claim=True))":
    "            measured_story_ink_RGB=[0,8,0],bounded_framebuffer_alignment_only_no_backing_owner_claim=True))",
    "            assert not cyan or cyan==positions\n            if cyan:selected.append(i)\n            else:assert all(im.getpixel(p)==(205,198,180) for p in positions)":
    """            # At4560 the first highlight occupies only the measured lower11
            # rows. At4680 the moved second highlight fills its complete20rows.
            # Check the exact sampled form; do not claim a full first highlight.
            band=(277,288) if wanted==0 else (288,308)
            expected_cyan={p for p in positions if i==wanted and band[0]<=p[1]<band[1]}
            assert cyan==expected_cyan
            assert all(im.getpixel(p)==((0,165,172) if p in expected_cyan else (205,198,180)) for p in positions)
            if cyan:selected.append(i)""",
    "selected_option=wanted,both_complete_caption_glyphs_blank_guards_andhighlight_exact=True":
    "selected_option=wanted,both_complete_caption_glyphs_andblank_guards_exact=True,sampled_highlight_RGB_exact=True,initial_highlight_partial_in_this_capture=wanted==0,highlight_band=list(band)",
})
exec(compile(source,__file__+'::measured-framebuffer-comparison','exec'),globals())
