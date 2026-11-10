"""Save the uncredited Maria390 review and durable native-run handoff."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B152_B175_clean_20261109')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native-live', action='store_true')
    args = parser.parse_args()
    prosepath = Path('translations/maria_B152_B175_contextual_review_v1.json')
    namespath = Path('translations/maria_B152_B175_scoped_names_v1.json')
    planpath = ROOT / 'plan_continuity_v1/automatic_plans.json'
    releasepath = Path('work/maria335_B137_B151_release_v1/registered_release_verification.json')
    prose, names, plan, release = map(load, [prosepath, namespath, planpath, releasepath])
    assert (prose['source_objects'], prose['complete_exchanges'], prose['proposed_revisions'], prose['justified_retentions']) == (390, 24, 153, 237)
    gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    assert all(r['review'] == gates for r in prose['records'])
    assert len(names['records']) == 47 and all(r['review'] == gates for r in names['records'])
    assert len(plan['records']) == 373 and sum(r['expected_native_pages'] for r in plan['records']) == 373
    assert not plan['failures'] and not any(i['severity'] in ['warning', 'error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (718, 114, 53)
    assert release['registered_market_format_andboth_data_pointers_preserved']
    receipts = sorted((ROOT / 'native_pages_v1').glob('complete_*.json'))
    assert 0 < len(receipts) <= 373
    paths = [prosepath, namespath, planpath, releasepath, ROOT / 'source_selection_v1.json',
        ROOT / 'clean_source_packet.json', ROOT / 'all390_clean_meanings_v1.json',
        ROOT / 'all390_independent_drafts_v1.json', ROOT / 'all390_contextual_proposals_v1.json',
        ROOT / 'current_v1/current_effective.json', ROOT / 'current_objects_v1/current_objects.json',
        ROOT / 'scoped_names_macros_reference_v1.json', ROOT / 'scoped_terms_reference_v2.json',
        ROOT / 'scoped_category_terms_v1.json', ROOT / 'prose_gates_v1.json',
        ROOT / 'continuity_preferences_v1.json', ROOT / 'continuity_findings_v1.json',
        ROOT / 'formatting_v1/native_macro_measurements.json', ROOT / 'native_pages_v1/native_run_inputs.json',
        Path('work/market_goods_info_terminator_release_v1/source_current_registered_coverage.json'), Path(__file__)]
    evidence = {str(p): digest(p) for p in paths}
    native_status = ('Native worker77136 was last confirmed live; resume that handle and reuse its durable receipts.'
        if args.native_live else 'Native worker77136 is terminal; inspect the aggregate result before further credit.')
    summary = ('Maria B152–B175 has390 contextual reviews:153 revisions/237 justified retentions across24 exchanges and47 scoped name reviews. '
        'The first four gates pass; fifth gates remain pending. Fresh plans fit373 bodies on373 pages, reclaiming one planned aside page; '
        'eight matching FE guard reserves preserve full prose. Native checks have durable per-record receipts; only25 body pages have been directly viewed, '
        'and a next/time phrase wrap needs refinement. ' + native_status + ' No new ROM or credit; registered c97e9677, integrated21,691 and full scope remain unchanged.')
    document = 'docs/editorial_Maria390_B152_B175_prose_layout_20261110.md'
    text = f'''# Maria390 B152–B175 review checkpoint — November 10, 2026

390 original objects in24 complete clean SC3 exchanges have contextual decisions:153 revisions and237 justified retentions. There are373 bodies (341 progressive/32 FE),17 captions in8 menus,47 scoped name reviews and five actual FI substitutions. All first four individual gates pass; every fifth gate remains pending. No completion credit, new ROM or gameplay is claimed for this batch.

The clean meanings and independent drafts were saved before current English was extracted. Exact source/current references, individual findings and retention reasons are preserved in [selected prose](../translations/maria_B152_B175_contextual_review_v1.json), [names](../translations/maria_B152_B175_scoped_names_v1.json) and the source/current/proposal records under `work/Maria_B152_B175_clean_20261109`. The original intake, sealed meanings/drafts and comparison files remain intact.

Seven Japanese wine lines are translated. Findings include Scents versus Spices, collecting paintings versus painting, unsupported gender/kinship/rank claims, hearsay changed into fact, full-width punctuation and the full-width50000 offer, ambiguous delegation, lost private asides and ritual repetition. Preserve every original offer and branch outcome. Use exact installed Wits, Artwork, China and Glassmaking Guide terms where those UI references are intended. Preserve Namahage and giyaman with source context; speculative celestial/legendary/cure claims remain attributed to characters. Good tea-shopping dialogue, natural comic exchanges and valid functional stat notices are retained with reasons. The47 actual actors/94 getter bindings do not imply global name approval. Rocco is a spoken historical name, not a fabricated actor-table entry. Four scoped packed-category getter calls reuse the existing qualified ABI; Sweets is descriptive and does not invent a recipe or category.

Fresh plan: `plan_continuity_v1/automatic_plans.json`. All373 bodies fit373 planned pages without warnings or shortened prose, versus374 initial pages. The124-character B169R73 bargaining aside keeps at least twice more together on one planned page. Eight exact long-FE cases reuse the previously qualified36-cell guard reserve while preserving physical228-pixel geometry. Native and visual proof is still required. Twenty matching prior macro cases are reused only after their complete dependencies match; all five actual FI records still receive fresh native alignment checks.

{native_status} At checkpoint serialization, {len(receipts)} per-record receipt files existed. This is a partial journal count, not an aggregate success or integration count. Run directory: `native_pages_v1`; exact native inputs are hashed in `native_run_inputs.json`. Do not restart completed native records merely because an observation timed out.

Directly viewed so far: B152_part1 (12 pages), B152_part2 (2), B153_part1 (11), total25. No visual approval receipt is sealed. The attempted B154_part1 image was lost to context truncation and must be opened again. B153R27 splits next/time: collect it as a concrete required-pair refinement in a successor preference/plan, preserving V1 and rerendering only changed compiled records after the current native run. B153R4's short opening line retains the complete object phrase that wonderful fragrance; it is readable rather than a broken question tag. Do not count unseen sheets as reviewed.

Next: finish/reuse the journaled373-body run, view every newly generated page, collect concrete phrase/page findings and rerender changed plans only. Verify all17 captions in8 two/three-option menus, scoped name planes, script storage/branches/allocation and representative initialized gameplay before approving fifth gates or registered integration. Gameplay should sample the repaired wine, forecasts, bargaining aside/prices/delegation, three-option menu, Namahage, full-width amount and Wits notice. Original conditions, natural activation, complete route and hardware remain unvisited unless separately observed.

The user's newly confirmed testing filename is `all_routes_rafael2952_extended_checkpoint_v1_20261106_candidate`. Its Trade-screen suffix is already exactly bound in [the registered Market defect coverage](../work/market_goods_info_terminator_release_v1/source_current_registered_coverage.json). The missing terminator exposed program bytes; it was not a Japanese sentence awaiting translation. The November9 fix has native Cheese/Food101 evidence and actual Local/Cargo Olive Oil gameplay. This current registered parent explicitly preserves the corrected format and both pointers. Do not repeat the diagnosis or award dialogue credit for it.

Registered parent remains `work/maria335_B137_B151_release_v1/all_routes_maria335_B137_B151_candidate.nds`, SHA-256 `{release['candidate_sha256']}`,718 entries/114 layers/53 checks, with own startup/getters and exact clean-input patch. Integrated21,691 =13,046 revisions+8,645 retentions; historical source/prose/draft21,694. Native story remainder4,207 =Lil1,805+Maria2,402, including this unregistered390. Main is unchanged. Preserve every accepted layer, Market allocation, ASCII bounds, names/fonts/graphics, source25 guards, canonical baseline, earlier translations and ROMs. No promotion, commit, push or cleanup.

The full editorial scope remains active: all storylines, earlier unfinished contextual passes, town/shop/random/player prose and names/roles. Early Rafael/tutorial priority remains. No guide photos. Deferred graphics artwork and later older-record technical re-audit remain separate. Main promotion requires user acceptance. Continue from this checkpoint without repeating completed source/prose checks.
'''
    checkpoint(mutation=ROOT / 'prose_layout_progress_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria390 B152–B175:153 revisions/237 retentions;47 names;four prose gates pass.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, proposed_revisions=153, justified_retentions=237,
            native_job_live=args.native_live, native_sessions=[77136] if args.native_live else [],
            native_run_directory=str(ROOT / 'native_pages_v1'), observed_native_receipt_count=len(receipts),
            body_pages_directly_viewed=25, registered_build_live=False, registered_cumulative_build_live=False,
            guide_photos=False, current_batch_evidence=evidence,
            next_action='Finish/reuse373-body native journal; view all pages; refine next/time; caption/name/storage/representative gameplay, then registered integration.'),
        new_entries={'Maria_SC3_B152_B175_clean_20261109': dict(new_credit=0, source_objects=390, complete_exchanges=24,
            source_bodies=373, source_FE_panels=32, typed_captions=17, menus=8, scoped_name_retentions=47,
            proposed_revisions=153, justified_retentions=237, first_four_individual_prose_gates_pass=True,
            all_individual_fifth_gates_still_pending=True, planned_native_body_pages=373, planned_pages_reclaimed=1,
            native_pixels_andvisual_checks_pending=True, stored_andrepresentative_gameplay_pending=True,
            registered_integration_pending=True, full_goal_complete=False, evidence=evidence)},
        summary=summary, document=document, document_text=text, completed=21691,
        protected={'translations/release_stack.json':release['registry_sha256'], release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'], release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256']})
    print('Saved Maria390 uncredited checkpoint; registered release, integrated21691 and full objective preserved.')


if __name__ == '__main__':
    main()
