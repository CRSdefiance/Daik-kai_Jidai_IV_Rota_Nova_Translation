"""Record the viewed 25 B183 panels and fourteen paired full screens."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B183_actual_review_v4961')
INPUT=ROOT/'paired_all149_samples37_commands25_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all5_actual_sheets25_planes_fullscreens_return_and_final_state.json'

if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT)
    assert d['visual_review_pending'] and d['nontext_equal_samples']==149 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[8855,8854] and d['exact_timing_difference_counts']==dict(total=11,speech=9,control_or_end=2)
    assert d['sampled_postscene_first_frame']==8890 and d['all_sampled_postscene_whole_RGB_equal']
    assert d['whole_RGB_final11001_equal'] and not d['sampled_postscene_whole_RGB_differences_unmasked']
    assert all(d['postscene11001_native_component_equality'].values()) and d['postscene11001_whole1A04_actor_models_and_captain2_equal']
    assert not d['PRNG_equality'] and d['postscene11001_PRNG_seeds']==[1228390232,713326998]
    assert d['all_content_jobs_terminal'] and d['actual37_of37_stored_fixture_commands_selected']
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'review':
            'Viewed all25 actual panels on five separate sheets. Five distinct progressive portraits/nameplates remain Square Shopkeeper85,Shipwright110,Priest132,Guildmaster148 and Sailor153;the separate catalogue Retainer is not substituted. The competitive artist judgments,predicted lasting fame,recommendation,purchase intentions and public service lead coherently through impersonal Slam!,private complaint,rich-person pastime echo,limited connoisseurship,candid laughter and secrecy. The fitting R35 question stays intact on line1,then That one over there / is obviously better! without a word change. Both FE objects clear portrait/name;the closing Artwork/Basra forecast remains prospective. All leading/internal/final glyphs,punctuation,bounds and one-page consumption pass. Nine individually justified retained lines work in the whole exchange. No named artist,rank,relationship,price,ownership provenance,objective art verdict,earned boom or earlier shop location is invented.'})
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
            'Viewed all14 complete paired screens.4810 shows the intact fitting question,5770 courteous service,6010 impersonal Slam! with portrait/name cleared,6250 shopkeeper portrait/name restored for the private complaint,8650 the impersonal prospective Artwork/Basra notice,and8890 normal return to initialized Amsterdam town/Port.11001 shows the identical following Camille sailing instruction. The forecast does not establish the prior conversation location.149 paired nontext samples and all sampled postscene whole RGB agree without masking or retiming.11 command timings and final PRNG seeds differ and remain disclosed;five native state groups and whole1A04 actor/captain2 agree. No PRNG causal,future-world or full-RAM equivalence claim. Following B120 adds no editorial credit. No natural event183 eligibility,earned fashion state,full route or hardware claim.'})
    assert len(panels)==5 and len(screens)==4 and sum(len(s['frames'])*2 for s in screens)==14
    actual=read(d['actual_proof'])
    for v in actual['versions']:
        assert v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] and v['source_C200']['UI_pending_after']==1
    d.update(all5_actual_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_source_command_omission_flattening_or_forced_actor=True,no_additional_focus_run_without_concrete_risk=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,actual_new_cold_boot_runs=2,total_frames=22002,
        actual_C200_request_words=[1,2,13,0,2,0,1],actual_C200_pending=1,
        isolated_C200_zero_resource_fields_not_imposed_on_actual_effect_body=True,
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUTPUT,d)
    print('Viewed25 panels/5 sheets/14 full screens. Returns8855/8854;11 timings differ;sampled RGB,five state groups and whole actor agree. Unequal PRNG disclosed. No further focus risk.')
