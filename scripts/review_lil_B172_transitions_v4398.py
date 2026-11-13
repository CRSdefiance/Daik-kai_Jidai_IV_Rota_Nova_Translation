"""Record viewed B172 dialogue, scoped transition timing and later-state findings."""
from pathlib import Path
from PIL import Image,ImageChops
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B172_transition_review_v4398')
ACTUAL=Path('work/analysis/lil_B172_actual_v4394/actual_all27_presentations_resources_C200_A000_and_end.json')
VIEWS=Path('work/analysis/lil_B172_transition_views_v4396b/paired_full_screen_and_region_inventory.json')
REPEAT=Path('work/analysis/lil_B172_repeat_verification_v4397/post_B172_actor_captain_and_same_ROM_repeat_comparison.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__=='__main__':
    assert not ROOT.exists()
    actual,views,repeat=map(read,[ACTUAL,VIEWS,REPEAT])
    assert not actual['failures'] and not actual['offline_only_display_IDs']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==27
    assert actual['paired_region_differences']==[dict(id='DK4_MES_B172_R0007',frame=2950,native_text_plane_exact=True,paired_source_upper_or_portrait_region_differs=True,not_masked_or_retimed=True)]
    assert repeat['paired_town9370_whole1A04_actor_models_and_captain2_equal']
    assert repeat['each_same_ROM_repeat_all47_command_times_results_and_single_end_equal']
    assert repeat['cross_language_command_order_results_and_single_end_word_equal']
    assert repeat['all_requested_same_ROM_repeat_frames_whole_RGB_equal']
    for sample in repeat['paired_native_persistent_state_and_PRNG_samples']:
        if sample['frame']<=14050:assert all(sample['component_equality'].values())
    timing=repeat['cross_language_command_timing_differences']
    assert len(timing)==30 and sum(r['source']['word']==0x4000 for r in timing)==24
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[9336,9335]
    for version in actual['versions']:
        assert len(version['selected_B22_command_pairs'])==47
        assert version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        assert version['actual_C200']['result_words']==version['actual_source_A000']['result_words']==[3,0]
        assert version['source_A000_hex']=='00a0ffff010cc960'
    sheets=[]
    for sheet in actual['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        sheets.append({**sheet,'viewed':True,'review':'Viewed every complete panel in exchange order. Julian Lopes,Mihwa and Lil Argot portraits/nameplates are intact;spoken given names remain Julian/Mihwa. Complete leading/internal/final glyphs and ordinary grammar wraps preserve all words. Smile/life hyperbole,missing smile,uncertain crown report and affordability,the date request and qualified response,overeager promise/departure,Lil curiosity/independent search and final offer/request reversal remain coherent. No text loss,extra page or translation-specific display finding.'})
    assert len(sheets)==5
    full=[]
    for sheet in views['paired_view_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        full.append({**sheet,'viewed':True,'review':'Viewed all paired original full screens. Original Julian figure and tavern background,departure fade,figure removal,Mihwa follow-up,final reversal and initialized Amsterdam town return are intact. Early portrait refresh and shifted fade are explicitly retained;later sailing differs.'})
    assert len(full)==4
    notes={3010:'Complete opening,original Julian upper figure and correct portrait/full nameplate.',
        2950:'Five frames after the first speech starts:complete English text plane;only portrait top10 rows differ. Original upper figure and nameplate match. Portrait finishes identically by3010.',
        6010:'Complete conditional date request;original figure and native four-row English preserved.',
        6610:'Complete overeager promise/departure reply with original figure still present.',
        6730:'Original4620 departure fade in progress. Source6696..6736 versus English6694..6734;English is two frames further into the original transition. Portrait/nameplate match.',
        6790:'Both original figures are removed;identical tavern background and Mihwa portrait/name,complete interrupted expectation.',
        9130:'Complete final reversal with Mihwa asking Lil to show the crown.',
        9370:'Whole-RGB-identical initialized Amsterdam town return after C200,source A000,6240 and single end.',
        14170:'Following B120 has ended;later sailing world/boat display differs and is retained.',
        19990:'Later sailing/food-depletion outcome differs;no equal-world claim.'}
    source_views=[];english_views=[]
    for frame,note in notes.items():
        pair=[]
        for case,target in [('clean_Japanese',source_views),('reviewed_English',english_views)]:
            p=BASE/('lil_B172_display_v4390_'+case)/f'frame_{frame:06d}_cold_boot.png'
            assert Image.open(p).size==(256,384)
            target.append(dict(frame=frame,path=str(p),sha256=sha(p.read_bytes()),viewed=True,review=note))
            pair.append(Image.open(p).convert('RGB'))
        if frame==2950:
            assert pair[0].crop((0,0,256,192)).tobytes()==pair[1].crop((0,0,256,192)).tobytes()
            assert ImageChops.difference(pair[0].crop((0,192,256,294)),pair[1].crop((0,192,256,294))).getbbox()==(0,0,72,10)
        if frame in [3010,6010,6610,6790,9130,9370]:
            assert pair[0].crop((0,0,256,294)).tobytes()==pair[1].crop((0,0,256,294)).tobytes()
        if frame==9370:assert pair[0].tobytes()==pair[1].tobytes()
    checks=views['all_sampled_region_checks'];differences=views['nontext_region_differences']
    assert len(checks)==299 and len(differences)==101
    early=[c for c in differences if c['frame']<14170]
    later=[c for c in differences if c['frame']>=14170]
    assert [c['frame'] for c in early]==[2950,6730] and len(later)==99
    following=[]
    for case in ['clean_Japanese','reviewed_English']:
        trace=read(BASE/('lil_B172_display_v4390_'+case)/'observer/commands.json');rows=trace['rows'];flow=[]
        for row in rows:
            if row['kind']!='after_command':continue
            entry=rows[row['entry_row']]
            if entry['source']['block']==120:
                flow.append(dict(offset=entry['source']['instruction_offset'],word=entry['source']['first_word'],
                    start=entry['frame'],returned=row['frame'],result_words=row['result_words']))
        assert len(flow)==30 and flow[-1]['word']==0
        following.append(dict(case=case,block=120,commands=flow,new_editorial_credit=0))
    assert [v['commands'][-1]['returned'] for v in following]==[14133,14136]
    shape=lambda v:[(r['offset'],r['word'],r['result_words']) for r in v['commands']]
    assert shape(following[0])==shape(following[1])
    ROOT.mkdir(parents=True)
    paths=[ACTUAL,VIEWS,REPEAT,Path('translations/lil_B172_editorial_manuscript_v3.json'),Path(__file__)]
    save(ROOT/'all5_sheets_departure_C200_A000_and_paired_return_review.json',dict(
        all5_actual_sheets_viewed=sheets,all4_paired_full_screen_sheets_viewed=full,
        English_full_screen_views=english_views,Japanese_full_screen_views=source_views,
        all299_sampled_nontext_region_checks=checks,early_two_transient_nontext_differences=early,
        later99_sailing_samples_including_final20001=later,following_B120_same_command_shape=following,
        single_source_end1880_actual=True,C200_before_source_A0006240_and_end_actual=True,
        source_A000_raw_hex='00a0ffff010cc960',source_A000_packed_semantics_not_inferred=True,
        all27_complete_native_held_planes_and_paired_portrait_name_upper_regions_match=True,
        original_presentations_fade_and_normal_return_observed=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_open_translation_specific_display_or_control_finding=True,
        early_refresh_and_fade_timing_not_hidden_or_retimed=True,
        exact_timing_differences=dict(total=30,speech=24,control_or_end=6),
        later_difference_scope='99 of299 sampled nontext comparisons differ after both following B120 exits;two additional transient comparisons differ during B172. Same-ROM focused repeats reproduce all47 command times/results and requested complete frames. Five native component fingerprints agree at3010,6610,post-effect town9370 and14050;whole1A04 actor model/captain2 agree at9370. Later19990 models,persistent objects and calendar differ. PRNG agrees at3010 and differs from6610. Original wait/yield/generator/wrapper code spans are source exact and bound to documented V824 scheduler entropy. Consistency is an inference,not a fresh every-RAND causal trace or equal-world claim.',
        initial_focus_preparer_sampling_note_amendment='V4395 rationale counted the98 ordinary later captures;the authoritative capture report also includes final20001,so complete report counts99 later differences and101 total. No sample is removed.',
        failed_pre_view_V4396_zero_transient_assertion_preserved=True,
        no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim=True,new_emulator_runs=4,
        evidence={str(p):sha(p.read_bytes()) for p in paths},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Viewed5 actual sheets and4 paired full-screen sheets;27 complete panels pass. Two transient and99 later nontext samples retained;four boots terminal.')
