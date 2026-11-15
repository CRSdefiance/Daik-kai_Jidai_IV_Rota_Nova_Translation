"""Publish the verified cumulative release, concise coverage andnext clean-only intake."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

ROOT = Path('work/maria303_release_v1')
RESEARCH = Path('work/Maria_B58_B70_clean_20261109')
NEXT = Path('work/Maria_B73_B95_clean_20261109')


def main():
    release_path = ROOT/'registered_release_verification.json'
    done_path = ROOT/'completion_checkpoint.json'
    census_path = Path('work/story_source_coverage_20261109_SC3_v6/coverage.json')
    actual_path = RESEARCH/'gameplay_review_v1.json'
    ready_path = RESEARCH/'research_final_v1/research_completion.json'
    release, done, census, actual, ready = map(load, [release_path, done_path, census_path, actual_path, ready_path])
    assert done['new_credit'] == 303 and done['counts'] == dict(completed=20361, revised=12245, retained=8116)
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (714,114,49)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert release['registered_market_format_andboth_data_pointers_preserved']
    assert len(census['records']) == 5129 and len(census['missing']) == 3732
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert (actual['distinct_source_utterances'], actual['distinct_body_pages'], actual['offline_only_source_utterances']) == (116,116,183)
    assert ready['all_individual_five_gates_pass'] and ready['records'] == 303
    assert digest('translations/release_stack.json') == release['registry_sha256']
    registry = load('translations/release_stack.json')
    prior = load(ROOT/'release_stack_before_Maria303.json')
    assert registry['latest_promoted_build'] == prior['latest_promoted_build']
    assert registry['accepted_layers'] == prior['accepted_layers']
    assert all(registry['profiles'][k] == v for k,v in prior['profiles'].items())
    selection_path = NEXT/'source_selection_v1.json'
    packet_path = NEXT/'clean_source_packet.json'
    selected, packet = map(load, [selection_path, packet_path])
    assert packet['source_only_not_current_English'] and packet['records'] == selected['source_objects'] == 328
    assert selected['complete_exchanges'] == 21 and selected['no_current_English_read_orapproval']
    assert selected['no_meanings_drafts_orlocalization_approval_yet']
    testing = ROOT/'testing_handoff.md'
    assert not testing.exists()
    testing.write_text(f'''# Translation DS cumulative test candidate

[ROM](all_routes_maria303_candidate.nds) · [clean-input patch](all_routes_maria303_candidate.xdelta) · [manifest](all_routes_maria303_candidate.manifest.json)

SHA-256 `{release['candidate_sha256']}`. Includes the Trade/Goods Info fix and all registered work through Maria B58–B70. Main is unchanged. Preserve your original save and use a copy with the matching ROM basename.

Native checks, representative emulator review, exact clean-input reconstruction and own startup pass. Original late-event activation and hardware remain unvisited. [Coverage and evidence](../../docs/editorial_Maria303_registered_20261109.md).
''', encoding='utf-8', newline='\n')
    summary = ('Maria303 is registered and credited once: 181 revisions/122 justified retentions, seven wrap improvements, '
        'two reclaimed pages and one mixed-width letter correction. All299 body pages/four captions/24 name strings pass; '
        '116 pages andboth menus are observed in representative emulator QA. The cumulative714-entry/114-layer candidate '
        'passes49 checks, exact clean-input reconstruction, own startup and24 protected getters. Integrated20,361; '
        '5,537 native story objects remain. Next328 clean-only objects in21 complete exchanges are selected; alltheir '
        'meanings/drafts/comparisons/gates remain pending. Main andfull editorial scope are unchanged.')
    text = f'''# Maria303 registered checkpoint — November 9, 2026

**303 source objects are integrated and credited once: 181 revisions and 122 justified retentions.** All five individual gates pass. The ten complete exchanges are SC3 blocks58/59/60/61/62/64/65/66/68/70. Seven wrap improvements reclaim two pages while preserving every word. One full-width I is corrected; all18 prior non-ASCII targets, including ten formerly Japanese sailor speeches, pass native glyph checks. The20 scoped name/role retentions include24 distinct short/full strings; wider name review remains open.

Registered cumulative [ROM](../work/maria303_release_v1/all_routes_maria303_candidate.nds), SHA-256 `{release['candidate_sha256']}`; [clean-input patch](../work/maria303_release_v1/all_routes_maria303_candidate.xdelta), SHA-256 `{release['patch_sha256']}`. The patch reconstructs the exact ROM from clean `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`. The [manifest](../work/maria303_release_v1/all_routes_maria303_candidate.manifest.json) retains all713 predecessor entries and114 accepted layers andpasses49 checks. Own31,000-frame Maria/Hangzhou startup, RAM identity andboth getters for12 protected actors pass. Main is unchanged; no promotion, cleanup or Git push occurred.

Reuse [the offline checkpoint](editorial_Maria303_offline_20261109.md) and `work/Maria_B58_B70_clean_20261109/research_final_v1/research_completion.json`. All299 final speech pages, four menu captions and24 name strings were directly reviewed. Stored checks cover491 commands,24 relative sites/120 native branch cases, all299 original catalogue bodies,303 SC3 loads/cache hits and606 parent handoffs. Only146 parity-dependent stored pages needed fresh execution;153 exact pages were reused. Five final layout refinements required20 fresh alignment cases; the1196-case final selection reuses1176 exact cases. No completed source inventory or unchanged native page review was repeated.

`gameplay_review_v1.json` binds **116 distinct utterances/pages**,232 complete body timing holds and214 header holds across two emulator runs. All116 pages were directly viewed on ten readable sheets; two full-scene sheets, both menus/four captions andsix resupply/departure/sailing captures were also viewed. Representative cases include labeled FE boy dialogue andnamed portrait returns, fear comparisons, the corrected I andnormal F, both reclaimed one-page explanations, the sailor belief branch andcomplete tomato/banana/meal-payer exchanges. Both menus show cursor0 andordinary A return to the next copied speech. Other menu indices, cancellation/numeric return registers anddisbelief/stat outcomes are offline-only. **183 bodies remain offline-only.** These are disclosed initialized Hangzhou QA fixtures, with an existing system-only unlock that is not earned; original scene conditions, locations, chronology, effects, full routes/catalogue UI andhardware remain unvisited. No guide photos.

The pure production transaction is `dk4tool/patch/maria303_release_v1.py`; the registered driver is `scripts/build_registered_maria303_v1.py`. It extends registered Maria310 `465cb3c3…` andchanges only the ten owned SC3 blocks. Source/current controls, runtime substitutions, menus, allocation, complete block/archive/serialized-ROM inverses andfour-archive source25 guard pass. An exact historical B62R53 source/current terminator shift has a qualified owner-specific inverse span in `dk4tool/script/maria303_source_alignment_v1.py`: semantic Japanese bytes stay unchanged, the original38-byte command is preserved andfour malformed ownership cases are rejected. Eight production-scope negatives pass. This is storage reconstruction bookkeeping, not another runtime orfont change. Preserve the earlier B54R507 amendment in the parent; do not apply it again to this disjoint batch. Market allocation/pointers, six-section ARM9, ASCII right-bound correction, fonts, graphics andall other files/components remain exact.

`translations/maria303_integrated_final_review_v1.json` and `work/maria303_release_v1/exact_integrated_record_bindings.json` bind every clean/current/final reference, individual finding, revision/retention andfive gates. `completion_checkpoint.json` proves once-only credit andpreservation of earlier ledger keys/prefixes. Integrated totals are **20,361 =12,245 revisions +8,116 retentions**; historical source/prose/draft counts remain three higher at20,364. The SC3_v6 census rechecks all5,129 exact source positions using the completed native inventory:1,397 covered/3,732 remaining, zero duplicate orunresolved bindings. Remaining native story objects: **5,537 (Lil1,805/Maria3,732)**. Other shared town/shop/random/UI andremaining player prose stay separately in scope; this is not a full player-facing orreachability census.

**Next:328 clean-only objects in21 complete exchanges, B73–B95**, under `work/Maria_B73_B95_clean_20261109/clean_source_packet.json` and `source_selection_v1.json`. Exact clean source positions anddisjointness are checked. No current English, meanings, independent drafts, contextual decisions orreview gates are claimed yet. Start with clean Japanese meanings andlogical English drafts before current-English comparison; keep individual findings/retentions, names/roles, full-width automatic wraps andglyph/control review. Continue the full unfinished objective efficiently; earlier translations still need their unfinished contextual pass. Integrate passing batches over this registered successor, preserving all runtime fixes andaccepted layers. Deferred graphics artwork andthe later older-record technical re-audit remain separate. All ROMs, earlier translations andevidence are preserved. No process is live at this checkpoint.
'''
    evidence = {str(p):digest(p) for p in [release_path, done_path, census_path, actual_path, ready_path,
        testing, selection_path, packet_path, Path(__file__)]}
    checkpoint(mutation=ROOT/'registered_progress_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria303 registered;next328 clean objects/21 complete exchanges selected.',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True,
            proposed_revisions=0, justified_retentions=0, native_job_live=False, registered_build_live=False, guide_photos=False,
            next_action='Save clean Japanese meanings and independent logical drafts for Maria B73–B95 before current English.',
            registered_checkpoint_evidence=evidence),
        new_entries={'Maria_SC3_B73_B95_clean_20261109':dict(new_credit=0, source_objects=328, complete_exchanges=21,
            source_packet=str(packet_path), source_packet_sha256=digest(packet_path), all_exact_clean_positions_checked=True,
            source_only_no_current_English_read=True, meanings_drafts_contextual_comparisons_andall_five_gates_pending=True,
            native_inventory_compatible_proof_reused_not_replayed=True, actual_gameplay_observations=0,
            registered_integration_pending=True, guide_photos=False)},
        summary=summary, document='docs/editorial_Maria303_registered_20261109.md', document_text=text, completed=20361,
        protected={'translations/release_stack.json':release['registry_sha256'], release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'], release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256']})
    continuity = Path('docs/build_continuity_protocol.md')
    before = continuity.read_bytes()
    backup = ROOT/'continuity_before_Maria303.md'
    assert not backup.exists()
    backup.write_bytes(before)
    prefix = ('Maria303 is the registered successor to Maria310:714 entries/49 checks,114 accepted layers. '
        'Use `scripts/build_registered_maria303_v1.py` andthe exact pure303-record transaction. OnlySC3 '
        'B58/59/60/61/62/64/65/66/68/70 change; retain the B62R53 qualified source inverse alignment span. '
        'No new FE continuation orB54 amendment is applied. Whole source/current/block/archive/NDS inverses, '
        'all299 stored/effective bodies,120 native relative cases,303 loads/606 handoffs,all299 page/four-caption '
        'approvals andrepresentative116-page/two-menu QA pass. Preserve the713-entry parent,114 accepted layers, '
        'market pointers/read-only allocation,six-section ARM9,ASCII right-bound correction andv2 source25 guard. '
        'Exact clean-input patch,own startup and24 protected getters pass before registration/credit. '
        'Main promotion requires acceptance. Continue from [the registered checkpoint](editorial_Maria303_registered_20261109.md); '
        'preceding workflow entries below are preserved history.\n\n').encode('utf-8')
    staged = continuity.with_name('build_continuity_protocol.Maria303.pending.md')
    assert not staged.exists() and continuity.read_bytes() == before
    staged.write_bytes(prefix+before)
    assert staged.read_bytes() == prefix+before
    os.replace(staged, continuity)
    save(ROOT/'continuity_checkpoint.json', dict(before_sha256=digest(backup), after_sha256=digest(continuity),
        all_previous_document_bytes_preserved=True, new_credit=0))
    print('Published Maria303 registered checkpoint;20,361 integrated;5,537 native story objects remain;full scope active.')


if __name__ == '__main__':
    main()
