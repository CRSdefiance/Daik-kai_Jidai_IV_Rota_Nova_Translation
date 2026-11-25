"""Seal ten viewed panels and twelve full screens with measured equal scope."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B181_actual_review_v4862')
INPUT=ROOT/'paired_all115_samples22_commands10_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all2_actual_sheets10_planes_fullscreens_return_and_final_state.json'

if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT)
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[5257,5257] and d['exact_timing_difference_counts']==dict(total=0,speech=0,control_or_end=0)
    assert d['all_sampled_postscene_whole_RGB_equal'] and d['whole_RGB_final9001_equal'] and not d['sampled_postscene_whole_RGB_differences_unmasked']
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[790984746,790984746]
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'review':
            'Viewed all10 actual panels on both separate sheets. Distinct Lady166/167/168 portraits and matching Lady labels are preserved. The red-ruby question,admiration,third speaker joining,the necklace explanation and recognition remain coherent. The explicit once-in-a-lifetime wish for a gift from a man leads into three individually voiced Ahh... sighs,the first retaining Quite so. Five retained lines work in the whole exchange. The impersonal Rubies/Athens forecast remains prospective and clears portrait/name. Leading/internal/final glyphs,punctuation,full bounds and one-page consumption pass. No noble rank,kinship,spouse,suitor,giver identity,necklace gift provenance,price,shortage,earned boom or earlier location is invented.'})
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
            'Viewed all12 complete paired screens.4090 shows the complete wish,4330 the first agreement/sigh,4810 the third sigh and5050 the impersonal prospective Rubies/Athens notice.5290 shows normal return to initialized Amsterdam town/Port;9001 shows the same following steering instruction. Athens occurs in the forecast and does not establish the prior conversation location. All paired nontext regions and sampled postscene whole RGB agree without masking or retiming. Following dialogue adds no review credit;no natural event181 eligibility,earned fashion state,full route or hardware claim.'})
    assert len(panels)==2 and len(screens)==3 and sum(len(s['frames'])*2 for s in screens)==12
    d.update(all2_actual_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_source_command_omission_flattening_or_forced_actor=True,no_additional_focus_run_without_concrete_risk=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,actual_new_cold_boot_runs=2,total_frames=18002,
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUTPUT,d)
    print('Viewed10 panels/2 sheets/12 full screens. Both returns5257;zero measured timing/RGB differences,five state groups/whole actor/PRNG790984746 agree. No further focus risk.')
