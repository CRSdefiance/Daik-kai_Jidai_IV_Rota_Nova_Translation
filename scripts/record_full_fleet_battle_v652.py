"""Archive actual full-fleet coverage and open findings without reducing scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/full_fleet_battle_v652')
DOC = Path('docs/full_fleet_battle_v652_checkpoint.md')
KEY = 'ordinary125_crew_five_ship_duel_loss_Oslo_recovery_and_three_queued_portrait_wrap_findings_v652'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V652 Full fleet encounter')


def main():
    pre, proof = read(ROOT / 'preflight.json'), read(ROOT / 'battle_proof.json')
    assert proof['all_four_runs_terminal'] and proof['miniature_mask_match_count'] == 0
    assert proof['victory_full_fleet_rewards_or_captured_ship_selection_not_reached']
    assert not proof['full_goal_complete']
    for path, digest in {**pre['release_hashes'], **proof['scripts']}.items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.txt'), *ROOT.glob('*.log'),
                   *map(Path, proof['scripts']), Path(__file__)]:
        checked_copy(source, ARCHIVE / source.name)
    for receipt in proof['reports']:
        path = Path(receipt['path'])
        assert sha(path.read_bytes()) == receipt['sha256']
        folder = ARCHIVE / path.parent.name
        folder.mkdir(exist_ok=True)
        checked_copy(path, folder / path.name)
        journal = path.parent / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, folder / journal.name)
        report = read(path)
        for shot in report['frames_captured']:
            checked_copy(shot['path'], folder / Path(shot['path']).name)
    staffing = read(ROOT / 'staffing_proof.json')
    for label, row in (('staffed_repaired_Copenhagen_five_ship_test_copy.dsv', staffing['prepared_save']),
                       ('post_loss_Oslo_four_ship_test_copy.dsv', proof['post_loss_four_ship_save_cold_reload'])):
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
        checked_copy(row['path'], ARCHIVE / label)
    entry = {'documentation': str(DOC), 'proof': str(ROOT / 'battle_proof.json'),
             'proof_sha256': sha((ROOT / 'battle_proof.json').read_bytes()),
             'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
             'four_terminal_runs143_unmodified_capture_records': True,
             'ordinary125_crew_and_full_repair_and_independent_saved_five_ship_cold_boot': True,
             'two_coordinate_only_fixtures_no_healing_enemy_or_outcome_writes': True,
             'actual_five_ship_duel_loss_four_ship_Oslo_recovery_and_cold_reload': True,
             'five_miniature_masks_no_matches_only_in_sampled_states': True,
             'victory_full_fleet_reward_controls_and_Confirm_parent_still_open': True,
             'three_source_bound_queued_portrait_word_wrap_families19_voices_need_repair': True,
             'actual_retreat_native_ID2684_disambiguated_by_original_call_fragment': True,
             'all18_original_plaques_incomplete_22_historical_scopes_exact': True,
             'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
             'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
    heading = '## V652: staffed five-ship encounter, loss/recovery and queued portrait findings'
    addition = ('Four terminal V651 runs produce143 unmodified captures. Normal hiring/Even '
        'confirmation commits125 crew;normal repair yields Vestaros60/49 plus four Latina25/19. '
        'Two source-water-checked coordinate-only fixtures reach the actual encounter/duel; '
        'no enemy,health or outcome writes. Original loss removes the lead ship and returns '
        'four surviving Latina to Oslo;that isolated save cold reloads. Full-fleet victory '
        'rewards are not reached. No complete five-miniature masks in these sampled states; '
        'all six control parents remain open. Cost890,unassigned71 and retreat2684 expose '
        'word splits across19 related voice entries in the two queued portrait paths. '
        'Original retreat call/selector disambiguates2684. Shared wrapping repair pending. '
        'Proof/captures/both test saves on E. ROM/patch/registry/pointers unchanged;all18 '
        'plaques incomplete and22 scopes exact;full goal active. See '
        '[V652 checkpoint](full_fleet_battle_v652_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'all_ROM_and_RAM_and_native_exports_remain_at_original_E_paths': True,
        'coordinate_fixtures_disclosed_no_normal_voyage_or_victory_credit': True,
        'no_final_guide_or_complete_gameplay_claim': True,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V652 archived;three audits updated;18 plaques/22 scopes and all release pointers preserved;three wrap families open.')


if __name__ == '__main__':
    main()
