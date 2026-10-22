"""Archive corrected complete names and retain every historical graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/commodity_fidelity_v636')
ROM = Path('out/all_routes_combined_v636_candidate.nds')
DOC = Path('docs/commodity_fidelity_v636_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V636 Complete commodity names')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V636 Complete commodity names')
KEY = 'complete17_source_faithful_commodity_names_and_actual_full_hints_v636'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_commodity_release_v635.py').read_bytes())
    assert proof['verification_wrapper_sha256'] == sha(Path('scripts/verify_commodity_release_v636.py').read_bytes())
    assert len(proof['all17_actual_controlled_full_name_tooltips']) == 17
    assert len(proof['all17_explicit_title_New_Game_captain_opening_story_frames_exact_V633']) == 17
    assert read('translations/release_stack.json')['profiles']['all-routes-unified-v635']['status'] == 'revoked'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    files = [DOC, Path('docs/glossary.md'), proof_path, ROM.with_suffix('.manifest.json'),
             Path('translations/commodity_fidelity_v2.json'), Path('translations/commodity_fidelity_manuscript_v2.json'),
             Path('dk4tool/patch/commodity_fidelity.py'), Path('scripts/prepare_commodity_fidelity_v635.py'),
             Path('scripts/prepare_commodity_fidelity_v636.py'), Path('scripts/verify_commodity_consumers_v635.py'),
             Path('scripts/verify_commodity_consumers_v636.py'), Path('scripts/verify_commodity_release_v635.py'),
             Path('scripts/verify_commodity_release_v636.py'), Path('scripts/native_commodity_label_fixture_v635.py'),
             Path('scripts/execute_sailing_footer_v317.py'), Path('scripts/headless_desmume_v193.py'), Path(__file__)]
    files.extend(ROOT / name for name in ('packing_plan.json', 'native_preview_proof.json',
                                         'consumer_native_proof.json', 'overlay_alias_proof.json',
                                         'terminology_decision.json', 'revoked_profile_guard.json',
                                         'tooltip_cases.json', 'patch_proof.json', 'preservation_proof.json',
                                         'build.log', 'all17_NATIVE_PREVIEW_SHEET.png'))
    files.extend(ROOT.glob('*NATIVE_PREVIEW.png'))
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    for path in (Path('work/analysis/commodity_fidelity_v635/source_rejection.json'),
                 Path('out/all_routes_combined_v635_candidate.manifest.json')):
        checked_copy(path, ARCHIVE / ('REVOKED_V635_' + path.name))
    rejected = ARCHIVE / 'REVOKED_V635_support_snapshot'
    rejected.mkdir(exist_ok=True)
    for path in Path('work/analysis/commodity_fidelity_v635/rejected_support_snapshot').iterdir():
        if path.is_file():
            checked_copy(path, rejected / path.name)
    Path('out/all_routes_combined_v635_candidate.REVOKED.txt').write_text(
        'V635 revoked before handoff:ヤシ油 was incorrectly expanded as Palm Oil.\n'
        'Use source-correct V636 instead. V635 is retained only as a diagnostic.\n', encoding='utf-8')
    tooltip_frames = {r['frame'] for r in read(ROOT / 'tooltip_cases.json')}
    screenshots, guides = [], []
    for receipt in proof['reports']:
        report_path = Path(receipt['path'])
        assert sha(report_path.read_bytes()) == receipt['sha256']
        report = read(report_path)
        label = report_path.parent.name
        checked_copy(report_path, ARCHIVE / (label + '_capture_report.json'))
        journal = report_path.parent / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        shots = {r['frame']: r for r in report['frames_captured']}
        controlled = label.endswith('_tooltips')
        current = report['ROM_sha256'] == proof['candidate_sha256']
        selected = tooltip_frames if controlled else (set(shots) if 'market' in label or 'startup' in label
                                                      else {4000, 4800, 9400, 19000, 19800, 20600, 21800, 22200, 22600})
        for frame in sorted(selected):
            row = shots[frame]
            prefix = 'CONTROLLED_LABEL_' if controlled else 'ORDINARY_'
            target = ARCHIVE / f'{prefix}{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(row['path'], target)
            record = {'path': str(target), 'frame': frame, 'sha256': row['PNG_sha256'],
                      'ROM_sha256': report['ROM_sha256'], 'unmodified_capture': True,
                      'cold_boot_no_savestate': True, 'controlled_name_pointer_only': controlled,
                      'normal_stock_or_acquisition_for_substituted_label_not_claimed': controlled,
                      'historical_control': not current}
            screenshots.append(record)
            guide_ok = current and not controlled and (
                label.endswith('_two_ship') and frame in (19000, 19800, 20600, 21800)
                or label.endswith('_startup_636') and frame in (1600, 3600))
            if guide_ok:
                destination = GUIDE / target.name
                checked_copy(row['path'], destination)
                guides.append({**record, 'path': str(destination), 'source_report': str(report_path),
                               'copied_save_and_test_purchase_disclosed_when_applicable': 'two_ship' in label,
                               'no_controlled_label_fixture': True})
    save(GUIDE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
                                   'screenshots': guides, 'publication_approved': False,
                                   'controlled_label_screenshots_excluded': True})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
                                     'screenshots': screenshots, 'guide_candidates': guides,
                                     'RAM_and_full_exports_retained_in_Generated_runs': True,
                                     'rejected_V635_kept_separate_not_a_release_parent': True,
                                     'publication_approved': False, 'full_goal_complete': False,
                                     'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
                                               for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
             'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
             'patch_sha256': proof['patch_sha256'], 'status': 'experimental_complete17_shared_names_verified',
             'all17_source_glosses_and_individual_reviews_complete': True,
             'coconut_oil_source_terminology_corrected_V635_revoked_before_handoff': True,
             'Iron_Ore_source_fidelity_followup_from_V634_resolved': True,
             'all124_live_cached_names248_Town124_Market_Local124_Price_cases_pass': True,
             'all17_actual_controlled_full_hint_composites_and_every_other_screen_pixel_exact': True,
             'all80_ordinary_compositions19_Market_and17_explicit_startup_frames_pass': True,
             'all470_batches114_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
             'all_original_code_fonts_palettes_native_helpers_and_memory_bounds_exact': True,
             'other107_commodity_names_preserved_not_newly_semantically_approved': True,
             'rare_goods_ordinary_stock_or_acquisition_not_inferred_from_label_fixtures': True,
             'all18_original_plaques_incomplete_all22_historical_objects_exact': True,
             'miniature_Confirm_village_legacy_material_movie_and_human_review_gates_open': True,
             'archive': str(ARCHIVE), 'guide_archive': str(GUIDE),
             'unmodified_archived_screenshots': len(screenshots), 'ordinary_guide_candidates': len(guides),
             'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        before = data.copy()
        data[KEY] = entry
        latest_key = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
        latest = data.get(latest_key, {}).copy()
        latest.update({'candidate': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
                       'complete17_source_faithful_commodity_labels_verified': True,
                       'broader_graphics_gates_remain_open': True})
        data[latest_key] = latest
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in before.items()
                   if k not in (KEY, latest_key, 'current_goal_turn_classification'))
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V636:17 complete source-faithful commodity labels'
    text = '''

Seventeen legacy abbreviations/material omissions now have full natural English,
including Iron Ore,Copper Ore,Raw Silk,Lacquerware,Frankincense,Whale Meat and
Smoked Salmon. Sourceヤシ油 is Coconut Oil;V635's Palm Oil draft was rejected
before handoff and its profile is revoked. Source-equivalent entries15/120 share
the complete Coconut Oil string while retaining separate original gameplay data.
All124 cached names,248 Town rasters,124 Market/Local and124 real-pointer Price
cases pass. All17 actual controlled hint composites include complete first/final
letters,white backing and every other screen pixel. All80 ordinary two-ship
compositions,19 no-save Market and17 explicit startup frames pass. No pool,
section,helper,font,palette or metadata change;995 name bytes in existing1124-byte
owned spans. Full470/114 stack,921/57 preservation and exact clean patch pass.
Experimental V636 SHA256:c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d.
ROM/patch,unmodified captures and ordinary guide candidates saved on E. Controlled
labels do not establish rare stock/acquisition. All18/22 historical scopes exact,
canonical/V610 verified pointers retained;only compiled experimental pointer moves.
The full graphics goal and remaining contexts remain open. See
[V636 checkpoint](commodity_fidelity_v636_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'V636 archived{len(screenshots)} unmodified screenshots and{len(guides)} ordinary guide candidates;18/22 scopes exact/open.')


if __name__ == '__main__':
    main()
