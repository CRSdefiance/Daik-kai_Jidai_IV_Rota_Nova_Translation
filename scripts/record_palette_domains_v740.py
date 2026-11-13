"""Carry forward a bounded source-art palette inspection, preserving open contexts."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.review_palette_domains_v740 import ROOT
from scripts.verify_village_wrap_v608 import read, save

MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
DOC = Path('docs/palette_domains_v740_checkpoint.md')
DECISION = Path('translations/stored_palette_art_decision_v740.json')
KEY = 'stored_palette_visibility_review_v740'
PREVIOUS = 'unresolved_display_context_recognition_packet_v739'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V740 Stored palette visibility')


def main():
    pp = ROOT / 'proof.json'
    proof = read(pp)
    assert proof['producer_sha256'] == sha(Path('scripts/review_palette_domains_v740.py').read_bytes())
    assert proof['statistics']['clean'] == proof['statistics']['current'] == {
        'PXL_files': 660, 'single_bank': 602, 'direct_color': 42,
        'multi_bank': 16, 'hidden_domain_files': 1}
    assert proof['all16_source_current_multi_bank_palettes_exact']
    assert proof['only_fontpanel_has_bank_zero_RGB_collisions_refined_elsewhere']
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, row in proof['previews'].items():
        assert sha(Path(path).read_bytes()) == row['file_sha256']
    assert sha(Path(proof['sheet']).read_bytes()) == proof['sheet_sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    snapshots = {}
    for live, name in ((MATRIX, 'graphics_requirements_at_V739.json'),
                       (LEDGER, 'graphics_work_at_V739.json')):
        target = ROOT / name
        assert not target.exists()
        target.write_bytes(live.read_bytes())
        snapshots[str(live)] = {'path': str(target), 'sha256': sha(target.read_bytes())}
    assert all(d[PREVIOUS]['current_matrix_sha256'] == snapshots[str(MATRIX)]['sha256'] and
               d[PREVIOUS]['current_work_ledger_sha256'] == snapshots[str(LEDGER)]['sha256']
               for d in before.values())
    save(DECISION, {
        'format': 'dk4-stored-palette-art-retention-v740',
        'path': '/_pxl/fontpanel.pxl', 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'clean_current_whole_file_exact': True,
        'dimensions': [44, 32], 'stored_palette_banks': 2,
        'both_complete_banks_visually_inspected_at_integer8x': True,
        'decision': 'retain-original-panel-art',
        'reason': 'Both stored RGB interpretations show textured/beveled panel surfaces. Neither shows a meaningful Japanese caption or instruction to translate. Preserve the original pixels and both palettes.',
        'runtime_palette_alpha_crop_and_other_consumers_not_inferred': True,
        'ROM_modified': False,
    })
    field = {'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
             'decision': str(DECISION), 'decision_sha256': sha(DECISION.read_bytes()),
             'scope': proof['scope'], 'full_goal_complete': False}
    ledger, matrix = read(LEDGER), read(MATRIX)
    assert len(ledger['completed_work_carried_forward']) == 28
    assert len(ledger['active_remaining_tasks']) == 5
    ledger['completed_work_carried_forward'].append({
        'id': 'stored-PXL-alternate-palette-RGB-visibility',
        'task': 'Stored PXL alternate-palette RGB visibility inspection',
        'evidence': str(pp), 'evidence_sha256': sha(pp.read_bytes()),
        'scope': 'All 660 PXL files per ROM classified; 16 multi-bank RGB partitions inspected. Only fontpanel conceals index distinctions in bank zero; both banks reviewed and retained as panel texture. No native context, alpha or low-contrast legibility closure.',
        'queue_status': 'complete-not-in-active-queue',
    })
    ledger['completed_scope_count'] = 29
    ledger['latest_evidence_checkpoint'] = 'V740 stored PXL alternate-palette source inspection'
    ledger['source_palette_visibility_v740'] = field
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V739_matrix_snapshot'] = snapshots[str(MATRIX)]
    matrix['latest_evidence_checkpoint'] = ledger['latest_evidence_checkpoint']
    matrix['source_palette_visibility_v740'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
             'current_matrix_sha256': sha(MATRIX.read_bytes()), 'current_work_ledger': str(LEDGER),
             'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
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
        'Every clean/current PXL file was classified: 660 per ROM, comprising 602 single-bank, '
        '42 direct-color and 16 multi-bank files. Among used indices, only fontpanel has '
        'equal bank-zero RGB colors that become distinct in another stored bank. Both complete '
        '44x32 interpretations were inspected at 8x; they contain panel texture, with no '
        'additional Japanese caption or instruction. Retain the clean-exact image and palettes. '
        'All 16 multi-bank palettes remain source-exact. This closes a bounded source RGB '
        'visibility check, not low-contrast legibility, bit15 opacity, external palettes, FLS '
        'or native contexts. Twenty-nine completed scoped checks now carry forward; five '
        'active groups remain. Original 18 incomplete audit objects and 22 historical '
        'requirements are preserved. V712 ROM/manifest/patch/registry/canonical and saves '
        'unchanged. Goal active, four Online-body exclusions and brown marks retained. '
        'See [V740 checkpoint](palette_domains_v740_checkpoint.md).\n')
    DOC.write_text(
        '# V740: stored PXL palette visibility\n\n' + summary +
        '\n## Evidence and limits\n\n'
        f'- [Both stored panel palettes at 8x](<{ARCHIVE.as_posix()}/fontpanel_banks_8x.png>)\n'
        '- `work/analysis/palette_domains_v740/proof.json` records the complete census, '
        'used indices, each concealed pair and distinguishing bank, and decoded PNG hashes.\n'
        '- `translations/stored_palette_art_decision_v740.json` records the visual retention decision.\n\n'
        'The comparison examines exact RGB equality: when bank zero distinguishes every '
        'used index pair that any stored bank distinguishes, another bank cannot reveal '
        'additional index geometry hidden by exact color equality. This does not imply '
        'every color contrast is readable or any bank is the native selection. Only the '
        'one newly identified hidden domain received new visual review. Existing full-source '
        'reviews carry forward. These PNGs are decoded artwork, not emulator screenshots.\n\n'
        'Original comic playback, small-control parents, village-card triggers, legacy '
        'consumer relationships and final integrated acceptance remain open. The prior '
        'context-recognition question remains pending. No absence of response is treated '
        'as a retention decision. Revisit older record-based checks after actual completion.\n',
        encoding='utf-8')
    heading = '## V740: stored alternate-palette source inspection'
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        if name == 'graphics_remaining_work.md':
            assert text.startswith('# Graphics: remaining work\n\nTwenty-eight completed checks')
            text = text.replace('Twenty-eight completed checks', 'Twenty-nine completed checks', 1)
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, DECISION, MATRIX, LEDGER, pp, Path(__file__),
                 Path('scripts/review_palette_domains_v740.py')):
        copy(path, ARCHIVE / 'evidence' / path.parent.name / path.name)
    for row in snapshots.values():
        copy(Path(row['path']), ARCHIVE / 'evidence' / Path(row['path']).name)
    for path in [Path(proof['sheet']), *(Path(p) for p in proof['previews'])]:
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {
        'files': {str(p.relative_to(ARCHIVE)).replace('\\', '/'): sha(p.read_bytes())
                  for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'decoded_artwork_not_native_screenshots': True, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V740 recorded: one newly exposed panel texture retained; 29 completed scopes, five active groups.', flush=True)


if __name__ == '__main__':
    main()
