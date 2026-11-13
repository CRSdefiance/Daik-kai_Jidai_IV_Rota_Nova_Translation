"""Record registered residual SC0 completion while preserving the wider editorial scope."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.build_registered_rafael5186_v1 import RELEASE,REGISTRY,PARENT_REGISTRY,CANDIDATE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import ROOT
from scripts.reconcile_rafael5186_coverage_v1 import OUT as COVERAGE
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

def main():
    release,ledger,package,coverage=map(load,(RELEASE,LEDGER,PACKAGE,COVERAGE))
    registry,parent=map(load,(REGISTRY,PARENT_REGISTRY))
    assert ledger['records_editorially_completed']==17031 and not ledger['full_goal_complete']
    assert ledger['Rafael_SC0_B0_B34_clean_20261106']['completion_credit_added']==283
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']==digest(CANDIDATE)
    assert digest(REGISTRY)==release['registry_sha256']
    assert registry['latest_promoted_build']==parent['latest_promoted_build']
    assert registry['accepted_layers']==parent['accepted_layers']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert coverage['source_objects']==6887 and not coverage['missing']
    summary=('Rafael B0–B34 is registered in Rafael5186 and credited once: 283 reviews, '
        '162 revisions and 121 justified retentions. Nineteen wraps and two dialogue glyph defects '
        'are corrected; three full-name fields use nine owned data bytes. All 284 stored pages passed; '
        '95 utterances and 96 pages were observed in the emulator. The clean-input patch, own startup '
        'and nine protected name getters passed. Integrated coverage is 17,031; main is unchanged.')
    doc=f'''# Rafael5186 registered checkpoint

{summary}

The experimental cumulative candidate preserves all 698 earlier manifest entries, 114 accepted layers and the registered ASCII right-bound correction. Its manifest has 700 entries and 35 passing release checks. Only the 35 reviewed SC0 blocks and nine exclusive ARM9 data bytes differ from Rafael4903. The source-bound transactions, fresh four-archive format guard, complete predecessor inverse and exact clean-input patch pass. All generated ROMs and research references are preserved and pinned.

- [Rafael5186 test candidate](../{CANDIDATE.as_posix()})
- [Manifest](../{Path(release['manifest']).as_posix()})
- [Patch from the clean Japanese input](../{Path(release['patch']).as_posix()})
- [Registered verification](../{RELEASE.as_posix()})
- [283 integrated decisions and exact references](../translations/rafael_B0_B34_integrated_final_review_v1.json)
- [Completed editorial and display research](editorial_Rafael_B0_B34_research_20261106.md)

Candidate SHA-256: `{release['candidate_sha256']}`. Canonical baseline remains `{release['canonical_base']}` with SHA-256 `{release['canonical_sha256']}`. The patch expects clean input SHA-256 `{release['clean_input_sha256']}`. The promoted main and existing Rafael3222 weekend ZIP are unchanged; this is not a main promotion or hardware acceptance.

The candidate-owned 4,001-frame cold boot matches all ten previously reviewed opening captures byte for byte. Both original name getters return all nine protected actors correctly, including Dinis de Albuquerque, Antony von Kuhn and Garcia de Oviedo in the full-name consumer. Their progressive nameplates remain Dinis Albuquerque, Antony Kuhn and Garcia Oviedo. Full catalogue UI remains unvisited.

Offline checks cover all 283 speeches and 284 pages, complete leading/internal/final glyphs, 675 relative cases, 343 archive blocks and 686 loader modes. All final offline pages and names were visually reviewed. The initialized emulator sequence observes 95 utterances, 96 pages, all 39 scoped headers and the poem page turn; all 16 capture sheets were inspected. The remaining 188 utterances are offline-only. Natural event activation, original locations and chronology, battle/tavern transitions, full-route play and hardware were not tested in this batch.

The [reconciled SC0 source census](../{COVERAGE.as_posix()}) accounts for all 6,887 native speech/style/caption objects across 343 blocks: 6,133 ordinary speeches, 626 physical style alternatives and 128 captions. It reuses 6,604 exact prior source bindings and adds the 283 newly registered ones, rechecking every source position. No residual objects remain in this specific native inventory. This is not a complete census of all player-facing resources, shared external scenes or reachable conditions, and does not replace the later older-record technical audit.

Next reconcile remaining shared tutorial coverage without restarting the 202 completed HELP records or other credited exchanges. Then resume the preserved Hodram B211–B230 intake: all 277 source meanings and 114 partial drafts remain saved. Continue other unfinished routes, shared/shop/town/random scenes, remaining player prose and the wider name review. Preserve prior coverage, translations and evidence. Graphics artwork and the later older-record re-audit remain separate; no guide photos are collected. The full editorial goal remains active.
'''
    checkpoint(mutation=CANDIDATE.parent/'registered_documentation_v1',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Residual SC0 B0–B34 registered and credited once in Rafael5186.',
            next_action='Reconcile remaining shared tutorial scope, then resume saved Hodram B211–B230 without restarting.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,
            registered_integration_pending=False,native_job_live=False,registered_build_live=False,
            registered_cumulative_build_live=False,guide_photos=False,
            native_SC0_source_inventory_complete=True,SC0_native_source_objects=6887,
            exact_source_coverage=str(COVERAGE),exact_source_coverage_sha256=digest(COVERAGE)),
        summary=summary,document='docs/editorial_Rafael5186_registered_20261106.md',document_text=doc,
        completed=17031,protected={str(REGISTRY):release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved registered Rafael5186 and complete native SC0 inventory. Full editorial goal remains active.')

if __name__=='__main__':main()
