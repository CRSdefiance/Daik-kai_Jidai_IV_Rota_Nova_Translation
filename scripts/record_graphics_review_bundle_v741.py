"""Record concrete combined-ROM review delivery and preserve unresolved work."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_graphics_review_bundle_v741 import BUNDLE, DOC, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
KEY = 'unchanged_combined_ROM_review_bundle_v741'
PREVIOUS = 'stored_palette_visibility_review_v740'
CHECKPOINT = Path('docs/graphics_review_handoff_v741_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V741 Review handoff')


def main():
    pp = ROOT / 'proof.json'
    proof = read(pp)
    assert proof['producer_sha256'] == sha(Path('scripts/prepare_graphics_review_bundle_v741.py').read_bytes())
    assert sha((BUNDLE / 'bundle_manifest.json').read_bytes()) == proof['bundle_manifest_sha256']
    for path, digest in proof['all_packaged_files_hash_verified'].items():
        assert sha((BUNDLE / path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    snapshots = {}
    for live, name in ((MATRIX, 'graphics_requirements_at_V740.json'),
                       (LEDGER, 'graphics_work_at_V740.json')):
        target = ROOT / name
        assert not target.exists()
        target.write_bytes(live.read_bytes())
        snapshots[str(live)] = {'path': str(target), 'sha256': sha(target.read_bytes())}
    assert all(d[PREVIOUS]['current_matrix_sha256'] == snapshots[str(MATRIX)]['sha256'] and
               d[PREVIOUS]['current_work_ledger_sha256'] == snapshots[str(LEDGER)]['sha256']
               for d in before.values())
    save(ROOT / 'external_context_leads.json', {
        'publisher_village_mechanic': {
            'url': 'https://www.gamecity.ne.jp/d4/promise/',
            'observed': 'Publisher describes 24 villages, village-specific promise words and opening their trade facilities. This corresponds to the arrival/password/development flow already tested in V734/V735.',
            'new_card_trigger_identified': False,
        },
        'Nintendo_DS_product_page': {
            'url': 'https://www.nintendo.co.jp/ds/software/adkj/index.html',
            'observed': 'General DS game and wireless-race description; no original comic viewer or village-card trigger identified in the retrieved text.',
        },
        'publisher_DS_portal': {
            'url': 'https://gw.gamecity.ne.jp/ds/d4/',
            'retrieval': 'web fetch cache miss; not treated as evidence of absent content',
        },
        'local_manual_source_search': '../manual-search/search-summary.json',
        'local_manual_result': 'Prior exact DS manual scan search remains unresolved; verified alternate manual is PlayStation, not evidence of DS additions.',
        'no_global_nonuse_or_new_native_display_claim': True,
    })
    field = {
        'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'bundle': str(BUNDLE), 'README': str(BUNDLE / 'README.md'),
        'bundle_manifest_sha256': proof['bundle_manifest_sha256'],
        'candidate_version': 'V712', 'packaging_checkpoint': 'V741',
        'cold_boot_test_question': 'accepted by async tool; user result pending',
        'cold_boot_acceptance_or_canonical_promotion': False,
        'no_new_gameplay_credit_or_completed_scope_count_increase': True,
        'full_goal_complete': False,
    }
    ledger, matrix = read(LEDGER), read(MATRIX)
    assert ledger['completed_scope_count'] == 29
    assert len(ledger['completed_work_carried_forward']) == 29 and len(ledger['active_remaining_tasks']) == 5
    ledger['graphics_review_bundle_v741'] = field
    ledger['latest_evidence_checkpoint'] = 'V741 unchanged combined-ROM review bundle and pending cold-boot test'
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V740_matrix_snapshot'] = snapshots[str(MATRIX)]
    matrix['latest_evidence_checkpoint'] = ledger['latest_evidence_checkpoint']
    matrix['graphics_review_bundle_v741'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(CHECKPOINT), **field,
             'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
             'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
             'all18_original_incomplete_objects22_historical_requirements_exact': True}
    for name, scope in frozen.items():
        path = Path('translations') / name
        d = read(path)
        assert d == before[name]
        assert d.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert d.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        for key, live in (('current_matrix', MATRIX), ('current_work_ledger', LEDGER)):
            d[PREVIOUS][key + '_live_path_at_recording'] = d[PREVIOUS][key]
            d[PREVIOUS][key] = snapshots[str(live)]['path']
        d[PREVIOUS]['immutable_snapshot_bytes_exact_original_recorded_hashes'] = True
        d[KEY] = entry
        save(path, d)
    summary = (
        'A concrete experimental review bundle on E now contains the unchanged V712 combined '
        'ROM, neighboring original manifest, exact clean-input xdelta, full applied-layer/change '
        'list, audit snapshots and review instructions. All 13 packaged payloads and the bundle '
        'manifest are hash-checked. The existing V721 patch reconstruction is still whole-byte '
        'exact, and V737 registered rebuild identity carries forward; no repeated patch application '
        'or new gameplay is claimed. Cold-boot review requested for title/New Game/Lil opening '
        'and the two plaque screens; response pending. The publisher village description '
        'corresponds to already tested password/development flows and yields no new card trigger. '
        'Five active groups and 29 completed checks unchanged; all 18 original audit objects '
        'incomplete and 22 historical requirements exact. Production ROM/art/manifest/patch/registry, '
        'canonical and saves unchanged. Goal active, exclusions/marks/older-record follow-up retained. '
        'See [V741 review handoff](graphics_review_handoff_v741_checkpoint.md).\n')
    CHECKPOINT.write_text(
        '# V741: combined graphics review handoff\n\n' + summary +
        f'\n[Review instructions](<{BUNDLE.as_posix()}/README.md>)\n\n'
        'V741 labels the review package, not a new ROM version. The retained V712 neighboring '
        'manifest names its original build paths; its local ROM, patch and manifest basenames '
        'are preserved. `bundle_manifest.json` hashes the portable payloads. The audit snapshot '
        'inside the package records the authoritative state before this handoff; current live '
        'audit files additionally link this handoff.\n\n'
        '## Context investigation\n\n'
        'The [publisher promise-word page](https://www.gamecity.ne.jp/d4/promise/) describes '
        '24 villages and their password-unlocked trade. It gives no newly identified ordinary '
        'trigger for the eight white cards. The [Nintendo DS product description]'
        '(https://www.nintendo.co.jp/ds/software/adkj/index.html) supplies general game/race '
        'information. A publisher portal fetch failed; no absence-of-content conclusion follows. '
        'The retained manual-source search distinguishes the available PlayStation manual '
        'from the missing verified exact DS booklet. These leads supply no new gameplay '
        'or global-unused-art proof.\n\n'
        '## Pending evidence\n\n'
        'The earlier comic-context recognition question and the concrete user cold-boot '
        'question remain pending. Neither is a running process or verified wait. No reply '
        'or user acceptance is inferred from elapsed time. The current short review covers '
        'only its named screens; final complete-goal sign-off remains separate.\n', encoding='utf-8')
    heading = '## V741: concrete combined graphics review handoff'
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (CHECKPOINT, DOC, MATRIX, LEDGER, pp, ROOT / 'external_context_leads.json',
                 Path(__file__), Path('scripts/prepare_graphics_review_bundle_v741.py')):
        copy(path, ARCHIVE / 'evidence' / path.parent.name / path.name)
    for row in snapshots.values():
        copy(Path(row['path']), ARCHIVE / 'evidence' / Path(row['path']).name)
    save(ARCHIVE / 'provenance.json', {
        'files': {str(p.relative_to(ARCHIVE)).replace('\\', '/'): sha(p.read_bytes())
                  for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'ROM_bundle': str(BUNDLE), 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V741 recorded: unchanged V712 review bundle delivered; cold-boot result pending, five groups open.', flush=True)


if __name__ == '__main__':
    main()
