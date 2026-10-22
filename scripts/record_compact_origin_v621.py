"""Archive complete scoped duel evidence without closing historical requirements."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_compact_origin_v621 import CAP, DONOR, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/compact_origin_v621_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V621 Compact source origins')
KEY = 'actual_boarding_duel_shared_compact_source_origin_repair_v621'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_compact_origin_v621.py').read_bytes())
    assert len(proof['complete_actual_duel_stat_cases']) == 4
    assert len(proof['three_complete_original_capture_and_victory_notices']) == 3
    assert sha(DONOR.read_bytes()) == '97997ce6fbeda9ff0272c08d7420e96676240b017e0037b721ed7c5eb52770d5'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, ROOT / 'actual_parent_proof.json', ROOT / 'transform_proof.json',
             ROOT / 'ordinary_regression_proof.json', ROOT / 'preservation_proof.json',
             ROOT / 'patch_proof.json', ROOT / 'static_combined_proof.json',
             ROM.with_suffix('.manifest.json'), Path('translations/compact_bitmap_origin_v1.json'),
             Path('dk4tool/patch/compact_bitmap_origin.py'), Path('scripts/native_battle_fixture_v620.py'),
             Path('scripts/probe_compact_origin_v621.py'), Path('scripts/prepare_compact_origin_v621.py'),
             Path('scripts/run_compact_origin_v621.py'), Path('scripts/verify_compact_origin_v621.py'),
             Path(__file__), Path('work/analysis/battle_contexts_v620/sea_encounter_prefix.json'),
             Path('work/analysis/battle_contexts_v620/source_fixture_proof.json'),
             Path('work/analysis/battle_contexts_v620/fixture_negative_controls.json')]
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    screenshots = []
    for name, run_path in (
        ('duel', CAP / 'compact_origin_v621_duel'),
        ('market', CAP / 'compact_origin_v621_market'),
        ('V620_failed_control', CAP / 'battle_contexts_v620_actual')):
        report_path = run_path / 'capture_report.json'
        report = read(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        checked_copy(report_path, ARCHIVE / (name + '_capture_report.json'))
        if (run_path / 'navigation_command_journal.json').exists():
            checked_copy(run_path / 'navigation_command_journal.json', ARCHIVE / (name + '_navigation_command_journal.json'))
        shots = {r['frame']: r for r in report['frames_captured']}
        frames = sorted(shots) if name != 'V620_failed_control' else [20800, 21200]
        for frame in frames:
            row = shots[frame]
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            target = ARCHIVE / f'{name}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(row['path'], target)
            screenshots.append({'path': str(target), 'frame': frame, 'sha256': row['PNG_sha256'],
                                'ROM_sha256': report['ROM_sha256'], 'context': name,
                                'proximity_fixture_active': name != 'market' and frame > 20400,
                                'unmodified_capture': True})
    save(ARCHIVE / 'provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'screenshots': screenshots, 'publication_approved': False, 'full_goal_complete': False,
        'donor_source_unchanged': str(DONOR), 'donor_source_sha256': sha(DONOR.read_bytes()),
        'full_RAM_and_native_exports_retained_in_generated_run_directories': True,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
        'patch_sha256': proof['patch_sha256'], 'status': 'experimental_actual_duel_source_origin_verified',
        'one_shared_callback_pointer_reuses_existing_Market_origin_wrapper': True,
        'no_new_code_or_pool_growth_no_other_file_or_component_changes_vs_V617': True,
        'all12_complete_stat_crops_in_two_actual_duel_states': True,
        'all19_ordinary_no_fixture_screens_exact_V617': True,
        'original_capture_and_victory_logic_reaches_Cargo_Setup_after_proximity_fixture': True,
        'Spoils_Distributed_Goods_and_miniature_graphics_still_open': True,
        'all18_original_plaques_incomplete_all22_historical_objects_exact': True,
        'archive': str(ARCHIVE), 'unmodified_screenshots': len(screenshots),
        'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        protected = {k: v for k, v in data.items() if k in (
            'candidate', 'candidate_sha256', 'latest_candidate', 'latest_candidate_sha256',
            'current_verified_release_candidate', 'current_verified_release_candidate_sha256',
            'latest_graphics_preservation')}
        data[KEY] = entry
        experimental = data.get('latest_compiled_experimental_candidate_with_inherited_native_gap', {}).copy()
        experimental.update({'candidate': str(ROM), 'sha256': proof['candidate_sha256'],
                             'profile': proof['profile'], 'duel_source_origin_native_gap_fixed': True,
                             'broader_graphics_gates_remain_open': True})
        data['latest_compiled_experimental_candidate_with_inherited_native_gap'] = experimental
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in protected.items())
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V621: shared compact bitmap origins and actual boarding duel'
    text = '''

V620's actual boarding duel exposed both stat rows painting at source row0,
overwriting a name and leaving the intended panels blank. V621 changes one shared
font callback pointer to the existing source-origin-aware Market wrapper. No new
code/pool allocation,strings,art,palettes,other files,components or arena bounds
change. Sixteen native origin replays and both actors across two actual duel states
pass full independent font masks/all12 original destination crops. All19 ordinary
no-save/no-fixture New Game/Market screens match V617;470/114 layers,921/57
preservation and exact clean-patch reconstruction pass.

Normal controls after one disclosed ship-proximity fixture produce three complete
capture/victory notices,then supplies/coins/national reward and Cargo Setup.
No enemy stats,outcome or reward flags are injected;earned voyage/campaign progress
is not claimed. Spoils/Distributed Goods/miniature controls remain unverified.
Screens,reports,input journal and hashed proofs are on E. Experimental V621 SHA256
`dde6c124f790c6f9dff2cb606064ee3cd02944a70570f45b978f68c32a114ef2`.
All18 plaques incomplete/all22 scopes exact;canonical and verified pointers remain
unchanged. Full graphics goal active;older-record review remains due at completion.
See [V621 checkpoint](compact_origin_v621_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'Archived{len(screenshots)} unmodified screenshots;3 audits/progress updated;18/22 scopes and canonical retained.')


if __name__ == '__main__':
    main()
