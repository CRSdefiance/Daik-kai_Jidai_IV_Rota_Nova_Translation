"""Record completed current storage checks without giving them native credit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_embedded_sync_v725 import ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
DECISIONS = Path('translations/contextual_embedded_graphics_decisions_v725.json')
DOC = Path('docs/embedded_sync_v725_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V725 Embedded copy consistency')
KEY = 'current_embedded_indexed_copy_consistency_and_contextual_MAPPOINT_review_v725'
PREVIOUS = 'current_name_atlas_and_press_button_complete_source_widget_fixtures_v724'


def main():
    proof_path = ROOT / 'storage_proof.json'
    proof = read(proof_path)
    assert proof['producer_sha256'] == sha(Path('scripts/audit_embedded_sync_v725.py').read_bytes())
    assert len(proof['all31_type16_images_with_source_headers_and_palettes']) == 31
    assert len(proof['nineteen_source_matched_complete_loose_planes_synchronized']) == 19
    sheets = proof['unmatched12_review_sheets_and_all_MAPPOINT_palette_bank_sheets']
    assert len(sheets) == 8
    for row in sheets:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    decisions = read(DECISIONS)
    assert len(decisions['decisions']) == 2
    review_path = ROOT / 'visual_review.json'
    assert not review_path.exists()
    save(review_path, {'storage_proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'all_eight_sheets_opened_and_reviewed': sheets,
        'unmatched12_images_current_source_decisions': 'Eleven clean-exact portraits,backdrops,ornament,Latin branding and original English; one unchanged localized Porto title.',
        'MAPPOINT_all21_palette_banks_reviewed_contextual_decisions': str(DECISIONS),
        'decisions_sha256': sha(DECISIONS.read_bytes()),
        'no_new_Japanese_instruction_or_menu_caption_requiring_translation_identified_in_reviewed_planes': True,
        'native_consumer_crops_palette_assignment_or_alpha_not_claimed': True,
        'remaining_raw_animation_and_ordinary_context_scope_retained': True, 'full_goal_complete': False})
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V724.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    ledger, matrix = read(LEDGER), read(MATRIX)
    for identifier, task, scope in (
        ('current-indexed-embedded-copy-consistency', 'Current indexed embedded and loose counterpart consistency',
         '31 type16 images with source-exact headers/palettes;19 entire counterpart planes and two65536-index Marker/Frame halves synchronized. Native relationships not inferred.'),
        ('current-embedded-contextual-icon-source-review', 'Twelve unmatched stored images and two MAPPOINT contextual-icon decisions',
         'Eight sheets opened:12 unmatched source/current images and all21 MAPPOINT palette banks. Original setting art retained with explicit rationale; native consumers and other raw/animation blocks remain separate.')):
        assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
        ledger['completed_work_carried_forward'].append({'id': identifier, 'task': task,
            'evidence': str(review_path), 'evidence_sha256': sha(review_path.read_bytes()),
            'scope': scope, 'queue_status': 'complete-not-in-active-queue'})
    village = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'village-and-environment-contexts')
    village['remaining_scope'] += (' V725 completes the current twelve unmatched type16 stored-image review '
        'and the two MAPPOINT contextual-icon decisions; carry those source decisions forward. '
        'Their original native consumers and other raw/animation coverage are not inferred.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V724_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V725 indexed embedded copy consistency and contextual icon source review'
    matrix['current_embedded_copy_consistency_v725'] = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'visual_review': str(review_path), 'visual_review_sha256': sha(review_path.read_bytes()),
        'contextual_decisions': str(DECISIONS), 'decisions_sha256': sha(DECISIONS.read_bytes()),
        'original_native_consumers_and_other_raw_animation_scopes_remain_open': True}
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **matrix['current_embedded_copy_consistency_v725'],
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V724_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
        'all18_original_incomplete_objects22_historical_requirements_exact': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == before[name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        previous = data[PREVIOUS]
        previous['matrix_live_path_at_recording'] = previous['current_matrix']
        previous['current_matrix'] = str(snapshot)
        previous['historical_snapshot_bytes_exact_original_recorded_hash'] = True
        data[KEY] = entry
        save(path, data)
    heading = '## V725: current embedded copy consistency and contextual icon decisions'
    summary = ('All57 GRP block extents and31 type16 image headers/palettes retain clean-source structure. '
        'All19 complete source-matched loose counterparts and both65536-index Marker/Frame halves are '
        'synchronized. Sixteen paired palettes match; two original bit15 differences and the original distinct '
        'CHARA palette are preserved separately. Eight sheets reviewed twelve unmatched images and every '
        'MAPPOINT bank. Eleven images are clean-exact non-Japanese-caption artwork/original Latin or English; '
        'the Porto title retains its complete English. Two new contextual MAPPOINT icon decisions preserve '
        'architectural signs without invented shop names. Four-bit icons are not claimed exact kbj copies. '
        'No new native/ordinary scene proof or raw/animation closure. E review archive checked;18 completed '
        'scopes carried forward,original18 incomplete objects/22 historical requirements exact. V712 ROM, '
        'manifest,patch,registry and canonical unchanged. Full goal active,exclusions and older-record note '
        'retained. See [V725 checkpoint](embedded_sync_v725_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for row in sheets:
        copy(row['path'], ARCHIVE / 'Storage comparisons' / Path(row['path']).name)
    for path in (DOC, MATRIX, LEDGER, DECISIONS, snapshot, proof_path, review_path, Path(__file__),
                 Path('scripts/audit_embedded_sync_v725.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'derived_storage_reviews_not_native_gameplay_or_guide': True, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V725 recorded: embedded copy consistency,12 unmatched reviews,two contextual decisions;18 completed scopes; E archive exact.')


if __name__ == '__main__':
    main()
