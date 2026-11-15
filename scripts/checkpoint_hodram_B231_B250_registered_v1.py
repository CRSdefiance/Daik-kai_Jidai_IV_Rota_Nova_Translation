"""Save the cumulative release and next clean-first action without reopening credited work."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_hodram_B231_B250_v1 import RELEASE,REGISTRY,PARENT_REGISTRY,CANDIDATE,INVERSE_PATCH
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

def main():
    release,ledger,package,registry,parent=map(load,(RELEASE,LEDGER,PACKAGE,REGISTRY,PARENT_REGISTRY))
    assert ledger['records_editorially_completed']==17533 and not ledger['full_goal_complete']
    assert ledger['Hodram_B231_B250_clean_next_20261107']['completion_credit_added']==225
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']==digest(CANDIDATE)
    assert digest(REGISTRY)==release['registry_sha256']
    assert registry['latest_promoted_build']==parent['latest_promoted_build'] and registry['accepted_layers']==parent['accepted_layers']
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(702,114,37)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    backup=CANDIDATE.parent/'retention_pins_before_registered_checkpoint.json';assert not backup.exists();backup.write_bytes(before)
    for rom in (CANDIDATE,INVERSE_PATCH):
        assert digest(rom)==release['candidate_sha256']
        if not any(Path(v['path']).resolve()==rom.resolve() for v in values):
            values.append(dict(path=str(rom.resolve()),reason='Preserve registered cumulative Hodram B231-B250 candidate and exact clean-input reconstruction. SHA256 '+digest(rom)))
    pending=pins.with_name('rom_retention_pins.Hodram_B231_B250.pending.json');assert not pending.exists()
    save(pending,values);assert pins.read_bytes()==before;os.replace(pending,pins)
    summary=('Hodram B231–B250 is registered and credited once: 225 reviews, 115 revisions and 110 justified retentions. '
        'Thirteen wraps and two mixed-font punctuation/letter defects improve; nine layout candidates retain better originals. '
        'All 228 stored pages pass; the emulator sample observes 63 utterances/68 pages. '
        'The cumulative candidate passes 702 manifest entries, 114 accepted layers, 37 release checks, exact clean-input reconstruction and its own startup. '
        'Integrated coverage is 17,533. Main is unchanged. Next prepare the clean B251–B270 intake with ledger overlap checks.')
    doc=f'''# Hodram B231–B250 registered checkpoint

{summary}

- [Cumulative test ROM](../{CANDIDATE.as_posix()})
- [Manifest](../{Path(release['manifest']).as_posix()})
- [Clean-input patch](../{Path(release['patch']).as_posix()})
- [Registered verification](../{RELEASE.as_posix()})
- [225 integrated decisions and exact source/current/final references](../translations/hodram_B231_B250_integrated_final_review_v1.json)
- [Completed offline display and storage scope](editorial_Hodram_B231_B250_display_20261107.md)
- [Five-gate research completion and representative scope](../work/Hodram_B231_B250_clean_20261107/research_final_v1/research_completion.json)

Candidate SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. The patch requires clean Japanese input `{release['clean_input_sha256']}`. The canonical baseline remains `{release['canonical_base']}`, SHA-256 `{release['canonical_sha256']}`. This is an experimental cumulative testing candidate, not a promotion. Main and the existing Rafael3222 weekend ZIP remain unchanged. The candidate and byte-identical clean-input reconstruction are pinned; every earlier ROM, translation, retention and evidence file is preserved.

The verified Hodram B211–B230 predecessor's 701 manifest entries and all 114 accepted layers are retained. The new source-bound SC1 transaction adds one entry and one release check. Only 18 eligible SC1 blocks change; B235 is control-only and exact, and credited B237 is excluded. ARM9, font, graphics, names, all other files/components, runtime and registered ASCII right-bound correction remain byte-identical to the predecessor. Fresh complete-block reconstruction, four-archive format safety, full predecessor inverse, eight production scope rejections, exact clean-input reconstruction, and pure caller preservation pass. The candidate's own 4,001-frame ordinary Rafael coldboot matches all ten previously viewed RGB captures and uses fresh read-only RAM; both original name getters return all nine protected names correctly. Startup is separate from Hodram scene coverage.

All 225 individual five-gate decisions pass: 115 wording revisions and 110 justified retentions. Exact clean/current references, source meanings, whole-exchange context, individual findings and reasons remain in the integrated review. The scoped term check justified retaining the existing spirit-beast wording, changing only that earlier proposed decision. The 19 scoped names and role labels retain approved public forms with source/context reasons. Regional metadata does not become biography. Full catalogue UI and the remaining global name review are open.

All 223 bodies/228 final pages and the two menu captions pass complete native, visual and stored checks. Native alignment/glyph/guard/bounds/consumption/pagination proofs and exact current references are qualified by this runtime. Thirteen wrapping changes preserve prose; nine tested layouts are retained with reasons. No QA heuristic waiver is needed. Two glyph defects are corrected: full-width F in Fernando in B239 R39 and the isolated full-width question mark in B244 R14. All 14 physical voice alternatives and 16 alias slots remain exact. Stored checks include 108 fresh parity-dependent pages, 120 exact reused pages, 170 relocated branch cases, 223 original catalogue lookups, 325 archive loads/cache hits, 36 fresh parent cases and 614 exact reuses.

The disclosed 21,521-frame emulator sequence observes 63 utterances/68 ordered pages, 144 complete body planes and 136 complete header planes across 13 selectors. Complete Jam letter/replies, the Rose exchange, and Rio survey job/reminder/reward exchanges are sampled, together with all four FE panel bodies, FI substitutions, both default-role voice selections, the glyph fixes and revised page turns. All 12 body contact sheets and the menu sheet were directly viewed. The other 160 speech variants remain offline-only. Native source commands and initializers are preserved, but the selected display sequence does not preserve original branch routing, original locations, earned chronology or event effects. Nondefault menu selection/cancellation, natural activation, battle transitions, full route, full catalogue UI and hardware remain unvisited.

The menu's complete captions, original centering, fixed geometry and every non-ink cell pass in two source-window-qualified captures, with default option zero observed. The previous flat-highlight matcher rejected these frames because a cyan cursor band enters/leaves the cell. The new exact-object check accepts only a contiguous edge-clipped band with a uniform approved color on every row; it still checks every blank pixel and complete glyph masks at the provider's original geometry. Six negative cases reject lost leading/final ink, foreign colors, mixed rows, disjoint and interior bands. No ROM code or capture was changed and no extra coldboot was needed. This is not a second gameplay run or a change to the native menu.

Registration and startup completed before the once-only ledger credit ran out of disk space. The authoritative ledger remained unchanged at 17,308; its exact compressed backup and completed integrated review were reused after validation. The zero-length failed pending file is preserved. Native NTFS compression now preserves eight generated ROM paths and hashes, and the translations directory marks future files for compression without changing logical bytes. The resumed atomic completion adds 225 records exactly once and proves all earlier keys and record prefixes intact. See `work/hodram_B231_B250_release_v1/completion_disk_full_resume_v2.json` and the storage receipts; no ROM or earlier translation was deleted or moved.

Integrated totals are 17,533 completed, 10,699 revised and 6,834 retained. Historical source/prose/draft counters remain three higher at 17,536; preserve this distinction. Continue with a clean-only inventory of complete B251–B270 exchanges, reconcile prior coverage before counting new objects, and save clean meanings/drafts before consulting eligible current English. Do not repeat completed B231–B250 checks or credit excluded B237 again.

Every remaining storyline, earlier unfinished contextual pass, shared town/shop/random exchange, speaker name/role label and player-facing resource stays in scope. Rafael/tutorial priority and completed SC0/known HELP/Deck proofs remain intact; those proofs do not claim a global player-resource census. Deferred graphics artwork and the later older-record technical re-audit stay separate. No guide photos are collected. The full editorial goal remains active.
'''
    checkpoint(mutation=CANDIDATE.parent/'registered_documentation_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Hodram B231–B250 registered and credited once; prepare clean B251–B270 intake.',
            next_action='Reconcile B251–B270 clean source scope with existing coverage, then read complete exchanges and seal clean meanings/drafts before current English.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,registered_integration_pending=False,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False),
        new_entries={'Hodram_B251_B270_clean_next_20261107':dict(new_credit=0,clean_intake_inventory_pending=True,
            overlap_reconciliation_pending=True,source_meanings_saved=0,localized_drafts_saved=0,current_English_comparisons=0,
            all_five_review_gates_pending=True,no_current_English_dialogue_consulted=True)},
        summary=summary,document='docs/editorial_Hodram_B231_B250_registered_20261107.md',document_text=doc,
        completed=17533,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved registered 17,533-record checkpoint and next clean-first action. Main and all earlier work preserved.')

if __name__=='__main__':main()
