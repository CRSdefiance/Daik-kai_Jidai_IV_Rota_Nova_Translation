"""Bind completed legacy source reviews and retain the unresolved native scope."""

from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_memory_streams_v682 import copy
from scripts.trace_legacy_owners_v719 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/legacy_owners_v719_checkpoint.md')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V719 Legacy source and owner evidence')
KEY = 'bounded_two_legacy_owner_flows_and_completed_source_reviews_carried_to_V712_v719'


def main():
    lead_path = ROOT / 'constant_flow_leads.json'
    lead = read(lead_path)
    assert lead['producer_sha256'] == sha(Path('scripts/trace_legacy_owners_v719.py').read_bytes())
    assert lead['analyzer_sha256'] == sha(Path(lead['analyzer']).read_bytes())
    assert lead['controls']['computed_alias_and_read_only_pointer_table_controls_pass']
    for version in lead['versions'].values():
        assert sha(Path(version['ROM']).read_bytes()) == version['ROM_sha256']
        assert {r['PC'] for r in version['owner_candidates']} == {0x0210E8A0, 0x0210E8AC, 0x0210FB20, 0x0210FB2C}
        assert all(r['direct_literal_owner_load'] for r in version['owner_candidates'])
        assert len(version['native_owners']) == 2
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    porto_path = Path('work/analysis/porto_review_v329/proof.json')
    porto = read(porto_path)
    assert sha(Path(porto['candidate']).read_bytes()) == porto['candidate_sha256']
    titles = []
    for row in porto['source_protection']:
        raw = current.read_file(row['resource'])
        assert sha(raw) == row['current_sha256']
        assert sha(clean.read_file(row['resource'])) == row['source_sha256']
        titles.append({'path': row['resource'], 'current_sha256': sha(raw),
            'exact_to_reviewed_V329_asset_including_embedded_archive': True,
            'source_protection_and_complete_word_planes_carried_forward': True})
    assert len(titles) == 3
    legacy_path = Path('work/analysis/movie_fades_v575/legacy_source_bindings.json')
    legacy = read(legacy_path)
    assert sha(Path(legacy['candidate']).read_bytes()) == legacy['candidate_sha256']
    blocks = []
    for row in legacy['legacy_blocks']:
        raw = IlnkContainer.parse(current.read_file(row['path'])).blocks[row['block']]
        source = IlnkContainer.parse(clean.read_file(row['path'])).blocks[row['block']]
        assert len(raw) == row['bytes'] and sha(raw) == row['current_sha256']
        assert sha(source) == row['source_sha256']
        review = Path(row['prior_source_review'])
        assert review.is_file() and row['all_bytes_accounted_under_reviewed_interpretation']
        blocks.append(dict(row, current_V712_bytes_exact_prior_review=True,
            prior_source_review_sha256=sha(review.read_bytes()),
            native_display_relationship_unresolved=True))
    assert len(blocks) == 11 and sum(r['reviewed_interpretation_images'] for r in blocks) == 560
    assert sum(r['current_sha256'] == r['source_sha256'] for r in blocks) == 10
    releases = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds')]
    release_hashes = {str(p): sha(p.read_bytes()) for p in releases}
    source_path = ROOT / 'source_carry_forward.json'
    save(source_path, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'Porto_source_proof': {'path': str(porto_path), 'sha256': sha(porto_path.read_bytes())},
        'three_complete_title_files': titles,
        'legacy_source_proof': {'path': str(legacy_path), 'sha256': sha(legacy_path.read_bytes())},
        'eleven_reviewed_legacy_storage_interpretations': blocks,
        'all560_stored_interpretations_accounted_not_new_native_displays': True,
        'comic21_overlap_V717_not_an_additional_unique_image_count': True,
        'normal_parent_and_runtime_import_geometry_display_still_open': True,
        'release_hashes_unchanged': release_hashes, 'full_goal_complete': False})
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    ledger = read(LEDGER)
    for identifier, task, scope in (
            ('Porto-title-stored-source-review', 'Three Porto Estado title copies: stored lettering and restoration review',
                'Current complete files exact to V329 source-protected full words and documented reconstruction; original native contexts remain open.'),
            ('eleven-legacy-block-stored-source-inspection', 'Eleven historical legacy blocks: stored source inspections and retention/localization decisions',
                '560 previously reviewed stored interpretations and all bytes bound to V712; overlaps V717 comic review,native relationships remain open.')):
        assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
        ledger['completed_work_carried_forward'].append({'id': identifier, 'task': task,
            'evidence': str(source_path), 'evidence_sha256': sha(source_path.read_bytes()),
            'scope': scope, 'queue_status': 'complete-not-in-active-queue'})
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'legacy-and-embedded-consumers')
    task['task'] = 'Resolve remaining ordinary legacy/embedded loading,import and display relationships.'
    task['remaining_scope'] = ('Standalone/Porto Estado title,sepia maps,copyright,ship textures and unresolved aliases: '
        'original parents,loading,crops and composition. Stored Porto review and all11 legacy-block source '
        'interpretations are complete; carry existing compatibility/tile/source proofs forward. '
        'V719 bounded computed ARM owner scan adds no display parent; do not repeat it as scene verification.')
    save(LEDGER, ledger)
    entry = {'documentation': str(DOC), 'lead_proof': str(lead_path),
        'lead_proof_sha256': sha(lead_path.read_bytes()), 'source_proof': str(source_path),
        'source_proof_sha256': sha(source_path.read_bytes()),
        'two_complete_original_owner_initializers_clean_current_match': True,
        'bounded_constant_flow_only_four_initializer_loads_no_new_normal_parent': True,
        'three_Portos_and11_stored_legacy_source_reviews_carried_forward_complete': True,
        'native_legacy_contexts_not_closed_and_no_global_unused_claim': True,
        'all18_original_objects_incomplete22_historical_requirements_exact': True,
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'release_hashes_unchanged': release_hashes, 'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == before[name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY] = entry
        save(path, data)
    path = Path('docs/graphics_remaining_work.md')
    text = path.read_text(encoding='utf-8')
    old = ('4. **Legacy/embedded consumers:** finish remaining standalone/Porto Estado title,\n'
        '   sepia/legacy, copyright, ship-texture and alias classifications/ordinary uses.\n'
        '   Existing source, software-copy and native tile proofs carry forward.')
    new = ('4. **Legacy/embedded consumers:** resolve remaining ordinary standalone/Porto\n'
        '   Estado title, sepia/legacy, copyright, ship-texture and alias loading/display\n'
        '   relationships. Porto stored lettering/restoration and all11 legacy-block\n'
        '   source interpretations are complete (V719); existing compatibility,\n'
        '   software-copy and native tile proofs carry forward.')
    assert old in text
    path.write_text(text.replace(old, new), encoding='utf-8')
    heading = '## V719: bounded legacy owner leads and completed stored-source work'
    summary = ('Complete original initialization binds20-byte winframe00/seamap owners in clean/V712. '
        'Bounded ARM constant flow across mapped main/pool/overlay units finds only four initializer loads, '
        'no new display parent; arbitrary dynamic/Thumb/native availability stays open. Three complete Porto '
        'title files remain exact to V329 source-protected full-word/restoration review. All11 legacy blocks '
        'retain the560 reviewed stored interpretations,ten clean-exact plus localized comic19; this overlaps '
        'V717 and is not560 new displays. Those completed source scopes leave active work; original native '
        'loading/import/geometry/display relationships remain. All18 original objects incomplete,22 scopes '
        'exact,Online exclusions/approved marks retained; no ROM/art/patch/registry/canonical change or new '
        'emulator/guide evidence. Full goal active; older-record follow-up retained. '
        'See [V719 checkpoint](legacy_owners_v719_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, LEDGER, Path('docs/graphics_remaining_work.md'), Path(__file__),
            Path('scripts/trace_legacy_owners_v719.py'), lead_path, source_path, porto_path, legacy_path):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'external_current_audits_and_progress': {str(Path('translations') / n): sha((Path('translations') / n).read_bytes()) for n in frozen},
        'no_new_native_screenshot': True, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for name in frozen:
        data = read(Path('translations') / name)
        assert data.pop(KEY) == entry and data == before[name]
    assert all(sha(Path(p).read_bytes()) == digest for p, digest in release_hashes.items())
    print('V719: four initializer-only leads; three Porto files/11 blocks source-exact to reviewed versions; eleven completed scopes carried forward; archive checked.', flush=True)


if __name__ == '__main__':
    main()
