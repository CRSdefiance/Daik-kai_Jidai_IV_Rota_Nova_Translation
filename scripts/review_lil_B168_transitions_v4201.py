"""Record viewed source/English progressive, FE, contact reaction and normal town return."""
import re
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B168_transition_review_v4201')
ACTUAL = Path('work/analysis/lil_B168_actual_v4200/actual_progressive_FE_three_predicates_full_effect_and_return.json')
FONT = Path('work/analysis/lil_B168_native_approval_v4187/all54_native_progressive_FE_and_source_reconciliation.json')
BASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__ == '__main__':
    assert not ROOT.exists()
    actual, font = read(ACTUAL), read(FONT)
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 51
    offline = ['DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135']
    assert actual['offline_only_display_IDs'] == offline
    views = []
    for frame, note in [(5530, 'Complete Mikhail peppercorn explanation, original nameplate/portrait and source town background.'),
                        (13450, 'Lil objects to unwanted touching; complete protest and original portrait/name.'),
                        (14170, 'Null-actor FE naturalist/nonofficer/Deck notice after the original effect.'),
                        (14650, 'Complete X instruction with the already-displayed item-information condition.'),
                        (15130, 'Normal initialized Amsterdam town return after source end2906.')]:
        path = BASE / 'lil_B168_display_v4199_reviewed_English' / f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(path).size == (256, 384)
        views.append(dict(frame=frame, path=str(path), sha256=sha(path.read_bytes()), review='Viewed complete full screen. ' + note))
    source_views, returns = [], []
    for frame in [5530, 14650, 15130]:
        jp = BASE / 'lil_B168_display_v4199_clean_Japanese' / f'frame_{frame:06d}_cold_boot.png'
        en = BASE / 'lil_B168_display_v4199_reviewed_English' / f'frame_{frame:06d}_cold_boot.png'
        a, b = [Image.open(path).convert('RGB') for path in [jp, en]]
        source_views.append(dict(frame=frame, path=str(jp), sha256=sha(jp.read_bytes()), review='Viewed complete Japanese counterpart; same original actor/scene or town return.'))
        if frame == 15130:
            assert a.tobytes() == b.tobytes()
            returns.append(dict(frame=frame, source=str(jp), source_sha256=sha(jp.read_bytes()),
                English=str(en), English_sha256=sha(en.read_bytes()), whole_RGB_equal=True))
        else:
            assert a.crop((0, 0, 256, 294)).tobytes() == b.crop((0, 0, 256, 294)).tobytes()
    sheets = []
    for sheet in actual['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        sheets.append({**sheet, 'review': 'Viewed complete actual sheet. Complete first/internal/final glyphs, original portraits/names, natural phrase boundaries, pepper/droppings reversal, ambiguous teasing and unwelcome-contact protest remain coherent. FE switches clear the speaker and preserve complete notices. No finding.'})
    assert len(sheets) == 9
    assert [(v['case'], v['fixture_exit_frame']) for v in actual['versions']] == [('clean_Japanese', 15093), ('reviewed_English', 15094)]
    assert all([r['result_words'] for r in version['actual_three_unforced_predicates']] == [[2, 0], [2, 0], [2, 0]] for version in actual['versions'])
    assert all(len(version['selected_B22_command_pairs']) == 81 and version['selected_B22_command_pairs'][-1]['result_words'] == [0, 0] for version in actual['versions'])
    branches = {r['original_source_offset'] for version in actual['versions'] for r in version['selected_B22_command_pairs']
                if r.get('original_source_block') == 168 and r['word'] in [0x100, 0x200, 0x300, 0x400]}
    assert branches == {104, 112, 402, 410, 1502, 1510}
    plan = read('work/analysis/lil_B168_relocation_v4190/nested_source_relocation_research.json')
    all_branches = {edge['offset'] for edge in plan['blocks'][0]['relative_skip_fixups']}
    assert len(all_branches) == 12 and branches <= all_branches
    offline_cases = []
    for ident in offline:
        case = next(row for row in font['cases'] if row['id'] == ident)
        assert case['complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        offline_cases.append(dict(id=ident, source_selector=20 if ident.endswith('0135') else 6,
            native_plane=case['preview'], native_plane_sha256=case['preview_sha256'], actual_display_or_byte_identical_reuse_claim=False,
            reason='The initialized roster returns0 from both Julio predicates and the Fernando predicate. These remarks retain complete source preambles, names, dispatches, stored alignments and native planes offline. Same original progressive consumer/geometry; no distinct unresolved display behavior requires a forced visit.'))
    doc = read('translations/lil_B168_editorial_manuscript_v7.json')
    ids = {row['id'] for row in actual['actual_panels']}
    macro_counts = {macro: sum(len(re.findall(r'\{MACRO:' + macro + r'\}', row['english'])) for row in doc['records'] if row['id'] in ids) for macro in ['FI', 'FA', 'FO']}
    assert macro_counts == {'FI': 6, 'FA': 1, 'FO': 1}
    ROOT.mkdir(parents=True)
    save(ROOT / 'all9_sheets_contact_FE_source_effect_and_paired_return_review.json', dict(
        actual_proof=str(ACTUAL), actual_proof_sha256=sha(ACTUAL.read_bytes()), all9_actual_sheets_viewed=sheets,
        English_full_screen_views=views, Japanese_full_screen_views=source_views, paired_source_English_whole_RGB_returns=returns,
        all51_actual_panels_and_three_FE_notices_complete=True,
        actual_six_static_actors_original_nameplates_and_portraits_verified=True,
        actual_six_of_twelve_relative_sites_observed=True, actual_relative_sites=sorted(branches),
        offline_only_relative_sites=sorted(all_branches - branches), offline_only_display_cases=offline_cases,
        actual_FI6_FA1_FO1_expansions_verified_by_complete_native_masks=macro_counts,
        original_effect_after_contact_protest_sigh_before_FE_returns_normally=True,
        source_and_English_timing_recorded_without_false_equal_frame_animation_claim=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_open_translation_specific_display_or_control_finding=True,
        source_event168_eligibility_full_playthrough_hardware_or_item_information_X_mechanic_test_not_claimed=True,
        no_B168_source_command_omitted_or_forced=True, original_B22_four_A000_initialization_commands_retained=True,
        all2_runs_cold_boot20001_frames_no_savestate_no_RAM_fixture=True,
        new_emulator_runs_added_by_this_review=0, evidence={str(path): sha(path.read_bytes()) for path in [ACTUAL, FONT, Path(__file__)]},
        full_goal_complete=False))
    print('Viewed9 actual sheets/5 English full screens/3 Japanese counterparts;51 panels,three FE,full source effect and matching town return pass. Three conditional remarks offline only.')
