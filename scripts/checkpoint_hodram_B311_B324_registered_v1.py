"""Document already credited B311-B324 without replaying checks or changing ROMs."""
import os
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

OUT = Path('work/hodram_B311_B324_release_v1')
ROOT = Path('work/Hodram_B311_B324_clean_20261107')
RELEASE = OUT/'registered_release_verification.json'
REGISTRY = Path('translations/release_stack.json')


def main():
    release = load(RELEASE)
    completion = load(OUT/'completion_checkpoint.json')
    assert completion['new_credit'] == 400
    assert completion['counts'] == dict(completed=18767, revised=11311, retained=7456)
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (706, 114, 41)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert digest(REGISTRY) == release['registry_sha256']
    assert digest(release['manifest']) == release['manifest_sha256']
    for key in ['candidate', 'exact_clean_reconstruction']:
        assert digest(release[key]) == release['candidate_sha256']
    registry = load(REGISTRY)
    old = load(OUT/'release_stack_before_Hodram_B311_B324.json')
    assert registry['latest_promoted_build'] == old['latest_promoted_build']
    assert registry['accepted_layers'] == old['accepted_layers']
    assert all(registry['profiles'][k] == v for k, v in old['profiles'].items())
    assert set(registry['profiles']) - set(old['profiles']) == {release['profile']}
    pins = Path('translations/rom_retention_pins.json')
    before = pins.read_bytes()
    values = load(pins)
    backup = OUT/'retention_pins_before_registered_checkpoint.json'
    assert not backup.exists()
    backup.write_bytes(before)
    for key in ['candidate', 'exact_clean_reconstruction']:
        rom = Path(release[key])
        if not any(Path(v['path']).resolve() == rom.resolve() for v in values):
            values.append(dict(path=str(rom.resolve()), reason='Preserve registered cumulative Hodram B311-B324 and exact clean-input reconstruction. SHA256 '+digest(rom)))
    pending = pins.with_name('rom_retention_pins.Hodram_B311_B324.pending.json')
    assert not pending.exists()
    save(pending, values)
    assert pins.read_bytes() == before
    os.replace(pending, pins)
    summary = ('Hodram B311–B324 is registered and credited once: 400 reviews, 175 revisions and 225 justified retentions. '
        'Twenty-seven layouts and ten punctuation glyph targets improve; 12 layouts are retained with reasons. '
        'All 389 stored pages pass. Two bounded emulator runs observe 189 utterances/191 pages and six menus, with both returns verified. '
        'The cumulative candidate passes 706 manifest entries, 114 accepted layers, 41 release checks, exact clean-input reconstruction and its own startup. '
        'Integrated coverage is 18,767. Main is unchanged. Next reconcile remaining native source coverage before selecting a disjoint clean-source batch.')
    document = f'''# Hodram B311–B324 registered checkpoint

{summary}

- [Experimental cumulative ROM](../{Path(release['candidate']).as_posix()})
- [Manifest](../{Path(release['manifest']).as_posix()})
- [Clean-input patch](../{Path(release['patch']).as_posix()})
- [Registered verification](../{RELEASE.as_posix()})
- [400 integrated decisions and exact references](../translations/hodram_B311_B324_integrated_final_review_v1.json)
- [Completed research gates](../{ROOT.as_posix()}/research_final_v1/research_completion.json)
- [Once-only credit](../{OUT.as_posix()}/completion_checkpoint.json)

Candidate SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. Clean input: `{release['clean_input_sha256']}`. Canonical baseline remains `{release['canonical_base']}`, SHA-256 `{release['canonical_sha256']}`. All 705 predecessor entries, 114 accepted layers, prior profiles and registered ASCII right-bound correction are preserved. Only SC1 blocks 311–324 change. ARM9, fonts, names, artwork, all other files and components remain exact. The whole parent inverse, eight malformed-scope rejection cases, all four archive format guards and clean-input reconstruction pass. The candidate's own 4,001-frame Rafael startup matches ten existing capture pairs; both original getters verify all nine protected names. Main and the weekend package are unchanged.

The [offline checkpoint](editorial_Hodram_B311_B324_offline_20261107.md) retains the clean-source findings and individual retention reasons. All 400 five-gate decisions pass: 151 ordinary speeches, 236 physical voice alternatives in 38 commands and 13 captions in six menus. Source speaker/layout controls, actor zero and FI/FE behavior are preserved. No prose is shortened to fit or given ordinary authored line breaks. Twenty-seven selected layouts improve; 12 overconstrained alternatives retain the better layouts with reasons. Ten ASCII question/silence targets pass. Eleven scoped names are retained with reasons; 22 original getters and ten distinct progressive name strings are checked. Wider catalogue UI remains unvisited.

Offline checks cover 387 bodies/389 final pages, 304 personality slots, 495 relocated branch cases, all 387 complete native catalogue lookups, 325 archive loads/cache hits and 650 handoffs. All generated initial/final page sheets, changed trial pages and scoped menu/name sheets were directly viewed. Exact compatible technical evidence is reused and identified in the research receipts; changed text receives fresh formatting checks.

The [bounded observation set](../{ROOT.as_posix()}/bounded_combined_v1/fixture_set.json) comprises two initialized sequences: 57,202 frames, 189 utterances/191 pages and all six menus. All 151 ordinary speeches and 38 complete style commands display at original startup assignments; the other 198 physical style alternatives remain offline-only. Fourteen FE notices, three macro speeches including null-actor FI injury/treatment, source actor zero, 17 source header selectors and two multi-page passages are observed. All 398 complete body holds and 370 header holds match native planes and blank guards. All 191 pages on 16 readable sheets, the six-menu sheet and both return screens were directly viewed. Both sequences return to the original following resupply dialogue without undefined instructions. Menu index zero is observed; other choices/cancel retain offline proofs. These are synthetic native display sequences, not original conditional-scene activation, natural route completion or hardware tests. Rewards, chronology and future party assignments are unvisited.

The [source occurrence receipt](../{ROOT.as_posix()}/source_occurrence_resolution_v2.json) corrects one metadata-only fixture binding: byte-identical B313 commands at source offsets 856 and 1252 have distinct stored offsets 922 and 1308. The emitted ROM and actual observations were correct. Original fixture files, ROMs, observations and failed join are preserved. The joined evidence explicitly binds original source occurrences; no identity is inferred from similar pixels. Future fixtures use `prepare_hodram_display_fixtures_bounded_v2.py`. Reuse the frozen native QA capacity proof: these fixtures are 7,856/7,380 bytes, under the 9,216-byte bound. Production blocks are at most 3,048 bytes. No capacity trace or completed gameplay needs repeating.

Integrated totals are 18,767: 11,311 revisions and 7,456 justified retentions. Historical source/prose/draft counters remain 18,770, preserving their preexisting difference of three. Every prior family and record prefix survives; this documentation adds zero credit. All ROMs, earlier translations, evidence and failed experiments are preserved. No process remains live.

Block 324 ends the native SC1 archive, but numerical position alone does not establish complete contextual coverage. Next reconcile exact clean source positions/bytes against integrated review references across remaining scope, respecting historical alternate identifiers. Select complete unreviewed exchanges, then seal clean meanings and drafts before reading eligible current English. Do not restart completed batches or declare a route complete from block numbers alone.

The full objective stays active across every storyline, unfinished earlier contextual pass, shared town/shop/random dialogue, names and remaining player-facing prose, retaining Rafael/tutorial priority. Deferred graphics artwork and the later older-record technical re-audit remain separate. No guide photos or main promotion.
'''
    package = load(PACKAGE)
    checkpoint(mutation=OUT/'registered_documentation_checkpoint_v1',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,
            current_batch='Hodram B311–B324 registered; 400 reviews credited once. Next: exact remaining-source census.',
            next_action='Reconcile clean native source coverage against integrated references; select disjoint complete exchanges and seal clean meanings/drafts before current-English intake.',
            current_batch_not_yet_integrated=False, all_current_batch_fifth_gates_pending=False,
            registered_integration_pending=False, native_job_live=False, registered_build_live=False,
            registered_cumulative_build_live=False, guide_photos=False),
        summary=summary, document='docs/editorial_Hodram_B311_B324_registered_20261107.md',
        document_text=document, completed=18767,
        protected={str(REGISTRY):release['registry_sha256'], release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'], release['patch']:release['patch_sha256'],
            package['zip']:package['zip_sha256']})
    save(OUT/'final_checkpoint_audit_v1.json', dict(release=str(RELEASE), release_sha256=digest(RELEASE),
        ledger_sha256=digest('translations/editorial_review_current_v1.json'),
        main_accepted_layers_andall_prior_profiles_exact=True, counts=completion['counts'],
        all_prior_progress_translations_evidence_andROMs_preserved=True, full_goal_complete=False,
        next_action='Exact remaining-source census; clean-first next scope. No restart of completed proofs.', new_credit=0))
    print('Saved registered checkpoint: 18,767 integrated reviews; main unchanged; full objective active.')


if __name__ == '__main__':
    main()
