"""Seal all viewed B179 panels and20 full screens with fresh measured limits."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B179_actual_review_v4743')
INPUT=ROOT/'paired_all115_samples25_commands14_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all3_actual_sheets14_planes_fullscreens_return_and_final_state.json'
assert not OUTPUT.exists()
d=read(INPUT)
assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
assert d['all_content_jobs_terminal'] and d['fixture_return_frames']==[6216,6215]
assert d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[403514907,403514907]
assert d['exact_timing_difference_counts']=={'total':8,'speech':7,'control_or_end':1}
assert d['whole_RGB_final9001_equal'] and all(d['postscene9001_native_component_equality'].values())
assert d['postscene9001_whole1A04_actor_models_and_captain2_equal']
differences=d['sampled_postscene_whole_RGB_differences_unmasked']
assert [(r['frame'],r['whole_frame_difference_bbox']) for r in differences]==[
    (6970,[224,360,240,371]),(7150,[224,360,240,371]),(7930,[224,360,240,376]),(8110,[224,360,240,376])]
for r in differences:r['scope']='Viewed complete paired screens:original A-button indicator animation only;all other pixels agree. Retain exact full-RGB box without masking,retiming or PRNG-causal inference.'
for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h,p
sheets=[]
for s in d['actual_consumer_sheets']:
    assert sha(Path(s['path']).read_bytes())==s['sha256']
    sheets.append({**s,'viewed':True,'review':
        'Viewed all14 complete actual panels on three individual sheets. Source-bound Sailor152,Patron96 and Barkeep92 labels/portraits survive;the separate catalog Retainer152 is unchanged. The unspecified-drink challenge,defensive retort,concession,wine enthusiasm,repeated taste questions,personal hyperbole,one-glass trial,service,three gulps,delighted verdict,another-serving request and joining order remain in source sequence. All six retained wordings work in the complete exchange. The FE Sao Jorge wine forecast is impersonal and prospective,with portrait/name cleared. All first/internal/final letters,punctuation,bounds and one-page consumption pass. No invented drink type,brand,price,rank,relationship,drunkenness,medical claim,completed sale,active boom or earlier location.'})
assert len(sheets)==3
screens=[]
for s in d['paired_full_screen_sheets']:
    assert sha(Path(s['path']).read_bytes())==s['sha256']
    screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
        'Viewed both complete screens at every listed frame.4570 restores the Patron trial order;5050 retains three gulps.5770 shows Sailor joining the wine order;6010 shows the impersonal prospective Sao Jorge notice with portrait/name cleared.6250 shows normal return to initialized Amsterdam town information/Port;9001 shows the same following Lil reply.6970/7150 show the same About31daysatsea and Amsterdam information;7930/8110 show the same following Lil response. All four whole-RGB differences are confined to original A-button-indicator animation in their retained boxes. All other pixels in those frames agree. No screenshot retiming/masking,earned progress,full-RAM,future-world or PRNG-causality claim. Following B120 offset352 remains pending at8376/8375 through9001 and adds no editorial credit.'})
assert len(screens)==5 and sum(len(s['frames'])*2 for s in screens)==20
d.update(all3_actual_sheets_viewed=sheets,paired_full_screen_views=screens,visual_review_pending=False,
    representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
    no_source_command_omission_flattening_or_forced_actor=True,
    all_four_following_indicator_differences_viewed_in_full_and_retained=True,no_new_PRNG_causal_trace=True,
    sampled_postscene_whole_RGB_equal_except_four_original_A_indicator_frames=True,
    previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
    visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
save(OUTPUT,d)
print('Viewed14 actual panels/3 sheets/20 full screens. Retain8 timings/4 A-indicator differences;115 upper/name/portrait regions,five components,whole actor,PRNG403514907 and final RGB agree.')
