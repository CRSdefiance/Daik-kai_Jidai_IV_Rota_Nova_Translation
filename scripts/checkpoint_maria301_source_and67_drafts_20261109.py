"""Save remaining-source census and unfinished Maria drafts without release or review credit."""
from collections import Counter
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint


def main():
    root = Path('work/Maria_B0_B32_clean_20261109')
    packet_path = root / 'clean_source_packet.json'
    packet = load(packet_path)
    meaning_paths = [root / f'clean_meanings_{part}_v1.json' for part in ['B0_B10', 'B11_B21', 'B22_B32']]
    meanings = [r for path in meaning_paths for r in load(path)['records']]
    draft_path = root / 'independent_drafts_B0_B10_v1.json'
    drafts = load(draft_path)['records']
    source = {(r['block'], r['id']): r for g in packet['groups'] for r in g['records']}
    bykey = {(r['block'], r['id']): r for r in meanings}
    assert len(source) == len(bykey) == len(meanings) == 301 and source.keys() == bykey.keys()
    for key, original in source.items():
        row = bykey[key]
        assert all(row[k] == v for k, v in original.items()), key
        assert row['source_meaning'].strip() and row['current_English_unconsulted']
        assert row['source_first_independent_meaning_saved'] and not any(row['review'].values())
    assert len(drafts) == len({r['id'] for r in drafts}) == 67
    for row in drafts:
        meaning = bykey[(row['block'], row['id'])]
        assert all(row[k] == v for k, v in meaning.items() if k != 'localized_draft_pending')
        assert row['independent_draft_precedes_current_English_intake'] and not any(row['review'].values())
    assert Counter(r['kind'] for r in meanings) == Counter({
        'ordinary-speech': 292, 'physical-style-alternative': 7, 'typed-menu-caption': 2})
    censuses = {route: Path(f'work/story_source_coverage_20261109_SC{route}_{version}/coverage.json')
        for route, version in [(0, 'v1'), (2, 'v2'), (3, 'v1')]}
    ledger_path = Path('translations/editorial_review_current_v1.json')
    counts = {}
    for route, path in censuses.items():
        report = load(path)
        assert report['ledger_sha256'] == digest(ledger_path)
        assert not report['inventory_failures'] and not report['legacy_source_bindings_not_exact']
        counts[route] = dict(native_objects=len(report['records']), unreviewed=len(report['missing']))
    assert counts == {0: dict(native_objects=6887, unreviewed=0),
        2: dict(native_objects=6720, unreviewed=1805), 3: dict(native_objects=5129, unreviewed=4932)}
    all_meanings = root / 'all301_clean_meanings_v1.json'
    qualification = root / 'source_meanings_and67_drafts_qualification_v1.json'
    assert not all_meanings.exists() and not qualification.exists()
    save(all_meanings, dict(records=meanings, records_count=301, complete_exchanges=32,
        current_English_unconsulted=True, no_source_fields_orwording_changed=True,
        all_five_gates_pending=True, new_credit=0,
        evidence={str(p): digest(p) for p in [packet_path, *meaning_paths]}))
    save(qualification, dict(source_objects=301, complete_exchanges=32,
        source_meanings=301, independent_drafts=67, remaining_independent_drafts=234,
        current_comparisons=0, remaining_current_comparisons=301,
        source_packet=str(packet_path), source_packet_sha256=digest(packet_path),
        all_meanings=str(all_meanings), all_meanings_sha256=digest(all_meanings),
        first_drafts=str(draft_path), first_drafts_sha256=digest(draft_path),
        zero_credited_source_overlap_from_exact_clean_intake=True,
        all_original_source_records_preserved=True, all_five_review_gates_pending=True,
        source_meanings_anddrafts_not_revision_retention_orfinal_approval=True,
        no_new_native_pages_orobserved_gameplay=True, no_new_ROM_orregistry_change=True,
        integrated_completed=19161, story_scope_counts=counts,
        remaining_native_story_objects=6737, shared_UI_scope_not_included=True,
        new_credit=0, full_goal_complete=False,
        evidence={str(p): digest(p) for p in [*censuses.values(), *meaning_paths, draft_path,
            Path('work/Lil_B294_source_binding_20261109_v1/qualification.json'), Path(__file__)]}))
    release = load('work/hodram_residual_release_v1/registered_release_verification.json')
    protected = {'translations/release_stack.json': release['registry_sha256'],
        release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
        release['patch']: release['patch_sha256'],
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'}
    summary = ('Remaining native story coverage is reconciled: Rafael 6,887 exact/zero missing; '
        'Lil 1,805 and Maria 4,932 objects still await completed review. The one Lil legacy reference '
        'is recovered from exact preserved Japanese/control evidence with zero new credit. '
        'The next Maria batch has 301 uncredited objects in 32 complete exchanges, all clean-Japanese '
        'meanings saved and the first 67 independent logical English drafts sealed; 234 drafts and '
        'all 301 current comparisons remain. All five gates and fresh display checks remain pending. '
        'Integrated coverage stays 19,161; registered f166991f, main, all ROMs and full scope are preserved.')
    document_text = '''# Maria301 clean-source and remaining-story checkpoint — November 9, 2026

The full editorial goal remains active. This checkpoint continues the registered Hodram residual release; it does not restart completed Rafael/Hodram work. Rafael and tutorial priority remains preserved, with their completed proofs reused. All shared town/shop/random text, unfinished earlier contextual work, names/roles and remaining prose stay in scope. No guide photos or main promotion.

The exact-position source census covers Rafael SC0 (6,887 objects, zero missing), Lil SC2 (6,720 objects, 1,805 still unreviewed) and Maria SC3 (5,129 objects, 4,932 still unreviewed). Together with the completed SC1 census, this identifies **6,737 native story objects awaiting completed contextual review**. This number excludes remaining shared/UI resources and says nothing about natural event reachability. No inventory or unresolved legacy-binding issues remain in these three reports.

The single Lil B294 R73 legacy row retains all its historical wording, gates and credit. `work/Lil_B294_source_binding_20261109_v1/qualification.json` binds its preserved 48 Japanese bytes, prefix94, clean command636/body641 and native-control proof to the exact source. The original missing metadata and failed separator comparison remain as evidence. Use `scripts/reconcile_remaining_story_sources_v3.py` for this qualified path normalization; do not replay the failed v2 census or credit the row again.

## Current Maria batch

`work/Maria_B0_B32_clean_20261109/clean_source_packet.json` contains **301 uncredited objects in 32 complete exchanges**: 292 ordinary speeches, seven physical voice alternatives and two menu captions. B15 has no text. Numeric block order is not asserted as event chronology; these are encounters, outcomes and linked exchanges, not a newly identified opening sequence. The already reviewed Maria opening and linked B34/B108/B35 work remain intact.

All 301 independent clean-Japanese meanings are saved in `all301_clean_meanings_v1.json`; the first 67 logical American English drafts in eleven complete B0–B10 exchanges are saved in `independent_drafts_B0_B10_v1.json`. Existing conversation English remains unconsulted for this intake. Native literal substitutions pass exact token checks. These are provisional drafts, with names, terms, native consumer binding, comparisons and all five per-record gates still pending. No newly formatted pages or gameplay were approved. There are 234 independent drafts and 301 comparisons left in this batch.

Source findings to preserve include the speculative authenticity debate; Kurushima’s coercive surrender offer directed at Maria; Escante’s self-serving independence rationale; Aziza’s conditional million-gold demand and father’s keepsake; Manuel’s sea/mother elegy without invented bereavement; separate rescue outcomes; uncertainty about the ghost ship; iron plating without steam propulsion; and Kuhn’s false-flag fleet. Maria warned Camille in the latter exchange. Do not invent a direct warning mission to Lil, rename Richard to Robert to reconcile separate encounters, infer kinship from rough addresses, or turn branch alternatives into one simultaneous conversation. The 翔緋鯱 sobriquet and provisional English item/faction names require scoped term binding before final approval.

The compact source/draft qualification is `work/Maria_B0_B32_clean_20261109/source_meanings_and67_drafts_qualification_v1.json`. It binds every original source field, all three meanings files, first drafts, censuses and the Lil qualification. No blanket claim is made about historical exposure to earlier English.

## Continue here

Finish the 234 clean-first independent drafts from B11–B32, preserving complete exchanges, all alternatives and source substitutions. Then bind current native identities, role/name/term consumers and compare all 301 current records contextually, keeping good wording with individual reasons. Reuse proven engine behavior only after matching exact dependencies. The current registered ARM9 has 28 surname data-byte differences from the older source-context runtime; do not call an old whole-ARM9 snapshot a current match. A Maria-specific initialized context is needed where actor3 affects substitutions/roles; the existing isolated-system-unlock recipe is evidence, not earned gameplay or current-ROM proof.

Changed final text needs fresh formatting, all generated-page visual review, stored checks and representative gameplay, followed by registered cumulative integration and exact clean-input reconstruction. Keep offline checks separate from observed scenes. No new release or completion credit is claimed by this checkpoint.

Integrated totals remain **19,161 = 11,532 revisions + 7,629 retentions**. Historical source/prose/draft counters remain 19,164, preserving their preexisting difference of three. Registered candidate remains `work/hodram_residual_release_v1/all_routes_hodram_residual_candidate.nds`, SHA-256 `f166991f83f18859a7483850ccee07945b76993f1ded491dec3b37b7e4ae01d8`; its manifest, exact clean patch, accepted layers and ASCII right-bound correction remain unchanged. Main remains all-routes-unified-v4701. All ROMs, earlier translations, retentions, evidence and failures are preserved. Deferred graphics artwork and later older-record technical re-audit remain separate. No process is live.
'''
    checkpoint(mutation='work/Maria301_source67drafts_checkpoint_20261109',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria SC3 B0–B32:301 meanings/67 independent drafts; all five gates pending.',
            current_batch_not_yet_integrated=True, new_source_meanings=301, new_independent_drafts=67,
            new_current_comparisons=0, all_current_batch_five_gates_pending=True,
            registered_integration_pending=True, build_live=False,
            next_action='Finish234 clean-first Maria drafts, bind names/terms/native context, then compare301 current records and fresh-format final text.',
            guide_photos=False),
        new_entries={
            'remaining_story_source_census_20261109': dict(new_credit=0, counts=counts,
                remaining_native_story_objects=6737, shared_UI_scope_not_included=True,
                evidence={str(p): digest(p) for p in censuses.values()},
                legacy_Lil_B294_binding_qualification='work/Lil_B294_source_binding_20261109_v1/qualification.json'),
            'Maria_SC3_B0_B32_clean_20261109': dict(new_credit=0, source_objects=301,
                ordinary_speeches=292, physical_style_alternatives=7, typed_captions=2,
                complete_exchanges=32, source_meanings=301, independent_drafts=67,
                remaining_independent_drafts=234, current_comparisons=0, remaining_current_comparisons=301,
                qualification=str(qualification), qualification_sha256=digest(qualification),
                all_five_gates_pending=True, native_display_stored_andrepresentative_gameplay_pending=True,
                registered_integration_pending=True, source_meanings_anddrafts_not_final_approval=True)},
        summary=summary, document='docs/editorial_Maria301_source67drafts_20261109.md',
        document_text=document_text, completed=19161, protected=protected)
    print('Saved301 source meanings/67 logical drafts, exact remaining-story census andzero-credit checkpoint. Integrated19161; registered ROM/main unchanged; full goal active.')


if __name__ == '__main__':
    main()
