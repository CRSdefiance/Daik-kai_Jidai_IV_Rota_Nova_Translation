"""Save complete offline display/storage work without gameplay or integration credit."""
from pathlib import Path
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint


def main():
    release=load('work/maria337_release_v1/registered_release_verification.json')
    stored=load(ROOT/'stored_v1/stored_native_verification.json')
    loaders=load(ROOT/'loaders_v1/verification.json')
    rebuilt=load(ROOT/'reconstruction_v2/reconstruction.json')
    catalogue=load(ROOT/'stored_catalogue_all_v1/all333_stored_effective_body_bindings.json')
    approval=load(ROOT/'offline_display_approval_v1.json')
    alignment=load(ROOT/'inherited_alignment_guard_v1.json')
    selection=load(ROOT/'display_selection_v1.json')
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['complete_stored_pages']==333
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(172,161,100)
    assert loaders['fresh_whole_archive_loads_andcache_hits']==303 and loaders['fresh_parent_cases']==606
    for key in ['loads','modes']:assert digest(loaders[key])==loaders[key+'_sha256']
    assert loaders['all_native_executed_instructions_current_ROM_exact']
    assert (rebuilt['source_editorial_objects'],rebuilt['speech_count'],rebuilt['command_count'],rebuilt['relative_sites'])==(335,333,454,20)
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256'] and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert catalogue['all333_physical_bodies_checked']
    assert approval['all333_final_pages_directly_viewed'] and approval['all_names_andtwo_captions_directly_viewed']
    assert alignment['all_five_negative_controls_rejected'] and selection['selected_source_bodies']==44
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(717,114,52)
    assert digest('translations/release_stack.json')==release['registry_sha256']
    paths=[ROOT/p for p in ['offline_display_approval_v1.json','final_native_v1.json','body_visual_review_v1.json','mixed_visual_review_v1.json',
        'reconstruction_v2/reconstruction.json','stored_v1/stored_native_verification.json','loaders_v1/verification.json',
        'stored_catalogue_all_v1/all333_stored_effective_body_bindings.json','inherited_alignment_guard_v1.json',
        'native_layout_findings_v1.json','native_layout_findings_v2.json','plan_native_v4/automatic_plans.json',
        'menu_native_v1/menu_provider_and_planes.json','name_planes_v1/native_name_planes.json','display_selection_v1.json',
        'actual_menu_inputs_v1/native_menu_proof.json','display_fixtures_v1/fixtures.json']]
    paths.append(Path(__file__));evidence={str(p):digest(p) for p in paths}
    summary=('Maria B137–B151 passes offline display/storage: 335 contextual reviews (185 revisions/150 retentions), '
        '333 directly viewed final body pages, two repaired captions and 30 scoped name strings. Three premature pages are reclaimed; '
        'four phrase wraps and six scoped FE guard layouts improve without shortening prose. Two concrete native FE failures are repaired. '
        'All 333 catalogue lookups, 100 branch cases, 303 loads and 606 handoffs pass. Representative 44-body/two-choice gameplay is prepared but unrun; '
        'fifth gates and registered integration remain. No worker is live. Registered 9913f13e, integrated 21,356, main and full scope are unchanged.')
    text=f'''# Maria335 B137–B151 offline display and storage — November 9, 2026

{summary}

Continue the same 335 original objects in 15 complete exchanges from [the prose checkpoint](editorial_Maria335_B137_B151_prose_layout_20261109.md). Preserve all meanings, independent drafts, contextual decisions, 185 revisions/150 justified retentions, 26 scoped names and first four individual gates. Select final `proposed_English`/`english`. Fifth gates and once-only release credit remain pending.

Work root: `work/Maria_B137_B151_clean_20261109`. Final plan: `plan_native_v4/automatic_plans.json`, 333 bodies/333 pages with zero warnings/failures. All final pages have exact native and visual approval in `offline_display_approval_v1.json`, `final_native_v1.json` and `body_visual_review_v1.json`. Thirty-nine viewed body sheets contain 337 complete previews; four superseded layouts are excluded from final selection. Both name sheets and the caption sheet were viewed. Names cover 26 actors/52 getters/30 strings: 19 fresh planes and 11 exact compatible reuses. This is scoped review, not global name approval.

Two real FE defects were caught: B139R199 split the final w of view into another row; B145R57 created an extra blank row after a 36-character row. Diagnostics and both failed runs are preserved. Six exact failed/matching risks use the already qualified FE36 planning reserve: B139R199/R202, B145R51/R57/R77 and B150R36. Physical 228px geometry, prose, font, consumer and native guards remain unchanged. Four phrase refinements keep the short Only if you want to, of course reply, Private Cabin and two complete name questions together. Three complete paragraphs B141R43/B146R56/B148R8 reclaim three premature pages at the unchanged 216px width. Ordinary long-title soft wraps remain readable on consecutive rows. Findings retain exact source/current references in `native_layout_findings_v1/v2.json`.

Native receipt selection reuses 95 initial records, 155 from resumed v1 and 83 from resumed v2: 333 selected records/1332 alignments. All leading/internal/trailing glyphs, pixels, consumption, canaries, bounds, row membership and pagination pass. Executed completed cases include four superseded receipts/16 alignments; failed partial cases receive no credit. Both target-page and progressive-macro adapters remain bound to exact runtime inputs. The final 83-record run exited 0. The initial and resumed-v1 runs exited 1 at their documented failures; completed exact receipts are reusable.

B138C1274 has two corrected captions, Please do. and No, thanks. Six provider alignments, 18 bridged returns and seven compiler negatives pass. All four target normal/highlight planes and two valid current ASCII planes pass. Only the exact corrupt current option1 `丑o` is provider-checked without approving its old ASCII font rendering. `menu_native_approved_v1.json` binds the complete 0x2100 object. The zero-style proof executes no empty permutations.

`reconstruction_v2/reconstruction.json` rebuilds all 15 blocks: 333 speeches, two captions, 454 commands and 20 relative sites, within 9216-byte allocations. No styles or FE continuation commands are added. Complete clean/current/block/archive/serialized-ROM inverses pass. Pinned research ROM SHA256: `{rebuilt['research_ROM_sha256']}`. This is not a registered test candidate. All other components, including Market pointers/allocation, six-section ARM9, ASCII right bounds, names, fonts and graphics, match registered Maria337.

V1 reconstruction stopped at B139R177 after two block outputs. That inherited 26-byte English line uses one original NUL alignment byte beyond its 25-byte clean string. Both native commands are exactly 32 bytes and end at 2086. V2 binds the exact ID, bytes, offset and extents, normalizes only the original inverse span, then restores the actual 25-byte source reference in its proof. Full inverse guards still pass; five altered-ID/body/offset/padding controls reject. See `inherited_alignment_guard_v1.json`. The accidental generic SC1 planner call also failed its path guard before output; the scoped Maria planner passes. Preserve these histories.

Stored checks exited 0: 333 bodies/pages, 172 fresh parity-dependent pages, 161 exact reuses and 100 relocated branch cases. All 333 guarded pre-macro catalogue lookups pass. The SC3 loader/cache job exited 0 with 303 complete loads/cache hits and 606 parent handoffs. Exact payloads, executed instructions, metadata and neighbors pass; other routes are unchanged and were not replayed. These are offline checks, not observed gameplay.

Next run the prepared fixtures in `display_fixtures_v1/fixtures.json`: 44 distinct source bodies/44 main-run pages over 20801 frames and two second-choice pages over 10721 frames. Selection covers Julio's repaired I, Indeed, all eight tutorial room labels, both name questions, all three reclaimed paragraphs, six FE guards and named returns, Yifa/Sanghyeon references, bread teaching and three prospective forecasts. `actual_menu_inputs_v1` reuses the exact caption proof. Hosts retain the original Maria B33 seven-command prefix and all 40 nonspeech setup/effect/cleanup commands. Preserve normal 16-frame A pulses and the existing isolated system-only unlock disclosure. Verify both menu choices and resupply/departure/sailing returns. No new gameplay is claimed yet; unselected bodies remain offline-only. Original chronology, conditional outcomes, room effects, commodity outcomes, full-route and hardware coverage are not implied.

After necessary gameplay checks, seal fifth gates and integrate once over registered Maria337 with own startup/protected getters and an exact clean-input patch. Registered candidate remains 9913f13e: 717 entries/114 layers/52 checks. Integrated 21,356 = 12,861 revisions + 8,495 retentions; historical source/prose/draft 21,359. Native remainder 4542 (Lil1805/Maria2737), including this unintegrated335. Do not precredit or promote main without acceptance. Full story/shared town/shop/random/player prose scope, unfinished earlier passes, early Rafael/tutorial priority, deferred artwork and later older-record technical re-audit remain. No guide photos, cleanup, promotion, commit or push. No worker is live.

The confirmed Rafael2952 testing build has the already repaired [Market format-terminator defect](editorial_market_goods_info_fix_20261109.md). The registered 243e21fc fix candidate and current 9913f13e ROM were freshly SHA256-verified. Current parent preserves the fix. Do not reinvestigate or count new dialogue credit for it.
'''
    update=dict(new_credit=0,native_pixels_andvisual_checks_pending=False,stored_native_checks_pass=True,
        representative_gameplay_pending=True,registered_integration_pending=True,all_individual_fifth_gates_still_pending=True,
        body_pages=333,selected_native_alignments=1332,pages_reclaimed=3,phrase_wrap_fixes=4,scoped_FE_guard_fixes=6,
        distinct_name_strings=30,observed_current_batch_source_bodies=0,prepared_gameplay_source_bodies=44,evidence=evidence)
    checkpoint(mutation=ROOT/'stored_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch=summary,current_batch_evidence=evidence,
            native_job_live=False,native_sessions=[],registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False,
            next_action='Run prepared44-body/two-choice initialized Maria gameplay andboth sailing returns; then fifth gates andregistered integration.'),
        additional_updates={'Maria_SC3_B137_B151_clean_20261109':update},summary=summary,
        document='docs/editorial_Maria335_B137_B151_stored_20261109.md',document_text=text,completed=21356,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved Maria335 offline/storage checkpoint; representative gameplay/registration pending; zero new credit.')


if __name__=='__main__':main()
