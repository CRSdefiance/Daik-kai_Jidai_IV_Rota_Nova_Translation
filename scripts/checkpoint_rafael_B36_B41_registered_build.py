"""Record the sealed research batch, qualified registered build and shared tutorial follow-up."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_release_20261104')
CHECKED=Path('work/analysis/Rafael_B36_B41_checked_20261104')
QUALIFIED=Path('work/analysis/Rafael_B36_B41_release_qualification_v3_20261104/qualification.json')
SHARED=Path('work/analysis/Shared_Deck_tutorials_contextual_20261104/four_panel_contextual_review_v1.json')

if __name__=='__main__':
    prep=load(ROOT/'registered_preparation_v3.json');qualified=load(QUALIFIED);review=load(CHECKED/'formatting_checkpoint.json');shared=load(SHARED)
    assert len(qualified['semantic_rejections'])==9 and qualified['direct_andshared_scene_targets_equal']
    assert review['all_individual_five_gates_pass_in_research'] and review['prose_reviews']==175
    assert (shared['proposed_revisions'],shared['wording_retentions'])==(1,3)
    assert not Path('out/all_routes_combined_rafael_b36_b41_static_text_20261104_candidate.nds').exists()
    summary=('Rafael B36–B41:175 five-gate research reviews (76 revisions/99 retentions),177 pages/four wrap fixes/two ASCII-I fixes; '
        '11 scoped name retentions and40 actual header comparisons pass. Nine production rejection cases anddirect/shared plans pass. '
        'Registered cumulative build12117 was polled live;final manifest/patch/own startup/once-only credit pending. '
        'Shared Deck:four complete contextual reviews,one First Mate revision/three retentions,pending display. '
        '10346 integrated completions;experimental c555f555/main unchanged. Full scope/all prior work/ROMs retained;no guide photos.')
    document=Path('docs/editorial_rafael_B36_B41_registered_build_20261104.md')
    text=f'''# Rafael six-exchange registered build checkpoint

Previous goal turn made progress:40 tutorials integrated andcredited once,175-record research composition/loaders and16-utterance representative gameplay completed. This turn completes scoped header andfinal research gates,qualifies andstarts the next cumulative release,andreviews four shared tutorial panels. The full objective remains active.

## Sealed175-record batch

`translations/rafael_B36_B41_contextual_final_review_v1.json` seals175 individual five-gate reviews:76 revisions/99 justified retentions. All exact clean/current/final storage references andfindings remain. `translations/rafael_B36_B41_scoped_names_final_v1.json` records11 individual progressive-name retentions withspecific reasons;no duplicate dialogue credit andno name-data change. The source intrinsic identities andvoice bindings remain intact. Four formerly sparse/awkward layouts andtwo full-width I glyphs arecorrected. FU remains a distinct13-byte Rafael Castor macro.

All177 final/stored offline pages and400 relocated native cases pass;343 archive loads plus12 fresh/674 reused handoffs andfull archive/serialized ROM inverses pass. Existing matching source-block,ARM9,COMMON,font andactor-byte dependencies supply explicit reuse on the verified c555f555 successor. See [previous complete display/gameplay checkpoint](editorial_rafael_tutorial_release_and_focused_story_20261104.md);do not repeat those checks.

Fresh name checking paints six additional progressive strings through original style11 andindependent font oracle,withcomplete first/internal/final glyphs,bounds andblank guards. Four existing planes reuse exact code/font/actor dependencies. Allsix new native previews were directly viewed. Forty captured headers match these ten distinct strings forall11 actors at the original nameplate origin. Proofs: `work/analysis/Rafael_B36_B41_progressive_names_20261104/`. Use `actual_header_verification_v2.json`:the initial receipt had an inverted boolean label for catalogue scope,clarified without changing any comparison. Both full-catalogue field proposals remain qualified offline butunapplied;this header proof approves progressive names only. Keep the two catalogue-only corrections andfull UI coverage pending separately.

Representative actual coverage remains one10001-frame initialized synthetic display fixture:16 utterances/18 pages/40 complete body planes and40 complete header planes;three QA sheets directly viewed. Both two-page transitions,following selected utterances,FU,two ASCII-I glyphs andall four wrap fixes areobserved. The remaining159 utterances areoffline-only. Original opening artwork isfixture context,not their natural scene background. No natural activation,earned chronology,full-route orhardware claim. B40 isstill explicitly a later rematch,not proven early activation.

Final research gate receipt: `{CHECKED}/formatting_checkpoint.json`;actual review: `{CHECKED}/actual_review.json`. Immutable earlier intake flags in the source packet remain historical;the explicit per-record review gates andthis final receipt givecurrent status. Registered release/credit remainpending.

## Registered cumulative successor

Profile: `{prep['profile']}`. Current preparation: `{ROOT}/registered_preparation_v3.json`. Expected final identity: `{prep['target_ROM_sha256']}`. Registry hash: `{prep['registry_sha256']}`. All114 accepted layers,all older profiles andall six final runtime/name/static stages arepreserved,including ASCII right bounds. OnlySC0 B36–B41 change from c555f555;B42/B43 arepreserved. No catalogue-name metadata isapplied bythis scene layer.

The complete pure planner uses `dk4tool.patch.rafael_story_b36_b41_release_v1`,a byte-identical lowercase module copy ofthe preserved initial adapter. The shared framework correctly rejected the initial uppercase extension ID andmodule grammar before a playable build. V2 fixes the ID;V3 fixes the module name. Windows cannot host case-only duplicate filenames,so the valid distinct lowercase filename preserves the initial file andbytes. One post-commit receipt write encountered a duplicate inherited keyword;the finishing producer verified the exact committed registry against its backup andwrote V3 without further registry mutation. All initial qualification trees/backups/producers arepreserved. No ROM,configuration,native constant orstage bytes changed for these host registration corrections.

`{QUALIFIED}` passesdirect andshared positive175-record plans,nine semantic rejection cases andall six final-stage contract comparisons. Rejections:failed fifth gate,changed selector00,encoded glyph tampering,lost FU,missing actual page,failed name review,stale branch proof,failed header pixels andstale scene parent. Invalid inputs leavecaller NDS objects unchanged. Reuse unchanged earlier stage qualification.

Registered build session12117 uses `work/rf_story_1104` andthe unchanged `scripts/build_integrated_release_with_static_text.py`. It was polled live immediately before this checkpoint. Log: `{ROOT}/registered_build.log`. Intended candidate: `out/all_routes_combined_rafael_b36_b41_static_text_20261104_candidate.nds`. Poll the existing handle;do not restart for a quiet log orobservation timeout. Do not mutate the registry orfrozen dependencies while it runs.

When terminal success,run `scripts/verify_registered_scene_release_v7.py` withcandidate above,parent `out/all_routes_combined_rafael_early_tutorial_static_text_20261104_candidate.nds`,reconstruction `work/analysis/Rafael_B36_B41_rebuilt_20261104/reconstruction.json`,preparation **V3**,andout `work/analysis/Rafael_B36_B41_release_verified_20261104`. Require666 manifest entries/114 accepted layers/six final stages,onlysixSC0blocks,exact expected identity andbyte-exact clean-input patch. The final expected ee04bf6f image already has an ordinary4001-frame exact-identity coldboot in `work/analysis/Rafael_B36_B41_final_identity_coldboot_20261104/`;capture session45236 isterminal exit0. Use `scripts/verify_registered_rafael_startup_v2.py` withthat report andthe c555f555 parent's own startup proof;it preservesnative checks andthe exact reviewed Rafael RGB chain. Do not use the initial-context-only V1 helper. No new startup pass isclaimed until linked to the final registered image/manifest.

Then bind all175 exact final records andcredit once (future totals10521 completions/6253 revisions/4268 retentions). Current totals remain10346/6177/4169. Update status andpin allgenerated stages/research parents. Never promote main without user acceptance. Latest verified experimental ROM remainsc555f555;canonical main remains3cb827e4.

## Four shared Deck tutorial panels

`{SHARED}` reviews allfour complete Japanese panels andtheir exact current pointer/body references. One terminology revision: A First Mate lets you send negotiation documents from the guild. This aligns the visible assignment label andretains the existing useful lets-you-send sentence;the parallel A lookout/A captain panels supportthat wording. Preserve the earlier With-clause draft ashistory rather than credit a second record. Three retentions preserve complete functions:lookout easesdiscovery atsea;captain slows fatigue growth rather than reducing fatigue;oars arefor sailors andexclude named navigators. Inthis last panel 航海士 denotes the named companions,as Julio's reviewed tutorial explicitly explains,not just a navigation-duty role. Do not invent an officer rank orreplace that terminology piecemeal.

Four prose gates pass;allformatting gates remainfalse. The consumer-specific original formatter produces the First Mate paragraph inthree rows/69bytes including NUL,compared with68currentbytes. Four-byte allocation alignment requires72bytes. Qualify the complete original source-owned31-label/540-byte Deck pool andpointer owners before changing storage;do not shorten good prose for a slot oroverwrite the next label. No ROM ororiginal manuscript changed. Consumer-native rendering,full leading/trailing glyphs,bounds/allocation,representative Deck observation andregistered data integration remain.

Preserve all broader Rafael/shared/town/random/story/player-text scope,later245 source speeches,later Hodram drafts,all translations,ROMs andevidence. No guide photos,pruning,commit/push ormain promotion. Graphics artwork andlater older-record technical re-audit remainseparate.
'''
    checkpoint(mutation=ROOT/'registered_build_checkpoint_mutation_v1',batch_key='Rafael_SC0_B36_B41_contextual_20261104',
        batch_updates=dict(new_credit=0,final_review=review['final_review'],final_review_sha256=review['final_review_sha256'],
            all_fifth_gates_pending=False,all_five_individual_gates_pass_in_research=True,scoped_final_names=review['scoped_names'],
            scoped_progressive_names_retained=11,actual_header_planes=40,independent_header_pixel_binding_pending=False,
            registered_profile=prep['profile'],registered_preparation=str(ROOT/'registered_preparation_v3.json'),production_qualification=str(QUALIFIED),
            production_qualification_sha256=sha(QUALIFIED.read_bytes()),semantic_rejections=9,current_build_session=12117,
            build_observed_live_at_this_checkpoint=True,current_build_work='work/rf_story_1104',expected_final_ROM_sha256=prep['target_ROM_sha256'],
            final_candidate_verification_andpatch_andown_startup_pending=True,
            remaining=['Poll existing registered build12117','Complete manifest/clean patch/own startup verification','Once-only integrated credit']),
        additional_updates={'shared_First_Mate_tooltip_contextual_20261104':dict(new_credit=0,
            superseded_by_complete_four_panel_contextual_review=str(SHARED),same_record_pending_no_duplicate_credit=True)},
        new_entries={'shared_Deck_four_panel_contextual_20261104':dict(new_credit=0,total_editorial_objects=4,proposed_revisions=1,justified_retentions=3,
            review=str(SHARED),review_sha256=sha(SHARED.read_bytes()),all_four_prose_gates_pass=True,formatting_andintegration_pending=True,guide_photos=False)},
        completed=10346,summary=summary,document=document,document_text=text,
        protected={'translations/release_stack.json':prep['registry_sha256'],
            'out/all_routes_combined_rafael_early_tutorial_static_text_20261104_candidate.nds':'c555f555a0e6a15b35e10a27b87ac98ed17601ba814cfeb9ba3d98dcc87344a8',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('175 sealed reviews/nine rejections/live registered build12117 andfour shared panels saved;10346 completions unchanged.')
