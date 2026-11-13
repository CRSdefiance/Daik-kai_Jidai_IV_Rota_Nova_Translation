"""Publish the registered cumulative handoff and remaining exact source scope without new credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

OUT = Path('work/maria301_release_v1')
ROOT = Path('work/Maria_B0_B32_clean_20261109')
RELEASE = OUT/'registered_release_verification.json'
REGISTRY = Path('translations/release_stack.json')
CENSUS = Path('work/story_source_coverage_20261109_SC3_v2/coverage.json')


def main():
    release,completion,census = map(load,[RELEASE,OUT/'completion_checkpoint.json',CENSUS])
    assert completion['new_credit'] == 301 and completion['counts'] == dict(completed=19462,revised=11710,retained=7752)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks']) == (709,114,44)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']
    assert census['ledger_sha256'] == completion['ledger_after_sha256']
    assert len(census['records']) == 5129 and len(census['missing']) == 4631
    assert census['new_exact_bindings'] == 301 and census['previous_exact_bindings_reused'] == 197
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    pins = Path('translations/rom_retention_pins.json');before = pins.read_bytes();values = load(pins)
    for field in ['candidate','exact_clean_reconstruction']:
        path = Path(release[field]);absolute = str(path.resolve())
        if not any(Path(p['path']).resolve() == path.resolve() for p in values):
            values.append(dict(path=absolute,reason='Preserve Maria301 registered cumulative release/clean-input reconstruction. SHA256 '+digest(path)))
    if values != load(pins):
        (OUT/'pins.before.registered.json').write_bytes(before)
        pending = pins.with_name('rom_retention_pins.Maria301.pending.json');assert not pending.exists()
        save(pending,values);assert pins.read_bytes() == before
        __import__('os').replace(pending,pins)
    summary = ('Maria301 is registered and credited once: 301 reviews, 178 revisions/123 retentions, '
        '35 wrap improvements and 303 passing pages. The cumulative candidate retains 709 entries/114 accepted layers '
        'and passes 44 release checks, exact clean-input reconstruction, its own Maria/Hangzhou coldboot '
        'and 12 protected-name getters. Integrated totals are 19,462; native story objects remaining are 6,436. '
        'Main is unchanged; continue with the next clean, disjoint exchange batch.')
    text = f'''# Maria301 registered cumulative checkpoint — November 9, 2026

{summary}

Experimental testing candidate: [{Path(release['candidate']).name}](../{Path(release['candidate']).as_posix()}), SHA-256 `{release['candidate_sha256']}`.
[Manifest](../{Path(release['manifest']).as_posix()}) SHA-256 `{release['manifest_sha256']}`.
[Clean-input patch](../{Path(release['patch']).as_posix()}) SHA-256 `{release['patch_sha256']}` reconstructs the complete candidate from `work/clean.nds`, SHA-256 `{release['clean_input_sha256']}`, byte for byte.
The canonical construction baseline remains `{release['canonical_base']}`, SHA-256 `{release['canonical_sha256']}`. Main remains all-routes-unified-v4701; no promotion occurred.

The [registered verification](../{RELEASE.as_posix()}) preserves the whole 708-entry predecessor prefix and appends the 301-record SC3 transaction. All 114 accepted layers, earlier runtime/name/tutorial/graphics corrections and the ASCII right-bound correction remain. Only 32 SC3 blocks change; ARM9 and every other file/component remain exact. Complete archive and serialized parent inverses pass. All four final story-format checks run fresh. Eight malformed production scopes are rejected without caller mutation.

Reuse [the completed research](editorial_Maria301_research_20261109.md): 178 dialogue revisions/123 justified retentions, 36 scoped names, 35 wrap improvements, two layout retentions and one page reclaimed without shortening prose. All 303 final offline pages, 44 name strings and two captions were directly viewed. Stored checks pass all bodies, 635 branch cases, 299 catalogue lookups, 303 complete loads and 606 parent handoffs. The mixed I and eleven punctuation targets are checked. The whole caption source reference replaces a missing legacy offset alias in the versioned release adapter; all original guards remain. Preserve the rejected first preparation.

Representative display QA observes 92 distinct utterances/96 pages, 14 headers, the B29 default menu/A return and B32 default voice 4. All selected native planes match. Twelve reviewed QA sheets and focused resupply/departure/sailing frames are bound in `work/Maria_B0_B32_clean_20261109/gameplay_review_v1.json`. The other 207 bodies, six alternative lookout voices, other menu states/cancellation/numeric returns and original conditional branches remain offline-only. The prefix/tail-only QA exits are retained as diagnostics; the source-complete 47-nonspeech-command host reaches ordinary sailing. This adjusted the QA fixture, not production dialogue or engine code.

The candidate's own fresh 31,000-frame Maria coldboot reaches Hangzhou with ordinary controller inputs and the existing isolated system unlock, not earned progression. All six key frames were viewed; the three opening/town frames match the earlier reviewed RGB exactly. Native captain3/route3, the complete 123,264-byte staged payload, protected data and unowned memory checks pass. Both original getters return all 12 protected names from this candidate's own RAM. The first native load failed before any emulated frame; a fresh minimal harness process passes. No causal diagnosis beyond that scope is claimed. No savestate, historical RAM overlay, forced story/location/RNG/funds/outcome, full-route, full catalogue UI or hardware claim.

The [completion receipt](../{OUT.as_posix()}/completion_checkpoint.json) credits 301 disjoint source keys once and preserves every earlier record prefix and unrelated ledger key. Integrated totals are **19,462 = 11,710 revisions + 7,752 retentions**. Historical source/prose/draft counters are 19,465, retaining the preexisting difference of three. This documentation adds zero credit. All ROMs, translations and earlier evidence remain; current candidate and clean reconstruction are pinned.

The [SC3 source reconciliation](../{CENSUS.as_posix()}) checks all 5,129 clean positions and reuses the exact native inventory. It binds 498 reviewed objects, including these 301, and leaves 4,631. Lil still has 1,805 native objects remaining: **6,436 native story objects total**, with shared town/shop/random and remaining player-facing prose tracked separately. Rafael/SC0 and Hodram/SC1 native dialogue-object censuses remain covered; this is not a claim that every shared resource or the full editorial goal is finished.

Next continue with clean Japanese for disjoint complete Maria exchanges, beginning at B37; B37–B50 contains a practical 286-object batch. Numeric adjacency is not event chronology: resolve necessary linked source context and names before current-English comparison. Reuse this candidate's own Maria3 startup snapshot and exact current renderer/font dependencies. Do not repeat completed source/prose/native/visual/gameplay/release checks. Keep the full scope active, including unfinished earlier translations, other storylines, shared dialogue, names, premature wraps and remaining prose. No guide photos. Deferred graphics artwork and the later older-record technical re-audit remain separate. No process is live.
'''
    evidence = {str(p):digest(p) for p in [RELEASE,OUT/'completion_checkpoint.json',CENSUS,
        OUT/'own_registered_startup_verification.json',OUT/'own_registered_name_getters_v1.json',Path(__file__)]}
    checkpoint(mutation=OUT/'registered_documentation_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria301 registered;301 credited once;19462 total;6436 native story objects remain.',
            next_action='Clean source-first Maria B37-B50 complete exchanges, linked context and names; then current English andfresh formatting using own current Maria3 runtime.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False,evidence=evidence),
        new_entries={'Maria_SC3_source_coverage_after301_20261109':dict(new_credit=0,native_objects=5129,
            exact_reviewed=498,missing=4631,inventory_failures=0,legacy_source_binding_issues=0,
            coverage=str(CENSUS),coverage_sha256=digest(CENSUS),native_inventory_reused_not_replayed=True,
            remaining_native_story_objects_including_Lil=6436,shared_UI_scope_separate=True,full_goal_complete=False)},
        summary=summary,document='docs/editorial_Maria301_registered_20261109.md',document_text=text,
        completed=19462,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256']})
    print('Saved709-entry registered handoff;19462 integrated,6436 native story objects remain;main unchanged.')


if __name__ == '__main__':main()
