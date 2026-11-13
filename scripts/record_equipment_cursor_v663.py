"""Archive complete ordinary equipment selection evidence without closing the audit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/equipment_cursor_v663')
DOC = Path('docs/equipment_cursor_v663_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V663 Equipment cursor')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V653 Equipment cursor')
KEY = 'ordinary_five_equipment_slots320_complete_lower_scenes_including_source_scanline_blink_transitions_v663'


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert len(proof['five_actual_slot_windows320_frames']) == 5
    assert len(proof['all320_complete_hint_font_masks']) == 320
    assert len(proof['six_hint_first_last_letter_deletion_controls']) == 6
    assert len(proof['four_footer_deletion_controls']) == 4
    source = proof['ten_mixed_transition_frames_resolved_at_actual_source_row_reads']
    assert len(source['cases']) == 10 and len(source['twelve_host_prefix_ABI_controls']) == 12
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    for path in (DOC, Path(__file__), *(Path(p) for p in proof['scripts']),
                 *ROOT.glob('*.json'), *ROOT.glob('*.txt'), *ROOT.glob('*.png'), *ROOT.glob('*.bin')):
        copy(path, ARCHIVE / path.name)
    captures = []
    reports = dict(proof['reports'])
    reports['diagnostic_source_rows'] = {'path': source['report'], 'sha256': source['report_sha256']}
    for label, info in reports.items():
        report_path = Path(info['path'])
        assert sha(report_path.read_bytes()) == info['sha256']
        report = read(report_path)
        tag = label.upper() + ('_HOST_OBSERVED' if label == 'diagnostic_source_rows' else '_UNMODIFIED_CORE')
        for path in report_path.parent.rglob('*'):
            if path.is_file():
                copy(path, ARCHIVE / tag / path.relative_to(report_path.parent))
        for shot in report['frames_captured']:
            captures.append({'run': tag, 'frame': shot['frame'], 'source': shot['path'],
                'PNG_sha256': shot['PNG_sha256'], 'host_instrumented': label == 'diagnostic_source_rows',
                'no_gameplay_fixtures': True, 'publication_approved': False})
    current = read(proof['reports']['current']['path'])
    guide = []
    for frame, label in ((6400, 'Weapon'), (6800, 'Blue_Oak_Shield'), (8000, 'Equipped_Items')):
        shot = next(r for r in current['frames_captured'] if r['frame'] == frame)
        source_path = Path(shot['path'])
        target = GUIDE / f'V653_Sailor_Info_{label}_UNMODIFIED_NATIVE.png'
        copy(source_path, target)
        guide.append({'frame': frame, 'path': str(target), 'sha256': sha(target.read_bytes()),
                      'unmodified_original_capture': True, 'gameplay_fixtures': False,
                      'publication_approved': False, 'original18_plaque_user_review_still_pending': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'three_terminal8063_frame_ordinary_saved_cold_boots_host_observer_disclosed': True,
        'all325_whole_V636_control_pairs_and325_whole_observer_baseline_pairs_exact': True,
        'all320_complete_lower_frames15728640_RGB_pixels_verified_without_border_masks': True,
        'original_native_on_off_variants_plus_ten_actual_source_scanline_transition_compositions': True,
        'original_draw_order_explains204_204_204_200_236_visible_border_pixels': True,
        'native_SDK_clock_bridge_inputs_explicit_not_actual_CPU_tick_phase_claim': True,
        'all320_complete_hint_masks3200_plaque_crops_and_ten_letter_deletion_controls': True,
        'historical_V637_exclusion_not_relabelled_as_retested': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'other_control_card_legacy_material_character_gameplay_and_acceptance_gates_open': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'guide_candidates': guide, 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V663: complete ordinary five-slot borders, hints and blink transitions'
    addition = ('Three ordinary8063-frame saved cold boots finish normally. All325 full V636 '
        'control pairs and325 observed/unmodified-core pairs match. Original traversal, '
        'painters, tooltip and footer reconstruct both native blink variants over poison; '
        'all320 complete lower screens15,728,640 RGB pixels match with no ring mask. Ten '
        'mixed frames resolve through1,920 actual before-render bitmap rows and exact IO, '
        'without delay or row-phase fitting. Original draw order explains204/204/204/200/236 '
        'visible ring pixels. SDK clock inputs are isolated component contracts; no actual '
        'CPU-tick or hardware claim. All320 hints,3,200 plaque crops and ten first/final '
        'letter deletion controls pass. Ten active skill labels checked against Japanese '
        'source. Historical V637 exclusion retained as recorded. No ROM/patch/registry/pointer '
        'change; all18 plaques incomplete and22 historical scopes exact. Evidence and three '
        'unapproved ordinary guide candidates on E; full goal active. See '
        '[V663 checkpoint](equipment_cursor_v663_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'captures': captures, 'guide_candidates': guide,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), *(Path(p) for p in proof['scripts']))},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print(f'V663 archived {len(captures)} capture records and3 ordinary guide candidates; three audits/four documents updated; full goal active.')


if __name__ == '__main__':
    main()
