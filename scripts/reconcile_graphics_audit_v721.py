"""Refresh current build/audit pointers and retain every unresolved requirement."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import load_release_stack, resolve_release_batches
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/graphics_audit_v721')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
DOC = Path('docs/graphics_current_audit_v721.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V721 Current graphics audit')
KEY = 'current_full_goal_and22_historical_requirement_matrix_V712_v721'

EVIDENCE = {
    'comic': 'work/analysis/comic_restoration_v717/proof.json',
    'legacy': 'work/analysis/legacy_owners_v719/source_carry_forward.json',
    'environment': 'work/analysis/environment_reconciliation_v718/proof.json',
    'cards': 'work/analysis/village_cards_v699/final/proof.json',
    'controls': 'work/analysis/small_controls_v701/proof.json',
    'gender': 'work/analysis/gender_reconciliation_v720/proof.json',
    'material': 'work/analysis/plaque_acceptance_v715/acceptance.json',
    'plaques': 'work/analysis/plaque_review_v714/current_plaque_review_proof.json',
    'naming': 'docs/reviewed_name_release_v299.md',
    'characters': 'docs/characters_gallery_v525_checkpoint.md',
    'gallery': 'work/analysis/file_requests_v681/proof.json',
    'opening': 'work/analysis/movie_fades_v575/native_fade_proof.json',
    'movie_paths': 'docs/original_movies_v537_checkpoint.md',
    'movie_endings': 'docs/current_endings_v583_checkpoint.md',
    'movie_transitions': 'work/analysis/movie_transition_bitmaps_v648/transition_bitmap_proof.json',
    'standalone': 'work/analysis/standalone_resource_compatibility_v550/native_compositing_proof.json',
    'Extras': 'work/analysis/alternate_title_v238/native_display_proof.json',
    'equipment': 'work/analysis/equipment_catalogue_v586/native_catalogue_proof.json',
    'conditions': 'work/analysis/condition_matrix_v637/current_condition_matrix_proof.json',
    'cursor': 'docs/equipment_cursor_v663_checkpoint.md',
    'square': 'docs/square_caption_cells_v484_checkpoint.md',
    'COMMON': 'docs/refit_help_v713_checkpoint.md',
    'maps': 'work/analysis/sepia_consumers_v662/native_paint_proof.json',
    'source_protection': 'work/analysis/graphics_audit_v721/preservation_proof.json',
    'integration': 'work/analysis/refit_help_v712/release_proof.json',
    'new_game': 'work/analysis/refit_help_v712/display_proof.json',
}

# Each entry retains the historical text separately. Completed subscopes do not
# imply every original runtime/parent requirement has been demonstrated.
HISTORICAL = [
    (1, ['comic'], 'Stored captions,restoration and marks complete.', 'Original comic viewer/import/crops/readability unresolved.'),
    (2, ['legacy', 'gender'], 'All11 stored interpretations reviewed; selected loose/native copies verified.', 'Legacy descriptor,palette,import and ordinary consumers unresolved.'),
    (3, ['environment'], 'Six retained environmental assets and their tested native contexts complete.', 'No new earned-voyage or every-state claim; unclassified copies tracked separately.'),
    (4, ['cards'], 'Image207 fragment preserved; full card displayed through original event parent fixture.', 'Fragment reading not invented; original ordinary card trigger unresolved.'),
    (5, ['naming', 'characters', 'gallery', 'opening'], 'Selected names,source decisions,Gallery and observed opening lettering verified.', 'Other legacy title/caption contexts remain separate.'),
    (6, ['movie_paths', 'movie_endings', 'movie_transitions', 'gallery', 'gender'], 'Substantial actual loader,original-parent,source-bound display and transition evidence.', 'Remaining raw/legacy/standalone/control/card parents and full timing/scene claims unverified.'),
    (7, ['integration', 'new_game'], 'Registered combined V712,manifest,layer stack and exact clean patch verified.', 'Final whole-scope review remains open; no canonical promotion or user acceptance inferred.'),
    (8, ['opening', 'new_game'], 'Opening/main title has actual color,crop,fade and cold-boot evidence.', 'Does not close separate standalone/legacy consumers or every hardware/fade state.'),
    (9, ['Extras', 'standalone'], 'title05 Extras normal display complete; separate logo whole native fixture verified.', 'Standalone logo original parent remains unidentified.'),
    (10, ['legacy', 'standalone'], 'Three Porto title files source/letter/restoration reviewed; ocean title native fixture verified.', 'Original Porto parents and embedded whole-scene composition unresolved.'),
    (11, ['comic'], 'Recruitment,credits,ending source/word/restoration review complete.', 'Original raw comic scene loading/crops/readability unresolved.'),
    (12, ['comic'], 'Chase dialogue source/word/restoration review complete.', 'Original raw comic scene loading/crops/readability unresolved.'),
    (13, ['comic'], 'Creature introduction source/word/restoration review complete.', 'Original raw comic scene loading/crops/readability unresolved.'),
    (14, ['comic'], 'Decorative Maria source/word/restoration review complete.', 'Original raw comic scene loading/crops/readability unresolved.'),
    (15, ['comic'], 'Reaction/reveal source/word/restoration review and brown-mark retention complete.', 'Original raw comic scene loading/crops/readability unresolved.'),
    (16, ['naming', 'characters'], 'Original Camille/Kamil inconsistency superseded by approved naming integration.', 'Completed naming decision stays closed; unrelated legacy scene obligations remain.'),
    (17, ['naming', 'characters'], 'Original Maria field inconsistency superseded by approved naming integration.', 'Completed naming decision stays closed; unrelated legacy scene obligations remain.'),
    (18, ['material', 'plaques', 'gender'], 'Material accepted;18 base meanings/views and tested gender variants verified.', 'Original18 overall objects remain incomplete under user direction until final audit.'),
    (19, ['equipment', 'conditions', 'cursor', 'material'], 'All103 equipment names,84 condition fixtures and ordinary five-slot cursor coverage exist.', 'These scoped results do not prove every actor/state/acquisition combination; final audit remains.'),
    (20, ['square', 'environment'], 'Square caption repair and six environmental contexts verified within their documented scopes.', 'Other independent legacy/native context obligations remain; no all-city/all-menu claim.'),
    (21, ['COMMON', 'new_game'], 'Source-preserved COMMON prefix/copy checks and actual observed displays carry forward.', 'All actual message parents and older prose/record-based review are not proved; later requested follow-up retained.'),
    (22, ['maps'], 'Correct unlabeled map retention and64 complete native sepia painting contracts verified.', 'Original sepia/legacy map menu consumers and GPU states unresolved.'),
]


def main():
    assert ROOT.is_dir() and not MATRIX.exists()
    current = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    preservation_path = ROOT / 'preservation_proof.json'
    preservation = read(preservation_path)
    assert preservation['candidate_sha256'] == digest
    assert len(preservation['entries']) == 921 and len(preservation['embedded_block_extents']) == 57
    assert preservation['current921_format_palette_extent_checks'] and preservation['all57_embedded_block_extents_exact']
    registry = load_release_stack()
    manifest_path = ROM.with_suffix('.manifest.json')
    manifest = read(manifest_path)
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v712'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    expected_batches = resolve_release_batches(manifest['profile'], [], registry)
    assert [Path(p).as_posix() for p in manifest['batches']] == [p.as_posix() for p in expected_batches]
    assert len(expected_batches) == 470 and len(registry['accepted_layers']) == 114 and all(manifest['checks'].values())
    # Decode the existing patch into an explicitly research-only reconstruction;
    # never regenerate or overwrite the shipped patch as part of this audit.
    restored = ROOT / 'V712_patch_reconstruction_RESEARCH_ONLY.nds'
    assert not restored.exists()
    apply_xdelta(Path('work/clean.nds'), ROM.with_suffix('.xdelta'), restored)
    assert restored.read_bytes() == ROM.read_bytes()
    old = NdsImage.open('out/all_routes_combined_v692_candidate.nds')
    graphics = [(p, raw) for _, p, raw in current.iter_files() if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and all(raw == old.read_file(p) for p, raw in graphics)
    evidence = {k: {'path': p, 'sha256': sha(Path(p).read_bytes())} for k, p in EVIDENCE.items()}
    ledger = read('translations/graphics_current_work_v1.json')
    assert len(ledger['completed_work_carried_forward']) == 12
    for row in ledger['completed_work_carried_forward']:
        assert sha(Path(row['evidence']).read_bytes()) == row['evidence_sha256']
    requirements_path = Path('translations/graphics_completion_requirements_v313.json')
    requirements = read(requirements_path)
    historical = requirements['historical_pending_items_retained']
    assert len(historical) == 22 and [r['historical_item'] for r in historical] == list(range(1, 23))
    rows = []
    for number, refs, completed, remaining in HISTORICAL:
        original = historical[number - 1]
        rows.append({'historical_item': number, 'original_requirement': original['original_requirement'],
            'completed_subscopes': completed, 'remaining_scope_or_verification_limit': remaining,
            'evidence': [evidence[k] for k in refs],
            'original_historical_object_unchanged': True,
            'full_requirement_or_entire_goal_not_inferred_from_scoped_checks': True})
    visual_path = Path('translations/graphics_visual_audit_v150.json')
    visual = read(visual_path)
    confirmed = [r for r in visual['records'] if r['review_status'].startswith('confirmed-japanese')]
    assert len(confirmed) == 26
    batches = [(p, read(p)) for p in expected_batches]
    inventory = []
    for row in confirmed:
        path = row['path']
        matches = [str(p) for p, d in batches if str(d.get('file_path', '')).casefold() == path.casefold()]
        inventory.append({'path': path, 'texture_index': row['texture_index'],
            'source_review_status': row['review_status'],
            'current_whole_file_sha256': sha(current.read_file(path)),
            'matching_registered_file_batches': matches,
            'batch_link_is_not_complete_record_coverage_or_native_context_proof': True,
            'four_Online_bodies_excluded': '/online/Online' in path,
            'display_scope_requires_specific_evidence_in_matrix_or_followup': True})
    recheck = ['/_pxl/mysterymap/mys_hunt_d.pxl', '/_pxl/slackimg12.pxl',
        '/_pxl/slackimg20.pxl', '/Iseki/dock.pxl']
    assert all(any(r['path'] == p for r in inventory) for p in recheck)
    release_hashes = {str(p): sha(p.read_bytes()) for p in (ROM, manifest_path, ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path(manifest['base_rom']))}
    matrix = {'format': 'dk4-current-graphics-requirements-v1', 'candidate': str(ROM),
        'candidate_sha256': digest, 'profile': manifest['profile'], 'goal_status': 'active',
        'all_original_goal_scope_preserved': True, 'full_goal_complete': False,
        'explicit_goal_requirements': [
            {'id': 'PXL-FLS-localization', 'status': 'implementation-present-contexts-incomplete',
             'scope': 'Natural faithful English for every confirmed Japanese-bearing PXL/FLS; preserve the four Online body exclusions.',
             'proof': '26-entry source inventory below,registered470 batches,individual source/display proofs; batch links alone do not close display.'},
            {'id': 'gender', 'status': 'tested-loose-parents-complete-embedded-open', 'evidence': evidence['gender']},
            {'id': 'titles-subtitles', 'status': 'opening-main-Extras-observed-legacy-contexts-open',
             'evidence': [evidence[k] for k in ('opening', 'Extras', 'legacy', 'standalone')]},
            {'id': 'embedded-contextual-source-review', 'status': 'stored-reviews-complete-runtime-relationships-open',
             'evidence': [evidence[k] for k in ('legacy', 'comic', 'environment')]},
            {'id': 'source-preservation', 'status': 'current-format-palette-extents-verified',
             'evidence': evidence['source_protection'], 'limit': 'Does not prove every concealed background,unowned pixel or native display by itself.'},
            {'id': 'letters-bounds-native-loading-crops', 'status': 'partially-verified',
             'remaining': 'Six small controls,ordinary village cards,original raw comics and remaining legacy/standalone/import contexts; four original inventory assets require explicit evidence reconciliation.'},
            {'id': 'one-combined-ROM-exact-patch', 'status': 'current-integration-and-exact-patch-verified-final-review-open',
             'profile': manifest['profile'], 'accepted_layers': 114, 'batches': 470,
             'reconstruction': str(restored), 'reconstruction_sha256': sha(restored.read_bytes())},
            {'id': 'audit-progress-final-gameplay', 'status': 'updated-current-scope-final-verification-incomplete',
             'limit': 'Targeted emulator/fixture coverage does not establish full playthrough,all contexts,hardware or user acceptance.'}],
        'historical22_current_reconciliation': rows, 'original26_confirmed_entries_current_implementation_links': inventory,
        'four_original_inventory_assets_needing_explicit_native_evidence_reconciliation': recheck,
        'these_four_are_not_new_translation_defects_or_proven_untested_ever': True,
        'completed_work_ledger': 'translations/graphics_current_work_v1.json',
        'completed_work_ledger_sha256': sha(Path('translations/graphics_current_work_v1.json').read_bytes()),
        'all675_PXL_FLS_files_byte_exact_to_V692': True,
        'historical18_overall_plaque_objects_remain_incomplete22_original_objects_retained': True,
        'source_macro_IO_and_suffix_replay_limits_not_erased_or_called_production_defects': True,
        'older_record_based_checks_follow_after_actual_full_goal_completion': True,
        'release_hashes_unchanged': release_hashes, 'producer_sha256': sha(Path(__file__).read_bytes())}
    save(MATRIX, matrix)
    snapshot = {}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert KEY not in data
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        snapshot[name] = {k: data[k] for k in ('candidate', 'candidate_sha256', 'latest_candidate',
            'latest_candidate_sha256', 'source_preservation_proof', 'preservation_proof_sha256') if k in data}
        if name == requirements_path.name:
            data['candidate'], data['candidate_sha256'] = str(ROM), digest
            data['source_preservation_proof'] = str(preservation_path)
            data['preservation_proof_sha256'] = sha(preservation_path.read_bytes())
        if name == 'graphics_completion_campaign_v1.json':
            data['latest_candidate'], data['latest_candidate_sha256'] = str(ROM), digest
        data[KEY] = {'matrix': str(MATRIX), 'matrix_sha256': sha(MATRIX.read_bytes()),
            'documentation': str(DOC), 'candidate': str(ROM), 'candidate_sha256': digest,
            'previous_root_current_snapshot': snapshot[name],
            'all_original18_objects22_requirements_retained': True, 'full_goal_complete': False}
        save(path, data)
    save(ROOT / 'previous_root_metadata.json', snapshot)
    lines = ['# Current graphics completion audit — V721', '',
        'Current experimental ROM: **V712**. This audit refreshes stale V610 root pointers;',
        'it does not rebuild, promote or claim the full graphics goal complete.', '',
        '## Current preservation and integration', '',
        '- All921 PXL/FLS header, indexed palette, format and extent checks pass.',
        '- All57 embedded block extents pass. All675 complete PXL/FLS files equal V692.',
        '- Registered profile retains470 batches and114 accepted layers; manifest/base/registry hashes match.',
        '- The existing clean-ROM patch was decoded again; every reconstructed ROM byte equals V712.',
        '- These checks do not independently prove all original pixels,hidden restoration or gameplay.', '',
        '## All22 historical requirements', '',
        '| # | Completed or verified subscopes | Remaining scope or limit |', '|---|---|---|']
    for r in rows:
        lines.append(f"|{r['historical_item']}|{r['completed_subscopes']}|{r['remaining_scope_or_verification_limit']}|")
    lines += ['', '## Inventory reconciliation follow-up', '',
        'The original26 confirmed entries now have current whole-file hashes and registered implementation links.',
        'A matching file batch does not prove every region or an original display consumer. The following four',
        'need explicit linkage to their best native evidence before closure:', '',
        *[f'- `{p}`' for p in recheck], '',
        'This is not evidence of four new translation defects or a claim that they have never been tested.',
        'Review existing loader/widget/source proofs,then pursue a new normal context only where evidence is missing.', '',
        'The six small controls,eight village-card ordinary triggers,original raw comics,remaining legacy/standalone',
        'contexts and final whole-scope verification remain open. All18 original plaque/hint objects and22 historical',
        'objects remain exact. The four low-resolution Online bodies remain excluded. Older record checks remain',
        'queued after actual full completion. No new screenshot/guide approval,commit,push or canonical promotion.', '',
        f'Current matrix: `{MATRIX}`.', f'Candidate SHA256: `{digest}`.',
        f'Archive: `{ARCHIVE}`.', '']
    DOC.write_text('\n'.join(lines), encoding='utf-8')
    heading = '## V721: current whole-scope graphics matrix and exact patch audit'
    summary = ('Root audit pointers now identify V712,with prior V610 metadata retained. Fresh921 format/palette/'
        'extent and57 embedded extent checks pass;675 complete PXL/FLS files equal V692. Current470/114 '
        'registry/manifest integration matches; decoding the existing clean patch reconstructs every V712 '
        'byte. A new matrix retains all22 historical requirements,all26 original confirmed entries,the '
        'four Online exclusions and12 completed scoped evidence hashes. Treasure Name,slackimg12,'
        'Press a button and Iseki/dock need explicit native-evidence reconciliation,not automatic retesting '
        'or a new-defect claim. Unidentified control/card/comic/legacy contexts and final verification '
        'remain open; all18 original objects incomplete and22 original objects exact. No ROM/art/patch/'
        'registry/canonical change or new gameplay/guide claim. Goal active; older-record follow-up retained. '
        'See [current audit](graphics_current_audit_v721.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    path = Path('docs/graphics_remaining_work.md')
    text = path.read_text(encoding='utf-8')
    text += ('\n## Current requirement matrix\n\n'
        'V721 reconciles all22 historical requirements and the original26 confirmed entries against V712. '
        'See [current audit](graphics_current_audit_v721.md) and '
        '`translations/graphics_current_requirements_v1.json`. Four original resources need explicit '
        'native-evidence linkage: Treasure Name,slackimg12,Press a button,and Iseki/dock. Existing testing '
        'must be checked before selecting a new run; these are not newly declared graphics defects.\n')
    path.write_text(text, encoding='utf-8')
    for path in (MATRIX, DOC, Path(__file__), preservation_path, ROOT / 'previous_root_metadata.json'):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'exact_reconstruction_external_ROM': {'path': str(restored), 'sha256': digest,
            'research_only_not_a_new_release': True}, 'full_goal_complete': False})
    for path, digest in release_hashes.items():
        assert sha(Path(path).read_bytes()) == digest
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V721: current V712 root pointers,22 historical requirements,26 source entries,921/57 preservation,470/114 layers and exact patch verified; goal remains incomplete.', flush=True)


if __name__ == '__main__':
    main()
