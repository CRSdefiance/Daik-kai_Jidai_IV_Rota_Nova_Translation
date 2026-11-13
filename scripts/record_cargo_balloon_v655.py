"""Archive complete cargo hover composition without closing broader audit scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/cargo_tooltip_v655')
DOC = Path('docs/cargo_tooltip_v655_checkpoint.md')
KEY = 'actual_CBalloon_original2px_inset_five_complete_cargo_tooltip_banner_compositions_v655'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V655 Cargo tooltip composition')


def copy(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['script_sha256'] == sha(Path('scripts/verify_cargo_balloon_v655.py').read_bytes())
    cases = proof['actual_original_banner_then_balloon_callbacks']
    assert len(cases) == 5 and sum(c['compared_union_pixel_positions'] for c in cases) == 21480
    assert all(c['all4096_banner_and640_tooltip_pixels_exact'] for c in cases)
    assert all(c['all_union_pixels_assigned_by_native_writes_and_no_output_read_before_write'] for c in cases)
    assert not proof['full_goal_complete']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    scripts = ['scripts/research_cargo_tooltip_v655.py', 'scripts/probe_cargo_balloon_v655.py',
               'scripts/verify_cargo_balloon_v655.py', 'scripts/record_cargo_balloon_v655.py']
    for path in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.txt'),
                 *ROOT.glob('*.bin'), *map(Path, scripts)]:
        copy(path, ARCHIVE / path.name)
    report_path = Path(proof['reused_V654_terminal_report'])
    assert sha(report_path.read_bytes()) == proof['reused_report_sha256']
    copy(report_path, ARCHIVE / 'reused_V654_terminal_capture_report.json')
    report = read(report_path)
    for case in cases:
        shot = next(s for s in report['frames_captured'] if s['frame'] == case['frame'])
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        copy(shot['path'], ARCHIVE / 'reused_V654_unmodified_captures' / Path(shot['path']).name)
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'actual_modal_context_from_original_owner_list_is023117C4_not_underlying_sea': True,
        'unchanged_original2px_padding_establishes_actual18_268_text_origin': True,
        'source_Japanese_commodity95_Mokuzai_and_actual_Timber_name_getter_bound': True,
        'five_actual432_cell_name_views_and_all_complete_glyphs77_ink_points_each': True,
        'five4096_banner_plus640_tooltip_compositions21480_unique_pixel_positions_exact': True,
        'all_native_destination_union_pixels_written_no_read_before_write_or_finished_VRAM_input': True,
        'first_T13_final_r8_native_deletions_rejected_in_every_case': True,
        'V654_frame23200_369_pixel_popup_overlap_now_completely_explained_and_verified': True,
        'whole_cargo_scene_hardware_timer_and_supplied_constructor_diagnostics_not_clearance': True,
        'no_new_emulator_gameplay_guide_candidate_or_publication_claim': True,
        'ROM_patch_manifest_registry_canonical_and_all_release_pointers_unchanged': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V655: original cargo balloon geometry and complete hovered-banner composition'
    addition = ('Resolves V654\'s withheld hover comparison using its actual captures,not a new '
        'emulator run. Original cargo-owner metadata identifies context023117C4; '
        'the lower context is the underlying sea scene. Original CBalloon2px padding '
        'establishes18,268 text placement. Clean commodity95 is木材 and its real getter '
        'returns Timber. All432 source cells/77 glyph pixels and blank cells pass in '
        'five cases. Actual original banner/balloon callbacks match all4096 banner '
        'and640 tooltip pixels,21480 unique positions total. Native writes assign '
        'every compared pixel without reading prior output;first T13/final r8 native '
        'deletion controls fail exactly. No waived pixels or graphic repair. Whole-scene '
        'timer and supplied constructor probes receive no broader credit. No ROM,patch, '
        'registry or release-pointer change;all18 plaques incomplete and22 scopes exact. '
        'Evidence/reused captures on E;full goal active. See '
        '[V655 checkpoint](cargo_tooltip_v655_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'original_captures_are_reused_from_V654_not_new_gameplay': True,
        'native_cropped_reconstructions_are_derived_not_guide_captures': True,
        'original_RAM_native_state_exports_remain_on_E_at_reported_paths': True,
        'scripts': {p: sha(Path(p).read_bytes()) for p in scripts},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V655 complete hover evidence archived;three audits/four progress documents updated;full18/22 scope retained.')


if __name__ == '__main__':
    main()
