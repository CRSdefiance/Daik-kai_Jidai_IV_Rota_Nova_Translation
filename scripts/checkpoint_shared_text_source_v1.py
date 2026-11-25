"""Record the shared-text source and comparison checkpoint without release credit."""

from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
RELEASE = Path('work/lil261_B323_B335_release_v1/registered_release_verification.json')
DOCUMENT = Path('docs/editorial_shared_text_source_20261110.md')


def main():
    release = load(RELEASE)
    compared = load(ROOT / 'contextual_comparison_pending_consumers.json')
    native = load(ROOT / 'ship_command_native_descriptor.json')
    inventory = load(ROOT / 'remaining_COMMON_source_summary.json')
    assert compared['counts'] == {'retention-candidate': 30, 'revision-candidate': 16, 'source-mismatch': 8}
    assert len(compared['records']) == 54 and len(native['cases']) == 9
    assert inventory['remaining_native_COMMON_keys'] == 2068
    assert inventory['initial_clean_source_drafts'] + inventory['supplementary_clean_source_drafts'] == 57
    assert native['runtime']['candidate_sha256'] == compared['candidate_sha256'] == release['candidate_sha256']
    assert native['modal_UI_creation_at_02051FC0_is_an_explicit_unexecuted_boundary']
    assert digest('translations/release_stack.json') == release['registry_sha256']
    paths = sorted(p for p in ROOT.iterdir() if p.is_file())
    paths += [Path('scripts/seal_shared_text_source_v1.py'), Path('scripts/compare_shared_text_source_v1.py'),
        Path('scripts/check_ship_command_descriptor_v1.py'), Path('scripts/inventory_remaining_COMMON_source_v1.py')]
    evidence = {str(p): digest(p) for p in paths}
    summary = ('The four native story censuses cover all 24,092 dialogue, choice and personality positions. '
        'The next shared-text packet has 57 clean-source drafts, 54 current comparisons and one raw ship command. '
        'Thirty comparisons are retention candidates, 16 propose revisions and eight identify source mismatches. '
        'Consumer, display and release approval remain. Lil261 stays the registered candidate with 25,898 credited reviews.')
    notes = f"""# Shared messages and ship command source checkpoint

{summary}

The source packet contains 54 clean-first drafts across notices, setup prompts, storage branches, fleet commands and three Market replies. Current English was extracted after those drafts were sealed. Each comparison carries exact source and current bytes, native message references and an individual finding. Three supplementary drafts preserve the level-up notice and two punctuation-only reactions. [Source packet](../{ROOT.as_posix()}/clean_source_packet.json) · [Comparisons](../{ROOT.as_posix()}/contextual_comparison_pending_consumers.json)

Concrete current findings include a full-width initial I in COMMON95, a fragmented pirate-attack notice in COMMON94, a shortened retail-sign tutorial in COMMON136, unrelated square or save text in COMMON104–107 and COMMON113–114, and a save-warning sentence split across COMMON121–122. These are stored-content findings. The active DS screens and the legacy memory-card/controller branches need independent caller classification before storage changes. The existing captain chooser can use a separate description source. Source order supplies context leads and does not establish a single conversation.

The raw Japanese command 船を捨てる remains at ARM9 offset `0x134E54` with its sole aligned static pointer at `0x1150B4`. The source and registered caller load the same table at `0x021150B0` and call the unchanged descriptor helper at `0x02051E7C`. Nine offline helper cases and its zero-count branch pass the complete saved-register, stack and return checks. Original modal creation at `0x02051FC0` is an explicit unexecuted boundary. The proposed Abandon Ship label still needs storage allocation, font/bounds/cursor review, representative actual display, transitions and registered integration. These calls add no gameplay credit. [Native descriptor evidence](../{ROOT.as_posix()}/ship_command_native_descriptor.json)

The clean native COMMON catalogue has 3,668 keys. Of these, 1,600 have individual contextual completion credit and 2,068 remain for classification and review. Japanese-character detection finds 2,065 leads. The other three keys 97, 469 and 2196 remain in scope, with source-first drafts preserved. This source-key count includes platform-specific branches and supplies no full-ROM prose denominator. [Complete remaining source catalogue](../{ROOT.as_posix()}/remaining_COMMON_source_catalog.json.gz) · [Inventory summary](../{ROOT.as_posix()}/remaining_COMMON_source_summary.json)

The four existing story censuses have zero missing positions, inventory failures or legacy binding failures. Their individual record counts of 6,887, 5,356, 6,720 and 5,129 are bound by exact hashes in the comparison packet. Reuse these completed inventories and editorial proofs. Current work continues shared shop/town/random dialogue, remaining player-facing prose, broader names and roles, and earlier wrap/glyph leads. Deferred graphics artwork and the later older-record technical re-audit remain separate.

The preceding goal turn was progress. Lil261 was registered, packaged, credited once and pushed as `91a08be3`, with the remote branch and clean worktree verified. This turn adds source drafts, individual comparisons, the exact remaining COMMON catalogue and scoped native evidence. No new completion credit or ROM revision is claimed. Main V4701 awaits acceptance. Next bind the distinct COMMON consumers and original ship-menu display, finalize the appropriate exchanges, format and visually check every changed page, then integrate after the necessary checks.
"""
    checkpoint(mutation=Path('work/SharedText_20261110_v1/source_checkpoint'),
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(current_batch='Shared early-game notices, setup, fleet prompts and ship command',
            new_credit=0, current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence,
            no_batch_worker_live=True, guide_photos=False, previous_goal_turn_classification='progress',
            current_goal_turn_classification='progress',
            next_action='Bind COMMON consumers and the ship-menu display, then finalize full-context prose and fresh formatting.'),
        new_entries={
            'SharedText_20261110_v1': dict(new_credit=0, source_first_COMMON_drafts=57, current_COMMON_comparisons=54,
                raw_ship_command_drafts=1, retention_candidates=30, revision_candidates=16, stored_source_mismatches=8,
                all_consumer_anddisplay_gates_pending=True, original_ship_descriptor_native_cases=9,
                zero_count_branch_pass=True, no_new_gameplay_claim=True, registered_integration_pending=True,
                evidence=evidence),
            'editorial_scope_20261110_allroutes_COMMON_v1': dict(new_credit=0,
                complete_native_story_source_positions=24092, native_story_source_positions_remaining=0,
                per_route_native_source_counts=[6887,5356,6720,5129],
                native_COMMON_keys=3668, completed_COMMON_contextual_keys=1600, remaining_COMMON_native_keys=2068,
                actual_player_facing_andplatform_reachability_classification_pending=True,
                broader_UI_ARM9_names_items_retrospective_wraps_andother_resources_still_in_scope=True,
                full_goal_complete=False, evidence=evidence)},
        coverage_unit_updates={key: dict(status='in-progress', active_batch='SharedText_20261110_v1',
            progress_evidence=str(ROOT / 'remaining_COMMON_source_summary.json'),
            progress_evidence_sha256=digest(ROOT / 'remaining_COMMON_source_summary.json'))
            for key in ['shared-shop-town-dialogue', 'remaining-shared-dialogue', 'help-and-other-player-facing-prose']},
        summary=summary, document=DOCUMENT, document_text=notes, completed=25898,
        protected={'translations/release_stack.json': release['registry_sha256'],
            'translations/promoted_build.json': digest('translations/promoted_build.json'),
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            release['manifest']: release['manifest_sha256']})
    print('Saved the shared-text checkpoint. No ROM or completion credit changed.')


if __name__ == '__main__':
    main()
