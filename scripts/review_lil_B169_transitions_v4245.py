"""Bind all viewed B169 sheets, full screens, source effect and exact town return."""
import re
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_transition_review_v4245')
ACTUAL = Path('work/analysis/lil_B169_actual_v4244/actual_progressive_three_predicates_full_effect_and_return.json')
FONT = Path('work/analysis/lil_B169_native_approval_v4230/all36_native_progressive_and_source_reconciliation.json')
AMENDMENT = Path('work/analysis/lil_B169_operand_notation_v4243/source_A000_hex0029_0001_decimal41_1_metadata_correction.json')
BASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__ == '__main__':
    assert not ROOT.exists()
    actual,font,amendment = map(read,[ACTUAL,FONT,AMENDMENT])
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 33
    assert amendment['operand_hex_values'] == ['0029','0001'] and amendment['operand_decimal_values'] == [41,1]
    offline = ['DK4_MES_B169_R0067','DK4_MES_B169_R0082','DK4_MES_B169_R0097']
    assert actual['offline_only_display_IDs'] == offline
    views = []
    for frame,note in [(4570,'Camille flustered self-correction, full Mikhail Letzel address, naturalist flattery and unfinished question.'),
                       (5530,'Seven treasures and Seven Sages; locations marked on differently shaped maps, complete source nameplate/portrait and town background.'),
                       (10810,'Normal initialized Amsterdam town return after the final give-and-take, original hex0029/0001 A000 and single end2558.')]:
        path = BASE/'lil_B169_display_v4242_reviewed_English'/f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(path).size == (256,384)
        views.append(dict(frame=frame,path=str(path),sha256=sha(path.read_bytes()),review='Viewed complete full screen. '+note))
    source_views,returns = [],[]
    for frame in [5530,10810]:
        jp = BASE/'lil_B169_display_v4242_clean_Japanese'/f'frame_{frame:06d}_cold_boot.png'
        en = BASE/'lil_B169_display_v4242_reviewed_English'/f'frame_{frame:06d}_cold_boot.png'
        a,b = [Image.open(path).convert('RGB') for path in [jp,en]]
        source_views.append(dict(frame=frame,path=str(jp),sha256=sha(jp.read_bytes()),review='Viewed complete Japanese-content counterpart with original matching actor/scene or town return.'))
        if frame == 10810:
            assert a.tobytes() == b.tobytes()
            returns.append(dict(frame=frame,source=str(jp),source_sha256=sha(jp.read_bytes()),English=str(en),English_sha256=sha(en.read_bytes()),whole_RGB_equal=True))
        else:
            assert a.crop((0,0,256,294)).tobytes() == b.crop((0,0,256,294)).tobytes()
    sheets = []
    for sheet in actual['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        sheets.append({**sheet,'review':'Viewed complete actual sheet: all leading/internal/final glyphs, source portraits/names and natural phrase flow. Fluster, unwanted-touch threats, legend, conditional clues, sealed Proofs, Women follow-up and shared treasure-value give-and-take remain coherent. No translation-specific display finding.'})
    assert len(sheets) == 6
    assert [(v['case'],v['fixture_exit_frame']) for v in actual['versions']] == [('clean_Japanese',10776),('reviewed_English',10773)]
    for version in actual['versions']:
        assert [r['result_words'] for r in version['actual_three_unforced_predicates']] == [[2,0],[2,0],[2,0]]
        assert len(version['selected_B22_command_pairs']) == 53 and version['selected_B22_command_pairs'][-1]['result_words'] == [0,0]
        effect = version['actual_source_hex0029_0001_effect']
        assert effect['original_source_offset'] == 2550 and effect['result_words'] == [3,0]
        assert version['source_end_offset'] == 2558
    branches = {r['original_source_offset'] for v in actual['versions'] for r in v['selected_B22_command_pairs'] if r.get('original_source_block')==169 and r['word'] in [0x100,0x200,0x300,0x400]}
    assert branches == {1144,1152,1242,1250,1328,1336}
    plan = read('work/analysis/lil_B169_relocation_v4233/nested_source_relocation_research.json')
    all_branches = {edge['offset'] for edge in plan['blocks'][0]['relative_skip_fixups']}
    assert len(all_branches) == 12 and branches <= all_branches
    selectors = dict(zip(offline,[6,21,20],strict=True))
    offline_cases = []
    for ident in offline:
        case = next(row for row in font['cases'] if row['id']==ident)
        assert case['complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        offline_cases.append(dict(id=ident,source_selector=selectors[ident],native_plane=case['preview'],native_plane_sha256=case['preview_sha256'],
            actual_display_or_byte_identical_reuse_claim=False,reason='The initialized roster returns0 from the original Julio, Ian and Fernando predicates. These remarks retain complete source preambles, source-bound names, branches, dispatches, stored alignments and complete native planes offline. Same original progressive geometry; no distinct unresolved display behavior requires a forced visit.'))
    doc = read('translations/lil_B169_editorial_manuscript_v4.json')
    ids = {row['id'] for row in actual['actual_panels']}
    macro_counts = {macro:sum(len(re.findall(r'\{MACRO:'+macro+r'\}',row['english'])) for row in doc['records'] if row['id'] in ids) for macro in ['FI','FA','FO']}
    assert macro_counts == {'FI':5,'FA':0,'FO':1}
    ROOT.mkdir(parents=True)
    save(ROOT/'all6_sheets_source_effect_and_paired_return_review.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),all6_actual_sheets_viewed=sheets,
        English_full_screen_views=views,Japanese_full_screen_views=source_views,paired_source_English_whole_RGB_returns=returns,
        all33_actual_progressive_panels_complete=True,actual_three_static_actors_original_nameplates_and_portraits_verified=True,
        actual_six_of_twelve_relative_sites_observed=True,actual_relative_sites=sorted(branches),offline_only_relative_sites=sorted(all_branches-branches),
        offline_only_display_cases=offline_cases,actual_FI5_FA0_FO1_expansions_verified_by_complete_native_masks=macro_counts,
        original_hex0029_0001_effect_after_give_and_take_before_single_end_returns_normally=True,
        source_effect_operand_hex_values=['0029','0001'],source_effect_operand_decimal_values=[41,1],
        source_effect_operand_notation_amendment=str(AMENDMENT),source_effect_operand_notation_amendment_sha256=sha(AMENDMENT.read_bytes()),
        source_and_English_timing_recorded_without_false_equal_frame_animation_claim=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        source_event169_eligibility_earned_flag_full_playthrough_or_hardware_test_not_claimed=True,no_B169_source_command_omitted_or_forced=True,
        original_B22_four_A000_initialization_commands_retained=True,all2_runs_cold_boot20001_frames_no_savestate_no_RAM_fixture=True,
        new_emulator_runs_added_by_this_review=0,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,FONT,AMENDMENT,Path(__file__)]},full_goal_complete=False))
    print('Viewed6 actual sheets/3 English full screens/2 Japanese counterparts;33 panels,source effect and RGB-identical town return pass. Three conditional remarks offline only.')
