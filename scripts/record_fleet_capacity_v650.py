"""Archive the terminal fleet-capacity test and retain every prior requirement."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/fleet_capacity_v650')
DOC = Path('docs/fleet_capacity_v650_checkpoint.md')
KEY = 'ordinary_five_ship_capacity_dock_previews_and_actual_captain_wrap_defects_v650'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V650 Five ship capacity')


def main():
    pre = read(ROOT / 'preflight.json')
    pp = ROOT / 'fleet_capacity_proof.json'
    p = read(pp)
    assert p['terminal_frame'] == 56600 and p['screenshots'] == 156
    assert p['ordinary_four_Latina_purchases_five_ship_fleet_verified'] and not p['full_goal_complete']
    for path, digest in {**pre['release_hashes'], **p['scripts']}.items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        current = read(Path('translations') / name)
        assert all(current[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    run = Path(p['report']).parent
    for source in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *[Path(s) for s in p['scripts']],
                   Path(__file__), Path(p['report']), run / 'navigation_command_journal.json']:
        checked_copy(source, ARCHIVE / source.name)
    captures = ARCHIVE / 'Unmodified test captures'
    captures.mkdir(exist_ok=True)
    for row in p['five_miniature_complete_mask_scan']:
        source = Path(row['path'])
        checked_copy(source, captures / source.name)
    saved = Path(p['five_ship_test_save']['path'])
    checked_copy(saved, ARCHIVE / 'five_ship_Copenhagen_test_copy.dsv')
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
             'normal_terminal56600_frame_cold_boot_no_gameplay_fixtures': True,
             'one_to_five_original_ship_models_and_all_four_purchases_verified': True,
             '156_unmodified_captures_and_bounded_five_miniature_mask_search': True,
             'actual_captain_prompt269_and272_word_split_defects_open': True,
             'isolated_five_ship_save_needs_cold_reload_and_support_ship_crews': True,
             'miniature_Confirm_parents_and_wider_graphics_scope_still_open': True,
             'all18_plaques_incomplete_22_historical_scopes_exact': True,
             'ROM_patch_registry_release_pointers_unchanged': True,
             'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        current = read(path)
        current[KEY], current['current_goal_turn_classification'] = entry, 'progress'
        save(path, current)
    heading = '## V650: ordinary five-ship capacity and actual captain wrapping defects'
    addition = ('A terminal56600-frame ordinary V640 run makes four Latina purchases, verifies '
        'five original ship models in seven later states, exercises dock previews and saves an '
        'isolated five-ship setup. No gameplay fixtures applied. All156 captured screens have no '
        'complete five-miniature mask;this is not global non-use or Confirm parent proof. '
        'Actual COMMON269/272 instructions split want/the across rows;complete font masks retain '
        'all letters. Their missing modal word-wrap handling needs repair. Screenshots/save/proof '
        'are on E. No ROM/patch/registry/release-pointer changes. All18 plaques incomplete and '
        '22 historical scopes exact;full goal active. See [V650 checkpoint](fleet_capacity_v650_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': p['candidate_sha256'],
        'RAM_and_native_exports_retained_at_original_E_paths': True,
        'guide_or_complete_gameplay_credit': False,
        'files': {str(f.relative_to(ARCHIVE)): sha(f.read_bytes()) for f in ARCHIVE.rglob('*')
                  if f.is_file() and f.name != 'provenance.json'}})
    print('V650 archived and all3 audits updated;18 plaques/22 scopes and release identities preserved.')


if __name__ == '__main__':
    main()
