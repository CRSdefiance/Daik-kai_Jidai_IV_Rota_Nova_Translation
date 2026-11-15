"""Publish complete five-gate research without granting unregistered completion credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B176_B195_clean_20261110')


def main():
    release_path = Path('work/maria390_B152_B175_release_v1/registered_release_verification.json')
    ready_path = ROOT/'research_completion_v1/research_completion.json'
    actual_path = ROOT/'gameplay_review_v1.json'
    release, ready, actual = map(load, [release_path, ready_path, actual_path])
    assert (ready['records'], ready['revisions'], ready['retentions']) == (305, 205, 100)
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    for p,h in ready['evidence'].items():
        assert digest(p) == h
    assert actual['all135_actual_pages_seven_captions_andthree_host_transitions_directly_viewed']
    ledger = load('translations/editorial_review_current_v1.json')
    old = ledger['Maria_SC3_B176_B195_clean_20261110']
    evidence = {**old['evidence'], **ready['evidence'], **{str(p):digest(p) for p in [ready_path, actual_path, release_path, Path(__file__)]}}
    summary = ('Maria305 B176–B195 passes allfive individual gates:205 revisions/100 justified retentions and27 scoped names. '
        'Three initialized emulator runs verify127 distinct bodies/132 unique pages (135 observed),seven captions,12 FE panels,'
        'five page turns andthree sailing returns;all20 review artifacts aredirectly viewed. '
        'All302 stored pages,294 native lookups,170 branches,303 loads and606 handoffs pass. '
        'Registered integration/once-only credit remain;no worker islive. Integrated22,081,registered48c60d68,main andfull scope areunchanged.')
    document = 'docs/editorial_Maria305_B176_B195_research_ready_20261110.md'
    text = f'''# Maria305 five-gate research ready — November 10, 2026

{summary}

The previous goal turn was progress:it completed allstored/native checks andthe first73-body actual pixel binding. This turn finished the two remaining prepared emulator runs,all actual menus/visuals/transitions and305 individual fifth gates. It makes no new registered release orcompletion claim. Continue the full goal from this checkpoint without replaying these completed samples.

Final manuscripts are `translations/maria_B176_B195_final_review_v1.json` and `translations/maria_B176_B195_scoped_names_final_v1.json`. `work/Maria_B176_B195_clean_20261110/research_completion_v1/research_completion.json` seals205 revisions/100 justified retentions across19 complete source exchanges,27 scoped names andallfive gates. `research_completion_v1/source294_release_plans.json` retains the exact294 physical body plans with the final manuscript identity. English andfindings areunchanged bysealing. Earlier clean meanings,independent drafts,individual current comparisons,source/current references,four-gate inputs,provisional attribution correction,allretentions andall earlier ROMs/evidence remain preserved. Use [the offline checkpoint](editorial_Maria305_B176_B195_offline_20261110.md) fororiginal findings,26 layout changes,one observed FE blank-row repair andexact277-body reuse/17-fresh-body proof selection.

`gameplay_review_v1.json` binds three completed initialized runs:28,481+16,721+18,641 =63,843 frames. Historical sessions4423,32654 and97816 areterminal0;no process islive. All127 distinct source bodies/132 unique body pages areobserved;135 page occurrences include three repeated pages. All13 compact body sheets,three menu sheets,three full-screen host-return sheets andone final FE-clear capture aredirectly viewed. Every complete body/header glyph mask,blank guard,source call order andnative consumer matches. Eighteen header actors areidentified from source/dispatch proof,not numeric identity inferred from pixels. No original optional scene condition/location,earned chronology,reward/stat result,full-route orhardware isclaimed. Fixtures retain all47 native host setup/effect/cleanup commands andselected original display commands;they sample story fragments anddo not retain entire original story scene control flow. The isolated system-only unlock remains disclosed/not earned;all six original save slots stayexact. No guide photos arecollected.

Distinct actual behavior includes the complete parrot echo exchange,Emilio's first-person request,allthree crew-message objects atcurrent fallback156/voice4,formal Yukihisa/Janus letter pages andsignatures,the ordinary Sailor label,two corrected full-width I glyphs withoriginal FA substitution,the formerly Japanese Guan Yu reply,allthree hero-menu indices,the earrings' two visible price options,armor pagination,1000/100 figures andFI Charm text. Three menu objects showseven complete captions;their ordinary A return reaches the following fixture speech. Numeric modal return registers,original story branch outcomes,cancellation andthe other two menu objects/four captions areoffline-only. Three of22 physical style alternatives areobserved;19 alternatives andfuture roster/voice assignments remain unvisited. All24 native aliased slots werealready qualified offline.

Five two-page turns arebound toordinary16-frame A inputs andordered next page calls. Twelve of16 FE bodies areobserved. Eleven have immediate selected-speech/FE successors;the final Charm panel has native host cleanup anddelayed join messages instead. The first aggregate producer's universal immediate-successor assumption failed before publishing approval;retain `approve_maria305_actual_v1.py` as diagnostic evidence,not a target-ROM failure. Its source-locked v2 preserves allguards andadds the exact final case:FE paint12427,A12640/16frames,clear12720 before the next input,then first host join13384. The complete bottom screen at12720 hasonly the native two-color background;the individual frame wasdirectly viewed. Allthree hosts reachresupply,departure andordinary sailing. No new emulator replay wasneeded for this distinction.

Retain the automatically planned short Muramasa opening withan exact contextual reason in `gameplay_review_v1.json`:the next complete opening phrase uses36 ASCII cells,exceeding this indented35-cell row. Allprose andthe bane-of-Tokugawa/leader-of-Japan phrases remain intact in two pages. It isnot an authored dramatic break orpermission towrap early globally. Other narrow layout retentions remain individually source-bound inthe earlier final layout record. No prose was shortened tofit.

Storage evidence isunchanged andcomplete: `reconstruction_v1/reconstruction.json` binds19 complete SC3 blocks,397 commands/34 relative sites andwhole clean/current/block/archive/serialized-ROM inverses. OnlySC3 differs from the registered parent. `stored_v1/stored_native_verification.json` verifies272 ordinary bodies,22 physical styles and11 captions on302 pages,with148 fresh parity-dependent pages/154 exact compiled reuses and170 native branch cases. All294 original catalogue lookups,303 loads/cachehits and606 parent handoffs pass. The inherited B164R99 correction remains untouched. The complete offline/native/visual proofs apply tothe remaining167 bodies,four captions,four FE panels and19 physical style alternatives without claiming actual conditional visits.

**Next integrate this ready batch through the registered cumulative workflow.** Prepare the exact pure mixed-object SC3 transaction overthe719-entry Maria390 predecessor,preservingall114 accepted layers,all previous profiles/archives,the Market16-byte read-only allocation/both pointers,six-section ARM9,ASCII right-bound correction andsource25 v2 guard. Require full source/current/command/relative/block/archive/serialized inverses,pure semantic changing-input rejection checks,exact research-target ROM equality,all original final release checks,an exactly reconstructable clean-input patch,candidate-owned Maria/Hangzhou startup and24 protected name getters before registration orcredit. Reuse completed display/storage/gameplay proofs whentheir dependencies match. No new FE controls/continuations orstorage padding amendment areneeded. Do not promote main without user acceptance.

Registered testing candidate remains[Maria390](../work/maria390_B152_B175_release_v1/all_routes_maria390_B152_B175_candidate.nds),SHA256 `{release['candidate_sha256']}`,719entries/114accepted layers/54checks. It retainsthe Market Goods Info fix confirmed for the user's Rafael2952 screenshot. Main `all-routes-unified-v4701`,canonical andclean inputs areunchanged. Integrated22,081 =13,200 revisions+8,881 retentions;native story remainder3,817 =Maria2,012+Lil1,805 includes this uncredited305. Shared/player-facing inventories remain separate. Full story/town/shop/random/player prose/name/wrap/glyph scope,earlier unfinished contextual passes andearly Rafael/tutorial priority persist. Deferred artwork andlater older-record technical re-audit remain separate. No cleanup,promotion,commit orpush occurred.
'''
    checkpoint(mutation=ROOT/'research_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria305:allfive gates pass;registered cumulative integration andonce-only credit next.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=False, native_job_live=False, native_sessions=[], stored_job_live=False,
            stored_sessions=[], registered_build_live=False, current_batch_evidence=evidence,
            next_action='Prepare source-qualified mixed transaction;registered successor/patch/startup/getters;thenonce-only305 credit.',guide_photos=False),
        additional_updates={'Maria_SC3_B176_B195_clean_20261110':dict(new_credit=0,
            all_fifth_gates_pending=False, all_individual_five_gates_pass=True, actual_batch_gameplay_records=127,
            actual_batch_gameplay_pages=132, actual_page_occurrences=135, actual_frames=63843, actual_runs=3,
            actual_menus=3, actual_caption_strings=7, actual_FE_panels=12, actual_two_page_turns=5,
            actual_header_actors=18, offline_only_body_records=167, actual_direct_visual_review_pending=False,
            actual_menu_checks_pending=False, remaining_prepared_actual_runs=0, research_completion=str(ready_path),
            final_review=ready['manuscript'], final_names=ready['names'], registered_integration_pending=True,
            no_batch_worker_live=True, evidence=evidence, full_goal_complete=False)},
        summary=summary, document=document, document_text=text, completed=22081,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'research_checkpoint.json',dict(document=document,evidence=evidence,new_credit=0,
        all_individual_five_gates_pass=True,no_batch_worker_live=True,registered_integration_pending=True,full_goal_complete=False))
    print('Published305 five-gate reviews/27 scoped names and127-body actual coverage;registration/once-only credit remain.')


if __name__ == '__main__':
    main()
