"""Seal viewed B178 panels/full screens with all measured timing/indicator limits."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B178_actual_review_v4695')
INPUT=ROOT/'paired_all115_samples25_commands13_planes_expanded_fullscreens.json'
OUTPUT=ROOT/'all3_actual_sheets13_planes_fullscreens_return_and_final_state.json'
assert not OUTPUT.exists()
d=read(INPUT)
assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
assert d['all_content_jobs_terminal'] and d['fixture_return_frames']==[5977,5976]
assert d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[3306586022,3306586022]
assert d['exact_timing_difference_counts']=={'total':14,'speech':12,'control_or_end':2}
differences=d['sampled_postscene_whole_RGB_differences_unmasked']
assert [(r['frame'],r['whole_frame_difference_bbox']) for r in differences]==[
    (6970,[224,360,240,371]),(7150,[224,360,240,371]),(7930,[224,360,240,376]),(8110,[224,360,240,376])]
for r in differences:r['scope']='Viewed complete paired screens:original A-button indicator animation only. Full unmasked RGB difference box retained;all other pixels in each frame agree. No retiming or PRNG-causal trace.'
assert d['whole_RGB_final9001_equal'] and all(d['postscene9001_native_component_equality'].values())
assert d['postscene9001_whole1A04_actor_models_and_captain2_equal']
for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h,p
sheets=[]
for s in d['actual_consumer_sheets']:
    assert sha(Path(s['path']).read_bytes())==s['sha256']
    sheets.append({**s,'viewed':True,'review':
        'Viewed all thirteen complete actual panels across three sheets individually. Distinct Lady166/167/168 portraits and common Lady labels match the paired Japanese. Home-baking enthusiasm,the explicit second-speaker husband,curiosity,bakery boast,encouragement,her singular teaching offer,pleased response,shopping proposal,her ingredient question and third-speaker first-wheat reply remain in source order. All eleven retentions work in the whole exchange. The FE Amsterdam wheat forecast is impersonal/prospective and clears portrait/name fields. All first/internal/final letters,punctuation,bounds and one-page consumption pass. No invented rank,extra marriage,recipe,flour,quantity,price,completed purchase or earlier scene location.'})
assert len(sheets)==3
screens=[]
for s in d['paired_full_screen_sheets']:
    assert sha(Path(s['path']).read_bytes())==s['sha256']
    screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
        'Viewed both complete screens at every listed frame. Frame4570 shows the second Lady teaching offer;frame5770 shows the prospective impersonal FE notice with name/portrait cleared. At6010 the parent has resumed the following B120 Sailor crowd dialogue;9001 shows the same Lil reply. Frames6970/7150 show initialized Amsterdam information and About31daysatsea;7930/8110 show the same following Lil dialogue. All four differing frames vary only in the original A-button indicator animation within exact retained boxes. Source/English text,portraits,names,town information and all other pixels agree. No screenshot retiming/masking,earned progress,full-RAM,future-world or PRNG-causality claim. Following B120 adds no editorial credit.'})
assert len(screens)==4 and sum(len(s['frames'])*2 for s in screens)==16
d.update(all3_actual_sheets_viewed=sheets,paired_full_screen_views=screens,visual_review_pending=False,
    representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
    no_source_command_omission_flattening_or_forced_actor=True,
    all_four_following_indicator_differences_viewed_in_full_and_retained=True,no_new_PRNG_causal_trace=True,
    sampled_postscene_whole_RGB_equal_except_four_original_A_indicator_frames=True,
    previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
    visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
save(OUTPUT,d)
print('Viewed13 actual panels,3 consumer sheets,16 full screens;115 upper/name/portrait checks pass. Retain14 timings/4 A-indicator differences;five components,whole actor,PRNG3306586022 and final RGB agree.')
