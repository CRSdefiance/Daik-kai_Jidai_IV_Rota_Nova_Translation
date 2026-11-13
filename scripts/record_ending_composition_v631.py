"""Archive complete sampled Hodram composition while retaining all audit scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.research_ending_blend_v631 import CAP, ROOT
from scripts.verify_ending_composition_v631 import PREVIOUS, ROM
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/ending_composition_v631_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V631 Hodram composition')
KEY = 'actual_Hodram_complete_opaque_and_translucent_compositions_v631'


def main():
    proof_path = ROOT / 'native_composition_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_ending_composition_v631.py').read_bytes())
    assert proof['sampler_sha256'] == sha(Path('scripts/research_ending_blend_v631.py').read_bytes())
    assert len(proof['all12_complete_native_upper_frame_compositions']) == 12
    assert proof['all_four_V630_Hodram_photo_findings_resolved_with_no_pixel_waiver']
    assert proof['historical_V630_proof_sha256'] == sha(PREVIOUS.read_bytes())
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == 'fb4b3acb17f69174a53759c8ab74053737eade38c11d5cdee6c7d0afe3062966'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in (DOC, Path(__file__), Path('scripts/research_ending_blend_v631.py'),
                   Path('scripts/verify_ending_composition_v631.py'), proof_path, PREVIOUS,
                   ROM.with_suffix('.manifest.json'), CAP / 'capture_report.json',
                   CAP / 'navigation_command_journal.json'):
        checked_copy(source, ARCHIVE / source.name)
    for source in ROOT.glob('*.png'):
        checked_copy(source, ARCHIVE / source.name)
    for source in ROOT.glob('*diagnostic.json'):
        checked_copy(source, ARCHIVE / source.name)
    report = read(CAP / 'capture_report.json')
    shots = {s['frame']: s for s in report['frames_captured']}
    screenshots = []
    for state in report['read_only_capture_GPU_states']:
        frame = state['frame']
        shot = shots[frame]
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        target = ARCHIVE / f'Hodram_{frame:06d}_UNMODIFIED_NATIVE.png'
        checked_copy(shot['path'], target)
        screenshots.append({'frame': frame, 'path': str(target), 'sha256': shot['PNG_sha256'],
                            'ROM_sha256': report['ROM_sha256'], 'unmodified_capture': True})
        gpu_target = ARCHIVE / f'GPU_{frame:06d}'
        gpu_target.mkdir(parents=True, exist_ok=True)
        checked_copy(state['path'], gpu_target / 'gpu_state.json')
        for name, entry in state['files'].items():
            if name != 'arm9_main_ram.bin':
                checked_copy(entry['path'], gpu_target / name)
    save(ARCHIVE / 'provenance.json', {
        'verification_checkpoint': 'V631', 'candidate_sha256': proof['candidate_sha256'],
        'screenshots': screenshots, 'all20_GPU_exports_and_RAM_retained_on_E': True,
        'observed_submission_to_display_lag_frames': 2, 'no_per_frame_alignment_choice': True,
        'nine_opaque_three_translucent_complete_frames_exact': True,
        'authorized_ending_fixture_not_earned_completion': True, 'publication_approved': False,
        'full_goal_complete': False,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'status': 'four_retained_Hodram_photo_findings_resolved_sampled_full_composition_verified',
        'actual_V627_adjacent_GPU_state_exports': 20,
        'nine_opaque_and_three_translucent49152_RGB_planes_exact': True,
        'observed_fixed_two_frame_submission_display_phase_with_zero_one_three_negatives': True,
        'source_scenery_six_bit_photo_alpha_and46_46_19_star_points_composed_exactly': True,
        'blank_texel_geometry_shift_missing_star_scenery_wrong_alpha_controls_rejected': True,
        'historical_V630_failed_comparisons_and_proofs_preserved': True,
        'no_ROM_registry_patch_or_artwork_changes_no_pixel_waivers': True,
        'not_all_movie_frames_or_earned_route_completion_or_hardware_verification': True,
        'all18_original_plaques_incomplete_all22_historical_objects_retained': True,
        'broader_Confirm_miniature_village_card_legacy_comic_logo_movie_material_gates_open': True,
        'archive': str(ARCHIVE), 'unmodified_screenshots': len(screenshots),
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
    heading = '## V631: original Hodram photo timing and complete translucent composition'
    text = '''

One fresh V627 cold boot captures20 adjacent GPU states around the four retained
Hodram findings. A uniform two-frame submission-to-display relationship passes
every available pair; fixed0/1/3 controls fail. Source list swapping explains
the distinct stages; no screenshot is individually aligned. Nine opaque and
three translucent whole49152 RGB frames match exactly. The original scenery,
photo alpha8/10 and star46/46/19 points compose from source palettes and native
geometry. Blank/texel/shift and missing-star/scenery/wrong-alpha negatives fail.
All four V630 photo findings resolved without artwork edits or pixel waivers;
historical failures/proofs retained. This is a targeted authorized ending fixture,
not every movie frame,earned route or hardware credit. V627 unchanged. All18
plaques incomplete,all22 historical scopes/other entries/release pointers exact.
Twenty unmodified captures/GPU exports and source/proof are on E. Full graphics
goal active. See [V631 checkpoint](ending_composition_v631_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print('V631 archived20 unmodified screenshots/GPU exports;three audits updated;all18/22 scopes and ROM/release pointers exact.')


if __name__ == '__main__':
    main()
