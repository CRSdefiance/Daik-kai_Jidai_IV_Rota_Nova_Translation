"""Archive new cached-view evidence while keeping unresolved graphics gates open."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_view_getters_v679 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V679 Cached image views')
DOC = Path('docs/view_getters_v679_checkpoint.md')
KEY = 'actual_original_view_getter50656_entries32445_cached10_relocated_headers_and70_native_returns_v679'
SCRIPTS = ('scripts/prepare_view_getters_v679.py', 'scripts/observe_view_getters_v679.py',
    'scripts/check_view_getters_v679.py', 'scripts/run_view_getters_v679.py', 'scripts/verify_view_getters_v679.py',
    'scripts/record_view_getters_v679.py', 'scripts/verify_view_getters_archive_v679.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_view_getters_v679.py').read_bytes())
    assert proof['source_owner_getter_calls'] == 18211 and proof['cached_direct_getter_calls'] == 32445
    assert len(proof['70_full_original_native_cached_getter_replays']) == 70
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {'actual_editor_return_Japanese_input_and_Latin_page_opened': True,
        'four_frame_derived_sheet_opened': True, 'no_new_missing_letters_or_art_damage_identified_in_selected_views': True,
        'source_and_palette_provenance_separate_from_pixel_content_clearance': True,
        'no_guide_publication_or_new_graphics_completion_credit': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'actual_type4_and_cached_type5_view_paths_bound_six_control_parents_still_open',
        'three_terminal7900_frame_ordinary_cold_boots_no_save_savestate_or_gameplay_fixture': True,
        '24_full_screen_pairs_per_observer_and_all_terminal_RAM_exact_baseline': True,
        'all50656_entry_records_repeat_zero_read_guard_flags': True,
        '18211_actual_owner_requests_seven_filenames_and32445_cached_pointer_requests': True,
        'ten_actual_relocated_headers_resolve_original_text_palette02125A20': True,
        '35_actual_cached_views70_full_clean_current_original_getter_returns_and_ABI': True,
        'sixteen_native_host_controls_per_version_original_handler_and_restored_slot': True,
        'no_loose_file_identity_or_pixel_content_provenance_inferred_for_relocated_descriptors': True,
        'no_Frame_Confirm_owner_in_this_schedule_not_global_nonuse': True,
        'all18_plaques_incomplete22_original_requirements_exact_other_gates_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
    heading = '## V679: original cached-direct view inputs and relocated text-palette descriptors'
    addition = ('Three ordinary7900-frame name-editor cold boots have24 full-screen baseline '
        'pairs per observer and identical terminal RAM. A host-only read-only filter records '
        'all50656 original getter entries:18211 type4 owner requests/seven filenames and32445 '
        'cached type5 returns by contract. Both versions repeat CPU/view/name fields with zero '
        'read guards;the second adds ten actual relocated20-byte headers. All resolve the '
        'original02125A20 text palette;different layouts/shared pixels are not treated as '
        'whole loose PXL files.35 actual cached view combinations execute70 complete clean/'
        'current native getter cases with exact returns/ABI and only the saved LR stack write. '
        'Sixteen native host controls per observer and ten clean-identical callers pass. '
        'No Frame/Confirm owner occurs in this schedule;cached pixel provenance,other renderers '
        'and all six control parents remain open. Actual editor/Latin/input/return captures '
        'reviewed;no new graphic defect found in selected views. V678/patch/registry/pointers '
        'unchanged;all18 plaques incomplete and22 scopes exact. Evidence on E,no guide promotion. '
        'Full goal active. See [V679 checkpoint](view_getters_v679_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        value = path.read_text(encoding='utf-8')
        assert heading not in value
        path.write_text(value.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for tag in ('observed', 'baseline', 'observed_cached_headers'):
        folder = CAP / ('view_getters_v679_' + tag)
        for source in folder.rglob('*'):
            if source.is_file():
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
    save(ARCHIVE / 'provenance.json', {'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
            if p.is_file() and p.name != 'provenance.json'},
        'candidate_sha256': pre['candidate_sha256'], 'no_global_nonuse_or_guide_claim': True, 'full_goal_complete': False})
    print('V679 cached-view traces and original-code evidence archived; all18/22 scopes retained.', flush=True)


if __name__ == '__main__':
    main()
