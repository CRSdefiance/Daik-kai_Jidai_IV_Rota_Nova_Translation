"""Accept only the exact observed partial cursor bands with full glyph/blank checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=Path('scripts/analyze_native_choice_fixture_samples_v1.py')
BANDS={(177,5760):(278,288), (177,5880):(268,275), (179,13080):(268,287)}
FIXTURE_SHA='0196b486224baf701bcb36c523486fe03f51a29c645417bca44867a8eceae730'

source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    "    fixture,terminal=map(load,[args.fixture,args.terminal]);assert terminal['terminal'] and terminal['frames']==fixture['frames']":
        """    assert sha(args.fixture.read_bytes())==FIXTURE_SHA
    fixture,terminal=map(load,[args.fixture,args.terminal]);assert terminal['terminal'] and terminal['frames']==fixture['frames']""",
    """                    assert not cyan or cyan==blank
                    if cyan:selected.append(option)
                    else:assert all(im.getpixel(point)==(205,198,180) for point in blank)""":
        """                    if cyan:
                        selected.append(option)
                        if cyan!=blank:
                            assert option==0 and (declared['block'],cap['frame']) in BANDS
                            lo,hi=BANDS[declared['block'],cap['frame']]
                            assert cyan=={pt for pt in blank if lo<=pt[1]<hi}
                    assert all(im.getpixel(pt)==(205,198,180) for pt in blank-cyan)""",
    'visible_selected_option=selected[0] if selected else None,':
        "visible_selected_option=selected[0] if selected else None, exact_partial_cursor_band=BANDS.get((declared['block'],cap['frame'])),",
    'all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches=True,':
        "all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches=True,partial_cursor_bands_verified_at_exact_captured_frames=True,",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-complete-mask-with-three-exact-partial-cursor-frames','exec'),globals())
