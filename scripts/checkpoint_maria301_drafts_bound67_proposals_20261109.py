"""Save substantial Maria editorial progress with exact release protection andzero credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint


def main():
    root = Path('work/Maria_B0_B32_clean_20261109')
    drafts_path = root / 'all301_clean_meanings_andindependent_drafts_v1.json'
    current_path = root / 'current_v1/current_effective.json'
    objects_path = root / 'current_objects_v1/current_objects.json'
    proposals_path = root / 'contextual_proposals_B0_B10_v1.json'
    runtime_path = Path('work/Maria_current_context_20261109_v1/runtime_context_qualification.json')
    drafts, current, objects, proposals, runtime = map(load,
        [drafts_path, current_path, objects_path, proposals_path, runtime_path])
    assert drafts['records_count'] == 301 and len(drafts['records']) == 301
    ordinary = [r for g in current['groups'] for r in g['records']]
    bound_rows = ordinary + objects['style_records'] + objects['choice_records']
    bound = {r['id']: r for r in bound_rows}
    assert len(ordinary) == 292 and len(objects['style_records']) == 7 and len(objects['choice_records']) == 2
    assert len(bound) == len(bound_rows) == 301 and objects['native_style_getter_cases'] == 8
    assert current['runtime'] == objects['runtime'] == runtime['runtime']
    assert runtime['actual_captain_getter'] == 3 and current['all_source_preambles_andcommand_kinds_preserved']
    for row in drafts['records']:
        prior = bound[row['id']]
        assert row['source_hex'] == prior['source_hex'] and row['source_reference'] == prior['source_reference']
        assert prior['current_English_now_exposed'] and not any(row['review'].values())
    assert proposals['records_count'] == len(proposals['records']) == 67
    assert (proposals['revised'], proposals['retained']) == (46, 21)
    assert len({r['id'] for r in proposals['records']}) == 67
    for row in proposals['records']:
        prior = bound[row['id']]
        assert row['source_hex'] == prior['source_hex'] and row['current_reference'] == prior['current_reference']
        assert row['current_effective_hex'] == prior['current_effective_hex'] and row['finding']
        assert row['contextual_comparison_saved'] and not any(row['review'].values())
        assert row['no_proposal_may_ship_orreceive_completion_credit_yet']
    release_path = Path('work/hodram_residual_release_v1/registered_release_verification.json')
    release = load(release_path)
    assert current['current_ROM_sha256'] == proposals['current_ROM_sha256'] == release['candidate_sha256']
    qualification = root / 'drafts301_bound301_proposals67_qualification_v1.json'
    assert not qualification.exists()
    evidence = {str(p): digest(p) for p in [drafts_path, current_path, objects_path, proposals_path,
        runtime_path, root / 'all301_clean_draft_qualification_v1.json', release_path, Path(__file__)]}
    captures = [Path(f'work/Maria_current_context_20261109_v1/capture/frame_{n:06d}_cold_boot.png')
        for n in [4000, 16000, 31000]]
    save(qualification, dict(source_meanings=301, independent_drafts=301,
        current_native_bindings=301, original_ordinary_catalogue_lookups=292,
        physical_style_alternatives=7, native_style_getter_cases=8, menu_captions=2,
        complete_source_current_command_andpreamble_membership_exact=True,
        contextual_comparisons=67, proposed_revisions=46, justified_retentions=21,
        remaining_current_comparisons=234, all_five_gates_pending=True,
        source_reread_draft_refinements=4, integrated_completed=19161,
        current_Maria_context=runtime['runtime'], context_coldboot_frames=31000,
        directly_viewed_initialized_context_screens={str(p): digest(p) for p in captures},
        observed_opening_dialogue_andHangzhou_context=True,
        existing_isolated_system_unlock_not_earned=True,
        actual_changed_batch_gameplay_observed=False, new_final_formatted_pages_approved=0,
        native_bindings_offline_not_gameplay=True, no_name_term_orformatting_gate_inferred=True,
        all_prior_drafts_meanings_evidence_andROMs_preserved=True,
        new_credit=0, full_goal_complete=False, evidence=evidence))
    summary = ('Maria B0–B32 now has all 301 clean-first logical English drafts and exact current native bindings. '
        'Eleven complete exchanges have 67 individual contextual proposals:46 revisions/21 justified retentions; '
        '234 comparisons remain. Four source-reread draft refinements preserve motives, idioms and uncertainty. '
        'The current ROM’s31,000-frame Maria coldboot reaches Hangzhou; captain3 andthe staged payload are exact. '
        'This uses the existing isolated system unlock, not earned progression. Allfive gates, scoped names/terms '
        'andfresh final display checks remain pending. Integrated19,161/registeredf166991f/main andfull scope unchanged.')
    text = '''# Maria301 drafts, native bindings and first67 proposals — November9,2026

The full editorial goal remains active. The preceding [source67-draft checkpoint](editorial_Maria301_source67drafts_20261109.md) retains the exact all-route census, Lil metadata recovery and source-context constraints. Do not restart that work. Rafael/tutorial priority, earlier translations and all completed coverage remain intact; every remaining storyline, shared exchange, random scene, name and prose record stays in scope.

All **301 independent logical American English drafts** across32 complete exchanges are sealed in `work/Maria_B0_B32_clean_20261109/all301_clean_meanings_andindependent_drafts_v1.json`. All301 clean meanings and drafts preceded this intake’s current-English extraction. The original three draft chunks remain unchanged. Four documented source-reread refinements avoid selecting whom Aziza copied, preserve her comparative motive rather than denying her pirate ambition, retain Camille’s conditional confidence without an absolute safety claim, and preserve the noisy-fly comparison. Native literal substitutions remain exact.

The earlier source-qualified working epithet **Soaring Scarlet Orca** is reused from `docs/name_source_review_v294.md`; this is a localization inference in naval context, not an official English-name claim. Do not repeat its dictionary investigation or globally replace the separate Shachihoko item. Its scoped use and other name/item/faction consumers still need current approval.

## Exact current references

`current_v1/current_effective.json` binds292 ordinary speeches using the current registered ROM’s original native catalogue lookup. `current_objects_v1/current_objects.json` binds seven physical voice alternatives, all eight native style slots/alias relationships andtwo menu captions. Complete source/current command membership and speaker preambles are preserved. The unchanged reusable binders ran with explicit captain3. The unified source packet was projected without modifying any source bytes, meanings or draft wording; see `binding_inputs_v1/projection_qualification.json`.

These are **offline native bindings**, not display approval or scene activation. They do not replace the final text’s fresh formatting, full glyph/bounds/page review, storage, representative gameplay or release checks.

## Contextual proposals

`contextual_proposals_B0_B10_v1.json` saves **67 individual proposals in11 complete exchanges:46 revisions and21 justified retentions**. Every row has its exact source/current references, meaning, complete-exchange context, proposed wording and specific finding or retention reason. All five gates stay false pending scoped name/term/consumer approval and final display checks; nothing may ship or receive new credit from this proposal stage.

Findings include a question about authenticity reduced to a lie, an unsupported rightful-sovereign implication, loss of the mainland/samurai detail, an unnatural rigid-virtue insult, Escante’s distorted realization about his own generosity, an invented trade/treaty detail, flattened pirate/crew voices, and Maria’s incredulous humanity question changed into a possible identification. Two full-width reaction-punctuation targets require fresh consumer-specific glyph checks. Most proposed revisions are editorial improvements, not claims that all46 are factual errors.

Retentions include the already correct coercive surrender offer, Yukihisa’s formal counterargument, Maria’s clear rejection of Escante’s self-interest, the weapons/independence inference, gunnery readiness, natural acknowledgements and Yuris’s pretentious noble claim. Their retained wording still needs current formatting checks; old line breaks are not authoring instructions. A fresh source reread during comparison also removes the independent draft’s unsupported *our* before Gabriel’s agreement: Maria is not established as a party to that agreement.

## Current Maria initialization

The current registered candidate ran31,000 frames through ordinary Maria selection/opening inputs to Hangzhou. `work/Maria_current_context_20261109_v1/runtime_context_qualification.json` binds its own read-only RAM, captain3, exact123,264-byte staged payload, current ARM9/COMMON and original machine/registered-runtime guards. The existing isolated system-unlock save was copied byte-for-byte; all six route slots/footer remain preserved and the donor is unchanged. The unlock is **not earned progression**. No savestate or story/location/RNG/funds/outcome fixture was used.

Screens4000(opening),16000(Yukihisa dialogue/nameplate) and31000(Hangzhou town) were directly viewed. These establish current Maria context, not actual gameplay of B0–B32 or visual approval of their proposed English. The run is terminal0; no process remains live. Do not overlay an older ARM9 context onto this candidate or reuse a Rafael-captain snapshot for Maria-specific substitutions.

## Continue here

Compare the remaining234 records in complete B11–B32 exchanges against the now-bound current English. Preserve the sealed independent drafts as evidence, use existing good wording, and save individual reasons. Bind all scoped names/role labels, substitutions, item/faction/city terms and the sobriquet before approving prose gates. Then format the final301 logical paragraphs with validated consumers; review every newly generated page, including earlier premature wraps and glyph consistency. Run appropriate stored checks and representative gameplay before registered cumulative integration/clean-input reconstruction.

`drafts301_bound301_proposals67_qualification_v1.json` links the concise proof for this stage. The exact remaining native-story scope is still6,737 objects; shared/UI scope is separate. Integrated completion stays **19,161=11,532 revisions+7,629 retentions**; historical source/prose/draft counters retain19,164. No new credit is added.

Registered candidate, manifest, patch, accepted layers and ASCII right-bound stage remain unchanged: `work/hodram_residual_release_v1/all_routes_hodram_residual_candidate.nds`, SHA-256 `f166991f83f18859a7483850ccee07945b76993f1ded491dec3b37b7e4ae01d8`. Main remains all-routes-unified-v4701. No promotion or guide-photo collection. AllROMs, translations, retentions, evidence and failures are preserved. Deferred graphics artwork and the later older-record technical re-audit remain separate.
'''
    checkpoint(mutation='work/Maria301_drafts_bound67proposals_checkpoint_20261109',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria301:all clean drafts/current bindings,67 proposals;234 comparisons next.',
            current_batch_not_yet_integrated=True, new_source_meanings=301, new_independent_drafts=301,
            new_current_comparisons=67, proposed_revisions=46, justified_retentions=21,
            all_current_batch_five_gates_pending=True, guide_photos=False, build_live=False,
            next_action='Compare234 remaining Maria records, bind scoped names/terms/consumers, then fresh-format final301 paragraphs.'),
        additional_updates={'Maria_SC3_B0_B32_clean_20261109':dict(new_credit=0,
            independent_drafts=301, remaining_independent_drafts=0, current_native_bindings=301,
            current_comparisons=67, remaining_current_comparisons=234,
            proposed_revisions=46, justified_retentions=21,
            qualification=str(qualification), qualification_sha256=digest(qualification),
            all_five_gates_pending=True, native_display_stored_andrepresentative_gameplay_pending=True,
            registered_integration_pending=True, current_captain3_own_runtime_context=str(runtime_path))},
        summary=summary, document='docs/editorial_Maria301_drafts_bound67_proposals_20261109.md', document_text=text,
        completed=19161, protected={'translations/release_stack.json':release['registry_sha256'],
            release['candidate']:release['candidate_sha256'], release['manifest']:release['manifest_sha256'],
            release['patch']:release['patch_sha256'],
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('Saved301 drafts/current bindings and67 proposals (46 revisions/21 retentions);zero credit,19161 integrated;full goal active.')


if __name__ == '__main__':
    main()
