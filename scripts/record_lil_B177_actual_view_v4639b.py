"""Seal B177's viewed panels and twelve full screens with timing/indicator/PRNG limits."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B177_actual_review_v4639')
INPUT=ROOT/'paired_all115_samples22_commands10_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all2_actual_sheets10_planes_fullscreens_return_and_final_state.json'
assert not OUTPUT.exists()
doc=read(INPUT)
assert doc['visual_review_pending'] and doc['nontext_equal_samples']==115 and not doc['nontext_difference_samples']
assert doc['all_content_jobs_terminal'] and doc['fixture_return_frames']==[5255,5257]
assert not doc['PRNG_equality'] and doc['postscene9001_PRNG_seeds']==[463267532,403514907]
assert doc['exact_timing_difference_counts']=={'total':11,'speech':9,'control_or_end':2}
assert len(doc['fourteen_following_A_button_indicator_animation_differences_retained_unmasked'])==14
for path,digest in doc['evidence'].items():
    assert sha(Path(path).read_bytes())==digest,path
sheets=[]
for s in doc['actual_consumer_sheets']:
    assert sha(Path(s['path']).read_bytes())==s['sha256']
    sheets.append({**s,'viewed':True,'review':
        'Viewed all ten complete actual panels across two sheets individually. Owner enthusiasm and red-color passion become a consuming youthful-love recollection;Cook responds with dry politeness,then practical compliance and repeated casual acknowledgment. The full R12 recollection fits four complete rows with final young punctuation intact. The cooking/selling instruction,commercial exhortation,encouragement,distinctive laugh and prospective Genoa notice remain coherent. Owner/Cook portraits and role labels match Japanese;FE clears portrait/name fields. All five retained wordings remain natural in the full exchange. No added madam,lover,relationship,rank,food taboo,active boom or earlier location. No missing leading/internal/trailing glyph,overflow,extra page or blank text page was seen.'})
assert len(sheets)==2
screens=[]
for s in doc['paired_full_screen_sheets']:
    assert sha(Path(s['path']).read_bytes())==s['sha256']
    screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
        'Viewed both complete Japanese and English screens at every stated frame. Frame3370 shows the complete source reminiscence and four-row English version with identical Owner portrait/name and town backdrop. Frame5050 shows the impersonal prospective Genoa notice with portrait/name cleared. Frame5290 shows identical initialized Amsterdam town return;35,000 funds/town data are inherited fixture state. Frame9001 shows the same following B120 steering tutorial and black upper screen. Frames6010 and7210 show the differing vertical animation phase of the original A-button indicator;all other pixels in those frames agree. Fourteen full-frame difference boxes remain exact and unmasked within x224–240/y360–376;all115 upper/portrait/name comparisons agree. The following town/tutorial adds no editorial credit. No retiming,full-RAM,future-world or PRNG-causality claim.'})
assert len(screens)==3 and sum(len(s['frames'])*2 for s in screens)==12
doc.update(all2_actual_sheets_viewed=sheets,paired_full_screen_views=screens,visual_review_pending=False,
    representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
    no_open_translation_specific_display_or_control_finding=True,
    no_source_command_omission_flattening_or_forced_actor=True,
    fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained=True,
    no_new_PRNG_causal_trace=True,previous_analysis=str(INPUT),previous_analysis_sha256=sha(INPUT.read_bytes()),
    visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
save(OUTPUT,doc)
print('Viewed ten actual panels,two consumer sheets,twelve full screens;115 upper/portrait/name checks pass. Retain14 following A-indicator RGB differences,11 command timings and unequal PRNG seeds;five native components/actor and final RGB agree.')
