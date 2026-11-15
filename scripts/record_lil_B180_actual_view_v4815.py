"""Seal the eleven viewed panels,36 full screens and resolved effect-state scope."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B180_actual_review_v4812')
INPUT=ROOT/'paired_all115_samples_conditional_commands11_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all2_actual_sheets11_planes_fullscreens_and_resolved_effect_state.json'
FOCUS=Path('work/analysis/lil_B180_effect_focus_v4814b/two_actual_original_effects_and_exact_one_byte_final_town_difference.json')

if __name__=='__main__':
    assert not OUTPUT.exists();d,focus=read(INPUT),read(FOCUS)
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[5495,5496] and d['whole_RGB_final9001_equal']
    assert d['exact_timing_difference_counts']==dict(total=12,speech=8,control_or_end=4)
    assert d['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=False,tasks=True,calendar=True)
    assert d['postscene9001_whole1A04_actor_models_and_captain2_equal'] and not d['PRNG_equality']
    assert d['postscene9001_PRNG_seeds']==[2467799992,790984746]
    assert focus['final_town_difference_is_exact_observed_original_effect_value'] and focus['no_unresolved_translation_specific_state_difference_within_checked_arrays']
    assert d['observed_random_path_difference']['original_effects_by_case']==dict(clean_Japanese=[504],reviewed_English=[472])
    for p,h in {**d['evidence'],**focus['evidence']}.items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'review':
            'Viewed both complete actual sheets:all11 speeches,ten progressive Lady166/Lady167 and one impersonal FE. The shared lovely-fragrance question,shared notice,curiosity,explicit lack of knowledge,confident fashion prediction,surprise and first-to-acquire urgency,future proposal to work up the nerve,warm assent and courteous farewells remain coherent. The third person stays gender unspecified. Six retained replies/questions/farewells work in the complete exchange. Scents in Lisbon is prospective and category accurate. Full leading/internal/final glyphs,punctuation,one-page consumption and bounds pass. No rank,relationship,brand,ingredient,price,shortage,earned boom or prior scene location is invented.'})
    assert len(panels)==2
    differences=d['sampled_postscene_whole_RGB_differences_unmasked'];assert len(differences)==12
    assert [r['frame'] for r in differences]==[6250,6430,7450,7630,7690,7870,7930,8110,8410,8590,8770,8950]
    for r in differences:
        assert r['whole_frame_difference_bbox']==[224,360,240,376]
        r['scope']='Viewed full paired screens:original A-button indicator animation only. Retain every unmasked RGB difference;no retiming or broader state equivalence claim.'
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
            'Viewed both full screens for every listed frame. The opening question and future proposal preserve distinct Lady portraits/nameplates. The farewell-to-FE transition clears portrait/name. Lisbon is named only in the forecast;the initialized fixture background is Amsterdam,not proof of earlier scene location.5530 returns normally to Amsterdam town/Port;9001 shows the same following Camille reply. The12 differing following frames retain only the original A-indicator animation difference in the recorded box;all other pixels agree. Following dialogue adds no credit. No natural event eligibility,earned fashion state,full route,hardware or future-world equality claim.'})
    assert len(screens)==9 and sum(len(s['frames'])*2 for s in screens)==36
    d.update(all2_actual_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        all12_following_indicator_differences_viewed_and_retained=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_open_translation_specific_display_or_control_finding=True,
        measured_persistent_town_difference_resolved_to_original_effect=True,
        effect_boundary_proof=str(FOCUS),effect_boundary_proof_sha256=sha(FOCUS.read_bytes()),
        original_predicate_RNG_transitions_observed_without_forcing=True,
        PRNG_or_future_world_equivalence_not_claimed=True,no_source_command_omission_or_conditional_flattening=True,
        actual_new_cold_boot_runs=4,total_frames=30004,
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        evidence={**d['evidence'],str(FOCUS):sha(FOCUS.read_bytes())},
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUTPUT,d)
    print('Viewed11 panels/2 sheets/36 full screens;12 icon differences and unequal RNG retained. The one-byte town difference is source-effect bound. Four focused cold boots/30004 frames;integration pending.')
