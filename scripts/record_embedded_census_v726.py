"""Close current numeric source classification and remove stale queue entries."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_embedded_census_v726 import DECODE, LEGACY, ROOT, SELECT, TYPED
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
DOC = Path('docs/embedded_census_v726_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V726 Embedded block census')
KEY = 'current_numeric_CHARA_classification_and_all57_embedded_blocks_accounted_v726'
PREVIOUS = 'current_embedded_indexed_copy_consistency_and_contextual_MAPPOINT_review_v725'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['producer_sha256'] == sha(Path('scripts/reconcile_embedded_census_v726.py').read_bytes())
    assert len(proof['ten_current_numeric_containers']) == 10 and len(proof['all57_current_block_census']) == 57
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V725.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    identifier = 'current-numeric-CHARA-source-classification'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Current ten CHARA numeric-container source classification',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'Source/code/payload identities bind203 record pairs,406 prior native selections and8727 bounded controls. Numeric metadata retained; no new actor/atlas/display proof.',
        'queue_status': 'complete-not-in-active-queue'})
    village = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'village-and-environment-contexts')
    village['task'] = 'Resolve the eight village-card ordinary triggers.'
    village['remaining_scope'] = ('Eight white village cards,including preserved image207 fragment. '
        'Six retained town/icon decisions and their tested native compositions are complete. '
        'V725 contextual embedded decisions and V726 complete stored-block census carry forward; '
        'other unresolved native legacy relationships remain in their existing task.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V725_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V726 current numeric CHARA classification and complete embedded census'
    matrix['current_embedded_storage_census_v726'] = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'all57_blocks_accounted_under_documented_storage_classes': True,
        'eleven_reviewed_raw_interpretations_native_format_and_consumers_still_open': True}
    letters = next(r for r in matrix['explicit_goal_requirements'] if r['id'] == 'letters-bounds-native-loading-crops')
    letters['remaining'] = ('Original small-control parents/states,ordinary village triggers,raw comics and '
        'remaining legacy/standalone/embedded native relationships. The four original inventory evidence '
        'links are complete under V722-V724; name-atlas/prompt results retain source-command fixture limits.')
    sources = next(r for r in matrix['explicit_goal_requirements'] if r['id'] == 'embedded-contextual-source-review')
    sources['current57_block_census'] = matrix['current_embedded_storage_census_v726']
    sources['stored_numeric_CHARA_classification_complete'] = True
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **matrix['current_embedded_storage_census_v726'],
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V725_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
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
    remaining = Path('docs/graphics_remaining_work.md')
    text = remaining.read_text(encoding='utf-8')
    old = ('3. **Village/environment contexts:** resolve the remaining ordinary triggers for\n'
        '   eight village cards and unclassified legacy environmental copies. The six\n'
        '   retained town/icon art decisions and tested native contexts are complete;\n'
        '   carry their V718 evidence forward alongside completed map evidence.')
    new = ('3. **Village-card contexts:** resolve the ordinary triggers for eight village\n'
        '   cards. Retained town/icon native scopes and embedded contextual source\n'
        '   decisions are complete. Carry V718, V725 and V726 evidence forward;\n'
        '   unresolved native legacy relationships remain under the next task.')
    assert old in text
    remaining.write_text(text.replace(old, new), encoding='utf-8')
    heading = '## V726: current numeric CHARA source classification and embedded census'
    summary = ('The ten numeric CHARA blocks and original6944-byte decoder prefix,selector and parser '
        'ranges match their earlier native proof. All203 record pairs,406 historical native selections '
        'and8727 bounded numeric controls bind to current complete payload hashes. No native test is '
        'repeated or newly credited. A disjoint current census accounts for all57 blocks:30 type16,6 '
        'external-palette/pixel,10 numeric and11 reviewed raw interpretations. The eleven raw native '
        'formats/consumers remain open. Numeric source classification leaves routine work; village task '
        'now focuses on eight ordinary triggers. Stale four-inventory-gap text corrected. Nineteen '
        'completed scopes carried forward,original18 incomplete objects/22 historical requirements exact. '
        'V712 ROM/manifest/patch/registry/canonical unchanged; E evidence archive checked. Full goal '
        'active,exclusions/marks/older-record note retained. See [V726 checkpoint](embedded_census_v726_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, SELECT, DECODE, TYPED, LEGACY, Path(__file__),
                 Path('scripts/reconcile_embedded_census_v726.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'current_evidence_binding_not_new_emulator_or_native_execution': True, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V726 recorded: ten numeric blocks closed for source classification,57-block census complete;19 scopes; ordinary/native raw gaps retained.')


if __name__ == '__main__':
    main()
