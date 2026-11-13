"""Save completed offline display and the exact uncredited storage-repair handoff."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stored-live',action='store_true');args=ap.parse_args()
    releasepath=Path('work/maria335_B137_B151_release_v1/registered_release_verification.json')
    release=load(releasepath);approval=load(ROOT/'offline_display_approval_v1.json')
    rebuilt=load(ROOT/'reconstruction_v2/reconstruction.json');loader=load(ROOT/'loaders_v2/verification.json')
    amendment=load(rebuilt['owned_FE_storage_amendment'])
    assert approval['all373_final_pages_directly_viewed'] and approval['all_names_and17_captions_directly_viewed']
    assert (approval['additional_phrase_wrap_fixes'],approval['pages_reclaimed'],approval['selected_alignment_cases'])==(11,1,1492)
    assert (rebuilt['source_editorial_objects'],rebuilt['speech_count'],rebuilt['command_count'],rebuilt['relative_sites'])==(390,373,679,122)
    assert rebuilt['composed_block_archive_andserialized_parent_inverses_exact'] and digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    assert amendment['one_text_alignment_space_replaced_with_NUL'] and amendment['exact_changed_byte']==660
    assert amendment['full_block_inverse_exact'] and len(amendment['semantic_negatives_rejected'])==4
    assert loader['fresh_whole_archive_loads_andcache_hits']==303 and loader['fresh_parent_cases']==606
    assert loader['reconstruction_sha256']==digest(ROOT/'reconstruction_v2/reconstruction.json')
    paths=[ROOT/p for p in ['offline_display_approval_v1.json','final_native_v1.json','body_visual_review_v1.json',
        'mixed_visual_review_v1.json','initial_body_visual_review_v1.json','refined_body_visual_review_v1.json','farewell_body_visual_review_v1.json',
        'native_layout_findings_v1.json','native_layout_findings_v2.json','plan_continuity_v3/automatic_plans.json',
        'name_planes_v1/native_name_planes.json','menu_native_v1/group_verification.json','menu_native_approved_v2.json',
        'reconstruction_v1/reconstruction.json','reconstruction_v2/reconstruction.json','reconstruction_v2/FE_storage_alignment.json',
        'FE_storage_diagnostic_v1.json','loaders_v2/verification.json']]
    paths += [releasepath,Path('dk4tool/script/reviewed_FE_storage_padding_v2.py'),Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    storedpath=ROOT/'stored_v2/stored_native_verification.json'
    finished=storedpath.exists()
    assert not (finished and args.stored_live)
    stored=None
    if finished:
        stored=load(storedpath)
        assert stored['reconstruction_sha256']==digest(ROOT/'reconstruction_v2/reconstruction.json')
        assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
        assert stored['complete_stored_pages']==373 and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
        evidence[str(storedpath)]=digest(storedpath)
    receipts=list((ROOT/'stored_v2').glob('record_*.json'))
    status=('Stored worker82040 was last confirmed live; resume the same handle and its durable per-record receipts.' if args.stored_live
        else 'Stored worker82040 is terminal; the full stored proof passes.' if finished else 'Stored worker82040 is terminal without full stored approval; inspect its last result before continuing.')
    summary=('Maria B152–B175 passes complete offline display:390 contextual reviews (153 revisions/237 retentions),373 directly viewed body pages,17 captions and33 name strings. '
        'Eleven phrase wraps improve andone premature page is reclaimed. A stored FE blank-row defect in B164R99 is repaired byone owned padding byte, preserving its44-byte command andall373 compiled pages. '
        'Full inverses,303 loads and606 handoffs pass. '+status+' Fifth gates,representative gameplay andregistration remain;integrated21,691,registered c97e9677 andmain are unchanged.')
    document='docs/editorial_Maria390_B152_B175_display_storage_20261110.md'
    text=f'''# Maria390 B152–B175 display and storage checkpoint — November 10, 2026

{summary}

Continue the same390 original objects/24 complete exchanges from [the prose checkpoint](editorial_Maria390_B152_B175_prose_layout_20261110.md). The153 revisions/237 justified retentions,47 scoped name reviews, clean-first meanings/drafts, source/current comparisons and first four individual gates are unchanged. All fifth gates remain false. No new registered candidate, gameplay observation or completion credit is claimed here.

Final body plan: `work/Maria_B152_B175_clean_20261109/plan_continuity_v3/automatic_plans.json`. It has373 bodies/pages, zero warnings/failures,341 progressive speeches/32 FE panels, five actual FI occurrences, no styles and no new FE controls. `offline_display_approval_v1.json`, `final_native_v1.json` and `body_visual_review_v1.json` bind every final page to direct visual review. All original leading/internal/trailing codes and pixels, controls, substitutions, bounds, complete consumption, row membership and pagination pass.

Native jobs77136,35421 and the final single-record job are terminal0. Selected receipts are362 initial,10 first-refinement andone final farewell:373 records/1492 alignments. The complete executed total is385 records/1540 alignments including12 superseded receipts. All385 previews on48 body sheets were viewed; superseded compiled bytes cannot approve changed pages. Forty initial sheets were viewed across the preceding and current turns; seven refinement sheets andone farewell sheet were also viewed. Reuse these exact selected proofs rather than rerendering them.

Eleven phrase refinements preserve next time, caught on, Coming right up, two exact prices with gold, How about, handsome man, fall in love and its full complement, both repeated Namahage calls and What sort of. The farewell's first refinement left a short like you tail; the final native plan uses three balanced complete phrases without shortening words or widening the viewport. B153R4 retains its short opening because the complete object phrase that wonderful fragrance reads naturally on row2. B169R73's complete124-character private bargaining aside now fits one native page; the initial plan stranded twice more on page2. Eight matching FE reserve preferences preserve physical228px geometry and remain record-bound.

Names:47 actors/94 exact getter references,33 strings,18 compatible native planes reused and15 fresh. All three sheets were viewed and their tiles match the independent native planes exactly. Menus:seven two-option objects andone three-option object,17 captions,48 source/current/target provider alignments,150 bridged selected/cancel returns,68 current/target normal/highlight planes and57 compiler negatives. All eight caption sheets were viewed. You decide. now states delegation clearly at the original third index. Complete indices, counts, labels, alignment, centering and bounds pass. These are offline provider/font checks; actual controller selections and full catalogue UI remain unvisited.

Initial complete-block reconstructionv1 passes679 commands/122 relative sites across24 changed SC3 blocks, within9216-byte native allocations, with complete source/current/block/archive/serialized-ROM inverses. It preserves all other files/components, Market pointers/read-only allocation, six-section ARM9, ASCII bounds, names/fonts/graphics and all earlier layers. The research-only ROM remains pinned and preserved.

The initial stored run40805 passed through B163 then exited1 at B164R99's FE row-membership assertion. The compiled forecast Dyes may soon be popular in Calicut. fits one row; its automatically appended storage space creates an extra row containing two blank glyphs. `FE_storage_diagnostic_v1.json` proves both exact cases and equality of the unpadded physical plane to the directly viewed approved plane. The initial stored runner had no per-record journal; its partial log is not an aggregate proof. Do not claim it passed.

The first amendment attemptv1 stopped before output because the earlier Maria310 helper requires even-length compiled text andremoves two bytes. This exact owner has odd-length compiled text and a44-byte command. The successful `amend_maria390_FE_storage_v2.py` uses `dk4tool/script/reviewed_FE_storage_padding_v2.py`:replace exactly B164 block byte660 from20 to00, retaining the original terminator and every command extent/offset/result/scope/branch. Four altered-control/body/offset/stored-command cases reject. The whole block inverse is byte exact. This is one new source-bound storage behavior; do not apply the older even-length removal helper or treat it as an engine/font change. The unchanged unpadded paragraph and all373 approved planes are reused exactly.

Selected reconstruction: `reconstruction_v2/reconstruction.json`, research-only ROM SHA256 `{rebuilt['research_ROM_sha256']}`. It composes the amendment with the complete prior transaction, recomputes native catalogue record indices and retains all679 commands/122 relative sites. Block/archive/serialized-parent inverses pass. Both original and amended ROMs remain pinned. The amended archive freshly passes303 whole SC3 loads/cache hits and606 parent handoffs in `loaders_v2/verification.json`; earlier loader proofs are preserved as history rather than substituted for the changed archive.

{status} At checkpoint serialization,{len(receipts)} successful stored-record receipt files existed. Full stored proof present:{finished}. Use `check_maria390_stored_v2.py` with reconstructionv2, final_native_v1, stored_v2, captain3 andformatting_v1/native_macro_measurements.json. Journaled completed records are evidence only within their exact reconstruction/native identities. Native display jobs are no longer live. No build worker is live.

Next after full stored success:run `scripts.check_maria390_catalogue_v2`, then `scripts.select_maria390_display_v1`. The prepared selection script samples all17 town forecasts with nearby named speech,the whole repaired wine exchange,the reclaimed bargaining aside,exact prices and50000,Wits,Namahage repeated FE calls andreturns,Glassmaking Guide and two/three-choice behavior. Its three fixture specifications are not yet created or run. Use the qualified Maria host helper `scripts.prepare_maria301_display_fixtures_v1` with reconstructionv2,stored_v2,display_selection_v1 andformatting_v1/role_bindings.json. Retain all seven original B33 setup commands and40 nonspeech exit/effect/cleanup commands, normal16-frame A pulses andthe existing isolated system-only unlock disclosure. Observe all three original three-choice indices andboth two-choice options; bridge-only tests are not actual controller coverage. The selection is a disclosed command montage, not original natural events or earned stats/items. Check host resupply/departure/sailing returns. Full route,hardware,original conditions/chronology andunselected content stay unvisited.

After necessary gameplay/storage checks,seal all fifth gates andintegrate390 once over registered c97e9677, carrying this exact odd-length FE padding correction into the pure registered transaction. Require own startup/protected getters andan exactly reconstructable clean-input patch. Registered main candidate remains718 entries/114 layers/53 checks. Integrated21,691 =13,046 revisions+8,645 retentions;historical source/prose/draft21,694;native remainder4,207 (Lil1,805/Maria2,402),including this unregistered390. No precredit,promotion,commit,push orcleanup. Main promotion requires acceptance.

The full story/shared town/shop/random/player-facing prose objective andunfinished earlier contextual passes remain intact. Keep early Rafael/tutorial priority,approved names,no guide photos,deferred graphics artwork andthe later older-record technical re-audit. The reported Rafael2952 Market suffix is already fixed in the registered parent;do not repeat its diagnosis or award dialogue credit.
'''
    updates=dict(new_credit=0,native_pixels_andvisual_checks_pending=False,all_individual_fifth_gates_still_pending=True,
        stored_native_checks_pass=finished,stored_native_checks_pending=not finished,representative_gameplay_pending=True,
        registered_integration_pending=True,planned_native_body_pages=373,body_pages_directly_viewed=373,
        phrase_wrap_fixes=11,pages_reclaimed=1,owned_FE_storage_byte_fix=True,all_prose_andcompiled_planes_preserved=True,evidence=evidence)
    checkpoint(mutation=ROOT/'display_storage_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria390 B152–B175:373 body pages,17 captions and33 names visually approved;one owned FE storage byte repaired.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,native_sessions=[],stored_job_live=args.stored_live,stored_sessions=[82040] if args.stored_live else [],
            registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False,current_batch_evidence=evidence,
            next_action='Finish journaled stored_v2 job82040;all373 catalogue lookups;create/run representative Maria fixtures,then registered integration.'),
        additional_updates={'Maria_SC3_B152_B175_clean_20261109':updates},summary=summary,document=document,document_text=text,completed=21691,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved complete Maria390 display andowned FE storage handoff;integrated21691 andregistered release unchanged.')


if __name__=='__main__':main()
