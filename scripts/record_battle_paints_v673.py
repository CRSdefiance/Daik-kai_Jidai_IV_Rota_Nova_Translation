"""Retain actual battle image selections without retiring unresolved graphics."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_paints_v673 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V673 Battle image calls')
DOC = Path('docs/battle_paints_v673_checkpoint.md')
KEY = 'actual_battle_victory253536_image_entries164_current_retained_pairs_and_coordinate_only_guards_v673'
SCRIPTS = ('scripts/native_battle_proximity_v673.py', 'scripts/prepare_battle_paints_v673.py',
           'scripts/run_battle_paints_v673.py', 'scripts/verify_battle_paints_v673.py',
           'scripts/record_battle_paints_v673.py', 'scripts/verify_battle_archive_v673.py',
           'scripts/observe_graphic_paints_v669.py', 'scripts/native_full_fleet_proximity_v653.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_battle_paints_v673.py').read_bytes())
    assert proof['records'] == 253536 and proof['target_control_source_hits'] == []
    assert proof['binding_counts'] == {'0': 159259, '1': 89501, '6': 4776}
    assert proof['guard_counts'] == {'0': 253536}
    assert all(r.get('kind') == 'direct_original_ARM_BL' for r in proof['caller_bindings'])
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'actual_battle_result_schedule_verified_six_control_contexts_still_open',
        'two_terminal28400_frame_cold_boots_observed_and_baseline': True,
        'all82_current_and82_retained_whole_two_screen_pairs_exact': True,
        'all253536_entry_argument_guards_pass89501_Frame4776_Marker_complete_files': True,
        'sixteen_original_direct_callers78_target_geometry_palette_primitive_tuples': True,
        'no_five_miniature_or_separate_Confirm_source_selection_in_this_schedule': True,
        'two_coordinate_only_fixtures_replayed_receipts_and_full_before_RAM_equal_between_runs': True,
        'current_wrapper_exact_V666_transform_guard_and_three_rejection_controls': True,
        'native_reward_funds25975_to30250_and_five_survivors_not_assigned_by_fixture': True,
        'no_per_entry_paint_completion_other_primitive_or_global_nonuse_credit': True,
        'six_control_displays_other_contexts_and_legacy_consumers_open': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        target = Path('translations') / name
        data = read(target)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(target, data)
    heading = '## V673: actual encounter, victory and Spoils source selections'
    addition = ('Two28400-frame cold boots repeat the original V654 battle/result schedule on '
        'V666. All82 current baseline and82 retained whole two-screen pairs match. The unchanged '
        'host observer records253536 guarded primitive entries:89501 complete Frame files, '
        '4776 Marker files,16 original direct callers and78 target geometry/palette tuples. '
        'No miniature/Confirm source selection occurs through these primitives in this sequence. '
        'The current strict wrapper repeats only two eight-byte coordinate approaches; each '
        'fixture is replayed from actual before RAM and all receipts match. Original funds '
        'rise25975 to30250 and all five ships survive; no result, health or reward writes. '
        'Read-only native export requests alone are removed from79 otherwise exact commands. '
        'No individual paint-return or global unused-art claim. Six actual control contexts, '
        'other source consumers and broader graphics remain open. No ROM/patch/registry/pointer '
        'or guide changes; all18 plaques incomplete and22 scopes exact. See '
        '[V673 checkpoint](battle_paints_v673_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        target = Path('docs') / name
        text = target.read_text(encoding='utf-8')
        if heading not in text:
            target.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for receipt in proof['reports']:
        folder = Path(receipt['path']).parent
        assert sha(Path(receipt['path']).read_bytes()) == receipt['sha256']
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in ('.json', '.png', '.bin'):
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
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'], 'reports': proof['reports'],
        'all_two_runs_terminal': True, 'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'no_global_nonuse_or_guide_publication_inferred': True, 'full_goal_complete': False})
    print('V673 two completed battle traces/screens archived; three audits/four docs updated;18/22 scopes retained.')


if __name__ == '__main__':
    main()
