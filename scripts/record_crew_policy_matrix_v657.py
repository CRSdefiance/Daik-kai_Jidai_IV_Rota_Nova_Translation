"""Archive ordinary policy evidence and preserve all original open audit items."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/crew_policy_matrix_v657')
DOC = Path('docs/crew_policy_matrix_v657_checkpoint.md')
KEY = 'ordinary_five_ship_three_original_allocation_policies91_whole_plaques_and_six_native_notices_v657'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V657 Crew policies')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V653 Crew policies')


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert len(proof['all_three_policy_native_and_actual_models']) == 3
    assert len(proof['all_seven_plaques_each_complete_in_thirteen_actual_contexts']) == 91
    assert len(proof['six_complete_native_notices_and_confirmation_planes']) == 6
    assert proof['whole_plaque_pixel_comparisons'] == 95836 and not proof['full_goal_complete']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    folder = Path(pre['output'])
    report_path = folder / 'capture_report.json'
    assert sha(report_path.read_bytes()) == proof['report_sha256']
    report = read(report_path)
    sources = [DOC, Path(__file__), *(Path(p) for p in proof['scripts']),
               *ROOT.glob('*.json'), *ROOT.glob('*.txt')]
    for source in sources:
        copy(source, ARCHIVE / source.name)
    copy(report_path, ARCHIVE / 'actual' / 'capture_report.json')
    for shot in report['frames_captured']:
        copy(shot['path'], ARCHIVE / 'actual' / Path(shot['path']).name)
    for key in ('read_only_capture_RAM_snapshots', 'read_only_pause_RAM_snapshots'):
        for row in report[key]:
            copy(row['path'], ARCHIVE / 'actual' / Path(row['path']).name)
    for row in proof['six_complete_native_notices_and_confirmation_planes']:
        manifest = Path(row['native_state_manifest'])
        for source in manifest.parent.iterdir():
            if source.is_file():
                copy(source, ARCHIVE / 'actual' / manifest.parent.name / source.name)
    copy(pre['donor'], ARCHIVE / 'ordinary_slot6_input.dsv')
    copy(report['battery_save_preloaded']['destination'], ARCHIVE / 'isolated_emulator_output.dsv')
    shots = {s['frame']: s for s in report['frames_captured']}
    guide = []
    for label, frame in (('Flagship', 5500), ('Minimum', 7500), ('Even', 9100)):
        source = Path(shots[frame]['path'])
        dest = GUIDE / f'V653_Assign_Sailors_{label}_UNMODIFIED_NATIVE.png'
        copy(source, dest)
        guide.append({'label': label, 'frame': frame, 'path': str(dest), 'sha256': sha(dest.read_bytes()),
                      'unmodified_original_capture': True, 'no_synthetic_gameplay_fixtures': True,
                      'publication_approved': False, 'original18_plaque_user_review_still_pending': True})
    save(GUIDE / 'provenance.json', {'candidate': proof['candidate'],
        'candidate_sha256': proof['candidate_sha256'], 'ordinary_battery_save_cold_boot': True,
        'input_save_sha256': pre['donor_sha256'], 'source_capture_report': str(report_path),
        'source_capture_report_sha256': proof['report_sha256'], 'screenshots': guide,
        'publication_approved': False, 'full_goal_complete': False})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'one_terminal17500_frame_ordinary_saved_game_cold_boot_no_savestate_or_gameplay_fixtures': True,
        'all_three_original_native_policy_models_and_source_label_notice_fidelity_pass': True,
        'all91_whole_plaque_regions95836_pixels_and273_field_masks_pass': True,
        'six_complete_native_notice_confirmation_display_and_actual_bitmap_views_pass': True,
        'actual_Flagship_commit_reopen_and_Even_restore_through_original_controls': True,
        'B_cancel_returns_same_Even_counts_not_different_preview_rollback_proof': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'no_new_ROM_patch_registry_canonical_or_release_pointer_changes': True,
        'other_graphics_gameplay_and_final_acceptance_requirements_open': True,
        'archive': str(ARCHIVE), 'guide_candidates': guide, 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V657: three ordinary five-ship crew policies and complete plaque fields'
    addition = ('The existing session completes normally at17500 frames:40 distinct captures,37 '
        'read-only RAM states,no savestate or gameplay fixtures. Original Flagship/Even/Minimum '
        'allocators reproduce complete48-byte captured models;source labels and notices are '
        'faithful. Fleet Crew plus Unassigned conserves125;Minimum shows75+50. All91 whole '
        'plaque regions95836 pixels,273 fields,three popup labels and six complete native '
        'notice/confirmation planes pass. Flagship confirmation/reopening commits89/9/9/9/9; '
        'Even restores49/19/19/19/19. B cancels an already-equal Even preview;different-preview '
        'rollback and saved-game cold reload are not claimed. Existing V632 plaque packet '
        'still matches current resources/material tile. Evidence and three unapproved guide '
        'candidates saved on E. No ROM/patch/registry/pointer changes. All18 plaques remain '
        'incomplete and22 historical scopes exact;full graphics goal remains active. '
        'See [V657 checkpoint](crew_policy_matrix_v657_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'ordinary_saved_game_no_synthetic_gameplay_fixtures': True, 'guide_candidates': guide,
        'publication_approved': False, 'full_goal_complete': False,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), *(Path(p) for p in proof['scripts']))},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}})
    print('V657 evidence archived; three audits/four progress documents updated;18 original plaques remain open.')


if __name__ == '__main__':
    main()
