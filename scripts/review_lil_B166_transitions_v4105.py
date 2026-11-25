"""Record viewed actual sheets/full screens and distinguish the unvisited Fernando remark."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B166_transition_review_v4105')
ACTUAL = Path('work/analysis/lil_B166_actual_v4104/actual_both_choices_conditional_panels_and_single_return.json')
BASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__ == '__main__':
    assert not ROOT.exists()
    actual = read(ACTUAL)
    assert not actual['failures'] and actual['fresh_actual_unique_speech_panels'] == 41
    assert actual['complete_matching_observations'] == actual['actual_English_speech_observations'] == 73
    assert actual['offline_only_display_IDs'] == ['DK4_MES_B166_R0087']
    notes = {
        (0,2950): 'Complete absorbed sail-placement opening; original Manuel Almeida nameplate and portrait.',
        (0,3550): 'Original 4641 full Manuel figure, complete nameplate/portrait and gently enthusiastic ship-care speech.',
        (0,7510): 'Camille original portrait/name; FI expands to Lil in the complete crying-ship callback.',
        (0,9970): 'Manuel grateful consent before the advice menu; no runtime recruitment effect is inferred.',
        (0,10150): 'Complete source-owned Manuel Almeida spoken introduction and original nameplate.',
        (0,10630): 'Complete Please do and Decline captions; first option visibly selected before native result 0.',
        (0,11170): 'Complete high Speech and First Mate\'s Office/Chapel advice; all four rows and final word intact.',
        (0,12850): 'Normal initialized Amsterdam town return after the sole declared source end.',
        (1,10750): 'Complete captions and visibly selected Decline before native result 1; advice alone is declined.',
        (1,10930): 'Complete decline-only response with original Manuel nameplate and portrait.',
        (1,11230): 'Normal initialized Amsterdam town return after the same source end on the decline path.',
    }
    views = []
    for (option,frame),note in notes.items():
        path = BASE / f'lil_B166_display_v4103_O{option}_reviewed_English' / f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(path).size == (256,384)
        views.append(dict(option_index=option,frame=frame,path=str(path),sha256=sha(path.read_bytes()),review='Viewed complete full screen. ' + note))
    sourceviews, returns = [], []
    for option,frame in [(0,3550),(0,12850),(1,11230)]:
        jp = BASE / f'lil_B166_display_v4103_O{option}_clean_Japanese' / f'frame_{frame:06d}_cold_boot.png'
        en = BASE / f'lil_B166_display_v4103_O{option}_reviewed_English' / f'frame_{frame:06d}_cold_boot.png'
        a,b = [Image.open(p).convert('RGB') for p in [jp,en]]
        sourceviews.append(dict(option_index=option,frame=frame,path=str(jp),sha256=sha(jp.read_bytes()),
            review='Viewed complete Japanese counterpart; original Manuel figure/portrait/name or normal town return agrees with English.'))
        if frame == 3550:
            assert a.crop((0,0,256,294)).tobytes() == b.crop((0,0,256,294)).tobytes()
        else:
            assert a.tobytes() == b.tobytes()
            returns.append(dict(option_index=option,frame=frame,source=str(jp),source_sha256=sha(jp.read_bytes()),
                English=str(en),English_sha256=sha(en.read_bytes()),whole_RGB_equal=True))
    sheets = []
    for sheet in actual['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        sheets.append({**sheet,'review':'Viewed complete actual dialogue sheet. All 41 distinct speeches preserve Manuel\'s apologetic absorption and professional advice, Lil\'s impatience and Camille\'s enthusiasm. Crying-ship callbacks, room/stat/role terms and branch-specific ending remain coherent. Complete glyphs and natural clause wraps; no finding.'})
    assert len(sheets) == 7
    en = [v for v in actual['versions'] if v['case'] == 'reviewed_English']
    jp = [v for v in actual['versions'] if v['case'] == 'clean_Japanese']
    assert [(v['option_index'],v['fixture_exit_frame']) for v in en] == [(0,12693),(1,11015)]
    assert [(v['option_index'],v['fixture_exit_frame']) for v in jp] == [(0,12695),(1,11016)]
    branches = {p['original_source_offset'] for v in en for p in v['selected_B22_command_pairs']
                if p['word'] in [0x100,0x200,0x300,0x400]}
    assert branches == {1168,1176,2180,2184,2892,2934}
    assert all(v['actual_unforced_Fernando_predicate']['result_words'] == [2,0] for v in actual['versions'])
    assert all(v['source_end_offset'] == 2948 for v in actual['versions'])
    assert actual['both_versions_visible_highlight_matches_returned_option_and_unselected_never_highlighted']
    native = read('work/analysis/lil_B166_native_approval_v4082/all44_native_speech_choice_source_and_actual_menu_reconciliation.json')
    case = next(r for r in native['cases'] if r['id'] == 'DK4_MES_B166_R0087')
    assert case['complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
    assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    ROOT.mkdir(parents=True)
    save(ROOT / 'both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),all7_actual_sheets_viewed=sheets,
        English_full_screen_views=views,Japanese_full_screen_views=sourceviews,paired_source_English_whole_RGB_returns=returns,
        all41_unique_panels73_English_observations_and_both_menu_labels_complete=True,
        actual_Manuel_original_nameplate_portrait_full_figure_and_FI3_verified=True,
        actual_six_of_eight_relative_sites_observed=True,offline_only_relative_sites=[1172,1212],
        offline_only_display_cases=[dict(id='DK4_MES_B166_R0087',source_selector=20,native_plane=case['preview'],
            native_plane_sha256=case['preview_sha256'],actual_display_or_byte_identical_reuse_claim=False,
            reason='The original unforced Fernando membership query returns 0 in all four fresh initialized boots. His one short static-actor remark is skipped. Complete source/current preamble, actor/name consumers, relocated dispatch, four stored macro alignments and native plane pass; no distinct untested display behavior requires forcing this conditional visit.')],
        both_advice_paths_actually_return_at_same_source_end_preserving_choice_word=True,
        source_English_menu_entry_two_frames_apart_and_blink_phases_recorded=True,
        complete_189_English_foreground_pixels_and_per_version_visible_selection_return_association_pass=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_open_translation_specific_display_or_control_finding=True,
        source_event166_eligibility_and_recruitment_effect_not_claimed=True,
        all4_runs_cold_boot20001_frames_no_savestate_no_RAM_fixture=True,new_emulator_runs_added_by_this_review=0,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,Path(__file__)]},full_goal_complete=False))
    print('Viewed7 actual sheets/11 English full screens/3 Japanese counterparts;41 unique/73 observations,both menus and RGB-identical town returns pass;Fernando remark offline only.')
