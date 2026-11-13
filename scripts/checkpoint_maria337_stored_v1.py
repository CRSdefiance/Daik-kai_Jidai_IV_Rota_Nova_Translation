"""Save completed Maria337 display/storage evidence without release credit."""
from pathlib import Path
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint


def main():
    release=load('work/maria330_release_v1/registered_release_verification.json')
    stored=load(ROOT/'stored_v1/stored_native_verification.json')
    loaders=load(ROOT/'loaders_v1/verification.json')
    rebuilt=load(ROOT/'reconstruction_v1/reconstruction.json')
    catalogue=load(ROOT/'stored_catalogue_all_v1/all335_stored_effective_body_bindings.json')
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert loaders['fresh_whole_archive_loads_andcache_hits']==303 and loaders['fresh_parent_cases']==606
    for key in ['loads','modes']:
        assert digest(loaders[key])==loaders[key+'_sha256']
    assert loaders['all_native_executed_instructions_current_ROM_exact']
    assert rebuilt['source_editorial_objects']==337 and rebuilt['speech_count']==335
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert catalogue['all335_physical_bodies_checked']
    paths=[ROOT/p for p in ['offline_display_approval_v1.json','final_native_v1.json',
        'body_visual_review_v1.json','mixed_visual_review_v1.json','reconstruction_v1/reconstruction.json',
        'stored_v1/stored_native_verification.json','loaders_v1/verification.json',
        'stored_catalogue_all_v1/all335_stored_effective_body_bindings.json','native_visual_findings_v1.json',
        'plan_visual_v5/automatic_plans.json','menu_native_v2/menu_provider_and_planes.json',
        'name_planes_v1/native_name_planes.json']]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria337 passes offline display and stored-script checks: 224 revisions/113 justified retentions, '
        '335 bodies/339 directly viewed final pages, two repaired captions and 28 name strings. '
        'Four tutorial page boundaries and eight phrase wraps improve without shortening prose. '
        'All 335 catalogue lookups, 430 branch cases, 303 loads and 606 handoffs pass. '
        'Representative gameplay and registered integration remain; fifth gates and credit are pending. '
        'No worker is live. Registered 2ea13d92, integrated 21,019, main and the full objective are unchanged.')
    text=f'''# Maria337 offline display and storage — November 9, 2026

{summary}

Continue the same 337 source objects in 12 complete exchanges from [the prose checkpoint](editorial_Maria337_prose_layout_20261109.md). The 21 scoped actor/role reviews remain; do not restart the source-first meanings, independent drafts, contextual comparisons or first four gates. Select `proposed_English`, not the preserved independent draft. All fifth gates remain pending until representative gameplay and release qualification pass.

Work root: `work/Maria_B125_B136_clean_20261109`. Selected plan is `plan_visual_v5/automatic_plans.json`: 335 bodies/339 pages, zero warnings/failures. Thirty-five initial and four changed-body contact sheets were directly viewed. Only eight bodies needed a fresh native rerun after visual phrase findings; 327 exact initial proofs are reused. Selected alignments total1340. The eight fixes join where/she/is, on/you, the whole short Admiral question tag, dead/weight, all three price thresholds/range, Supplies/holds, over/there and each/other. Four earlier tutorial clause boundaries remain; zero pages are reclaimed and all words/macros/controls remain exact. The failed 338-page trial is retained and unselected.

`offline_display_approval_v1.json`, `body_visual_review_v1.json` and `mixed_visual_review_v1.json` seal every selected page, both caption strings and all28 name strings. Fifteen exact prior name planes are reused and13 are fresh; both name sheets were viewed. The menu's current captions contain known non-ASCII corruption. `menu_native_v2/menu_provider_and_planes.json` checks the exact corrupt provider bytes but explicitly does not approve their old ASCII font rendering. All four corrected target planes, six provider alignments, 18 bridged returns and seven compiler rejection cases pass; the target caption sheet was viewed. Original Japanese pixels and natural menu outcomes are not claimed.

`reconstruction_v1/reconstruction.json` rebuilds all12 complete blocks125–136 with335 speech commands and one complete0x2100 object/two source captions. There are no style objects or added FE continuations. All610 commands and86 relative sites are mapped, allocations stay within9216 bytes, and clean/current/block/archive/serialized-ROM inverses pass. Other components, market allocation/pointers, ASCII right bounds, names, fonts and graphics remain exact to registered Maria330. Pinned research ROM SHA-256: `{rebuilt['research_ROM_sha256']}`. It is not a registered testing candidate.

`stored_v1/stored_native_verification.json` passes335 bodies/339 pages, with176 fresh parity pages and163 exact reuses, complete leading/internal/trailing glyphs, controls, substitutions, canaries, bounds and pagination. All430 relative branch cases pass. `stored_catalogue_all_v1/all335_stored_effective_body_bindings.json` checks every body through the unchanged guarded native catalogue before macro expansion. `loaders_v1/verification.json` binds303 complete SC3 loads/cache hits and606 native parent handoffs to exact payloads, executed instructions and neighbors. Its final receipt and payload hashes are verified; no Python process remains. The original loader terminal output was lost during tool-output truncation, so no native exit-code claim is added for that job. Other routes were unchanged and not replayed. These are offline checks, not new gameplay.

Next: representative ordinary-controller emulator tests for the four two-page tutorial cases, price/equipment prose, repaired Latin I, family-loss FE and patron/applause transitions, Carlo/Cesare/Fernando names, and both repaired menu choices. Copy complete reviewed commands behind the qualified full Maria host prefix and all40 setup/effect/cleanup commands; preserve the isolated existing system-only unlock disclosure. Verify return to resupply/departure/sailing. Original chronology, optional event conditions, minigame/rewards/stats and naturally unvisited lines remain explicitly unvisited. No exhaustive playthrough or guide photos.

Then seal fifth gates and integrate the337 source reviews once through the registered cumulative workflow over Maria330. Preserve716 entries/114 accepted layers/51 checks until a qualified successor exists. Integrated21,019 and remaining4,879 native story objects are unchanged; this337 is not yet credited. Main promotion requires user acceptance. Shared/town/shop/random/player-facing prose, unfinished contextual passes, names/roles, deferred artwork and the later older-record technical re-audit retain their existing scope.
'''
    update=dict(new_credit=0,native_pixels_andvisual_checks_pending=False,stored_native_checks_pass=True,
        representative_gameplay_pending=True,registered_integration_pending=True,
        all_individual_fifth_gates_still_pending=True,evidence=evidence)
    checkpoint(mutation=ROOT/'stored_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch=summary,current_batch_evidence=evidence,
            native_job_live=False,native_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,guide_photos=False,
            next_action='Focused Maria337 emulator display/transition/menu checks; then fifth gates and registered integration.'),
        additional_updates={'Maria_SC3_B125_B136_clean_20261109':update},summary=summary,
        document='docs/editorial_Maria337_stored_20261109.md',document_text=text,completed=21019,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256']})
    print('Saved Maria337 offline/storage checkpoint; gameplay and registration pending; zero new credit.')


if __name__=='__main__':main()
