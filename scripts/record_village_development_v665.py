"""Archive actual village development evidence and retain all confirmed repair gates."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_development_v665 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/village_development_v665_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V665 Village development')
KEY = 'all24_typed_original_village_acceptances23_complete_Town_scenes_five_name_and_two_indent_repairs_identified_v665'


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    cases = proof['all24_development_cases']
    assert len(cases) == 24 and [c['index'] for c in cases] == list(range(24))
    assert sum(c['native_Town_replay'] is not None for c in cases) == 23
    assert sum(len(c['complete_developed_menu']['complete_menu_labels']) for c in cases) == 73
    assert [c['index'] for c in cases if not c['Town_name_matches_locked_village_name']] == [6, 12, 16, 21, 22]
    assert proof['two_clue_alignment_defects_require_repair'] == [4, 23]
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data, old = read(Path('translations') / name), pre['all_original_audits_before'][name]
        assert set(data) <= set(old) | {KEY, 'current_goal_turn_classification'}
        assert all(data[k] == v for k, v in old.items() if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        inventory = data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory')
        assert inventory == scope['ongoing_plaque_inventory']
        if inventory is not None:
            assert len(inventory) == 18 and all(x['fully_completed'] is False for x in inventory)
    script_paths = [Path(__file__), *(Path(p) for p in proof['scripts']),
                    Path('dk4tool/patch/village_port_consistency.py')]
    for path in (DOC, *script_paths, Path('translations/release_stack.json')):
        copy(path, ARCHIVE / 'Reproduction' / path.name)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'Analysis' / path.relative_to(ROOT))
    captures, reports = [], []
    for folder in sorted(CAP.glob('village_development_v665_*')):
        rp = folder / 'capture_report.json'
        if not rp.exists():
            continue
        r = read(rp)
        assert r['ROM_sha256'] == pre['candidate_sha256'] and r['cold_boot'] and not r['savestate_loaded']
        assert not r['callback_errors']
        controller = read(folder / 'controller_progress.json')
        for s in r['frames_captured']:
            assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
        for s in r['read_only_pause_RAM_snapshots']:
            assert sha(Path(s['path']).read_bytes()) == s['sha256']
        for path in folder.rglob('*'):
            if path.is_file():
                copy(path, ARCHIVE / folder.name / path.relative_to(folder))
        reports.append({'path': str(rp), 'sha256': sha(rp.read_bytes()), 'frames': r['frames'],
            'controller_error': controller['error'], 'intended_outcome_not_inferred_from_terminal_report': True})
        for s in r['frames_captured']:
            captures.append({'run': folder.name, 'frame': s['frame'], 'source': s['path'],
                'PNG_sha256': s['PNG_sha256'], 'coordinate_fixtures': len(r['synthetic_location_fixtures']),
                'unmodified_original_capture': True, 'publication_approved': False})
    assert len(reports) == 35
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'all24_passwords_typed_through_native_keyboard_complete_prefix_buffers_cursor_capacity_and_display': True,
        'all24_original_0_to2_development_branches_and73_post_success_menu_labels': True,
        'all23_intended_Town_headers_specialty_fields_and2260992_native_screen_pixels': True,
        'original_visibility_results_support_variable_facility_node_counts': True,
        'original_cached_footer_and_submission_fragment_contract_explicit_no_pixel_waivers': True,
        'five_actual_port_name_discrepancies': proof['five_existing_developed_port_name_discrepancies_require_repair'],
        'two_actual_clue_indent_discrepancies': [4, 23],
        'data_only_five_alias_and_two_reflow_implementation_prepared_actual_registered_candidate_still_required': True,
        'prepared_ARM9_sha256': 'b92df335942af8db216b149f54c0eac75626ddde2cf573b6f41c20f3e217bda8',
        'Karibib_developed_port_return_and_all_eight_white_card_contexts_still_open': True,
        'all35_terminal_attempts_retained_failed_outcomes_not_credited': True,
        'no_password_development_scene_resource_or_victory_flag_injection': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'archive': str(ARCHIVE), 'guide_candidates': [], 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        old = pre['all_original_audits_before'][name]
        assert set(data) == set(old) | {KEY, 'current_goal_turn_classification'}
        assert all(data[k] == v for k, v in old.items() if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V665: all 24 password acceptances, 23 developed ports and seven confirmed repairs'
    addition = ('All24 passwords are typed through the actual Latin/symbol keyboard; every prefix, cursor, '
        'capacity and full visible input field pass. Original acceptance changes each intended village0 to2; '
        'all73 remaining menu labels pass. Twenty-three actual intended ports have complete native two-screen '
        'reconstructions (2,260,992 pixels), title masks and specialty names. Original visibility handles '
        'variable facility counts; source CPage footer submission resolves consumed-queue captures without '
        'masking1600 footer pixels. Karibib\'s encounter interrupts its return; exploratory defeat/Game Over/'
        'Syracuse and two failed follow-ups receive no return credit. Five actual old Town labels (Cod,Dixon,'
        'Lebeque,Tsukushi,Corfu) disagree with approved village names; Valparaiso/Wanganui have6px clue indents. '
        'A version-locked data repair is implemented for five existing name-pointer aliases and two generated '
        'reflows, with no growth or English prose change; registration/build/actual repaired captures remain '
        'next. V653/patch/registry/pointers unchanged. All35 attempts and derived sheets archived on E. All18 '
        'plaques incomplete and22 scopes exact; white-card/other graphics and acceptance gates remain open. '
        'See [V665 checkpoint](village_development_v665_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        before = path.read_text(encoding='utf-8')
        if heading not in before:
            path.write_text(before.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'], 'reports': reports,
        'captures': captures, 'guide_candidates': [],
        'scripts': {str(p): sha(p.read_bytes()) for p in script_paths},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print(f'V665 archived35 attempts/{len(captures)} capture records;24 acceptances/23 Town scenes; seven repairs and full goal remain open.')


if __name__ == '__main__':
    main()
