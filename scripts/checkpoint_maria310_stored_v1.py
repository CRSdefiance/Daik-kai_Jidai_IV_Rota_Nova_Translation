"""Save the exact completed storage checkpoint without new editorial credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    reconstruction=ROOT/'reconstruction_v2/reconstruction.json'
    stored_path=ROOT/'stored_v3/stored_native_verification.json'
    catalogue_path=ROOT/'stored_catalogue_all_v2/all310_stored_effective_body_bindings.json'
    loader_path=ROOT/'loaders_v2/verification.json';selection=ROOT/'display_selection_v2.json'
    r,s,c,l=map(load,[reconstruction,stored_path,catalogue_path,loader_path])
    assert s['reconstruction_sha256']==l['reconstruction_sha256']==digest(reconstruction)
    assert c['stored_sha256']==digest(stored_path)
    assert len(s['records'])==len(c['records'])==310 and s['complete_stored_pages']==318
    assert s['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert s['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (l['fresh_whole_archive_loads_andcache_hits'],l['fresh_parent_cases'])==(303,606)
    assert len(list((ROOT/'stored_v3').glob('record_*.json')))==310
    assert r['all318_compiled_native_pages_unchanged'] and r['all_source_native_commands_preserved']
    amendment=Path(r['owned_FE_storage_amendment']);a=load(amendment)
    assert digest(amendment)==r['owned_FE_storage_amendment_sha256'] and a['full_block_inverse_exact']
    assert a['no_new_pages_no_changes_to_compiled_text_controls_orpixels'] and len(a['semantic_negatives_rejected'])==4
    release=load('work/maria_B50_release_v1/registered_release_verification.json')
    assert digest('translations/release_stack.json')==release['registry_sha256'] and r['parent_sha256']==release['candidate_sha256']
    proof_paths=[reconstruction,stored_path,catalogue_path,loader_path,amendment,selection,
        ROOT/'offline_display_approval_v1.json',ROOT/'final_native_v1.json',
        Path('dk4tool/script/reviewed_FE_storage_padding_v1.py'),Path('scripts/amend_maria310_FE_storage_v2.py'),
        Path('scripts/check_maria310_stored_v3.py'),Path(__file__)]
    evidence={str(p):digest(p) for p in proof_paths}
    summary=('Maria310 now passes complete stored-script, allocation, native branch, catalogue and loader checks: '
        '310 source utterances/318 unchanged viewed pages, 604 commands and 132 relative sites. '
        'One source-bound FE storage padding defect is corrected with exact block/archive/ROM inverses; '
        'no prose, controls, font, page or engine changes. Representative gameplay and registration remain; '
        'all fifth gates stay false. Integrated 19,748, registered de2ffce1/main and full scope are unchanged; zero new credit.')
    text=f'''# Maria310 stored checkpoint — November 9, 2026

**All 310 reviewed bodies pass stored-script checks, preserving all 318 approved pages.** Seven complete SC3 blocks (51–57), 604 commands and 132 relative sites pass reconstruction/inverse checks. All 310 catalogue bodies, 303 complete loads/cache hits, 606 parent handoffs and {s['fresh_relocated_native_relative_cases']} relocated native branch cases pass. Representative gameplay and registered integration remain; fifth gates stay false and new credit remains zero.

All paths below are under `work/Maria_B51_B57_clean_20261109`. Continue from `reconstruction_v2/reconstruction.json`; research ROM SHA-256 `{r['research_ROM_sha256']}`. This ROM is research only. Terminal passing proofs are `stored_v3/stored_native_verification.json` (310 individual receipts), `stored_catalogue_all_v2/all310_stored_effective_body_bindings.json` and `loaders_v2/verification.json`. Earlier loader_v1 applies only to the initial target.

Reuse the [offline checkpoint](editorial_Maria310_offline_20261109.md): 184 revisions/126 justified retentions, 15 wrap improvements, five FE row repairs, three mixed-width letter fixes and 26 names/31 strings. All compiled buffers, pixels and four-alignment proofs remain exact. Storage freshly checks {s['fresh_parity_dependent_pages']} parity-dependent pages and reuses {s['exact_compiled_pages_reused']} exact compiled pages; all original native assertions remain enforced.

**One additional storage defect was corrected at SC3 B54 R507**, clean/current selector offset 4509, preamble `0040ffff00fe`. Its full 139-byte compiled body consumed correctly; the automatically appended parity space did not. Initial ROM `reconstruction_v1/reviewed_RESEARCH_ONLY.nds` (`ab2a8eacd2009ca14c3fee6a0dbefb6cdeaabd34287e383ee3af446a7f3c936b`), failed checks and diagnostic alternatives remain preserved.

`dk4tool/script/reviewed_FE_storage_padding_v1.py` removes that space and one redundant NUL alignment byte, retaining the terminator. The owned command becomes 146 instead of 148 bytes. Native inventory/count/scopes remain exact; subsequent offsets, catalogue indices, branch spans and ends are recomputed. Four malformed cases are rejected. Exact block inverse composes with the original clean/current, archive and serialized-ROM inverses. No prose, control, page, font, viewport or engine changes occur. Receipt: `reconstruction_v2/FE_storage_alignment.json`.

The eventual registered pure transaction **must execute and bind this exact amendment after the ordinary rebuild**, as `scripts/amend_maria310_FE_storage_v2.py` does. Otherwise it regenerates the failed version. Historical builders remain unchanged. `stored_v2` failed during checker initialization; v3 binds the existing compound helper and journals successful individual records without changing guards.

**Next run the two representative fixtures selected in `display_selection_v2.json`: 64 utterances/70 pages.** They cover six distinct two-page layouts, all five repaired FE panels, R507 storage, inline Bianca/Angelo voices, FE/progressive transitions, I/F fixes, sampled headers and host exit/resupply/sailing. Use `scripts/prepare_maria270_display_fixtures_v2.py`, `scripts/run_maria270_display_v1.py`, `scripts/analyze_maria301_display_v1.py` and readable contact sheets. Directly view new pages. The B52 town alternatives are conditional display cases, not naturally consecutive events. Existing system-only unlock is disclosed, not earned. Current-batch gameplay observations remain zero; original story activation/outcomes and hardware are unvisited. No guide photos or exhaustive playthroughs.

After representative checks pass, seal fifth gates and integrate with an exact clean-input patch, own Maria/Hangzhou startup and 24 protected-name getters. Preserve the market allocation/pointers, six-section ARM9, ASCII right-bound correction and v2 source25 guard. The user's tested old build is `all_routes_rafael2952_extended_checkpoint_v1_20261106_candidate`; its [Trade-screen defect is already fixed](editorial_market_goods_info_fix_20261109.md) in the registered parent.

Registered candidate: `work/maria_B50_release_v1/all_routes_maria_B50_candidate.nds`, SHA `{release['candidate_sha256']}`, 712 entries/114 accepted layers/47 checks. Integrated **19,748 = 11,880 revisions + 7,868 retentions**; remaining native story objects **6,150 (Lil 1,805 / Maria 4,345)**. Shared/town/random/UI prose is tracked separately. Main, all ROMs, translations, retentions and evidence are preserved; no promotion without acceptance. Full unfinished editorial scope remains active. Deferred artwork and later older-record technical re-audit remain separate. No worker is live at this checkpoint.
'''
    checkpoint(mutation=ROOT/'stored_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria310 stored/native/catalogue/loaders complete;representative gameplay next.',
            proposed_revisions=184,justified_retentions=126,all_current_batch_fifth_gates_pending=True,
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Run64-utterance/70-page representative display fixtures,then registered cumulative integration with exact FE storage amendment.'),
        additional_updates={'Maria_SC3_B51_B57_clean_20261109':dict(new_credit=0,
            stored_native_pass=True,stored_catalogue_pass=True,complete_archive_loaders_pass=True,
            stored_verification=str(stored_path),stored_verification_sha256=digest(stored_path),
            stored_reconstruction=str(reconstruction),stored_reconstruction_sha256=digest(reconstruction),
            FE_storage_padding_defects_corrected=1,compiled_native_pages_unchanged=318,
            current_batch_actual_gameplay_observations=0,all_fifth_formatting_gates_pending=True,
            representative_gameplay_andregistered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria310_stored_20261109.md',document_text=text,completed=19748,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256']})
    print('Saved Maria310 stored checkpoint;all318 approved pages preserved;gameplay/integration pending;zero new credit.')

if __name__=='__main__':main()
