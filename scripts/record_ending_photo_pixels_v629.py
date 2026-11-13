"""Record bounded ending-image progress while retaining every historical gate."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_ending_photo_pixels_v629 import PRIOR, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/ending_photo_pixels_v629_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V629 Ending photo pixels')
KEY = 'ending_photo_original_FIFO_and_complete_M32_frames_v629'


def main():
    proof_path = ROOT / 'native_photo_pixels_proof.json'
    proof, prior = read(proof_path), read(PRIOR)
    assert proof['script_sha256'] == sha(Path('scripts/verify_ending_photo_pixels_v629.py').read_bytes())
    assert proof['current_candidate_sha256'] == sha(ROM.read_bytes())
    assert len(proof['cases']) == 11
    assert [r['frame'] for r in proof['complete_source_photo_frames']] == [9280, 9360]
    continuity = proof['M32_controller_continuity']
    assert continuity['original_update_calls'] == 1920 and continuity['complete_original_draw_calls'] == 5760
    assert len(continuity['actual_whole_controller_anchors']) == 6
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == 'fb4b3acb17f69174a53759c8ab74053737eade38c11d5cdee6c7d0afe3062966'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in (DOC, Path(__file__), Path('scripts/verify_ending_photo_pixels_v629.py'), proof_path,
                   ROM.with_suffix('.manifest.json'), PRIOR):
        checked_copy(source, ARCHIVE / source.name)
    shots = {}
    for row in proof['cases'] + continuity['all_captured_sampling_comparisons_in_replayed_interval']:
        source = Path(row['source_PNG'])
        assert sha(source.read_bytes()) == row['source_PNG_sha256']
        label = 'hodram' if 'hodram' in str(source) else 'maria'
        shots[label, row['frame']] = (source, row['source_PNG_sha256'])
    archive_shots = []
    for (label, frame), (source, digest) in sorted(shots.items()):
        target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
        checked_copy(source, target)
        archive_shots.append({'path': str(target), 'sha256': digest, 'frame': frame,
                              'captain': label, 'unmodified_capture': True,
                              'captured_ROM_sha256': proof['captured_candidate_sha256']})
    for case in prior['cases']:
        checked_copy(case['reports']['control']['path'], ARCHIVE / (case['label'] + '_capture_report.json'))
    for source in ROOT.glob('*.png'):
        checked_copy(source, ARCHIVE / source.name)
    # Failed exploratory hypotheses are retained explicitly, not overwritten by a
    # successful subset or interpreted as defects in the original graphics.
    for source in ROOT.glob('*diagnostic.json'):
        checked_copy(source, ARCHIVE / source.name)
    save(ARCHIVE / 'provenance.json', {
        'verification_checkpoint': 'V629', 'current_ROM_unchanged': proof['current_candidate_sha256'],
        'screenshots': archive_shots, 'full_photo_frames_exact': proof['complete_source_photo_frames'],
        'source_views_reconstructions_and_native_captures_separately_labeled': True,
        'reuses_authorized_V594_ending_fixtures_not_new_playthroughs': True,
        'unmatched_sampling_states_remain_open': True, 'publication_approved': False,
        'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'current_candidate': str(ROM), 'current_candidate_sha256': proof['current_candidate_sha256'],
        'captured_candidate_sha256': proof['captured_candidate_sha256'],
        'status': 'original_draw_commands_controller_and_two_whole_photo_frames_verified_other_composition_open',
        'complete_original_GPU_command_stream_snapshots': 11,
        'M32_original_updates': 1920, 'M32_complete_original_draw_calls': 5760,
        'all6936_controller_bytes_exact_at_six_actual_anchors': True,
        'M32_complete49152_RGB_pixel_source_reconstructions_frames': [9280, 9360],
        'blank_shift_and_source_texel_negative_controls_rejected': True,
        'all24_replayed_interval_sampling_results_and_failed_hypotheses_retained': True,
        'original_vertex_quantization_now_observed_through_actual_GPU_writes': True,
        'other_photo_projection_clip_alpha_and_composition_states_remain_open': True,
        'no_ROM_changes_no_new_emulator_run_no_earned_ending_claim': True,
        'all18_original_plaques_incomplete_all22_historical_objects_retained': True,
        'broader_Confirm_miniature_village_card_legacy_comic_logo_movie_material_gates_open': True,
        'archive': str(ARCHIVE), 'unmodified_screenshots': len(archive_shots),
        'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        before = data.copy()
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in before.items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V629: complete original ending draw commands and two whole Maria photo frames'
    text = '''

The complete original quad function now executes through its GPU writes and
return for11 actual photo snapshots, preserving the original stack/register ABI.
Its emitted quantized vertices and256x192 native texture coordinates are retained.
Maria's original1920 updates and5760 complete draw calls reproduce all6936
controller bytes at six real RAM anchors. Independent source reconstructions
match every49152 RGB pixel at frames9280/9360; blank/shift/source-texel negatives
fail. All24 interval sampling comparisons remain recorded, including unmatched
zoom states and the late left-column model discrepancy. These are unresolved
sampling/composition questions, not proven artwork defects or waived pixels.
Existing V594 synthetic-ending captures are reused; no new ROM/emulator run,
earned ending or hardware claim. V627 remains unchanged and experimental.
All18 plaques incomplete,all22 historical scopes and all other audit/release
pointers exact. Proofs and unmodified evidence are on E. Full goal active. See
[V629 checkpoint](ending_photo_pixels_v629_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'V629 archived{len(archive_shots)} unmodified screenshots;three audits updated;18/22 scopes and all ROM pointers retained.')


if __name__ == '__main__':
    main()
