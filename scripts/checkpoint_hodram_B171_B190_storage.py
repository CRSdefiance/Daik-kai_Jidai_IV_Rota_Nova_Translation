"""Save exact stored references and passing reconstruction/loader evidence without credit."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_editorial_progress_checkpoint_v1 import checkpoint

ROOT = Path('work/analysis/Hodram_B171_B190_storage_checked_20261104')
INPUT = Path('work/analysis/Hodram_B171_B190_storage_inputs_20261104')
REBUILT = Path('work/analysis/Hodram_B171_B190_rebuilt_20261104/reconstruction.json')
STORED = Path('work/analysis/Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json')
LOADERS = Path('work/analysis/Hodram_B171_B190_loaders_20261104/verification.json')
DIAGNOSTIC = Path('work/analysis/Hodram_B171_B190_stored_FE_diagnostic_20261104/diagnostic.json')
SUMMARY = ('B171–B190: 435 contextual decisions (195 revisions/240 retentions), 49 scoped name/term retentions and all 15 layout corrections preserved. '
    '433 stored speeches/439 viewed native pages, both menu captions, 390 relative cases and 325 archive loads pass. '
    'One owned terminal alignment-space/zero-ink flush row is narrowly qualified with identical visible pixels. '
    'Representative English gameplay and registered integration remain. No credit or playable candidate added; 9498 complete, experimental 7774721f/main unchanged. '
    'Full scope/all ROMs/evidence preserved; no guide photos.')


if __name__ == '__main__':
    assert not ROOT.exists()
    doc, rebuilt, stored, loaders, diagnostic = map(load, [INPUT / 'storage_manuscript.json', REBUILT, STORED, LOADERS, DIAGNOSTIC])
    assert rebuilt['manuscript_sha256'] == sha((INPUT / 'storage_manuscript.json').read_bytes())
    assert stored['reconstruction_sha256'] == loaders['reconstruction_sha256'] == sha(REBUILT.read_bytes())
    assert len(stored['records']) == 433 and stored['complete_stored_pages'] == 439
    assert stored['typed_labels_checked'] == 2 and not stored['style_records']
    assert stored['fresh_relocated_native_relative_cases'] == 390
    assert stored['fresh_parity_dependent_pages'] == 232 and stored['exact_compiled_pages_reused'] == 207
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (325, 40, 610)
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and rebuilt['all_other_files_components_exact']
    assert rebuilt['command_count'] == 636 and rebuilt['relative_sites'] == 78 and len(rebuilt['groups']) == 20
    assert all(r['complete_visible_rows_match'] and r['complete_plane_equal'] for r in diagnostic['records'])
    qualified = [r for r in stored['records'] if r['complete_stored_native_display'].get('planned_native_row_comparison', {}).get('exact_owned_terminal_alignment_space_andzeroink_flush_row_qualified')]
    assert len(qualified) == 1 and qualified[0]['id'] == 'DK4_MES_B179_R0047'
    blocks = IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    speech = {r['id']: r for r in stored['records']}
    choices = {r['id']: (obj, r) for obj in stored['typed_objects'] for r in obj['label_references']}
    bindings = []
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            obj, item = choices[row['id']]
            at = item['offset']
            raw = bytes.fromhex(item['stored_hex'])
            reference = dict(command_offset=obj['offset'], source_index=row['source_index'], record_index=item['record_index'])
        else:
            item = speech[row['id']]
            at = item['new_offset']
            raw = bytes.fromhex(item['stored_hex'])
            assert blocks[row['block']][at - 5:at + 1].hex() == row['source_complete_preamble_hex']
            reference = dict(record_index=item['new_record_index'], complete_source_preamble_hex=row['source_complete_preamble_hex'])
        assert blocks[row['block']][at:at + len(raw) + 1] == raw + b'\0'
        bindings.append(dict(id=row['id'], decision=row['decision'], source_reference=row['source_reference'],
            current_reference=row['current_reference'], finding=row['finding'], review=row['review'],
            stored_research_reference=dict(file_path=row['file_path'], block=row['block'], offset=at, bytes=len(raw),
                exact_stored_hex=raw.hex(), target_archive_sha256=rebuilt['target_archive_sha256'], **reference),
            registered_release_gameplay_andcredit_pending=True))
    assert len(bindings) == 435 and all(not r['review']['formatting'] for r in bindings)
    ROOT.mkdir()
    binding_path = ROOT / 'stored_record_bindings_v1.json'
    save(binding_path, dict(records=bindings, source_current_andstored_exact_individual_references=True,
        research_ROM=rebuilt['research_ROM'], research_ROM_sha256=rebuilt['research_ROM_sha256'],
        complete_source_controls_command_maps_allocation_andrelatives_checked=True,
        no_completion_credit=True, registered_release_andrepresentative_gameplay_pending=True,
        evidence={str(p): sha(p.read_bytes()) for p in [INPUT / 'storage_manuscript.json', REBUILT, STORED, LOADERS]}))
    checkpoint_path = ROOT / 'checkpoint.json'
    save(checkpoint_path, dict(prose_reviews=435, proposed_revisions=195, justified_retentions=240,
        scoped_name_andterm_retentions=49, final_native_andviewed_pages=439, layout_corrections=15,
        stored_speech_records=433, typed_captions=2, physical_menus=1, native_relative_cases=390,
        fresh_parity_pages=232, exact_compiled_pages_reused=207, native_archive_loads=325,
        fresh_parent_cases=40, exact_reused_parent_cases=610, source_target_commands=636,
        exact_whole_block_archive_serialized_NDS_inverses=True, research_ROM=rebuilt['research_ROM'], research_ROM_sha256=rebuilt['research_ROM_sha256'],
        owned_terminal_space_andzeroink_flush_case='DK4_MES_B179_R0047', all_visible_rows_andcomplete_planes_exact=True,
        jobs=[dict(session=96954, terminal=True, exit_code=0), dict(session=19698, terminal=True, exit_code=1,
            failure_resolved_by_exact_terminal_space_qualification=True), dict(session=39015, terminal=True, exit_code=0)],
        actual_new_batch_gameplay=False, representative_gameplay_andregistered_release_pending=True,
        all_individual_fifth_gates_still_false=True, new_credit=0, full_goal_complete=False, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [REBUILT, STORED, LOADERS, DIAGNOSTIC, binding_path, Path(__file__)]}))
    text = '''# Hodram B171–B190: complete stored reconstruction passes

The complete prose/display checkpoint is preserved: 435 contextual comparisons (195 proposed revisions/240 justified retentions), 49 scoped name/term retentions, 433 native speeches/439 visually approved final pages and 15 layout corrections. Do not repeat those source, prose or display reviews. Both captions and all 31 scoped name strings remain native/visually checked.

All twenty complete SC1 blocks are reconstructed with exact clean/current command maps: 636 commands, 78 relocated relative sites and one native two-choice object. Full block, archive and serialized NDS inverses pass. Every other ROM file and component matches the registered experimental parent, including fonts, graphics and all existing runtime/name/static layers and ASCII right bounds. The pinned research ROM is `work/analysis/Hodram_B171_B190_rebuilt_20261104/reviewed_RESEARCH_ONLY.nds`, SHA256 `d14c24ba6aefd312099970423b8e1a9611a5913bc85f87feeb70fae00b0fe19a`. It is a research input, not a registered playable handoff.

Stored checks cover all 433 speeches/439 pages and both captions, with exact source/current/stored per-record references. 232 parity-dependent pages receive fresh native checks; 207 identical compiled pages reuse their exact proofs. All stored planes match the directly viewed pages. Complete leading/internal/trailing characters, speaker preambles, macro expansions, native bounds, canaries, consumption, allocation and pagination pass. All 390 native relative cases pass. All 325 native archive loads/cache hits pass; 40 changed-block handoffs are fresh and 610 exact parent cases are reused after checking the executed instructions against the current runtime.

The first stored job, session 19698, is terminal/exit 1. It exposed a strict row-membership edge case at B179 R47 after the rebuilder added its owned terminal alignment space. Native diagnosis shows exactly two extra style-15 ASCII-space events at x0/x6,y24: the alignment space and zero-ink pair flush. Every visible row and the complete pixel plane are identical to the reviewed two-row page. All stored FE bodies with such alignment were checked; only this one has an extra blank event row. The scoped successor qualifies this exact expanded byte string, exact event list, exact source alignment flag, diagnostic hash and complete plane hash. Every other FE record still uses the original strict row checker. No prose, compiled layout, ROM or glyph was changed to resolve it; it adds no sixteenth wrap correction. The successor also writes each completed block proof, allowing future partial-run reuse if needed.

Session 39015 completed all twenty stored blocks, exit 0. Research reconstruction session 96954 also exited 0. All jobs are terminal. The generic loader check completed successfully. No process should be restarted on the basis of the older failure. The completed storage proofs are:

- `work/analysis/Hodram_B171_B190_rebuilt_20261104/reconstruction.json`.
- `work/analysis/Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json`, plus twenty individual block proofs.
- `work/analysis/Hodram_B171_B190_loaders_20261104/verification.json`.
- `work/analysis/Hodram_B171_B190_stored_FE_diagnostic_20261104/diagnostic.json`.
- `work/analysis/Hodram_B171_B190_storage_checked_20261104/stored_record_bindings_v1.json` and `checkpoint.json`.

These are offline checks. Representative English gameplay is still required before final fifth gates and registered integration. Focus next on the B171 sail-lesson menu's two selections/branches, the newly generated page-boundary behavior, speaker/portrait transitions, the B179 FE behavior and broad town-scene samples. Reuse completed native/visual and archive proofs; exact conditional visits or a full natural playthrough are unnecessary. Any initialized content fixture must disclose excluded conditions, retained effects, synthetic ordering and unvisited content. No new gameplay or guide-photo run is claimed for this batch.

After necessary gameplay checks pass, close the individual fifth gates, register the complete scene through a generic two-choice-compatible successor to the existing mixed-scene workflow, and build through `scripts/build_integrated_release_with_static_text.py` with every accepted and experimental parent layer preserved. The B156-specific cinematic module is not this batch's template. Produce the exact clean-input patch, full manifest and candidate-own startup proof before once-only completion credit. Main promotion still requires user acceptance.

Coverage remains 9498 completed: 5809 revisions/3689 retentions. Historical source/prose/draft counters remain 9501; these 435 records are not credited yet. Registered experimental SHA256 `7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399` and main SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` are unchanged. No promotion, commit/push, pruning or guide photos. Preserve all ROMs, translations, retentions and evidence. Full editorial scope remains active across every storyline, earlier dialogue, shared shop/town exchange, random scene and remaining player-facing prose. Graphics artwork and the later older-record technical re-audit remain separate.
'''
    protected = {'translations/release_stack.json': '7e7288fe7920fb601ab96a6bde937793c2c9873dd6a9573be796853d7924d143',
        'out/all_routes_combined_hodram_b151_b170_static_text_20261102_candidate.nds': '7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        rebuilt['research_ROM']: rebuilt['research_ROM_sha256']}
    checkpoint(mutation=ROOT / 'ledger_mutation_v1', batch_key='Hodram_B171_B190_clean_next_20261102',
        batch_updates=dict(stored_reconstruction_andnative_checks_pass=True, source_target_commands=636,
            fresh_relocated_native_relative_cases=390, native_archive_loads=325, fresh_parent_cases=40, exact_reused_parent_cases=610,
            fresh_parity_dependent_pages=232, exact_compiled_pages_reused=207, stored_speeches=433, stored_captions=2,
            research_ROM=rebuilt['research_ROM'], research_ROM_sha256=rebuilt['research_ROM_sha256'],
            stored_record_bindings=str(binding_path), stored_record_bindings_sha256=sha(binding_path.read_bytes()),
            storage_checkpoint=str(checkpoint_path), storage_checkpoint_sha256=sha(checkpoint_path.read_bytes()),
            stored_reconstruction_gameplay_andregistered_release_pending=False, representative_gameplay_andregistered_release_pending=True,
            all_individual_fifth_gates_still_false=True, actual_new_batch_gameplay=False, no_live_job=True,
            new_credit=0, full_goal_complete=False, guide_photos=False), summary=SUMMARY,
        document='docs/editorial_hodram_B171_B190_storage_20261104.md', document_text=text, completed=9498, protected=protected)
    print('Saved 435 exact stored bindings; all 439 pages, 390 relative cases and 325 loads pass. Gameplay and registered release remain; no credit added.')
