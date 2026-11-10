"""Persist exact stored references and completed storage/name work without credit."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_editorial_progress_checkpoint_v1 import checkpoint

ROOT = Path('work/analysis/Hodram_B191_B210_storage_checked_20261104')
INPUT = Path('work/analysis/Hodram_B191_B210_storage_inputs_20261104')
REBUILT = Path('work/analysis/Hodram_B191_B210_rebuilt_20261104/reconstruction.json')
STORED = Path('work/analysis/Hodram_B191_B210_stored_20261104/stored_native_verification.json')
LOADERS = Path('work/analysis/Hodram_B191_B210_loaders_20261104/verification.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, rebuilt, stored, loaders = map(load, [INPUT / 'storage_manuscript.json', REBUILT, STORED, LOADERS])
    assert rebuilt['manuscript_sha256'] == sha((INPUT / 'storage_manuscript.json').read_bytes())
    assert stored['reconstruction_sha256'] == loaders['reconstruction_sha256'] == sha(REBUILT.read_bytes())
    assert len(stored['records']) == 352 and stored['complete_stored_pages'] == 355
    assert stored['typed_labels_checked'] == 21 and not stored['style_records']
    assert stored['fresh_relocated_native_relative_cases'] == 540
    assert (stored['fresh_parity_dependent_pages'], stored['exact_compiled_pages_reused']) == (175, 180)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (325, 40, 610)
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and rebuilt['all_other_files_components_exact']
    assert rebuilt['command_count'] == 644 and rebuilt['relative_sites'] == 108 and len(rebuilt['groups']) == 20
    blocks = IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    speeches = {r['id']: r for r in stored['records']}
    captions = {r['id']: (obj, r) for obj in stored['typed_objects'] for r in obj['label_references']}
    bindings = []
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            obj, item = captions[row['id']]
            at = item['offset']
            ref = dict(command_offset=obj['offset'], source_index=row['source_index'], record_index=item['record_index'],
                native_command_word=int.from_bytes(bytes.fromhex(row['source_choice_object_hex'])[:2], 'little'))
        else:
            item = speeches[row['id']]
            at = item['new_offset']
            assert blocks[row['block']][at - 5:at + 1].hex() == row['source_complete_preamble_hex']
            ref = dict(record_index=item['new_record_index'], complete_source_preamble_hex=row['source_complete_preamble_hex'])
        raw = bytes.fromhex(item['stored_hex'])
        assert blocks[row['block']][at:at + len(raw) + 1] == raw + b'\0'
        bindings.append(dict(id=row['id'], decision=row['decision'], source_reference=row['source_reference'],
            current_reference=row['current_reference'], finding=row['finding'], review=row['review'],
            stored_research_reference=dict(file_path=row['file_path'], block=row['block'], offset=at, bytes=len(raw),
                exact_stored_hex=raw.hex(), target_archive_sha256=rebuilt['target_archive_sha256'], **ref),
            registered_release_gameplay_andcredit_pending=True))
    assert len(bindings) == 373 and all(not r['review']['formatting'] for r in bindings)
    ROOT.mkdir()
    binding_path = ROOT / 'stored_record_bindings_v1.json'
    save(binding_path, dict(records=bindings, source_current_andstored_exact_individual_references=True,
        research_ROM=rebuilt['research_ROM'], research_ROM_sha256=rebuilt['research_ROM_sha256'],
        complete_source_controls_command_maps_allocation_andrelatives_checked=True,
        no_completion_credit=True, registered_release_andrepresentative_gameplay_pending=True,
        evidence={str(p): sha(p.read_bytes()) for p in [INPUT / 'storage_manuscript.json', REBUILT, STORED, LOADERS]}))
    summary = ('B191–B210: 373 contextual comparisons/154 proposed revisions/219 justified retentions and70 scoped name/term retentions preserved. '
        'All355 speech pages,21 captions and36 name strings pass native/visual checks. Stored reconstruction,540 relative cases and325 archive loads pass;all unowned files/components exact. '
        'Six initialized English fixture runs are in progress or awaiting analysis;no gameplay pass claimed yet. Registered integration remains. '
        '9933 completions,experimental d14c24ba/main unchanged. Full scope/all evidence preserved;no guide photos.')
    document = '''# Hodram B191–B210: stored reconstruction and names checked

The [complete prose/display checkpoint](editorial_hodram_B191_B210_prose_display_20261104.md) remains valid: 373 individual comparisons (154 proposed revisions,219 justified retentions),70 scoped name/term retentions,355 final speech pages,21 captions andfour layout corrections. Reuse those completed checks.

All43 actors/86 name consumers are bound to36 complete native strings:7 fresh planes and29 exact compatible reuses. Allthree name sheets were directly viewed. No name table changed. Full-name literal proofs do not establish actual catalogue layout or global207-name approval.

Twenty complete SC1 blocks are reconstructed:644 commands,108 relative sites andten mixed two/three-choice objects. All373 exact source/current/stored references are in `work/analysis/Hodram_B191_B210_storage_checked_20261104/stored_record_bindings_v1.json`. Full clean/current block,archive andserialized NDS inverses pass. Other files/components match registered d14c24ba,including all runtime/name/static stages andASCII right bounds.

All352 stored speeches/355 pages and21 captions pass complete leading/internal/trailing glyph,control,substitution,consumption,bounds,canary,allocation andpagination checks.175 parity-dependent pages were checked fresh;180 identical compiled planes were reused. Allstored planes equal the directly viewed pages. Strict FE row checking passes without a terminal-row exception. All540 relocated relative cases pass.325 native archive loads/cache hits pass,with40 fresh handoffs and610 exact parent reuses.

Primary evidence: `work/analysis/Hodram_B191_B210_rebuilt_20261104/reconstruction.json`, `work/analysis/Hodram_B191_B210_stored_20261104/stored_native_verification.json`, `work/analysis/Hodram_B191_B210_loaders_20261104/verification.json` and `work/analysis/Hodram_B191_B210_storage_inputs_20261104/scoped_name_visual_approval.json`.

Pinned research ROM: `work/analysis/Hodram_B191_B210_rebuilt_20261104/reviewed_RESEARCH_ONLY.nds`,SHA256 `88e9984f767a0fa14bde5e9ce07392d1fbcf44fb41a6815e4ca466740fb82a15`. It is not a registered testing handoff. Reconstruction session47725 andstored session57420 exited0;the loader check passed. Fixture preparation is complete;do not restart it because an old tool handle expired.

Next analyze six initialized English content coldboots: nine town exchanges,book default/delegate choices,castle letter,parrot andearrings. Preserve the actual run receipts anddisclose excluded activation/market conditions,unvisited branches andoriginal locations. These headless QA captures are not guide photos orfull natural playthroughs. Close individual formatting gates only after necessary focused tests pass,then register the cumulative release,verify its exact clean patch andown startup,andcredit373 once. No main promotion.

Coverage remains9933 completed (6004 revisions/3929 retentions);historical source/prose/draft counters9936. This batch haszero completion credit. AllROMs,translations,retentions andevidence remain preserved. Every route/shared/town/random/player-facing text stays in scope,including unfinished contextual passes ofearlier translations. Deferred graphics artwork andthe later older-record technical re-audit remain separate. No guide photos,pruning,commit/push ormain promotion.
'''
    protected = {'translations/release_stack.json': sha(Path('translations/release_stack.json').read_bytes()),
        rebuilt['parent']: rebuilt['parent_sha256'], rebuilt['research_ROM']: rebuilt['research_ROM_sha256'],
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'}
    checkpoint(mutation=ROOT / 'ledger_mutation_v1', batch_key='Hodram_B191_B210_clean_next_20261104',
        batch_updates=dict(stored_reconstruction_andnative_checks_pass=True, source_target_commands=644,
            fresh_relocated_native_relative_cases=540, native_archive_loads=325, fresh_parent_cases=40, exact_reused_parent_cases=610,
            fresh_parity_dependent_pages=175, exact_compiled_pages_reused=180, stored_speeches=352, stored_captions=21,
            research_ROM=rebuilt['research_ROM'], research_ROM_sha256=rebuilt['research_ROM_sha256'],
            stored_record_bindings=str(binding_path), stored_record_bindings_sha256=sha(binding_path.read_bytes()),
            scoped_name_visual=str(INPUT / 'scoped_name_visual_approval.json'), actual_analysis_andrelease_pending=True,
            all_fifth_formatting_gates_pending=True, new_credit=0), summary=summary,
        document='docs/editorial_hodram_B191_B210_storage_20261104.md', document_text=document, completed=9933, protected=protected)
    print('373 exact source/current/stored bindings saved; storage/name checkpoint saved without credit.')
