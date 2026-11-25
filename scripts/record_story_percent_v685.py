"""Archive the tested combined repair and preserve all inherited audit scope."""

from pathlib import Path
from xml.etree import ElementTree

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_story_percent_v685 import ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.run_village_visits_v664 import CAP
from scripts.verify_story_percent_v685 import ROM
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V685 Story percent repairs')
DOC = Path('docs/story_percent_v685_checkpoint.md')
KEY = 'four_story_literal_percent_repairs_final_source_contract_gate_and_actual_Maria_report_v685'
POINTER = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
SOURCES = ('scripts/prepare_story_percent_v685.py', 'scripts/register_story_percent_v685.py',
    'scripts/verify_story_percent_v685.py', 'scripts/run_story_percent_v685.py',
    'scripts/finish_story_percent_v685.py', 'scripts/record_story_percent_v685.py',
    'scripts/verify_story_percent_archive_v685.py', 'scripts/build_integrated_release.py',
    'dk4tool/patch/story_literal_percent.py', 'dk4tool/script/format_safety.py',
    'dk4tool/dialogue/profiles.py', 'tests/test_story_format_safety.py', 'AGENTS.md',
    'docs/build_continuity_protocol.md', 'docs/natural_dialogue_workflow.md')


def main():
    pp = ROOT / 'proof.json'
    pre, proof = read(ROOT / 'preflight.json'), read(pp)
    assert not proof['cold_boot_verification_pending']
    assert proof['verifier_sha256'] == sha(Path('scripts/finish_story_percent_v685.py').read_bytes())
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['registry_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    test = ElementTree.parse(ROOT / 'format_gate_tests.xml').getroot()
    suite = test.find('testsuite')
    assert suite is not None and suite.attrib['tests'] == '10' and suite.attrib['failures'] == suite.attrib['errors'] == '0'
    for name in ('rafael', 'lil', 'maria'):
        report = read(ROOT / f'qa_{name}/report.json')
        assert all(not any(i['severity'] in ('error', 'warning') for i in row['issues']) for row in report['records'])
    save(ROOT / 'visual_review.json', {'all_four_final_exact_font_previews_opened': True,
        'actual_before_fixed_following_and_Hangzhou_sheet_opened': True,
        'whole_corrected_three_line_phrase_including_percent_and_following_text_readable': True,
        'source_quantities_direction_and_conditional_meanings_reviewed': True,
        'deep_other_records_not_given_new_live_parent_or_user_acceptance_credit': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': pre['profile'],
        'status': 'experimental_four_source_bound_percent_repairs_and_actual_Maria_report_verified_broader_graphics_open',
        'four_canonical_source_natural_dialogue_v2_records_original_allocations_controls_and_other_records_exact': True,
        'source_bound_final_build_gate_all_four_story_archives_rejects_old_four_hazards': True,
        'ten_focused_format_contract_tests_and16_complete_original_native_printf_controls_pass': True,
        'four_previews_zero_unwaived_QA_and_complete_actual_fixed_percent_line_masks_verified': True,
        '49_current_Maria_baseline_pairs48_unchanged_Maria_frames89_ordinary_regression_frames_exact': True,
        'only_actual24400_dialogue_rectangle_changes_source_art_and_portrait_borders_exact': True,
        'all45_current_source_photo_holds_and_complete_repaired_resident_chapters_verified': True,
        'all675_graphics_ARM9_other_files_components470_batches114_accepted_layers_and_prior_profiles_preserved': True,
        'clean_patch_reconstruction_exact': True, 'patch_sha256': proof['patch_sha256'],
        'three_other_records_have_QA_and_native_controls_not_new_live_parent_credit': True,
        'source_unlock_save_not_earned_no_guide_or_canonical_promotion': True,
        'older_SC3_B33_R0107_naturalness_review_and_three_blank_hold_classifications_remain_open': True,
        'all18_plaques_incomplete22_original_requirements_and_other_graphics_gates_open': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        latest = dict(data[POINTER])
        latest.update(candidate=str(ROM), sha256=proof['candidate_sha256'], profile=pre['profile'])
        data[POINTER], data[KEY], data['current_goal_turn_classification'] = latest, entry, 'progress'
        save(path, data)
    heading = '## V685: four natural percentage repairs and final source-bound format guard'
    addition = ('Full Maria opening exposed 3% of sales being read as an octal conversion. '
        'A final source-bound census finds four hazards:SC0B177R0180,SC2B133R0136,'
        'SC3B33R0137,SC3B135R0325. Four clean-source natural-dialogue-v2 records use '
        'percent,with quantities/direction/conditions and exact allocations preserved. '
        'All four previews pass QA;10 focused tests and16 original-native printf '
        'controls pass. The final builder rejects introduced commands even when '
        'valid C syntax,preserving source-leading25. V685 retains all470 batches,'
        '114 accepted layers,all graphics/ARM9/other components;only four spans in '
        'SC0/SC2/SC3 change from V678. Clean patch reconstruction is exact. Actual '
        'Maria/baseline49 full pairs match;48 unaffected Maria frames and89 '
        'ordinary title/selection/story/Town frames match V678. The corrected '
        'three lines including percent and empty rows pass complete font masks; '
        'Hangzhou follows normally. Other deep records have native/QA coverage,'
        'not new live-parent credit. Experimental pointer advances to V685; '
        'canonical/V610 pointers unchanged. Older B33R0107 wording,three blank '
        'holds,all18 plaques,22 historical scopes and broader graphics remain '
        'open. ROM/patch/evidence saved on E,no guide promotion or commit/push. '
        'See [V685 checkpoint](story_percent_v685_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for case in ('maria', 'baseline', 'ordinary'):
        folder = CAP / ('story_percent_v685_' + case)
        for source in folder.rglob('*'):
            if source.is_file():
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta')):
        copy(source, ARCHIVE / 'release' / source.name)
    for source in (*map(Path, SOURCES), DOC, Path('translations/story_literal_percent_v1.json'),
                   Path('translations/release_stack.json'), *map(Path, pre['batches'])):
        copy(source, ARCHIVE / 'sources' / source)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'source_files': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
            if p.is_file() and p.name != 'provenance.json'}, 'candidate_sha256': proof['candidate_sha256'],
        'experimental_not_canonical_or_full_graphics_acceptance': True, 'full_goal_complete': False})
    print('V685 tested combined percentage repair, source gate and full retained scope archived.', flush=True)


if __name__ == '__main__':
    main()
