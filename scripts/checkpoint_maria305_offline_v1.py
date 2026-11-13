"""Publish complete offline display progress with zero integration or gameplay credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B176_B195_clean_20261110')


def main():
    releasepath=Path('work/maria390_B152_B175_release_v1/registered_release_verification.json');release=load(releasepath)
    approvalpath=ROOT/'offline_display_approval_v1.json';approval=load(approvalpath)
    native=load(ROOT/'final_native_v1.json');doc=load(ROOT/'formatting_v1/formatting_input.json')
    assert (approval['source_objects'],approval['body_pages'],approval['dialogue_revisions'],approval['dialogue_retentions'])==(305,302,205,100)
    assert approval['all_final_body_pages_directly_viewed'] and approval['all_names_andcaptions_directly_viewed']
    assert (approval['source_styles'],approval['source_style_objects'],approval['choice_captions'],approval['distinct_name_strings'])==(22,3,11,31)
    assert native['selected_alignment_cases']==1176 and sorted(native['selected_records_by_run'].values())==[17,40,237]
    assert all(not r['review']['formatting'] for r in doc['records'])
    oldplan=load(ROOT/'plan_v1/automatic_plans.json');planpath=ROOT/'plan_v8/automatic_plans.json';plan=load(planpath)
    previous={r['id']:r for r in oldplan['records']}
    changed=[dict(id=r['id'],before_lines=previous[r['id']]['lines'],after_lines=r['lines'],source_reference=r['planning_record']['source_reference'],
        current_reference=r['planning_record']['current_reference'],before_compiled_hex=previous[r['id']]['encoded_hex'],after_compiled_hex=r['encoded_hex'])
        for r in plan['records'] if r['encoded_hex']!=previous[r['id']]['encoded_hex']]
    assert len(changed)==26 and not plan['failures']
    layoutpath=ROOT/'final_layout_findings_v1.json';assert not layoutpath.exists()
    save(layoutpath,dict(records=changed,source_bound_layout_changes=26,earlier_page_phrase_improvements=7,additional_native_viewed_phrase_improvements=17,
        source_scoped_FE_guard_reserves=2,observed_native_FE_blank_row_defects_repaired=1,matched_unfailed_long_FE_row_risks_prevented=1,
        pages_before=302,pages_after=302,pages_reclaimed=0,no_prose_font_width_orengine_changes=True,
        proposals_retained_as_existing_layouts=['DK4_MES_B184_R0020','DK4_MES_B186_R0058'],
        proposed_phrase_already_intact_not_counted_as_fix='DK4_MES_B183_R0033',
        source_plan=str(ROOT/'plan_v1/automatic_plans.json'),source_plan_sha256=digest(ROOT/'plan_v1/automatic_plans.json'),
        final_plan=str(planpath),final_plan_sha256=digest(planpath),actual_gameplay=False,new_credit=0))
    evidencepaths=[releasepath,approvalpath,layoutpath,*[ROOT/p for p in ['final_native_v1.json','body_visual_review_v1.json',
        'initial_body_visual_review_v1.json','refined_body_visual_review_v1.json','mixed_visual_review_v1.json','menu_native_approved_v1.json',
        'compiled_styles_v2/compiled_style_objects.json','name_planes_v1/native_name_planes.json','native_final_selection_v1/resume_selection.json',
        'plan_v8/automatic_plans.json','formatting_v1/page_preferences_v9_phrases.json','FE_B177_R66_diagnostic_v1.json',
        'viewed_phrase_findings_v1.json']],Path('translations/maria_B176_B195_contextual_review_v1.json'),
        Path('translations/maria_B176_B195_scoped_names_v1.json'),Path(__file__)]
    evidence={str(p):digest(p) for p in evidencepaths}
    ledger=load('translations/editorial_review_current_v1.json');oldbatch=ledger['Maria_SC3_B176_B195_clean_20261110']
    evidence={**oldbatch['evidence'],**evidence}
    summary=('Maria B176–B195 passes complete offline display:205 proposed revisions/100 justified retentions across19 exchanges and27 scoped name reviews. '
        'All294 bodies/302 final pages,11 captions,31 name strings andthree complete style objects pass. '
        'Seventeen additional phrase wraps,seven earlier page/phrase layouts andtwo scoped FE guard layouts improve;one concrete blank-row defect is repaired. '
        'Exact277 body proofs are reused and17 changed layouts rerendered;1,176 selected alignments pass. '
        'Storage,representative gameplay,fifth gates andregistration remain. No batch worker is live;integrated22,081,registered48c60d68,main andfull scope are unchanged.')
    document='docs/editorial_Maria305_B176_B195_offline_20261110.md'
    text=f'''# Maria305 B176–B195 offline display checkpoint — November 10, 2026

{summary}

The previous goal turn made progress by saving305 clean meanings,independent drafts andcontextual comparisons/four prose gates,plus the first302-page plan. This turn completed native/visual/mixed-object display checks andresolved concrete findings. The full goal remains active. No current-batch record is integrated orcredited yet. Source scope is19 complete SC3 exchanges176–191/193–195:272 ordinary speeches,22 physical4100 alternatives and11 menu captions. Block192 remains already covered. Exact source/current references,individual findings andretentions remain in `translations/maria_B176_B195_contextual_review_v1.json`;all original drafts/provisional-context corrections andprevious approvals are preserved.

**Use these final inputs:**`formatting_v1/formatting_input.json`, `plan_v8/automatic_plans.json`, `native_final_selection_v1/resume_selection.json`, `final_native_v1.json`, `body_visual_review_v1.json`, `offline_display_approval_v1.json`, `menu_native_approved_v1.json`, `compiled_styles_v2/compiled_style_objects.json`. Paths are relative to `work/Maria_B176_B195_clean_20261110`. The first-four-gate manuscript isunchanged:205 revisions/100retentions. All fifth gates remain false pending complete stored/runtime/release prerequisites. Do not rerun the obsolete initial plan orall294 completed native cases.

The first native worker29835 stopped atB177R66 after40 completed per-record receipts. The exact FE painter showed two blank glyphs onan unintended third row andthe intended final line onrow4. The qualified record-specific FE36 guard reserve fixes that panel while preserving all words,FE selector,font,physical228px window andoriginal native assertions. B184R16 also had a matching37-cell FE row risk;its scoped reserve passes fresh native checks. Only B177R66 was directly observed tofail:do not call both cases observed defects. Source FE panel count remains16,no new control/continuation is added,andstorage padding is not yet proved.

Worker96990 reused those40 compatible receipts andcompleted the remaining254 records/262 pages/1,016 alignments. All294 initial selected bodies/302pages/1,176 alignments were directly reviewed on34 sheets. Seventeen changed phrase layouts were then freshly checked byworker76690:18pages/68 alignments on15 directly viewed sheets. All workers areterminal0 except the deliberately preserved first assertion failure. Final selected records byrun:40 original+237 fromthe full remaining run+17 fresh refinements. This is277 exact body proof reuses and17 fresh final-version bodies,not a fresh monolithic294-record rerun. The final1176 selected cases prove complete leading/interior/trailing glyphs,independent pixel planes,consumption,canaries,bounds,rows andpagination. Source/control/substitution/font/runtime dependencies match. All302 final pages have exact directly viewed tile bindings;historical changed-text images do not approve new layouts. The18 superseded initial pages remain preserved. QA sheets areeditorial evidence,not guide photos orgameplay coverage.

`final_layout_findings_v1.json` binds26 compiled layout changes toexact source/current positions,old/new bytes androws:seven earlier page/phrase improvements,17 new phrase improvements andtwo scoped FE reserves. Body pages remain302;zero page-reclamation claim. Changes include complete short questions,take our time,the closing private wish,bane of Tokugawa across the page turn,Mustve been,Two hundred years,leave it toyou,demon kings name,just west,move me,the out-of-nowhere expression andintact didnt it tag,drove back,seven boats andget back towork. Natural prose is unchanged. The ordinary complete-word he/drove boundary isqualified only in B194R56 so that drove back stays together ina readable three-row paragraph. No native glyph,bound,control,allocation orpagination guard iswaived.

Two proposed constraints made their existing paragraphs worse. Retain B184R20's readable two-row each/other soft wrap andB186R58's original Shandong/Peninsula soft wrap;forcing joins added sparse rows oran article-ending warning. B183R33 alreadykept ended up together,andis not counted asa found/fixed defect. B182R26 retains a short butcoherent formal opening;the final two-page letter keeps bane of Tokugawa intact andadds no page. The previously documented exact complete-question for? boundary inB191R31 isstill narrowly bound;all generic warning/error checks otherwise pass. These are contextual layout decisions,not authored manual breaks ornew text shortening.

Allthree source4100 objects preserve22 physical alternatives/24 aliased voice slots. The native target-slot checks and27 semantic compiler negatives pass. Final plans leave every style alternative byte-identical tothe checked earlier version;the complete source/current/alias/target compiler transaction was rechecked against the final plan andits original native/negative evidence reused explicitly. No repeat CPU permutations orfuture roster claim. Role208/current-startup fallback156 remains a scoped original-dispatch proof,not actual conditional participation.

Allfive two/three-choice objects preserve11 original indices/captions andpass30 provider alignments,96 bridged modal returns,44 current/target normal-highlight planes,22 target planes and36 rejection cases. Full Zhao Yun/Guan Yu/Zhuge Liang captions fit. Allfive menu sheets were directly viewed. These are native provider/foreground/canary proofs with bridged modal returns,not actual controller gameplay. Final source/current/target menu objects are frozen in `menu_native_approved_v1.json`.

Names cover27 scoped actors/54 original getter bindings and31 distinct strings. Twenty-five exact native style11 planes are reused after complete ARM9/font/text andprior direct-approval checks;six arefresh. Both new name sheets were directly viewed,andall31 exact tiles match their native planes. Complete names,including Jam Jack Ludwyan,Janus Pasar andYukihisa Genjo Shiraki,areconsistent. Preserve the Sailor nameplate/Retainer catalogue distinction. These are scoped literal font/name-consumer checks,not global207-name approval orfull catalogue-UI/header gameplay coverage. Mixed review binds allseven name/menu sheets.

**Next:**rebuild the complete19 reviewed SC3 groups through the qualified mixed speech/style/choice workflow,with allsource/current/control/relative maps andwhole block/archive/serialized-ROM inverses. Check stored parity/alignment,effective-body lookups,allocations,pagination,branches,loaders andhandoffs. Inparticular,the compiled FE repair doesnot itself prove that the later storage pad isharmless. Preserve the inherited B164R99 odd-length FE correction in the registered parent;do not apply a padding helper toanother owner without exact source/current qualification. Then use representative initialized gameplay covering the parrot echo exchange,FE letter return,menu branches,styles andlong-page transitions. Clearly identify fixtures andunvisited original conditions. Seal allfive individual gates andintegrate through the registered cumulative workflow only after necessary checks pass. Every original conditional line need not be visited. No batch gameplay ornew ROM exists yet.

Current registered parent:[Maria390 candidate](../work/maria390_B152_B175_release_v1/all_routes_maria390_B152_B175_candidate.nds),SHA256 `{release['candidate_sha256']}`,719entries/114accepted layers/54checks. Its exactly reconstructable clean-input patch,Market Goods Info fix,ASCII right bound,allprevious translated archives,names,font andgraphics remain intact. Main `all-routes-unified-v4701`,canonical andclean inputs areunchanged;no promotion/cleanup/commit/push occurred. Integrated22,081 =13,200 revisions+8,881retentions. Native story remainder3,817 =Maria2,012+Lil1,805 includes the uncredited305;shared/player-facing inventories remain separate. Full story/town/shop/random/prose/name scope,earlier unfinished contextual passes andearly Rafael/tutorial priority persist. Deferred graphics artwork andthe later older-record technical re-audit stayseparate.
'''
    checkpoint(mutation=ROOT/'offline_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria305 B176–B195:complete offline body/name/menu/style display;storage/gameplay/release remain.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True,proposed_revisions=205,justified_retentions=100,
            native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            current_batch_evidence=evidence,next_action='Rebuild andverify complete mixed stored SC3 blocks,thenrepresentative gameplay andregistered integration.',guide_photos=False),
        additional_updates={'Maria_SC3_B176_B195_clean_20261110':dict(new_credit=0,offline_display_complete=True,
            body_candidates=294,final_body_pages=302,selected_native_alignments=1176,final_native_reused_records=277,final_native_fresh_records=17,
            individual_contextual_revisions=205,individual_justified_retentions=100,scoped_name_reviews=27,distinct_name_strings=31,
            source_style_objects=3,style_native_slots=24,style_semantic_negatives=27,choice_objects=5,choice_captions=11,
            source_bound_layout_changes=26,additional_phrase_fixes=17,scoped_FE_guard_reserves=2,observed_FE_blank_rows_repaired=1,
            all_fifth_gates_pending=True,actual_batch_gameplay_records=0,stored_checks_pending=True,registered_integration_pending=True,
            no_batch_worker_live=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=22081,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'offline_checkpoint.json',dict(document=document,source_objects=305,body_records=294,body_pages=302,
        offline_native_visual_name_menu_style_complete=True,all_fifth_gates_pending=True,actual_gameplay=False,new_credit=0,
        no_batch_worker_live=True,current_registered_candidate_sha256=release['candidate_sha256'],full_goal_complete=False,evidence=evidence))
    print('Published Maria305 complete offline display:302 pages/11 captions/31 names;storage/gameplay/release remain;zero credit/main unchanged.')


if __name__=='__main__':main()
