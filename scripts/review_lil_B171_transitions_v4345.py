"""Bind viewed B171 panels, dream/morning presentation, town return and later-state scope."""
import re
from pathlib import Path
from PIL import Image,ImageChops
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B171_transition_review_v4345')
ACTUAL=Path('work/analysis/lil_B171_actual_v4342/actual_all37_dream_morning_presentations_resource_C200_and_first_end.json')
REPEAT=Path('work/analysis/lil_B171_repeat_verification_v4344/post_B171_actor_captain_and_same_ROM_repeat_comparison.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__=='__main__':
    assert not ROOT.exists()
    actual,repeat=map(read,[ACTUAL,REPEAT])
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs']
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==37
    assert repeat['paired_town11770_whole1A04_actor_models_and_captain2_equal']
    assert repeat['each_same_ROM_repeat_all53_command_times_results_and_first_end_equal']
    assert repeat['cross_language_command_order_results_and_first_end_word_equal']
    assert repeat['all_requested_same_ROM_repeat_frames_whole_RGB_equal']
    assert all(all(s['component_equality'].values()) for s in repeat['paired_native_persistent_state_and_PRNG_samples'] if s['frame']<=16450)
    notes={3130:'Initial faint call and Lil response over the original black upper screen.',
        4090:'Full Sanghyeon Kan portrait/nameplate and spoken Sanghyeon introduction; shared teacher and seniority complete.',
        7450:'Original bedroom fade becomes visible under Sanghyeon farewell after4621; no invented command meaning.',
        7510:'Bedroom at waking, Lil portrait/name and complete dream uncertainty.',
        7690:'Same bedroom with Yifa Sol morning greeting and complete interrupted call.',
        11770:'Normal initialized Amsterdam town return after ship-work reminder, final response, C200 and first end.'}
    views=[]
    for frame,note in notes.items():
        p=BASE/'lil_B171_display_v4341_reviewed_English'/f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(p).size==(256,384)
        views.append(dict(frame=frame,path=str(p),sha256=sha(p.read_bytes()),review='Viewed complete full screen. '+note))
    source_views=[];returns=[]
    for frame in [7450,7510,7690,11770]:
        paths=[BASE/('lil_B171_display_v4341_'+c)/f'frame_{frame:06d}_cold_boot.png' for c in ['clean_Japanese','reviewed_English']]
        a,b=[Image.open(p).convert('RGB') for p in paths]
        assert a.crop((0,0,256,294)).tobytes()==b.crop((0,0,256,294)).tobytes()
        source_views.append(dict(frame=frame,path=str(paths[0]),sha256=sha(paths[0].read_bytes()),review='Viewed clean Japanese-content counterpart; same original scene and character/name regions.'))
        if frame==11770:
            assert a.tobytes()==b.tobytes()
            returns.append(dict(frame=frame,source=str(paths[0]),source_sha256=sha(paths[0].read_bytes()),English=str(paths[1]),English_sha256=sha(paths[1].read_bytes()),whole_RGB_equal=True))
    sheets=[]
    for sheet in actual['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        sheets.append({**sheet,'review':'Viewed complete actual sheet: complete first/internal/final glyphs; Lil, Sanghyeon and Yifa portraits/full nameplates; formal introduction and humility, mountain/travel/expulsion facts, severed training bond then siblinglike affection, humble requests, dream uncertainty, morning recognition, Yifa arts explanation, training message and ship-work comic reminder read coherently. No translation-specific display finding.'})
    assert len(sheets)==7
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[11737,11735]
    for v in actual['versions']:
        assert len(v['selected_B22_command_pairs'])==53 and v['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        assert v['actual_C200']['result_words']==[3,0] and v['source_first_end_offset']==2112
        assert v['second_source_end2116_stored_and_decoded_offline_not_actually_reached']
        assert [r['word'] for r in v['actual_presentation_commands']]==[0x6000,0x4500,0x4621,0x61FF]
        assert [r['word'] for r in v['actual_resources']]==[0x6325]
    doc=read('translations/lil_B171_editorial_manuscript_v4.json')
    ids={r['id'] for r in actual['actual_panels']}
    macros={m:sum(len(re.findall(r'\{MACRO:'+m+r'\}',r['english'])) for r in doc['records'] if r['id'] in ids) for m in ['FI','FA','FO']}
    assert macros=={'FI':1,'FA':0,'FO':0}
    reports=[read(BASE/('lil_B171_display_v4341_'+c)/'capture_report.json') for c in ['clean_Japanese','reviewed_English']]
    jp={p['frame']:p for p in reports[0]['frames_captured']};checks=[];later=[]
    for en in reports[1]['frames_captured']:
        source=jp[en['frame']]
        for p in [source,en]:assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
        a,b=[Image.open(p['path']).convert('RGB') for p in [source,en]]
        box=ImageChops.difference(a.crop((0,0,256,294)),b.crop((0,0,256,294))).getbbox()
        row=dict(frame=en['frame'],source=source['path'],source_sha256=source['PNG_sha256'],English=en['path'],English_sha256=en['PNG_sha256'],upper_and_portrait_name_regions_equal=box is None)
        checks.append(row)
        if box:later.append({**row,'differing_upper_name_RGB_bounds':box,'not_masked_or_retimed':True})
    assert len(later)==59 and min(r['frame'] for r in later)==16570
    following=[]
    for case in ['clean_Japanese','reviewed_English']:
        trace=read(BASE/('lil_B171_display_v4341_'+case)/'observer/commands.json');rows=trace['rows'];flow=[]
        for row in rows:
            if row['kind']!='after_command':continue
            e=rows[row['entry_row']]
            if e['source']['block']==120:
                flow.append(dict(offset=e['source']['instruction_offset'],word=e['source']['first_word'],start=e['frame'],returned=row['frame'],result_words=row['result_words']))
        assert len(flow)==30 and flow[-1]['word']==0 and flow[-1]['returned']<16570
        following.append(dict(case=case,block=120,commands=flow,new_editorial_credit=0))
    shape=lambda v:[(r['offset'],r['word'],r['result_words']) for r in v['commands']]
    assert shape(following[0])==shape(following[1])
    later_views=[]
    for case in ['clean_Japanese','reviewed_English']:
        for frame in [16570,19990]:
            p=BASE/('lil_B171_display_v4341_'+case)/f'frame_{frame:06d}_cold_boot.png'
            later_views.append(dict(case=case,frame=frame,path=str(p),sha256=sha(p.read_bytes()),review='Viewed later sailing: departure display, boat/sea animation and later supplies differ. Preserved without equal-world or fresh causal-trace claim.'))
    ROOT.mkdir(parents=True)
    paths=[ACTUAL,REPEAT,Path('translations/lil_B171_editorial_manuscript_v4.json'),Path(__file__)]
    save(ROOT/'all7_sheets_dream_morning_C200_and_paired_return_review.json',dict(
        all7_actual_sheets_viewed=sheets,English_full_screen_views=views,Japanese_full_screen_views=source_views,
        paired_source_English_whole_RGB_town_returns=returns,all_sampled_nontext_region_checks=checks,
        later59_sailing_region_differences= later,later_sailing_views=later_views,following_B120_same_command_shape=following,
        actual_macro_counts=macros,first_end2112_actual_second_end2116_stored_and_native_decoder_only=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_open_translation_specific_display_or_control_finding=True,
        later_state_comparison=str(REPEAT),later_state_comparison_sha256=sha(REPEAT.read_bytes()),
        later_difference_scope='All sampled upper/portrait/name regions agree through B171, paired whole-RGB town11770 and following B120.59 later sampled regions differ after both B120 exits. Focused same-ROM repeats reproduce command times and requested frames; persistent component fingerprints agree through16450, whole actor models/captain2 agree at11770. PRNG and original source-exact wait/yield spans are measured and rebound to documented V824 scheduler entropy. That mechanism is a scoped inference, not a new B171 every-RAND causal trace or equal-world claim.',
        no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim=True,new_emulator_runs=4,
        evidence={str(p):sha(p.read_bytes()) for p in paths},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Viewed7 actual sheets and dream/morning/fullscreen/town pairs;all37 panels pass. Later59 sailing differences and four-boot state scope preserved.')
