"""Save original ending evidence and additive scope-preserving audit entries."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.research_ending_transitions_v642 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/ending_transitions_v642_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V642 Rafael Lil ending transitions')
KEY = 'all18_Rafael_Lil_ending_texture_bindings_full_RGB_fades_credits_and_terminal_holds_v642'


def main():
    proof_path = ROOT / 'native_ending_transitions_proof.json'
    proof, pre = read(proof_path), read(ROOT / 'preflight.json')
    assert proof['candidate_sha256'] == pre['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(proof['full_source_compositions']) == 78
    assert len(proof['separate_terminal_hold_compositions']) == 3
    assert proof['whole_comparison_pixels'] == 3981312 and proof['read_only_GPU_checkpoints'] == 135
    assert proof['actual_all18_source_texture_bindings'] == {'0': list(range(8)), '2': list(range(10))}
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    visual = read(ROOT / 'visual_review.json')
    assert visual['all27_declared_upper_anchor_crops_visually_inspected']
    assert sha(Path(visual['sheet']).read_bytes()) == visual['sha256']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    derived = ARCHIVE / 'Derived source compositions'
    derived.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, Path(__file__), ROOT / 'preflight.json', ROOT / 'run_configs.json',
        ROOT / 'additional_sample_plan.json', ROOT / 'fixture_guards.json', ROOT / 'visual_review.json',
        ROOT / 'rafael_inputs.json', ROOT / 'lil_inputs.json', ROM.with_suffix('.manifest.json')]
    files.extend(Path(p) for p in proof['scripts'])
    files.extend(ROOT / f'{label}_verified_native_bindings.json' for label in ('rafael', 'lil', 'rafael_detail', 'lil_detail'))
    files.extend(ROOT / f'{label}_transition_diagnostic.json' for label in ('rafael', 'lil'))
    files.extend(ROOT / f'{label}_native_bindings.json' for label in ('rafael', 'lil'))
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    checked_copy(visual['sheet'], derived / Path(visual['sheet']).name)
    for row in proof['full_source_compositions']:
        path = Path(row['source_reconstruction'])
        assert sha(path.read_bytes()) == row['source_reconstruction_sha256']
        checked_copy(path, derived / path.name)
    for row in proof['reports']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['sha256']
        checked_copy(path, ARCHIVE / (row['label'] + '_capture_report.json'))
        checked_copy(path.parent / 'navigation_command_journal.json', ARCHIVE / (row['label'] + '_navigation_journal.json'))
    screenshots = []
    selected = proof['all_screenshots'] + [{'label': r['label'], **r['PNG']} for r in proof['complete_ending_save_prompts']]
    for row in selected:
        source = Path(row['path'])
        assert sha(source.read_bytes()) == row['PNG_sha256']
        target = ARCHIVE / f"{row['label']}_frame{row['frame']:06d}_UNMODIFIED_NATIVE.png"
        checked_copy(source, target)
        screenshots.append({'path': str(target), 'frame': row['frame'], 'run': row['label'],
            'sha256': row['PNG_sha256'], 'unmodified_native_capture': True,
            'synthetic_ending_state_not_earned_ending_or_guide': True})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'screenshots': screenshots, 'guide_candidates_created': False,
        'full_RAM_GPU_and_original_run_files_retained_on_E': True, 'full_goal_complete': False,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'four_terminal_cold_boots135_read_only_GPU_checkpoints': True,
        'all8_M29_and10_M31_actual_original_source_texture_bindings_verified': True,
        'complete_active_source_compositions': 78, 'separate_complete_terminal_logo_holds': 3,
        'exact_whole_RGB_comparison_pixels': 3981312,
        'all165_original_native_draws_full_ABI_clean_code_and_actual_texture_palette_arguments': True,
        'fixed_two_frame_delay_and_all_six_alternative_delay_counterexamples_verified': True,
        '39_visible_wrong_alpha_controls_and_other_visible_texel_blank_geometry_controls_rejected': True,
        '12_complete_black_transitions_verified_without_visible_picture_control_claim': True,
        'four_complete_ending_save_prompts238_ink_and_blank_cells_verified': True,
        'source_art_and_original_English_credits_Fin_and_Koei_retained': True,
        'all18_original_plaques_incomplete_all22_historical_scopes_exact': True,
        'sepia_legacy_comic_title_village_miniature_Confirm_other_movie_material_acceptance_gates_open': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False, 'canonical_promoted': False,
        'forced_ending_fixture_not_earned_completion_every_frame_or_hardware': True}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        assert all(read(path)[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V642: complete sampled Rafael/Lil ending compositions and all texture bindings'
    addition = """

Four terminal V640 cold boots use the authorized one-byte ending-state fixture,
with original captain selection and no savestate/movie substitution.135 read-only
GPU checkpoints support78 complete active source compositions and3 separate final
logo holds:3981312 exact RGB comparisons,all8 M29/all10 M31 texture bindings,
165 complete original native draws with full ABI/clean-code checks,39 rejected
wrong-alpha controls and12 complete black transitions. Both original English
credit planes and all4 complete ending-save prompts pass. One fixed2-frame delay
passes;0/1/3 each fail for both captains. Initial terminal black-model failures are
retained and resolved by complete original static-logo comparisons.139 unmodified
full captures,78 derived source compositions and a27-anchor visual sheet are
archived on E;forced endings are excluded from ordinary guide evidence. No ROM,
patch,registry,canonical or release-pointer changes. All18 plaques incomplete,
all22 historical scopes exact;sepia/legacy and other graphics gates remain open.
See [V642 checkpoint](ending_transitions_v642_checkpoint.md).
"""
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n' + addition, encoding='utf-8')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    print(f'Archived{len(screenshots)} unmodified ending screenshots/78 source compositions;3 audits updated;all18/22 scopes and release artifacts preserved.')


if __name__ == '__main__':
    main()
