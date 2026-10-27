"""Record viewed source/English actual displays, distinct ends and query-owned final state."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_transition_review_v4152')
ACTUAL=Path('work/analysis/lil_B167_actual_v4151/actual_both_choices_conditional_panels_and_distinct_returns.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists();actual=read(ACTUAL)
    assert not actual['failures'] and actual['fresh_actual_unique_speech_panels']==25
    assert actual['complete_matching_observations']==actual['actual_English_speech_observations']==28
    offline=['DK4_MES_B167_R0045','DK4_MES_B167_R0131'];assert actual['offline_only_display_IDs']==offline
    notes={(0,3670):'Complete Okay/No thanks captions with Okay visibly selected; source menu result0 follows.',
        (0,7510):'Complete directly-astern explanation; original Shipwright nameplate/portrait, all clauses and final word intact.',
        (0,8230):'Complete company/return-to-work farewell before the lecture end.',
        (0,8410):'Normal initialized Amsterdam town return after source end2172.',
        (1,3670):'Complete labels with No thanks visibly selected; source menu result1 follows.',
        (1,3850):'Janus Pasar original nameplate/portrait and complete formal refusal response.',
        (1,4330):'Complete Shipwright greener-listener reply on the refusal path.',
        (1,4570):'Normal initialized Amsterdam town return after separate source end430.'}
    views=[]
    for (option,frame),note in notes.items():
        p=BASE/f'lil_B167_display_v4149_O{option}_reviewed_English'/f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(p).size==(256,384)
        views.append(dict(option_index=option,frame=frame,path=str(p),sha256=sha(p.read_bytes()),review='Viewed complete full screen. '+note))
    sourceviews,returns=[],[]
    for option,frame in [(0,7510),(0,8410),(1,4570)]:
        jp=BASE/f'lil_B167_display_v4149_O{option}_clean_Japanese'/f'frame_{frame:06d}_cold_boot.png'
        en=BASE/f'lil_B167_display_v4149_O{option}_reviewed_English'/f'frame_{frame:06d}_cold_boot.png'
        a,b=[Image.open(p).convert('RGB') for p in [jp,en]]
        sourceviews.append(dict(option_index=option,frame=frame,path=str(jp),sha256=sha(jp.read_bytes()),review='Viewed complete Japanese counterpart; original Shipwright actor or normal town return agrees with English.'))
        if frame==7510:assert a.crop((0,0,256,294)).tobytes()==b.crop((0,0,256,294)).tobytes()
        else:
            assert a.tobytes()==b.tobytes();returns.append(dict(option_index=option,frame=frame,source=str(jp),source_sha256=sha(jp.read_bytes()),English=str(en),English_sha256=sha(en.read_bytes()),whole_RGB_equal=True))
    sheets=[]
    for s in actual['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append({**s,'review':'Viewed complete actual sheet. Bored Shipwright humor, flattery, complete sail explanations and wind/mast facts, Manuel answer, Janus response and separate refusal/farewell remain coherent. All leading/internal/final glyphs, names, portraits and natural clause wraps intact; no finding.'})
    assert len(sheets)==5
    en=[v for v in actual['versions'] if v['case']=='reviewed_English'];jp=[v for v in actual['versions'] if v['case']=='clean_Japanese']
    assert [(v['option_index'],v['fixture_exit_frame']) for v in en]==[(0,8374),(1,4533)]
    assert [(v['option_index'],v['fixture_exit_frame']) for v in jp]==[(0,8375),(1,4534)]
    assert all(v['actual_unforced_Cesare_predicate']['result_words']==[2,0] for v in actual['versions'])
    assert all(v['source_end_offset']==(2172 if v['option_index']==0 else 430) for v in actual['versions'])
    assert all(v['selected_B22_command_pairs'][-1]['result_words']==[0,0] for v in actual['versions'])
    assert [v['actual_choice_command_pair']['result_words'] for v in en]==[[2,0],[2,1]]
    assert actual['both_versions_visible_highlight_matches_returned_option_and_unselected_never_highlighted']
    branches={p['original_source_offset'] for v in en for p in v['selected_B22_command_pairs'] if p.get('original_source_block')==167 and p['word'] in [0x100,0x200,0x300,0x400]}
    assert branches=={180,184,188,272,280,2016,2024}
    plan=read('work/analysis/lil_B167_relocation_v4139/nested_source_relocation_research.json')
    allbranches={e['offset'] for e in plan['blocks'][0]['relative_skip_fixups']};assert len(allbranches)==12 and branches<=allbranches
    native=read('work/analysis/lil_B167_native_approval_v4135/all29_native_speech_choice_and_source_reconciliation.json');offcases=[]
    for ident in offline:
        c=next(r for r in native['cases'] if r['id']==ident)
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        offcases.append(dict(id=ident,source_selector=13,native_plane=c['preview'],native_plane_sha256=c['preview_sha256'],actual_display_or_byte_identical_reuse_claim=False,reason='Both source Cesare predicates remain unforced; the initialized roster returns0 on each path. These alternative-path remarks retain exact full preambles, actor/name consumers, relocated dispatch, stored alignments and complete native planes. They add no distinct unresolved display behavior requiring a forced visit.'))
    ROOT.mkdir(parents=True)
    save(ROOT/'both_choices_all5_sheets_static_names_and_distinct_returns_review.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),all5_actual_sheets_viewed=sheets,English_full_screen_views=views,Japanese_full_screen_views=sourceviews,paired_source_English_whole_RGB_returns=returns,all25_unique_panels28_English_observations_and_both_menu_labels_complete=True,actual_Shipwright109_Lil2_Janus4_Manuel23_original_names_and_portraits_verified=True,actual_seven_of_twelve_relative_sites_observed=True,actual_relative_sites=sorted(branches),offline_only_relative_sites=sorted(allbranches-branches),offline_only_display_cases=offcases,both_menu_options_actually_return_at_distinct_original_source_ends=True,final_type0_second_word_is_later_membership_result_not_forced_menu_index=True,source_and_English_timing_recorded_without_false_equal_frame_animation_claim=True,complete_English_label_foreground_and_per_version_highlight_return_association_pass=True,representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,source_event167_eligibility_full_playthrough_and_hardware_not_claimed=True,no_B167_A000_or_any_source_command_omitted_from_fixture=True,original_B22_four_A000_initialization_commands_retained=True,all4_runs_cold_boot14401_frames_no_savestate_no_RAM_fixture=True,new_emulator_runs_added_by_this_review=0,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,Path(__file__)]},full_goal_complete=False))
    print('Viewed5 actual sheets/8 English full screens/3 Japanese counterparts;25 unique/28 observations,both menu results,distinct ends and matching town returns pass. Two Cesare remarks offline only.')
