"""Archive bounded local-art evidence without reducing the graphics goal."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/local_art_correspondence_v649')
DOC = Path('docs/local_art_correspondence_v649_checkpoint.md')
KEY = 'local_multiscale_native_art_correspondence921_views126_queries6_geometric_controls_v649'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V649 Local artwork correspondence')


def main():
    pp = ROOT / 'correspondence_proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['all921_original_loose_native_views_source_hashes_and_dimensions_checked']
    assert proof['zero_two_patch_actual_geometric_leads_under_declared_thresholds']
    assert proof['not_global_copy_exclusion_or_legacy_runtime_non_use_proof']
    assert not proof['native_loading_crop_composition_or_new_gameplay_screenshot_credit']
    assert not proof['full_goal_complete']
    for p, h in proof['scripts'].items():
        assert sha(Path(p).read_bytes()) == h
    for p, h in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == h
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        current = read(Path('translations') / name)
        assert all(current[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.py'), *ROOT.glob('*.log'),
                   *[Path(p) for p in proof['scripts']], Path(__file__)]:
        checked_copy(source, ARCHIVE / source.name)
    controls = ARCHIVE / 'Synthetic search controls NOT GAMEPLAY'
    controls.mkdir(exist_ok=True)
    for source in (ROOT / 'Synthetic search controls').glob('*.png'):
        checked_copy(source, controls / source.name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'all_source_previews_and_large_feature_cache_remain_on_E_at_proof_paths': True,
        'feature_cache': proof['feature_cache'], 'no_new_emulator_or_guide_screenshots': True,
        'derived_source_search_controls_distinct_from_gameplay': True,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        '921_clean_native_views_and126_source_patch_queries_bound': True,
        '904_views_eligible_17_explicit_without_eligible_windows': True,
        '6_source_transform_controls_found_at_correct_known_positions': True,
        'failed_hash_only_control_preserved_full_correlation_added': True,
        '21_best_actual_leads_reviewed_no_new_complete_picture_or_caption_copy_established': True,
        'not_global_duplicate_exclusion_or_unused_legacy_asset_proof': True,
        'no_new_native_consumer_or_gameplay_credit': True,
        'all18_plaques_incomplete_22_historical_scopes_exact': True,
        'plaque_material_review_question_presented_no_response_inferred': True,
        'ROM_patch_registry_canonical_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        current = read(path)
        current[KEY], current['current_goal_turn_classification'] = entry, 'progress'
        save(path, current)
        assert all(read(path)[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V649: bounded local transformed-art correspondence investigation'
    addition = ('All921 clean PXL/FLS source views are bound by original hashes/declared native '
        'extents;904 have eligible local windows and17 are explicitly outside the feature model. '
        '126 raw-art patch queries use multiscale local correlation. The initial hash-only failure '
        'is retained;all6 transformed controls now match at independently known warp positions '
        'with2+ distinct source patches. Three labeled sheets/all21 best actual leads were reviewed; '
        'no complete picture/caption copy or two-patch geometric lead is established. This is not '
        'global copy exclusion or legacy non-use proof;no new native consumer/gameplay credit. '
        'Proof/source previews on E,no ROM/patch/registry/pointer changes. Repaired plaque packet '
        'presented for user material review;all18 entries incomplete and22 scopes exact. '
        'Full goal active. See [V649 checkpoint](local_art_correspondence_v649_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for p, h in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == h
    print('V649 archived;bounded source-correspondence evidence only;18 plaques/22 scopes and release identities preserved.')


if __name__ == '__main__':
    main()
