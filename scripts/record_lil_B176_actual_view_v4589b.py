"""Seal the individually viewed consumer sheets and eight paired full screens."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B176_actual_review_v4589')
INPUT=ROOT/'paired_all115_samples22_commands10_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all2_actual_sheets10_planes_fullscreens_return_and_final_state.json'
assert not OUTPUT.exists()
doc=read(INPUT)
assert doc['visual_review_pending'] and doc['nontext_equal_samples']==115 and not doc['nontext_difference_samples']
assert doc['all_content_jobs_terminal'] and doc['fixture_return_frames']==[5256,5256]
assert doc['PRNG_equality'] and doc['postscene9001_PRNG_seeds']==[403514907,403514907]
for path,digest in doc['evidence'].items():
    assert sha(Path(path).read_bytes())==digest,path
sheets=[]
for s in doc['actual_consumer_sheets']:
    assert sha(Path(s['path']).read_bytes())==s['sha256']
    sheets.append({**s,'viewed':True,'review':
        'Viewed all ten complete panels across two sheets individually. Owner/Cook portraits and role labels remain exact;the Cook moves from polite doubt to casual repeated acquiescence. The Owner remains emphatic and grandiose without an invented rank or relationship. Five retained wordings remain natural in the full exchange. The prospective Seville notice is impersonal with no portrait/nameplate. Every leading/internal/trailing glyph and punctuation is complete;no overflow,extra page or blank text page was seen.'})
assert len(sheets)==2
screens=[]
for s in doc['paired_full_screen_sheets']:
    assert sha(Path(s['path']).read_bytes())==s['sha256']
    screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
        'Viewed both Japanese and English full screens at each stated frame. Frame2950 shows the same Owner portrait/name and initialized town backdrop. Frame5050 shows the prospective Seville notice with portrait/name area cleared. Frame5290 shows the whole-RGB-identical initialized Amsterdam town return;the35,000 funds and town details are inherited fixture state. Frame9001 shows the same following B120 steering tutorial on a black upper screen. Following tutorial content adds no editorial credit. No natural Seville event location or earned boom is inferred from the Amsterdam fixture.'})
assert len(screens)==2 and sum(len(s['frames'])*2 for s in screens)==8
doc.update(all2_actual_sheets_viewed=sheets,paired_full_screen_views=screens,
    visual_review_pending=False,representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
    no_open_translation_specific_display_or_control_finding=True,
    no_source_command_omission_flattening_or_forced_actor=True,
    previous_analysis=str(INPUT),previous_analysis_sha256=sha(INPUT.read_bytes()),
    visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
save(OUTPUT,doc)
print('Viewed ten panels,two consumer sheets and eight full screens;all115 nontext samples,22 command timings,return and five native state components agree. Full-route/earned-state claims remain excluded.')
