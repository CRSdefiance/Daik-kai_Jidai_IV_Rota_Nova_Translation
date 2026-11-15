"""Record the six completed environmental contexts without changing old scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_environment_v718 import ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/environment_reconciliation_v718_checkpoint.md')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V718 Environmental coverage')
KEY = 'six_retained_environmental_decisions_actual_native_contexts_carried_to_V712_v718'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/reconcile_environment_v718.py').read_bytes())
    assert len(proof['six_retained_source_art_decisions']) == 6
    assert len(proof['current_source_against_historical_native_background_pixels']) == 11
    assert len(proof['current_source_font_against_six_historical_alternate_sign_caption_cases']) == 6
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    save(ROOT / 'audits_before.json', before)
    ledger = read(LEDGER)
    save(ROOT / 'ledger_before.json', ledger)
    identifier = 'six-retained-environmental-contexts'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Six retained environmental artwork decisions and their tested original native contexts',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'Six clean-exact art files,original town/code/font dependencies,eleven visible background regions and six complete alternate sprite/caption cases; historical runs retained with authorized fixture limits.',
        'queue_status': 'complete-not-in-active-queue'})
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'village-and-environment-contexts')
    task['task'] = 'Resolve the eight village-card ordinary triggers and remaining unclassified environmental copies.'
    task['remaining_scope'] = ('Eight white village cards,including preserved image207 fragment,and any unclassified legacy environmental copies. '
        'Six retained town/icon decisions and their tested native compositions are complete; do not repeat routine visits for unchanged assets.')
    save(LEDGER, ledger)
    entry = {'documentation': str(DOC), 'proof': str(proof_path),
        'proof_sha256': sha(proof_path.read_bytes()),
        'six_contextual_retention_source_and_tested_native_display_scopes_complete': True,
        'all_six_files_code_font_palette_and_original_caption_getters_carried_forward': True,
        'eleven_background_regions_six_alternate_full_sprite_caption_masks': True,
        'historical_reports_not_relabelled_as_new_V712_runs': True,
        'Osaka_Naha_authorized_coordinate_fixtures_not_earned_travel': True,
        'eight_village_cards_unclassified_copies_small_controls_comic_and_final_release_remain_open': True,
        'all18_original_incomplete_objects22_historical_requirements_exact': True,
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'release_hashes_unchanged': proof['release_hashes_unchanged'],
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == before[name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY] = entry
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    queue = Path('docs/graphics_remaining_work.md')
    text = queue.read_text(encoding='utf-8')
    old = ('3. **Village/environment contexts:** resolve the remaining ordinary triggers for\n'
        '   eight village cards and unverified contextual captions. Reuse completed\n'
        '   town, icon and map evidence.')
    new = ('3. **Village/environment contexts:** resolve the remaining ordinary triggers for\n'
        '   eight village cards and unclassified legacy environmental copies. The six\n'
        '   retained town/icon art decisions and tested native contexts are complete;\n'
        '   carry their V718 evidence forward alongside completed map evidence.')
    assert old in text
    queue.write_text(text.replace(old, new), encoding='utf-8')
    heading = '## V718: six retained environmental art contexts complete and carried forward'
    summary = ('All six original contextual-art decisions remain source-exact in V712. Current town/rendering '
        'code,font,palette and native Tavern/Inn getters match the historical versions. Eight historical '
        'reports and their PNGs re-read; current-source comparisons pass eleven visible background regions '
        'and six full alternate sprite/caption masks across Hangzhou,Seoul,Nagasaki,Osaka,Naha. This closes '
        'the six tested art/context scopes and removes routine repeat visits from active work. Historical '
        'captures are not new V712 runs; Osaka/Naha retain authorized coordinate-fixture limits. Eight '
        'village cards,unclassified legacy copies,small-control parents,original comics and final review '
        'remain open. All18 overall objects incomplete,22 historical objects exact; Online exclusions '
        'and approved marks retained. No ROM/art/patch/registry/canonical change,commit,push or guide '
        'approval. Full goal active; older record checks remain due after completion. '
        'See [V718 checkpoint](environment_reconciliation_v718_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (DOC, Path(__file__), Path('scripts/reconcile_environment_v718.py'), LEDGER, queue):
        copy(path, ARCHIVE / 'sources' / path.name)
    for path in ROOT.glob('*.json'):
        copy(path, ARCHIVE / 'analysis' / path.name)
    for row in proof['evidence'].values():
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['sha256']
        copy(path, ARCHIVE / 'carried_evidence' / path.parent.name / path.name)
    for path, digest in proof['reused_screenshots'].items():
        path = Path(path)
        assert sha(path.read_bytes()) == digest
        copy(path, ARCHIVE / 'Historical reused screenshots' / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'no_new_native_run_historical_screenshots_labelled': True, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for name in frozen:
        current = read(Path('translations') / name)
        assert current.pop(KEY) == entry
        assert current == before[name]
    assert all(sha(Path(p).read_bytes()) == digest for p, digest in proof['release_hashes_unchanged'].items())
    print('V718 recorded: nine completed scopes carried forward; 18/22 originals exact; E archive verified.', flush=True)


if __name__ == '__main__':
    main()
