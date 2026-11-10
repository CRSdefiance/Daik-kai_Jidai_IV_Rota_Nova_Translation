"""Save disjoint remaining SC1 scope; source inventory adds no review credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

ROOT = Path('work/Hodram_B0_B41_clean_20261107')
AUDIT = Path('work/Hodram_source_coverage_20261107_v1/coverage.json')
RELEASE = Path('work/hodram_B311_B324_release_v1/registered_release_verification.json')
REGISTRY = Path('translations/release_stack.json')
BATCH = 'Hodram_SC1_B0_B41_clean_next_20261107'


def main():
    packet, styles, menus, reconciliation, ledger, release, package = map(load, (
        ROOT/'clean_source_packet.json', ROOT/'clean_style_objects.json', ROOT/'clean_choice_objects.json',
        ROOT/'coverage_reconciliation_v1.json', Path('translations/editorial_review_current_v1.json'), RELEASE, PACKAGE))
    assert ledger['records_editorially_completed'] == 18767 and not ledger['full_goal_complete']
    assert reconciliation['source_objects'] == 5356 and reconciliation['exact_credited_objects'] == 4962
    assert reconciliation['missing_objects'] == 394 and reconciliation['all_prior_integrated_archive_keys_exactly_matched']
    assert not any(reconciliation[k] for k in ('duplicate_orambiguous_bindings','source_binding_failures','inventory_failures'))
    rows = [r for g in packet['groups'] for r in g['records']]+styles['records']+menus['records']
    keys = {(r['file_path'], r['id']) for r in rows}
    known = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    assert len(rows) == len(keys) == 394 and not keys & known
    assert packet['records'] == 341 and len(packet['groups']) == 39
    assert (styles['object_count'], styles['physical_alternatives'], styles['style_alias_slots']) == (7,47,56)
    assert (menus['object_count'], menus['caption_count']) == (3,6)
    scope = ROOT/'clean_intake_scope_v1.json'
    assert not scope.exists()
    evidence = {str(p):digest(p) for p in (AUDIT,ROOT/'coverage_reconciliation_v1.json',ROOT/'clean_source_packet.json',
        ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json',Path(__file__))}
    save(scope,dict(total_editorial_objects=394, ordinary_speeches=341, physical_personality_alternatives=47,
        physical_style_objects=7, personality_alias_slots=56, typed_caption_records=6, typed_choice_objects=3,
        reviewed_block_numbers=[g['block'] for g in packet['groups']], all18767_completed_keys_checked=True,
        all4962_credited_SC1_source_positions_andbytes_exact=True, source_key_overlap_with_completed_credit=0,
        source_meanings_saved=0, localized_drafts_saved=0, current_English_comparisons=0,
        source_meanings_pending=True, localized_drafts_pending=True, all_five_review_gates_pending=True,
        scoped_names_pending=True, fresh_native_body_pages_pending=True, stored_reconstruction_pending=True,
        representative_gameplay_pending=True, registered_integration_pending=True,
        no_eligible_current_English_extracted=True, numerical_blocks_not_event_chronology=True,
        complete_native_inventory_reused_not_rerun=True, evidence=evidence, new_credit=0, full_goal_complete=False))
    summary = ('Hodram B311–B324 remains registered; integrated coverage is 18,767. '
        'The full SC1 source-object census now binds all 4,962 credited objects exactly and identifies 394 unreviewed objects '
        'across 39 complete B0–B41 exchanges: 341 speeches, 47 physical voice alternatives and six captions. '
        'No inventory or legacy source-binding errors remain. The next clean-source scope is prepared; meanings, drafts, '
        'comparisons and all five gates remain. No new review credit or ROM; main is unchanged.')
    document = f'''# Remaining Hodram source scope

{summary}

The [native clean-source census](../{AUDIT.as_posix()}) accounts for all 325 SC1 blocks: 4,556 ordinary speeches, 681 physical style alternatives and 119 typed menu captions, totaling 5,356 source objects. All 4,962 integrated SC1 keys match unique clean positions and bytes. There are no unmatched credited keys, ambiguous matches, legacy source-reference failures or native inventory failures. Exact source matching preserves older alternate identifiers and prevents duplicate review. This is dialogue-object coverage, not a full player-facing resource or event-reachability census.

The [qualified residual scope](../{scope.as_posix()}) contains 394 wholly uncredited objects in 39 complete source blocks. Seven style commands retain all 56 alias slots; three menus contain six captions. Six label-free controls remain separate. [Packet](../{ROOT.as_posix()}/clean_source_packet.json), [styles](../{ROOT.as_posix()}/clean_style_objects.json), [menus](../{ROOT.as_posix()}/clean_choice_objects.json), [coverage reconciliation](../{ROOT.as_posix()}/coverage_reconciliation_v1.json). Existing native inventories are reused with exact whole-command bytes; no display, gameplay or localization approval is inferred. No eligible existing English was extracted. Block numbers do not establish early-game timing or consecutive event chronology.

Next read each complete clean exchange and necessary linked context, save individual meanings, then natural logical drafts before current-English comparison. Preserve good wording when compared and document why. All scoped name decisions, formatting/visual/stored checks and representative gameplay remain. The [registered B311–B324 checkpoint](editorial_Hodram_B311_B324_registered_20261107.md) remains the current cumulative candidate; do not repeat its completed checks or add its credit again.

The goal is active. Every remaining route, unfinished earlier contextual pass, shared town/shop/random exchange, speaker label and remaining player-facing prose stays in scope, with Rafael/tutorial priority. Preserve all existing evidence and ROMs. No main promotion or guide photos; artwork and the later older-record technical re-audit remain separate.
'''
    checkpoint(mutation=ROOT/'source_scope_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Hodram residual B0–B41: 394 disjoint clean-source objects.',
            next_action='Read complete clean exchanges; seal 394 source meanings and logical drafts before eligible current-English extraction. Then contextual comparison and fresh display gates.',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True,
            registered_integration_pending=True, native_job_live=False, registered_build_live=False,
            registered_cumulative_build_live=False, guide_photos=False),
        new_entries={BATCH:{**load(scope),'source_scope':str(scope),'source_scope_sha256':digest(scope)}},
        summary=summary, document='docs/editorial_Hodram_B0_B41_source_scope_20261107.md', document_text=document,
        completed=18767, protected={str(REGISTRY):release['registry_sha256'], release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'], release['patch']:release['patch_sha256'],
            package['zip']:package['zip_sha256']})
    print('Saved source-only next scope: 394 disjoint objects; integrated total 18,767; full goal active.')


if __name__ == '__main__':
    main()
