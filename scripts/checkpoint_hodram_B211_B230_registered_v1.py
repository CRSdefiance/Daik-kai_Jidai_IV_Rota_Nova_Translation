"""Save cumulative release, retention pins and the next clean-only intake checkpoint."""
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_hodram_B211_B230_v1 import RELEASE,REGISTRY,PARENT_REGISTRY,CANDIDATE,INVERSE_PATCH
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B231_B250_scope_v1 import SCOPE,ROOT as NEXT
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

def main():
    release,ledger,package,scope=map(load,(RELEASE,LEDGER,PACKAGE,SCOPE))
    registry,parent=map(load,(REGISTRY,PARENT_REGISTRY))
    assert ledger['records_editorially_completed']==17308 and not ledger['full_goal_complete']
    assert ledger['Hodram_B211_B230_clean_next_20261104']['completion_credit_added']==277
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']==digest(CANDIDATE)
    assert digest(REGISTRY)==release['registry_sha256']
    assert registry['latest_promoted_build']==parent['latest_promoted_build'] and registry['accepted_layers']==parent['accepted_layers']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert scope['total_editorial_objects']==225 and len(scope['excluded_credited_records'])==18
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    backup=CANDIDATE.parent/'retention_pins_before_registered_checkpoint.json';assert not backup.exists()
    backup.write_bytes(before)
    for rom in (CANDIDATE,INVERSE_PATCH):
        assert digest(rom)==release['candidate_sha256']
        if not any(Path(v['path']).resolve()==rom.resolve() for v in values):
            values.append(dict(path=str(rom.resolve()),reason='Preserve registered cumulative Hodram B211-B230 and its exact clean-input reconstruction. SHA256 '+digest(rom)))
    pending=pins.with_name('rom_retention_pins.Hodram_B211_B230.pending.json');assert not pending.exists()
    save(pending,values);assert pins.read_bytes()==before;os.replace(pending,pins)
    summary=('Hodram B211–B230 is registered and credited once: 277 reviews, 170 revisions and 107 justified retentions. '
        'Twenty-seven layouts and one FE punctuation wrap improve; four layout candidates are retained. '
        'The cumulative candidate passes 701 manifest entries, 114 accepted layers, 36 release checks, exact clean-input reconstruction and its own startup. '
        'Integrated coverage is 17,308. The next clean intake has 225 eligible objects, excluding 18 completed B237 records. Main is unchanged.')
    doc=f'''# Hodram B211–B230 registered checkpoint

{summary}

- [Cumulative test ROM](../{CANDIDATE.as_posix()})
- [Manifest](../{Path(release['manifest']).as_posix()})
- [Patch from clean Japanese input](../{Path(release['patch']).as_posix()})
- [Registered verification](../{RELEASE.as_posix()})
- [277 integrated decisions and exact source/current/final references](../translations/hodram_B211_B230_integrated_final_review_v1.json)
- [Completed editorial, native display and gameplay scope](editorial_Hodram_B211_B230_research_20261107.md)

Candidate SHA-256: `{release['candidate_sha256']}`. Canonical baseline remains `{release['canonical_base']}`, SHA-256 `{release['canonical_sha256']}`. The patch requires clean input SHA-256 `{release['clean_input_sha256']}`. Both the candidate and the byte-identical clean-input reconstruction are pinned. All earlier ROMs, translations, justified retentions and evidence remain preserved. The existing weekend ZIP and promoted main are unchanged; this is an experimental testing candidate.

The complete verified Rafael5186 predecessor was reused, including all 700 prior manifest entries and 114 accepted layers. The new source-bound SC1 transaction adds one entry and one release check. Only 19 reviewed SC1 blocks differ; control-only B222 remains exact. ARM9, fonts, graphics, names, all other archives and accepted runtime stages are unchanged. The registered ASCII right-bound correction is preserved. Fresh complete-block reconstruction, four-archive format safety, complete predecessor inverse, exact clean-input patch, eight production rejection cases and pure caller preservation pass. The own 4,001-frame ordinary Rafael coldboot matches all ten previously reviewed RGB captures; both original getters return all nine protected names correctly. That startup is separate from Hodram scene coverage.

All 277 individual five-gate reviews pass: 170 revisions and 107 justified retentions. All 270 bodies/284 final pages and seven captions pass native/visual/stored checks; 126 parity-dependent stored pages were rendered fresh and 158 exact planes reused. Four voice objects preserve 29 physical alternatives and all 32 alias slots. All 150 relocated branch cases, 270 pre-macro lookups, 325 archive loads/cache hits, 38 fresh handoffs and 612 exact unchanged parent cases pass. Every newly generated final-layout page was directly viewed. The 23 scoped names are retained with individual source/context reasons; full catalogue UI and the wider name review remain open.

The disclosed Hodram emulator fixture observes 65 utterances/74 ordered pages, 156 complete body planes and 148 complete header planes across 14 selectors. All four FE panels, the FI substitution, four default-role voice selections and representative revised page turns are observed. Thirteen body sheets and the representative menu sheet were viewed. Two distinct menu types have source-key/window-qualified complete live pixels and default highlights. B224's repeated Yes/No menu retains exact offline provider/bytes proofs; it receives no duplicated stable-highlight occurrence credit. The rejected duplicate-pixel attribution and transition-state samples are preserved. The other 205 speech variants are offline-only. Nondefault controller choices/cancellation, natural activation, original locations, earned chronology, battle transitions, full route, full catalogue UI and hardware remain unvisited.

The single B229 R36 heuristic waiver is retained exactly: an ordinary complete-word soft wrap after “horsemen of” keeps all prose on one page and Western Roman Empires intact. The original warning, exact line, source/current/prose bindings and rationale remain in the final review. No glyph, bounds, control, consumption, allocation or pagination check is waived. Two initial suspected name splits were disproved by enlarged native pages/events; two tested layouts were retained because the alternatives read worse. No good prose was shortened to fit.

The [next clean-only scope](../{SCOPE.as_posix()}) covers B231–B250 excluding B237: 209 speeches, 14 physical voice alternatives and two captions across 19 complete blocks; B235 is control-only. All 18 B237 papal-trade source bytes/positions match the already credited review and are excluded from new credit. Raw intake is preserved. No eligible current English has been consulted; all 225 clean meanings, drafts, comparisons, names/terms and display checks remain pending. Continue whole exchanges from this intake without reopening completed B237 or other completed checks.

Every remaining storyline, shared/shop/town exchange, random scene, earlier unfinished contextual pass, name/role label and player-facing resource remains in scope. Rafael's native SC0 census and the known 202 HELP/four Deck priority proofs remain completed; this does not claim a global player-resource census. Keep deferred graphics artwork and the later older-record technical re-audit separate. No guide photos, cleanup or main promotion are part of this checkpoint. The full editorial goal stays active.
'''
    checkpoint(mutation=CANDIDATE.parent/'registered_documentation_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Hodram B211–B230 registered and credited once; next clean B231–B250 scope excludes completed B237.',
            next_action='Read clean Japanese whole exchanges and write meanings/drafts for the 225 eligible objects before consulting current dialogue.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,registered_integration_pending=False,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False),
        additional_updates={'Hodram_B211_B230_clean_next_20261104':dict(registered_integration_pending=False,
            stored_reconstruction_andregistered_release_pending=False,prose_comparison_anddisplay_pending=False),
            'Hodram_B231_B250_clean_next_20261107':dict(source_scope=str(SCOPE),source_scope_sha256=digest(SCOPE),
                total_editorial_objects=225,ordinary_speeches=209,physical_personality_alternatives=14,typed_caption_records=2,
                excluded_exact_previously_credited_records=18,excluded_previously_credited_block=237,
                source_meanings_saved=0,localized_drafts_saved=0,remaining_current_English_comparisons=225,
                new_credit=0,all_five_review_gates_pending=True,no_current_English_dialogue_consulted=True)},
        summary=summary,document='docs/editorial_Hodram_B211_B230_registered_20261107.md',document_text=doc,
        completed=17308,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved registered checkpoint and 225-object clean intake. All earlier credit, main and ROMs preserved.')

if __name__=='__main__':main()
