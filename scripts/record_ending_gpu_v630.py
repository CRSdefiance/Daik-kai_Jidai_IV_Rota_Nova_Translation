"""Archive source-matched ending zoom checks without closing unrelated gates."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.research_photo_sampler_v630 import ROOT
from scripts.verify_ending_gpu_v630 import ROM
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/ending_gpu_v630_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V630 Ending GPU pixels')
KEY = 'actual_Maria_ending_zoom_source_clipping_and_GPU_states_v630'


def main():
    proof_path = ROOT / 'native_gpu_photo_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_ending_gpu_v630.py').read_bytes())
    assert proof['sampler_sha256'] == sha(Path('scripts/research_photo_sampler_v630.py').read_bytes())
    assert len(proof['M32_actual_GPU_export_complete_frames']) == 7
    assert len(proof['M32_existing_V593_whole_sequence_frames']) == 24
    assert len(proof['Hodram_separate_unresolved_states']) == 4
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == 'fb4b3acb17f69174a53759c8ab74053737eade38c11d5cdee6c7d0afe3062966'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in (DOC, Path(__file__), Path('scripts/verify_ending_gpu_v630.py'),
                   Path('scripts/research_photo_sampler_v630.py'), Path('scripts/inspect_desmume_gpu_v630.py'),
                   Path('scripts/headless_desmume_v193.py'), Path('scripts/native_ending_fixture_v537.py'),
                   proof_path, ROOT / 'preflight_proof.json', ROOT / 'gfx3d.cpp', ROOT / 'saves.cpp',
                   Path('work/analysis/ending_photo_pixels_v629/desmume_95b4d79_rasterize.cpp'),
                   ROM.with_suffix('.manifest.json')):
        checked_copy(source, ARCHIVE / source.name)
    for source in ROOT.glob('*diagnostic.json'):
        checked_copy(source, ARCHIVE / source.name)
    for source in ROOT.glob('*.png'):
        checked_copy(source, ARCHIVE / source.name)
    screenshots = []
    for label, rows in (('V627_Maria', proof['M32_actual_GPU_export_complete_frames']),
                        ('V593_Maria', proof['M32_existing_V593_whole_sequence_frames']),
                        ('V627_Hodram_UNRESOLVED', proof['Hodram_separate_unresolved_states'])):
        for row in rows:
            source = Path(row['source_PNG'])
            digest = row['PNG_sha256']
            assert sha(source.read_bytes()) == digest
            target = ARCHIVE / f"{label}_{row['frame']:06d}_UNMODIFIED_NATIVE.png"
            checked_copy(source, target)
            screenshots.append({'path': str(target), 'sha256': digest, 'frame': row['frame'],
                                'context': label, 'unmodified_capture': True,
                                'new_run': label.startswith('V627'), 'whole_photo_verified': 'UNRESOLVED' not in label})
    for label, key in (('Maria', 'M32_actual_V627_run'), ('Hodram', 'Hodram_actual_V627_run')):
        source = Path(proof[key]['path'])
        report = read(source)
        checked_copy(source, ARCHIVE / (label + '_capture_report.json'))
        journal = source.parent / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        for state in report['read_only_capture_GPU_states']:
            target = ARCHIVE / f"{label}_GPU_{state['frame']:06d}"
            target.mkdir(parents=True, exist_ok=True)
            checked_copy(state['path'], target / 'gpu_state.json')
            for name, field in state['files'].items():
                if name != 'arm9_main_ram.bin':
                    checked_copy(field['path'], target / name)
    save(ARCHIVE / 'provenance.json', {
        'verification_checkpoint': 'V630', 'candidate_sha256': proof['candidate_sha256'],
        'screenshots': screenshots, 'seven_new_plus24_existing_comparisons_not31_unique_timestamps': True,
        'all_read_only_RAM_exports_retained_in_Generated_runs_with_hashes': True,
        'two_authorized_ending_fixtures_not_earned_routes': True,
        'Hodram_sampling_and_composition_unresolved': True, 'publication_approved': False,
        'full_goal_complete': False,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'status': 'sampled_M32_zoom_complete_source_RGB_verified_Hodram_separate_open',
        'fresh_V627_cold_boot_GPU_exports_Maria': 7, 'fresh_Hodram_diagnostic_exports': 4,
        'all7_new_Maria_and24_existing_whole49152_RGB_planes_exact': True,
        'clipping_truncation_and_native_scanline_interpolants_explain_M32_model_failures': True,
        'late_black_column_predicted_from_source_coverage_no_pixels_waived': True,
        'blank_source_texel_and_one_pixel_geometry_shift_controls_rejected_for_all31_comparisons': True,
        'no_per_frame_alignment_color_tolerance_ROM_or_artwork_changes': True,
        'Hodram_four_transition_or_composition_states_still_open': True,
        'native_state_exports_read_only_no_savestates_loaded': True,
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
    heading = '## V630: source clipping resolves the complete sampled Maria ending zoom'
    text = '''

Two fresh V627 cold boots capture7 Maria and4 Hodram GPU states through a new
opt-in read-only diagnostic. Original end-state fixtures/donors/code are pinned;
no savestate is loaded or ROM changed. Source clipping, actual truncating FX4
coordinate conversion and scanline float32 interpolation explain every former
Maria discrepancy, including the192-pixel black edge. All7 new and24 existing
full49152 RGB planes match exactly, with blank/source-texel/one-pixel-shift
negatives rejecting changes. These are31 plane comparisons,25 unique animation
timestamps, not a full GPU or every-frame claim. Four separate Hodram photo
states remain unresolved (one alpha10 overlap,three unmatched opaque states);
no defect or waiver is inferred. Historical failures/proofs retained. All18
plaques incomplete,all22 historical objects and all other entries/pointers exact.
V627 stays experimental and unchanged. Proof/source/unmodified evidence saved
on E;full graphics goal active. See [V630 checkpoint](ending_gpu_v630_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'V630 archived{len(screenshots)} unmodified screenshots and11 GPU exports;three audits updated;18/22 scopes/ROM pointers exact.')


if __name__ == '__main__':
    main()
