"""Document the registered mixed successor and exact SC1 census without adding credit again."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

OUT=Path('work/hodram_residual_release_v1')
ROOT=Path('work/Hodram_B0_B41_clean_20261107')
RELEASE=OUT/'registered_release_verification.json'
REGISTRY=Path('translations/release_stack.json')
CENSUS=Path('work/Hodram_source_coverage_20261109_v2/coverage.json')

def main():
    release,completion,census,package=map(load,(RELEASE,OUT/'completion_checkpoint.json',CENSUS,PACKAGE))
    assert completion['new_credit']==394 and completion['counts']==dict(completed=19161,revised=11532,retained=7629)
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(708,114,43)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact'] and release['owned_Hodram_residual_surnames_verified']
    assert census['ledger_sha256']==completion['ledger_after_sha256']
    assert len(census['records'])==5356 and not census['missing'] and not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert all(r['covered'] and r['exact_credited_source_bindings'] for r in census['records'])
    assert census['object_counts']=={'ordinary-speech':4556,'physical-style-alternative':681,'typed-menu-caption':119}
    summary=('The cumulative Hodram residual dialogue/name candidate is registered: 708 entries, 114 accepted layers and 43 passing release checks. '
        'All 394 reviews are credited once; integrated totals are 19,161 (11,532 revisions/7,629 retentions). '
        'The clean-input patch, own cold boot and both getters for 12 protected names pass. '
        'The fresh exact-position SC1 census covers all 5,356 native dialogue objects with zero missing or legacy-binding issues. '
        'Main is unchanged; continue with the next unfinished source scope.')
    document=f'''# Hodram residual dialogue and surnames: registered cumulative candidate

{summary}

The experimental testing candidate is [{Path(release['candidate']).name}](../{Path(release['candidate']).as_posix()}), SHA-256 `{release['candidate_sha256']}`. Its [manifest](../{Path(release['manifest']).as_posix()}) retains the complete 706-entry predecessor prefix and appends the reviewed SC1 transaction and three exclusive surname fields. All 114 accepted layers and the ASCII right-bound correction remain. The [clean-input patch](../{Path(release['patch']).as_posix()}), SHA-256 `{release['patch_sha256']}`, reconstructs the entire ROM byte-for-byte from `work/clean.nds`, SHA-256 `{release['clean_input_sha256']}`. Canonical baseline remains `{release['canonical_base']}`, SHA-256 `{release['canonical_sha256']}`. Main remains all-routes-unified-v4701; no promotion occurred.

The [registered verification](../{RELEASE.as_posix()}) binds all 394 exact source/current/stored references. Only 39 reviewed SC1 blocks and 28 already owned ARM9 surname bytes change relative to the predecessor. The whole archive, story-only target and serialized complete parent inverses pass. All four story-format guards run on the new archive; eight malformed story scopes and six malformed surname policies are rejected without changing caller ROMs. Earlier native ownership, style, glyph and menu rejection proofs remain qualified by exact dependencies.

The candidate's own 4,001-frame cold boot uses the predecessor's exact ordinary New Game schedule. Its ten captured frames match the previously reviewed startup RGB byte-for-byte. The final read-only RAM snapshot contains the exact current 123,264-byte staged payload and corrected surname spans, with original pointers and neighboring data intact. Both original getters return all 12 protected names, including David Flahven, Georg Salzgitter and Nagayoshi Kamuro. This is a fresh candidate-owned Rafael startup smoke test and native getter check; it is not a new natural Hodram playthrough or catalogue UI visit.

The [research/gameplay checkpoint](editorial_Hodram_B0_B41_gameplay_20261107.md) preserves the detailed findings: 221 revisions and 173 justified retentions, all 32 tutorial prose decisions, 388 speech bodies/389 final pages, six captions, 42 scoped names, five visual wrap fixes, the earlier comparison-phrase wrap and one FE blank-row repair. No logical prose was shortened to fit. The FO identification is corrected to avoid “Bergstrom Fleet's fleet.” Two intentionally opaque source cries retain their native script and verified ink/shadow masks. The first malformed run-plan lookup stopped qualification before any ROM was produced; its versioned repair freezes the real sibling run plans. All prior failures remain.

All final pages were visually reviewed. Stored checks cover every body and caption, all 56 style slots and 685 native branch cases. When gameplay found the additional All/hands split, only its one native page and parity check were rerun; the other 388 stored pages reused exact byte/position/prefix/parity/runtime/font/plane proofs. All 388 effective native buffers pass. Whole-archive loading covers 325 loads/cache hits, with two fresh B29 parent cases and 648 exact incremental reuses. These are offline checks.

Representative native gameplay comprises three initialized display runs, 57,363 frames, 169 distinct utterances/170 final pages, all three menus/default A returns and all following resupply transitions. All 17 body/name/wrap sheets, the menu sheet and three final return screens were directly viewed. Corrected headers are separately observed. The 219 other body variants, other menu selections/cancel, original conditional activation, rewards, locations, chronology and hardware remain unvisited or covered only by their disclosed offline checks. No guide photos were collected.

The [refreshed clean-source census](../{CENSUS.as_posix()}) now binds all 5,356 SC1 native dialogue objects exactly: 4,556 ordinary speeches, 681 physical style alternatives and 119 menu captions across 325 blocks. Missing objects, inventory failures and legacy source-binding issues are all zero. This proves contextual review coverage for this native story-object scope; it is not a census of every shared resource, remaining player-facing prose, graphics or reachable event path.

The [once-only completion receipt](../{OUT.as_posix()}/completion_checkpoint.json) adds 394 disjoint keys after checking every earlier record prefix and all unrelated ledger data. Totals are 19,161 integrated reviews: 11,532 revisions and 7,629 justified retentions. Historical source/prose/draft counters remain 19,164, preserving the preexisting difference of three. This documentation adds zero credit. All generated ROMs, translations, earlier evidence and the weekend ZIP remain preserved.

Next reconcile exact clean native coverage for the other unfinished storylines and shared resources before selecting a disjoint complete-exchange batch. Reuse completed Rafael/Hodram editorial and display proofs; do not restart reviewed records merely because their block numbers are early. Prioritize remaining natural dialogue, premature wraps and name/glyph consistency. The full editorial goal remains active, including earlier unfinished passes, town/shop/random dialogue and remaining player-facing prose. Deferred graphics artwork and the later older-record technical re-audit remain separate. No process is live.
'''
    evidence={str(p):digest(p) for p in [RELEASE,OUT/'completion_checkpoint.json',CENSUS,OUT/'own_registered_startup_verification.json',OUT/'own_registered_name_getters_v1.json',Path(__file__)]}
    checkpoint(mutation=OUT/'registered_documentation_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Residual Hodram SC1 dialogue andthree surnames registered;394 credited once;SC1 census5356/5356 exact.',
            next_action='Reconcile remaining storyline/shared-resource native source coverage; select a disjoint complete-exchange batch andseal clean meanings/drafts before comparing current English.',
            current_batch_not_yet_integrated=False,all_current_batch_fifth_gates_pending=False,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False,evidence=evidence),
        new_entries={'Hodram_SC1_native_source_coverage_complete_20261109':dict(new_credit=0,
            native_objects=5356,ordinary_speeches=4556,physical_style_alternatives=681,typed_captions=119,
            missing=0,inventory_failures=0,legacy_source_binding_issues=0,coverage=str(CENSUS),coverage_sha256=digest(CENSUS),
            all_exact_credited_source_bindings=True,scope='SC1 native dialogue objects only; shared resources andfull player-facing/reachability scope remain separate',full_goal_complete=False)},
        summary=summary,document='docs/editorial_Hodram_residual_registered_20261109.md',document_text=document,
        completed=19161,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved registered708-entry handoff and5356/5356 exact SC1 census;19161 integrated,zero duplicate credit,main unchanged.')

if __name__=='__main__':main()
