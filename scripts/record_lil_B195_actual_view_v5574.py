"""Record the returned twenty-panel and twenty-fullscreen cheese-scene review."""
from pathlib import Path
from PIL import Image
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B195_actual_review_v5573')
INPUT=ROOT/'paired_all115_samples32_commands20_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all20_panels20_fullscreens_three_roles_return_and_measured_differences.json'

if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[7655,7657]
    assert d['exact_timing_difference_counts']==dict(total=15,speech=13,control_or_end=2)
    assert d['whole_RGB_final9001_equal'] and not d['all_sampled_postscene_whole_RGB_equal']
    differences=d['sampled_postscene_whole_RGB_differences_unmasked']
    assert [(r['frame'],r['whole_frame_difference_bbox'],r['nontext_difference_bbox']) for r in differences]==[
        (f,[224,370,240,376],None) for f in [8410,8590,8770,8950]]
    assert all(d['postscene9001_native_component_equality'].values())
    assert d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert not d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[3942509462,3085513495]
    assert len(actual['actual_panels'])==20 and sum(len(r['holds']) for r in actual['actual_panels'])==79
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[32,32]
    assert all(v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] for v in actual['versions'])
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    # Verify all held portraits consistently bind each of the three original selectors.
    # This compares actual pixels, independently of the contact-sheet presentation.
    portraits={};portrait_checks=[]
    for r in actual['actual_panels']:
        if r['prefix']==254:continue
        hashes={sha(Image.open(h['capture']).convert('RGB').crop((8,200,70,270)).tobytes()) for h in r['holds']}
        assert len(hashes)==1;digest=hashes.pop()
        assert portraits.setdefault(r['prefix'],digest)==digest
        portrait_checks.append(dict(id=r['id'],selector=r['prefix'],actual_portrait_crop_sha256=digest,held_samples=len(r['holds'])))
    assert set(portraits)=={92,103,119} and len(set(portraits.values()))==3
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'viewed_after_image_return':True,'review':
            'Viewed all20 panels as one Port Worker/Patron/Barkeep exchange. The three source roles and distinct portraits remain consistent. R17 displays its complete cheese-rich specialty statement on three required rows. The one shared order,quick service,playful humor-me invitation,two separately spoken chewing beats,taste payoff,satisfaction,personal tell-everyone intention and Patron prediction remain intact. R69 displays its complete two-row paragraph. The prospective Cheese/Veracruz FE clears portrait and name. Complete first/internal/final glyphs and punctuation fit. No authored break,font,width,guard,phase or pagination exception.'})
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'viewed_after_image_return':True,'visual_review_pending':False,'review':
            'Viewed complete paired Japanese/English specialty explanation,coaxing,personal intention,prospective notice and normal Amsterdam town return. Later unchanged sailing tutorial adds no credit. The four later whole-RGB differences are confined to the lower portion of the original A advance indicator at x224..239/y370..375,as the returned full screens show. All115 sampled upper/portrait/name comparisons and final9001 RGB agree. Fifteen command timings and unequal final PRNG remain disclosed without masking,retiming,seed forcing,causal,future-world or full-RAM claims. The initialized B22 fixture town does not establish original scene location or natural event195 activation.'})
    assert len(panels)==4 and len(screens)==5 and sum(len(s['frames'])*2 for s in screens)==20
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,
        all79_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all23_original_commands_and9_initializers_stored_and32_executed_per_version=True,
        fifteen_timing_four_later_indicator_RGB_and_unequal_PRNG_differences_retained_without_masking_or_retiming=True,
        original_three_roles_R17_three_rows_two_chewing_beats_R69_intention_and_FE_clear_observed=True,
        actual_held_portrait_consistency_checks=portrait_checks,three_distinct_selector_portrait_hashes={str(k):v for k,v in portraits.items()},
        no_PRNG_causal_or_future_world_equivalence_claim=True,no_forced_seed_effect_outcome_or_synthetic_actor=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,
        actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[80525,7941],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d)
    print('Viewed20 panels/20 full screens;79 holds/115 nontext pairs pass. Fifteen timings,four lower A-indicator differences and unequal PRNG retained.')
