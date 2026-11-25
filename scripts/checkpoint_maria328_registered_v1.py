"""Publish the registered candidate and exact remaining scope without changing completion credit."""
import os
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

def main():
    releasepath=Path('work/maria328_release_v1/registered_release_verification.json');release=load(releasepath)
    completepath=Path('work/maria328_release_v1/completion_checkpoint.json');complete=load(completepath)
    censuspath=Path('work/story_source_coverage_20261109_SC3_v7/coverage.json');census=load(censuspath)
    ledger=load('translations/editorial_review_current_v1.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(715,114,50)
    assert complete['new_credit']==328 and complete['counts']==dict(completed=20689,revised=12388,retained=8301)
    assert ledger['records_editorially_completed']==20689 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    assert len(census['records'])==5129 and len(census['missing'])==3404 and census['new_exact_bindings']==328
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    assert digest(release['candidate'])==release['candidate_sha256'] and digest(release['patch'])==release['patch_sha256']
    assert digest(release['manifest'])==release['manifest_sha256']
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    bindings=load(release['exact_record_bindings'])['records']
    assert len(bindings)==328 and sum(len(r['registered_native_pages']) for r in bindings)==329
    evidence={str(p):digest(p) for p in [releasepath,completepath,censuspath,
        Path('translations/maria328_integrated_final_review_v1.json'),ROOT/'research_completion_v1/research_completion.json',
        ROOT/'gameplay_review_v1.json',Path('work/maria328_release_v1/own_registered_startup_verification.json'),
        Path('work/maria328_release_v1/own_registered_name_getters_v1.json'),Path(__file__)]}
    summary=('Maria328 is registered and credited once: 143 revisions/185 justified retentions, 12 layout improvements, '
        'one reclaimed page, two FE defect repairs and two corrupted rescue replies corrected. All 321 body pages, '
        '15 captions and 28 name strings pass; representative emulator QA observes 43 source bodies/48 pages and six captions. '
        'The cumulative 715-entry/114-layer candidate passes 50 checks, exact clean-input reconstruction, own startup '
        'and 24 protected getters. Integrated 20,689; 5,209 native story objects remain. Next clean exchanges begin '
        'at B96/B98 in the SC3_v7 residual packet. Main and the full editorial scope are unchanged.')
    text=f'''# Maria328 registered checkpoint — November 9, 2026

**328 source objects are integrated and credited once: 143 revisions and 185 justified retentions.** All five individual gates pass across 21 complete exchanges, SC3 blocks 73/74/75/76/77/78/81/82/83/84/85/86/87/88/89/90/91/92/93/94/95. Twelve layout improvements reclaim one page without shortening the prose. Two FE display defects and two corrupted rescue replies are corrected. All 20 former non-ASCII targets now render complete English. The 24 scoped name/role retentions cover 28 short/full strings; the wider review remains open.

Registered cumulative [ROM](../work/maria328_release_v1/all_routes_maria328_candidate.nds), SHA-256 `{release['candidate_sha256']}`. [Clean-input patch](../work/maria328_release_v1/all_routes_maria328_candidate.xdelta), SHA-256 `{release['patch_sha256']}`. The patch reconstructs the exact ROM from clean `{release['clean_input_sha256']}`. The manifest preserves all 714 predecessor entries and 114 accepted layers and passes 50 checks. The candidate's own 31,000-frame Maria/Hangzhou startup, complete RAM/payload identity and both getters for 12 protected names pass. All six startup checkpoints were viewed. Main is unchanged; no promotion, cleanup or Git push occurred.

Reuse [the research-ready checkpoint](editorial_Maria328_research_ready_20261109.md), [the offline checkpoint](editorial_Maria328_offline_20261109.md) and `work/Maria_B73_B95_clean_20261109/research_completion_v1/research_completion.json`. Every reviewed paragraph retains its exact clean/current references, finding, decision and justified retention. All 321 body pages, 15 menu captions and 28 name strings have native and direct visual proofs. The final 1,256 alignment-case selection reuses 892 exact cases; only changed or unfinished layouts were rerendered. Storage freshly checks 148 parity-dependent pages and reuses 173 exact pages. All 314 effective body lookups, 315 native branch cases, 303 SC3 loads/cache hits and 606 parent handoffs pass. The four complete style objects preserve all eight-slot aliases; 32 target getters and 36 malformed cases pass. Five three-choice menus have 30 native provider alignments, 120 bridged selection/cancel returns, 60 caption style planes and 40 malformed cases checked.

`gameplay_review_v1.json` records one 22,001-frame disclosed initialized emulator run: **43 original source bodies, 44 physical candidates, 48 pages and six captions in two menus**. All selected pages and transitions were directly viewed. Complete pixel comparisons cover 96 body holds and 72 header holds across eight actual actors and source selectors 207/208/214/215. The new two-panel riddle advances with ordinary A input through its menu to the next named speech without a blank panel. The repaired bean tutorial, four progressive continuations, FI substitution, FE/named returns and three complete style objects pass. The formerly corrupted `SC3_B95_STYLE_400_42` reply is observed cleanly; `_18` remains offline-only. Both menus show option 0 and normal A return. Original host setup/effects/cleanup reach resupply, departure and ordinary sailing.

The remaining **270 source body objects and nine captions are offline-only**. Other selections/cancellation and numeric branch returns have native offline proofs. The isolated preexisting system unlock is disclosed, not earned. Original optional conditions, locations, chronology, rewards, story effects, full routes, catalogue UI and hardware remain unvisited. No guide photos are collected. The first coverage-audit version confused source and relocated menu offsets; v2 binds both separately. The first release-driver derivation stopped before any outputs; staging v2 uses the correct original import. Failed producers and all intermediate ROMs/evidence remain preserved.

The pure transaction is `dk4tool/patch/maria328_release_v1.py`; stage with `scripts/build_registered_maria328_v2.py` and register with `scripts/register_maria328_v1.py`. It changes only the 21 owned SC3 blocks. The qualified FE helper inserts one original six-byte `0040ffff00fe` continuation under B87 R139's original conditional ancestors, preserving its complete paragraph. Both relocation stages compose command, menu/style and relative references. Seven invalid FE insertions and eight production-scope mutations are rejected. Full clean/current/block/archive/serialized-ROM inverses pass. The registry binds both physical children under that one source record: 328 source bindings / 329 stored text references, never 329 source credits. Preserve the earlier B54R507 storage and B62R53 source-span corrections in the predecessor; do not reapply them to this disjoint batch.

Market read-only allocation and both Local/Cargo pointers, the six-section ARM9, ASCII right-bound correction, source25 v2 guard, COMMON, fonts, graphics and all unowned files/components remain exact. This candidate therefore retains the fix for the untranslated/garbled Market Goods Info seen in the user's older `all_routes_rafael2952_extended_checkpoint_v1_20261106_candidate` build. No new graphics work is bundled.

`translations/maria328_integrated_final_review_v1.json` and `work/maria328_release_v1/exact_integrated_record_bindings.json` bind every source/current/final reference and all five individual gates, including the FE children. `completion_checkpoint.json` proves once-only credit and exact earlier ledger-key/record-prefix retention. Integrated totals are **20,689 = 12,388 revisions + 8,301 retentions**; historical source/prose/draft counts remain three higher at **20,692**. The SC3_v7 census rechecks all 5,129 exact source positions using the completed native inventory: **1,725 covered / 3,404 remaining**, with no duplicate or unresolved bindings. Remaining native story objects are **5,209 (Lil 1,805 / Maria 3,404)**. Shared town/shop/random/UI and other player-facing prose remain separately in scope; this is not a full reachability census.

**Next begin clean meanings and independent logical English drafts from `work/story_source_coverage_20261109_SC3_v7/residual_clean_source_packet.json`.** First complete exchanges are B96 (6), B98 (6), B99 (20), B100 (5), B101 (8), B102 (43), B103 (8), B104 (1), B105 (34), B106 (12), B107 (9), B110 (10), B111 (16), B112 (10), B113 (20) and B114 (9). Choose a substantial batch of complete exchanges. No new meanings/drafts/current-English comparison are claimed for them yet. Reuse completed inventories and technical proofs when dependencies match; every changed paragraph still receives fresh formatting and readable page review. Retain the early Rafael/tutorial priority and full unfinished objective: every storyline, earlier unfinished contextual pass, shared shop/town/random exchange, names/roles and remaining prose. Deferred graphics artwork and the later older-record technical re-audit remain separate. All ROMs and earlier translations are preserved. No worker is live.
'''
    mutation=ROOT/'registered_progress_checkpoint_v1'
    checkpoint(mutation=mutation,batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria328 registered and credited once; next clean exchanges start at B96/B98.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,
            proposed_revisions=143,justified_retentions=185,current_batch_registered_andcredited_once=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,
            registered_profile=release['profile'],remaining_native_story_objects=5209,remaining_native_Maria_objects=3404,
            guide_photos=False,next_action='Select complete exchanges from SC3_v7 residual clean packet; save Japanese meanings and independent drafts before current-English comparison.',
            current_batch_evidence=evidence),summary=summary,document='docs/editorial_Maria328_registered_20261109.md',
        document_text=text,completed=20689,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    protocol=Path('docs/build_continuity_protocol.md');before=protocol.read_bytes()
    prefix=('Maria328 is the registered successor to Maria303: 715 entries, 114 accepted layers and 50 checks. '
        'Use `scripts/build_registered_maria328_v2.py` for staging and `scripts/register_maria328_v1.py` for registration. '
        'The pure transaction `dk4tool/patch/maria328_release_v1.py` owns 328 source objects in SC3 B73–B95\'s 21 reviewed blocks. '
        'Apply the existing FE continuation helper once under B87R139, retain both child references and compose both relocation stages. '
        'Keep the source paragraph intact; 314 physical bodies / 321 pages and 15 captions are not additional source credits. '
        'All stored/native/visual/representative checks, exact clean-input reconstruction, own startup and 24 protected getters pass. '
        'Preserve the entire 714-entry predecessor, market allocation/pointers, six-section ARM9, ASCII right-bound correction and v2 source25 guard. '
        'Earlier B54/B62 amendments are already in the predecessor. Main promotion requires acceptance. '
        'Continue from [the registered checkpoint](editorial_Maria328_registered_20261109.md); older entries below are history.\n\n')
    after=prefix.encode()+before;(mutation/'build_continuity_protocol.before').write_bytes(before)
    pending=protocol.with_name('build_continuity_protocol.Maria328.pending.md');assert not pending.exists();pending.write_bytes(after)
    assert protocol.read_bytes()==before;os.replace(pending,protocol)
    save(mutation/'build_protocol_update.json',dict(path=str(protocol),before_sha256=digest(mutation/'build_continuity_protocol.before'),
        after_sha256=digest(protocol),registered_release=str(releasepath),registered_release_sha256=digest(releasepath),no_release_orcredit_change=True))
    print('Published registered Maria328:20,689 integrated;5,209 native story objects remain;main/full scope preserved.')

if __name__=='__main__':main()
