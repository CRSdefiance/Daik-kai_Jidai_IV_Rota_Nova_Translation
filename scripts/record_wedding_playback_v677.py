"""Record actual wedding artwork evidence with explicit forced-story provenance."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_wedding_fixture_v677 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V677 Original Lil wedding playback')
DOC = Path('docs/wedding_playback_v677_checkpoint.md')
KEY = 'actual_original_Lil_M26_wedding152_source_frames705_pairs_and_disclosed_chapter_fixture_v677'
SCRIPTS = ('scripts/native_wedding_fixture_v677.py', 'scripts/check_wedding_fixture_v677.py',
           'scripts/run_wedding_playback_v677.py', 'scripts/research_wedding_composition_v677.py',
           'scripts/verify_wedding_playback_v677.py', 'scripts/record_wedding_playback_v677.py',
           'scripts/verify_wedding_playback_archive_v677.py', 'scripts/observe_wedding_runtime_v676.py',
           'scripts/observe_graphic_paints_v669.py', 'scripts/inspect_committed_gpu_v646.py',
           'scripts/research_ending_transitions_v642.py', 'scripts/research_ending_blend_v631.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_wedding_playback_v677.py').read_bytes())
    assert proof['152_complete_source_compositions_all_native_counters0_through151']
    assert proof['full_native_draws_with_GPU_commands'] == 165
    assert proof['whole_RGB_pixel_comparisons'] == 7471104
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    review = read(ROOT / 'visual_review_packet.json')
    assert sha(Path(review['sheet']).read_bytes()) == review['sha256']
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'targeted_original_M26_source_loading_crops_internal_fade_verified_in_isolated_original_chapter70',
        'fixture_only_ARM9_R1_at_original_loader22_to70_no_ROM_script_movie_or_WRAM_injection': True,
        '705_whole_observed_common_fixture_baseline_pairs67_pilot12_disabled_unmodified_pairs': True,
        '152_source_compositions7471104_RGB_pixels_all_actual_counters0_through151': True,
        'both_original_photos_complete_native_extents_palettes_and_selected_crops_verified': True,
        '165_full_original_draws_emitting_GPU_commands_with_ABI_clean_words': True,
        'one_retained_final_fade_command_bound_to_original_draw_not_waived': True,
        'five_full_original_final_photo_holds_and_source_geometry_alpha_negatives': True,
        '11_policy5_native_host_controls_and_original_pointers_restored': True,
        'initial_wrong_reader_marker_failed_safely_before_state_change_artifacts_retained': True,
        'no_earned_story_route_every_console_frame_GPU_or_hardware_claim': True,
        'older_record_followup': 'B70 R0397 orphan line; B70 R0615 clothes mistranslated as dress; source-faithful dialogue fix/build pending',
        'all18_plaques_incomplete22_original_requirements_exact_other_gates_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[key] == value for key, value in pre['all_original_audits_before'][name].items()
                   if key != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
    heading = '## V677: actual original wedding movie, complete source samples and isolated chapter fixture'
    addition = ('A source-guarded fixture changes only ARM9 R1 from22 to70 at the original '
        'Lil chapter loader. The original script reaches its own4906/M26 request at14489; '
        'no ROM,script,movie,quest flag or WRAM is injected.705 complete common-fixture '
        'baseline pairs,67 pilot pairs,12 disabled/unmodified pairs and corresponding '
        'terminal RAM states match.152 independent full source compositions cover native '
        'counters0..151:7471104 exact RGB pixels,both original photos,complete palettes/native '
        'crops and crossfade.165 emitting native draws pass full ABI/clean-word checks. '
        'The final fading command at14740 is bound to the actual14736 original draw; '
        'current zero-opacity drawing returns without commands. No pixel waiver or '
        'per-case delay. Five final photo holds,source/geometry/alpha negatives and11+5 '
        'fixture/host controls pass. The original empty marker isFFF; initial FFFFFFFF '
        'guard failure changes no game bytes and is retained. Earned story/full-route/'
        'hardware/every-console-frame GPU verification are not claimed. Older B70 R0397 '
        'orphan layout and R0615 clothes/dress mistranslation are queued for source-faithful '
        'dialogue correction and integrated testing. V666/patch/registry/pointers unchanged; '
        'all18 plaques incomplete and22 scopes exact. Evidence on E,no guide promotion. '
        'See [V677 checkpoint](wedding_playback_v677_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        value = path.read_text(encoding='utf-8')
        if heading not in value:
            path.write_text(value.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for tag in ('pilot', 'disabled', 'pilot_v2', 'disabled_v2', 'observed', 'fixture_baseline'):
        folder = CAP / ('wedding_playback_v677_' + tag)
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in ('.json', '.png', '.bin', '.log', '.txt'):
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (DOC, *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'],
        'all_attempts_terminal_four_successful_scoped_runs': True,
        'source_scripts': {path: sha(Path(path).read_bytes()) for path in SCRIPTS},
        'files': {str(path.relative_to(ARCHIVE)): sha(path.read_bytes()) for path in ARCHIVE.rglob('*')
                  if path.is_file() and path.name != 'provenance.json'},
        'isolated_original_story_fixture_not_earned_wedding_or_guide_approval': True,
        'full_goal_complete': False})
    print('V677 wedding playback/source evidence archived; three audits/four docs updated;18/22 scopes retained.', flush=True)


if __name__ == '__main__':
    main()
