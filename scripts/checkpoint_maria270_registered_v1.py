"""Save registered progress after once-only credit; preserve B50 and every generated ROM."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

ROOT=Path('work/maria270_release_v1')
SOURCE=Path('work/Maria_B37_B50_clean_20261109')
def main():
    release=load(ROOT/'registered_release_verification.json');done=load(ROOT/'completion_checkpoint.json')
    census=load('work/story_source_coverage_20261109_SC3_v3/coverage.json')
    assert done['new_credit']==270 and done['counts']==dict(completed=19732,revised=11871,retained=7861)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(711,114,46)
    assert not release['own_registered_startup_pending'] and release['registered_market_format_andboth_data_pointers_preserved']
    assert len(census['missing'])==4361 and not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path)
    for value in [release['candidate'],release['exact_clean_reconstruction']]:
        path=Path(value)
        assert digest(path)==release['candidate_sha256']
        assert not any(Path(r['path']).resolve()==path.resolve() for r in pins)
        pins.append(dict(path=str(path.resolve()),reason='Preserve Maria270 registered cumulative candidate/exact clean-input reconstruction. SHA256 '+release['candidate_sha256']))
    (ROOT/'retention_pins.before.json').write_bytes(before)
    pending=pins_path.with_name('rom_retention_pins.Maria270_registered.pending.json');assert not pending.exists()
    save(pending,pins);assert pins_path.read_bytes()==before;os.replace(pending,pins_path)
    save(ROOT/'retention_registration_v1.json',dict(candidate_sha256=release['candidate_sha256'],
        pinned_ROMs=[release['candidate'],release['exact_clean_reconstruction']],no_deletions=True,pins_sha256=digest(pins_path)))
    summary=('Maria270 is registered and credited once: 270 reviews, 161 revisions/109 retentions, 26 wrap improvements '
        'and 272 passing pages. The cumulative candidate retains 711 entries/114 accepted layers, passes 46 release checks, '
        'exact clean-input reconstruction, own Maria/Hangzhou startup and 24 protected getters. The market and ASCII '
        'right-bound fixes remain exact. Integrated totals are 19,732; native story objects remaining are 6,166. '
        'Main is unchanged. Next resolve the separately preserved B50 long-FE issue; full editorial scope remains active.')
    text=f'''# Maria270 registered checkpoint — November 9, 2026

**270 contextual reviews are integrated exactly once: 161 revisions and 109 justified retentions in 13 complete B37–B49 exchanges.** Twenty-six wrap improvements, six justified layout retentions and four reclaimed pages preserve all prose. Every one of the 272 final body pages, four captions and 28 scoped names/42 strings has current native and direct visual approval.

Candidate: [all_routes_maria270_candidate.nds](../{release['candidate'].replace(chr(92),'/')}), SHA-256 `{release['candidate_sha256']}`.
Clean-input patch: [all_routes_maria270_candidate.xdelta](../{release['patch'].replace(chr(92),'/')}), SHA-256 `{release['patch_sha256']}`.
Manifest: `{release['manifest']}`, SHA-256 `{release['manifest_sha256']}`.
Registry SHA-256: `{release['registry_sha256']}`.

The registered profile is `{release['profile']}`. It retains the exact 710-entry market-corrected prefix and all 114 accepted layers, then adds the reviewed SC3 transaction as entry711/check46. Only the 13 reviewed SC3 blocks change. All six ARM9 sections, the 16-byte market literal at01FFD000, both Local/Cargo pointers, original town-capture opcode, ASCII right-bound repair, other story routes, names, UI and artwork remain byte-exact to the parent. Whole source/current block, archive and serialized NDS inverses pass. Applying the patch to clean input `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` reconstructs the whole candidate exactly.

The original four-archive format check detected two Abraham speaker controls whose indices shifted after the corrected B38 choice. Their exact source records44/52 and final records43/51 are now independently bound to full native preambles, offsets, record bytes and block hashes. All five prior SC0 bindings remain unchanged. All four malformed/nonleading command cases reject. The detector is unchanged, and the manifest discloses the multi-archive receipt and handler. Use `scripts/build_registered_maria270_v2.py` and follow [build continuity](build_continuity_protocol.md); an SC0-only format adapter is insufficient for this profile. Early schema, fixture and negative-test producer failures are preserved; no guards were waived and no production text was altered to bypass them.

The candidate's own 31,000-frame Maria New Game reaches Hangzhou using ordinary inputs and the disclosed existing system-only unlock. Its six key captures are directly viewed; three opening/town frames exactly match the previously approved RGB. The complete staged payload, protected data, captain3/route3 and nonmutating original getters pass. Both original name getters return all12 protected names from this candidate's own RAM. This is emulator evidence; the unlock is not earned, and optional late story events, full catalogue UI and hardware remain unvisited.

Reuse [the research checkpoint](editorial_Maria270_research_20261109.md) for all exact source meanings, independent drafts, contextual decisions, individual references and stored proofs. All266 bodies/272 pages, four captions, 480 native relocated branches, 266 pre-macro catalogue lookups, 303 full SC3 loads/cache hits and606 native handoffs pass. Only parity-dependent pages were rerendered. Four representative coldboots observe63 distinct utterances/69 distinct pages, all six two-page cases, the FE-to-named transition, eight headers, both menus/default A returns and resupply/departure/sailing. All generated pages are directly viewed. The203 unvisited bodies retain offline-only credit; conditional alternatives are disclosed display fixtures, not naturally activated story outcomes. No guide photos.

`translations/maria270_integrated_final_review_v1.json` and `exact_integrated_record_bindings.json` bind each final record to its registered offset and five gates. `completion_checkpoint.json` proves once-only credit with all earlier ledger keys and record prefixes preserved. The technical market release contributed no editorial credit; its exact ancestry is reconciled before this append. `work/story_source_coverage_20261109_SC3_v3/coverage.json` rechecks all5129 clean SC3 object positions without replaying the native census:768 are covered and4361 remain, with zero duplicate credit or legacy-binding failures.

Integrated totals are **19,732 = 11,871 revisions + 7,861 retentions**. Native story scope remaining is **6,166: Lil1,805 and Maria4,361**; shared town/shop/random/UI and other prose are tracked separately. The historical meaning/prose/draft counter remains three higher at19,735. Main `all-routes-unified-v4701`, canonical input, every previous profile, all ROMs, translations, drafts, failures and evidence remain preserved. The new candidate and inverse reconstruction are pinned. No main promotion or Git push occurred.

**Next: complete B50’s separate long-FE display work.** All16 Japanese meanings, independent drafts and contextual decisions (nine revisions/seven retentions) remain intact; none are credited or shipped by this pass. `FE_row_diagnostic_v1.json` preserves the generic38-cell failure and guarded36/37 limitations. Keep this text-display issue in the editorial goal, avoid shortening sound prose merely to fit, and reuse completed B37–B49 checks. All unfinished storylines, prior contextual passes, town/shop/random exchanges, names, wraps/glyphs and remaining player prose remain in scope. Deferred graphics artwork and the later older-record technical re-audit stay separate. No process is live at this checkpoint.
'''
    testing=ROOT/'testing_handoff.md';assert not testing.exists()
    testing.write_text(f'''# Translation DS testing candidate

[ROM](all_routes_maria270_candidate.nds) · [manifest](all_routes_maria270_candidate.manifest.json) · [clean-input patch](all_routes_maria270_candidate.xdelta)

SHA-256 `{release['candidate_sha256']}`. Cumulative registered test candidate; main is unchanged. Includes the Trade/Goods Info repair and270 additional contextual Maria reviews. Use a copy of your existing save with the matching new ROM basename and preserve the original save.

All accepted layers and runtime fixes are retained. Representative emulator checks pass; late source conditions and hardware remain unvisited. The held B50 long-FE exchange is not included. See [full review and evidence](../../docs/editorial_Maria270_registered_20261109.md).
''',encoding='utf-8',newline='\n')
    checkpoint(mutation=ROOT/'registered_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria270 registered andcredited once;resolve held B50 next.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Resolve complete B50 long-FE layout frompreserved source/prose andconcrete native diagnostic;thencontinue disjoint unfinished exchanges.'),
        additional_updates={'Maria_SC3_B37_B50_clean_20261109':dict(new_credit=0,
            integrated_complete_exchange_subset=270,subset_integrated_family=done['family'],
            subset_registered_candidate=release['candidate'],subset_registered_candidate_sha256=release['candidate_sha256'],
            withheld_complete_exchange=50,withheld_records=16,registered_integration_pending=True)},
        summary=summary,document='docs/editorial_Maria270_registered_20261109.md',document_text=text,completed=19732,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Savedregistered Maria270 progress:19,732 integrated/6,166 native story objects remain;main unchanged;B50 preserved.')
if __name__=='__main__':main()
