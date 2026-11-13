"""Keep the actual source highlight-off sample; verify complete native on/off pixels without phase equality."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_menu_phase_tools_v7950c');assert not root.exists()
    pixel="""                positions={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink}
                highlight_visible=bool(cyan)
                assert (cyan==positions and index==selected) or not cyan,(version,choice,frame,index,'partial orwrong highlight')
                background=(0,165,172) if highlight_visible else (205,198,180)
                assert all(im.getpixel(p)==background for p in positions),(version,choice,frame,index,'background glyph guard')
"""
    globalcheck="""    for g in groups:
        visible={s['visible_selected_option_index'] for s in g['samples'] if s['visible_selected_option_index'] is not None}
        assert visible==({0} if g['choice']=='accept' else {0,1})
    off=[dict(version=g['version'],choice=g['choice'],frame=s['frame'],logical_selected_option=s['selected_option_index'])
        for g in groups for s in g['samples'] if s['visible_selected_option_index'] is None]
    assert off==[dict(version='clean_Japanese',choice='accept',frame=4930,logical_selected_option=0)]
"""
    row=derive('scripts/audit_Rafael_B46_menu_v7950b.py','scripts/audit_Rafael_B46_menu_v7950c.py',{
        'Rafael_B46_menu_actual_v7950b':'Rafael_B46_menu_actual_v7950c',
        "                assert cyan==want,(version,choice,frame,index,'selected highlight')":pixel.rstrip(),
        'exact_cyan_selected_fill_equal=True,selected=index==selected':'exact_native_background_pixels_equal=True,selected_highlight_visible=highlight_visible,selected=index==selected',
        'samples.append(dict(frame=frame,selected_option_index=selected,':'samples.append(dict(frame=frame,selected_option_index=selected,visible_selected_option_index=next((c[\'option_index\'] for c in cases if c[\'selected_highlight_visible\']),None),',
        'actual_full_source_orEnglish_labels_visible_inboth_highlight_states':'actual_full_source_orEnglish_labels_visible_withmeasured_selection_state',
        "    path=ROOT/'source_English_both_choices_three_actual_menu_holds.png'":globalcheck+"    path=ROOT/'source_English_both_choices_three_actual_menu_holds.png'",
        'all24_visible_source_English_label_samples_full_first_internal_final_glyphs_bounds_andselected_backgrounds_exact=True':'all24_visible_source_English_label_samples_full_first_internal_final_glyphs_bounds_andnative_backgrounds_exact=True,source_highlight_off_samples=off,exact_cross_language_highlight_phase_equality_not_claimed=True',
        'Four actual menus/12 owned-backing samples/24 visible labels pass exact independent glyphs andboth highlights. Source84/target66 views,256x36 backing;sheet view pending.':'Four actual menus/12 backing samples/24 labels pass fullglyphs andexact native backgrounds;both logical highlights observed. One source4930 highlight-off sample retained,not phase equality. Sheet view pending.',
    })
    root.mkdir(parents=True);save(root/'source_locked_phase_audit.json',dict(derivation=row,
        evidence='Source accept4930 has complete glyphs anduniform native paper backgrounds inbothrows. Source accept4810/4870 show option0;source/English decline4930 show option1. English accept4930 still shows0.',
        full_owned_backing_glyph_bounds_rectangle_andbackground_assertions_retained=True,
        each_run_must_observe_its_correct_highlight_andboth_states_for_decline=True,
        source_only_off_sample_is_explicit_andexact_no_frame_exclusion_orcausal_animation_claim=True,
        no_failed_check_counted_aspassing_negative=True,no_ROM_image_snapshot_input_mutation=True,new_credit=0,full_goal_complete=False))
