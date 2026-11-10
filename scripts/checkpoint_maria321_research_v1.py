"""Publish the complete five-gate321-record research batch with zero release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B196_B215_clean_20261110')


def main():
    releasepath = Path('work/maria305_B176_B195_release_v1/registered_release_verification.json')
    release = load(releasepath)
    completionpath = ROOT/'research_completion_v1/research_completion.json'
    complete = load(completionpath)
    assert (complete['records'], complete['revisions'], complete['retentions'], complete['complete_exchanges']) == (321,171,150,18)
    assert complete['all_individual_five_gates_pass'] and complete['registered_integration_pending']
    final, names = map(load, [complete['manuscript'], complete['names']])
    assert len(final['records']) == 321 and len(names['records']) == 24
    assert all(all(r['review'].values()) and len(r['review']) == 5 for r in final['records']+names['records'])
    actual = load(ROOT/'gameplay_review_v1.json')
    assert (actual['distinct_source_body_objects'], actual['distinct_body_pages'], actual['observed_pages_including_repeats']) == (156,162,178)
    assert actual['all178_actual_pages_four_captions_andthree_host_transitions_directly_viewed']
    assert len(actual['two_page_transitions']) == 6 and len(actual['ordinary_A_FE_returns']) == 1
    stored = load(ROOT/'stored_v1/stored_native_verification.json')
    assert stored['complete_stored_pages'] == 325 and stored['fresh_relocated_native_relative_cases'] == 120
    rebuilt = load(ROOT/'reconstruction_v1/reconstruction.json')
    assert len(rebuilt['changed_blocks']) == 18 and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    for index in range(3):
        terminal = load(ROOT/f'display_run_menu{index}_v1/terminal.json')
        assert terminal['terminal'] and terminal['frames'] == [29201,26801,17441][index]
    evidencepaths = [releasepath, completionpath, Path(complete['manuscript']), Path(complete['names']),
        Path(complete['source_release_plans']), *[ROOT/p for p in ['gameplay_review_v1.json',
            'offline_display_approval_v1.json', 'final_native_v1.json', 'body_visual_review_v1.json',
            'final_layout_findings_v1.json', 'mixed_visual_review_v1.json', 'menu_native_approved_v1.json',
            'compiled_styles_v2/compiled_style_objects.json', 'reconstruction_v1/reconstruction.json',
            'stored_v1/stored_native_verification.json', 'stored_catalogue_all_v1/all_stored_effective_body_bindings.json',
            'loaders_v1/verification.json', 'display_selection_v1.json', 'transition_review_v1/receipt.json', 'name_header_transition_v1.json']], Path(__file__)]
    evidence = {str(p):digest(p) for p in evidencepaths}
    summary = ('Maria B196–B215 passes all five individual gates: 171 revisions, 150 justified retentions and 24 scoped names. '
        'All 317 bodies/325 final pages, four captions and 28 name strings pass native and direct visual checks. '
        'Storage passes 317 effective lookups, 120 branch cases, 303 loads and 606 handoffs. '
        'Three initialized emulator runs observe 156 bodies/162 unique pages, all four captions, six page turns, one FE return and three sailing returns. '
        'Registered integration and once-only credit remain; no worker is live. Integrated 22,386, registered d5bc0dc5, main and full scope are unchanged.')
    document = 'docs/editorial_Maria321_B196_B215_research_ready_20261110.md'
    text = f'''# Maria321 B196–B215 ready for registered integration — November 10, 2026

{summary}

This turn completes fresh display, storage and representative gameplay checks for the previously reviewed321 source objects in18 complete exchanges. Allfive gates now pass individually in `{complete['manuscript']}` and `{complete['names']}`, with exact clean/current/target references and observed-versus-offline coverage. The171 revisions/150 retentions and24 scoped name decisions preserve the earlier clean meanings, independent drafts and contextual findings. See [the prose checkpoint](editorial_Maria321_B196_B215_prose_layout_20261110.md) for those findings. No registered completion credit is added yet; the full goal remains active.

Use `{completionpath}` and `research_completion_v1/source317_release_plans.json`. Final working inputs under `{ROOT}` are `plan_v5/automatic_plans.json`, `final_native_v1.json`, `offline_display_approval_v1.json`, `compiled_styles_v2/compiled_style_objects.json` and `menu_native_approved_v1.json`. All317 bodies/325 selected pages, four captions and28 name strings pass. Every generated body page is directly viewed:325 initial pages plus two superseding pages. The final proof selects316 unchanged receipts andone rerendered paragraph, for1,268 exact alignments. Only B200R15 is rerendered after direct review found strength/of mind split across pages. Nineteen unique layouts change from the first plan, andone Jam letter page is reclaimed without shortening prose. Ten better ordinary wraps are retained with reasons. See `final_layout_findings_v1.json`; no native glyph, width, bound or pagination guard is waived.

Allthree complete4100 objects preserve21 physical alternatives/24 aliased slots andpass27 compiler negatives. Both two-choice objects preserve four captions andindices. Names bind24 actors/48 getters:13 exact approved font proofs are reused and15 strings freshly rendered. Sailor nameplates, Retainer catalogue labels and Boy162 remain distinct. Default macro proofs are reused only with matching dependencies; all changed text receives fresh formatting. Full catalogue UI andfuture conditional rosters are not approved here.

Reconstruction changes only18 SC3 groups, with433 commands/24 relative sites andcomplete clean/current/block/archive/serialized-ROM inverses. Research ROM:`{rebuilt['research_ROM']}`, SHA256:`{rebuilt['research_ROM_sha256']}`. It is retained research evidence, not a registered playable candidate. Storage passes325 pages (156 fresh parity-dependent pages/169 reused planes),317 effective-body lookups and120 relocated branch cases. The archive passes303 loads/cache hits and606 handoffs. Two source FE panels remain; no new FE control, padding amendment, font orengine change occurs.

Three terminal0 initialized runs total73,443 frames:75 bodies/79 pages,67/69 and30/30. They observe156 distinct bodies/162 unique pages (178 including repeats),all four captions,both figurehead cursor indices,six ordinary-A page turns,the Frozen Rose FE return andthree resupply/departure/sailing returns. All16 compact body sheets,three menu sheets andthree transition sheets are directly viewed. The repaired training page,reclaimed Jam page,Ian/Jam signatures,Boy/Sailor headers andcorrected Julio instruction are observed. These fixtures retain all47 original host initialization/setup/effect/cleanup commands; they do not claim natural quest activation,earned geography,original branch/reward execution,full route orhardware. The161 unvisited bodies,figurehead success/FI Spirit panel andunsampled voice alternatives are explicitly offline-only.

One extra capture at10740,only four frames after a menu return,has nine still-opening top-edge Priest pixels. Both ordinary holds at10800/10920 match the complete body andheader exactly. `name_header_transition_v1.json` binds the original unchanged captures andnative planes. The early frame remains unapproved transition evidence; the final analyzer requires two complete holds for every selected page. No ROM/input/font change or emulator replay occurs. A separate suspected contact-sheet speaker mismatch is disproved by the original Maria capture andexact tile equality. Failed preparation/analysis producers remain preserved; `analyze_maria321_refusal_stable_v2.py` and `finalize_maria321_research_v3.py` pass the final assertions.

**Next:** register the complete321-record cumulative transaction over Maria305, preserving its720-entry prefix,114 accepted layers,Market read-only allocation/both pointers,six-section ARM9,ASCII right bounds,source25v2 andinherited B164R99 correction. Require full source/current/compound/control/relative/inverse/negative guards,exact clean-input patch,own startup and24 protected getters. Only then credit321 once. Reuse the completed display/storage/gameplay evidence; main promotion still requires user acceptance.

Registered parent:`{release['candidate']}`, SHA256:`{release['candidate_sha256']}`. Its registry/ROM/manifest/patch/canonical hashes andmain `all-routes-unified-v4701` remain unchanged. Integrated22,386 =13,405 revisions+8,981 retentions; historical source/prose/draft22,389. Native story remainder3,512 =Maria1,707+Lil1,805 includes this uncredited321; shared/player-facing inventories remain separate. Preserve full story/town/shop/random/player-prose/name/wrap/glyph scope andearly Rafael/tutorial priority. No guide photos. Deferred artwork andlater older-record technical re-audit remain separate. All ROMs,translations andevidence are preserved. No cleanup,promotion,commit orpush occurred;no worker is live.
'''
    checkpoint(mutation=ROOT/'research_ready_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria321:all five gates/native/visual/storage/representative gameplay pass;registered integration/once-only credit pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            proposed_revisions=171, justified_retentions=150, all_current_batch_fifth_gates_pending=False,
            native_job_live=False, native_sessions=[], stored_job_live=False, stored_sessions=[],
            actual_gameplay_job_live=False, actual_sessions=[], registered_build_live=False,
            registered_cumulative_build_live=False, current_batch_evidence=evidence, guide_photos=False,
            previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            next_action='Register the full321-record cumulative transaction, clean-input patch, own startup andprotected getters;credit once only after all release checks pass.'),
        additional_updates={'Maria_SC3_B196_B215_clean_20261110':dict(new_credit=0,
            all_five_individual_review_gates_pass=True, all_five_review_gates_pending=False, all_fifth_gates_pending=False,
            final_manuscript=complete['manuscript'], final_scoped_names=complete['names'],
            native_body_candidates=317, final_body_pages=325, selected_alignment_cases=1268,
            native_pages_visually_reviewed=325, actual_batch_gameplay_records=156,
            actual_unique_pages=162, actual_observed_pages=178, offline_only_source_bodies=161,
            actual_caption_strings=4, actual_page_turns=6, actual_FE_returns=1, actual_sailing_returns=3,
            stored_lookup_bodies=317, stored_relative_cases=120, whole_archive_loads=303, parent_handoffs=606,
            registered_integration_pending=True, no_batch_worker_live=True, evidence=evidence, full_goal_complete=False)},
        summary=summary, document=document, document_text=text, completed=22386,
        protected={'translations/release_stack.json':release['registry_sha256'], release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'], release['patch']:release['patch_sha256'], release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'current_checkpoint.json',dict(document=document, source_objects=321, revisions=171, retentions=150,
        scoped_names=24, all_individual_five_gates_pass=True, registered_integration_pending=True,
        actual_records=156, actual_unique_pages=162, no_batch_worker_live=True, new_credit=0,
        full_goal_complete=False, evidence=evidence))
    print('Published321 five-gate reviews,156 actual bodies andcomplete stored proof;registered integration/credit remain.')


if __name__ == '__main__':
    main()
