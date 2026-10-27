"""Archive the seven verified repairs and retain every historical graphics gate."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_consistency_v666')
DOC = Path('docs/village_consistency_v666_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V666 Village consistency')
KEY = 'five_Town_name_aliases_two_aligned_clues_seven_actual_contexts_and_ordinary_New_Game_v666'
LATEST = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
SCRIPTS = ('dk4tool/patch/village_port_consistency.py', 'scripts/prepare_village_consistency_v666.py',
           'scripts/run_village_consistency_v666.py', 'scripts/verify_village_consistency_v666.py',
           'scripts/record_village_consistency_v666.py', 'scripts/build_integrated_release.py',
           'scripts/run_village_development_v665.py', 'scripts/run_village_return_v665.py',
           'scripts/native_village_visits_v664.py', 'scripts/native_village_town_v665.py',
           'scripts/headless_desmume_v193.py')


def copy(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    proof_path = ROOT / 'release_proof.json'
    proof, pre = read(proof_path), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_village_consistency_v666.py').read_bytes())
    assert proof['all_seven_changed_contexts_cold_boot_verified'] and len(proof['cases']) == 7
    assert len(proof['reports']) == 8 and len(proof['whole_header_first_final_deletion_controls']) == 14
    assert len(proof['newgame_whole_two_screen_frames_exact_V653']) == 89
    assert proof['village_unchanged_whole_two_screen_comparisons'] == 265
    assert not proof['full_goal_complete'] and not proof['canonical_promoted']
    rom = Path(proof['candidate'])
    for suffix, field in (('.nds', 'candidate_sha256'), ('.xdelta', 'patch_sha256'),
                          ('.manifest.json', 'manifest_sha256')):
        assert sha(rom.with_suffix(suffix).read_bytes()) == proof[field]
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, LATEST, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(rom), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
        'status': 'experimental_seven_data_repairs_actual_verified_broader_graphics_open',
        'five_original_Town_name_aliases_match_existing_approved_village_names': True,
        'five_complete_actual_docking_prompts_and_Town_headers_pass': True,
        'Valparaiso_and_Wanganui_clue_rows_start_at22_complete_words_and_letters': True,
        'all_English_prose_unchanged_no_growth_no_new_fonts_graphics_or_native_code': True,
        'seven_complete_two_screen_native_Town_compositions688128_pixels_pass': True,
        'all50_input_prefixes_and14_actual_header_edge_deletion_controls_pass': True,
        'all265_other_village_whole_screen_and89_ordinary_New_Game_comparisons_exact': True,
        'all470_batches114_accepted_layers921_views57_embedded_extents_and_exact_patch_retained': True,
        'location_only_test_fixtures_no_earned_travel_or_hardware_claim': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'Karibib_cards_small_controls_legacy_other_contexts_material_and_final_acceptance_open': True,
        'archive': str(ARCHIVE), 'canonical_promoted': False, 'full_goal_complete': False}
    for name in frozen:
        target = Path('translations') / name
        data = read(target)
        data[KEY] = entry
        latest = data.get(LATEST, {}).copy()
        latest.update(candidate=str(rom), sha256=proof['candidate_sha256'], profile=proof['profile'],
                      village_port_consistency_actual_verified=True, broader_graphics_gates_remain_open=True)
        data[LATEST], data['current_goal_turn_classification'] = latest, 'progress'
        save(target, data)
    heading = '## V666: five consistent port names and two aligned village clues'
    addition = ('The complete V653 stack now includes five existing Town metadata name aliases '
        '(Cape Cod, Dikson, Leveque, Tiksi, Korf) and two machine-generated clue reflows '
        '(Valparaiso/Wanganui). All English prose, graphics, fonts, native code, section lengths '
        'and arena/cache bounds remain unchanged. Seven fresh saved cold boots use only coordinate '
        'approach fixtures; all50 typed prefixes, full dialogue/menu fields, five docking prompts '
        'and headers,14 actual header edge deletions and688128 complete native Town pixels pass. '
        'Both changed clue rows start at22. All265 other village whole frames and89 ordinary '
        'New Game title/selection/story/town frames match V653. Eight terminal runs retain374 '
        'capture records. Initial docking-name comparison assumptions are retained and resolved '
        'with complete field checks; no ROM change or pixel waiver follows. All470 batches,114 '
        'accepted layers,921 views and57 embedded extents are preserved; the clean xdelta rebuild '
        'is byte-exact. Latest experimental compiled pointer advances to V666; canonical and V610 '
        'verified pointers remain. All18 plaque entries remain incomplete and22 scopes exact. '
        'Karibib return, eight cards, six controls, legacy/material/other contexts, older record '
        'checks and final acceptance remain open. Evidence on E; full goal active. See '
        '[V666 checkpoint](village_consistency_v666_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        target = Path('docs') / name
        before = target.read_text(encoding='utf-8')
        if heading not in before:
            after = before.rstrip() + '\n\n' + heading + '\n\n' + addition
            target.write_text(after, encoding='utf-8')
            assert target.read_text(encoding='utf-8').startswith(before.rstrip())
    save(ROOT / 'visual_review.json', {'sheets': proof['derived_comparison_sheets'],
        'both_sheets_visually_inspected': True,
        'observations': 'Five approved names display fully. Both complete clue paragraphs retain words/punctuation and now share the same left margin on both lines.',
        'derived_sheets_not_raw_screenshots_or_guide_publication_approval': True,
        'plaque_acceptance_inferred': False, 'full_goal_complete': False})
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    # Original RAM/native-state files already live on E. Keep exact references and hashes,
    # and duplicate the unmodified PNGs, reports and journals into the audit archive.
    retained_exports = {}
    for receipt in proof['reports']:
        rp = Path(receipt['path'])
        assert sha(rp.read_bytes()) == receipt['sha256']
        r = read(rp)
        destination = ARCHIVE / 'captures' / rp.parent.name
        for p in rp.parent.iterdir():
            if p.is_file() and p.suffix.lower() in ('.json', '.png'):
                copy(p, destination / p.name)
        for key in ('read_only_RAM_snapshot', 'read_only_native_state'):
            row = r.get(key)
            if row:
                retained_exports[row['path']] = row['sha256']
                retained_exports.update({x['path']: x['sha256'] for x in row.get('regions', {}).values()})
        for key in ('read_only_pause_RAM_snapshots', 'read_only_capture_RAM_snapshots'):
            retained_exports.update({row['path']: row['sha256'] for row in r.get(key, [])})
    for path, digest in retained_exports.items():
        assert Path(path).resolve().drive.upper() == 'E:' and sha(Path(path).read_bytes()) == digest
    for source in [DOC, *map(Path, SCRIPTS), Path('translations/village_port_consistency_v1.json'),
                   Path('translations/release_stack.json'), rom.with_suffix('.manifest.json')]:
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {
        'candidate_sha256': proof['candidate_sha256'], 'ROM_patch_and_reconstruction_retained_at_original_E_paths': True,
        'reports': proof['reports'], 'all_eight_runs_terminal': True,
        'unmodified_PNGs_and_exact_reports_copied': True, 'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'read_only_RAM_native_exports_retained_at_original_E_paths': retained_exports,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'no_guide_publication_or_plaque_completion_inferred': True, 'full_goal_complete': False})
    print('V666 archived; three audits/four documents updated; complete18/22 historical scope retained.', flush=True)


if __name__ == '__main__':
    main()
