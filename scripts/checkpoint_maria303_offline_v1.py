"""Publish completed native/visual work with exact next storage/gameplay scope and zero credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    approvalpath=ROOT/'offline_display_approval_v1.json';a=load(approvalpath)
    assert (a['records'],a['body_records'],a['final_body_pages'],a['choice_captions'],a['distinct_name_strings'])==(303,299,299,4,24)
    assert (a['accepted_layout_changes_count'],a['pages_reclaimed'],a['mixed_width_letter_corrections'])==(7,2,1)
    assert a['all299_final_pages_directly_viewed_or_exact_visual_dependency_reuse'] and a['all_fifth_review_gates_still_false']
    native=load(a['final_native']);assert digest(a['final_native'])==a['final_native_sha256']
    assert native['selected_alignment_cases']==native['fresh_compiled_alignments']+native['reused_compiled_alignments']==1196
    assert not native['direct_visual_review_pending'] and not native['actual_gameplay']
    releasepath=Path('work/maria310_release_v1/registered_release_verification.json');release=load(releasepath)
    assert native['runtime']['candidate_sha256']==release['candidate_sha256']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    paths=[approvalpath,Path(a['final_native']),Path(a['final_plan']),Path(a['full_formatted_manuscript']),
        ROOT/'native_inputs_v1/manuscript.json',ROOT/'native_inputs_v1/plans.json',ROOT/'plan_v6_visual/body_plans.json',
        ROOT/'native_pages_v1/compiled_native_pages.json',ROOT/'refined_pages_v1/compiled_native_pages.json',
        ROOT/'name_planes_v1/native_name_planes.json',ROOT/'menu_native_v1/group_verification.json',
        ROOT/'scoped20_names_editorial_review_v3.json',ROOT/'scoped_terms_reference_v1.json',
        ROOT/'current_v1/current_effective.json',ROOT/'current_objects_v1/current_objects.json',releasepath,Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria B58–B70 now passes offline native/visual checks for299 body pages,four captions and24 name strings '
        'after303 contextual decisions (181 proposed revisions/122 retentions). Seven wrap improvements reclaim two pages '
        'without changing prose;the full-width I andall18 non-ASCII targets are checked. Only five refined layouts were '
        'rerendered;294 exact body proofs and16 name planes were reused. Stored/allocation/branch checks,representative '
        'gameplay andregistered integration remain. All fifth gates stay false;integrated20,058/registered465cb3c3/main/full scope unchanged.')
    text='''# Maria303 offline native and visual checkpoint — November 9, 2026

**Offline checks pass for all303 editorial objects:299 complete speech pages,four choice captions and24 scoped name strings.** The181 proposed revisions/122 justified retentions and20 name/role retentions remain uncredited until stored/runtime/integration checks pass. Every fifth formatting gate remains false. The complete editorial objective is active.

Selected evidence under `work/Maria_B58_B70_clean_20261109`:

- `offline_display_approval_v1.json`: exact scope,all final page receipts,seven accepted wrap changes,two reclaimed pages,glyph targets,names/menus andexplicit unvisited scope.
- `final_native_v1.json`:299 final body records/pages,complete glyph codes andindependent font pixels,leading/interior/trailing characters,input guards,consumption,bounds andpagination. The final selection has1196 alignment cases:20 fresh forfive refinements and1176 exact reused cases for294 unchanged bodies. Initial299-record execution passed1196 cases;total executed forinitial plus refinements is1216,not extra review credit.
- `formatting_v3/formatting_input_complete_indices_v1.json`: selected full303-object formatting manuscript. `plan_v6_visual/automatic_plans.json` is its full299-speech plan; `plan_v6_visual/body_plans.json` projects that exact plan to `native_inputs_v1/manuscript.json` fornative/storage dependency reuse. Four typed captions remain separate from speech indices.
- `name_planes_v1/native_name_planes.json`:20 scoped actors/40 original getter bindings,24 distinct short/full strings. Sixteen exact planes reuse the previous completed proof after matching full ARM9/font/text;onlyeight were rendered fresh. All24 strings were directly viewed on two current sheets. Full-catalogue names here are literal font tests,not observations of catalogue UI layout.
- `menu_native_v1/group_verification.json`:two complete source/current/target choice objects,four reviewed captions,12 provider alignments,36 bridged selection/cancel returns,16 normal/highlight planes and14 rejected malformed cases. Both generated menu sheets were directly viewed. Actual controller visits andstored-menu integration remain pending.

All299 initial body pages were directly viewed on30 readable sheets. The five changed pages passed20 fresh native alignment cases andwere directly viewed together on `refined_visual_v1/review_01.png`;its `sheet_index.json` binds the complete previews. `visual_reviews_v1` journals exact initial page/sheet/native-receipt hashes,plus name/menu observations. These are offline CPU/font checks andvisual inspection,not emulator gameplay ornatural scene activation. No process is live.

**Seven wrap improvements preserve every word,source control,macro andvalidated width.** B61R23 andB70R34 now keep their complete thoughts on one panel each,removing the short second-page tails. Ordinary adjacent soft-row We/get andauxiliary-verb continuations receive explicit contextual reasons,withzero host errors/warnings andno QA/native waiver. The otherfive keep Where are they,worth your while,You understand don't you,See you andLet's get out of here together. The first one-page trial's actual with-ending warning remains preserved;the selected successor passes unchanged QA. No prose shortening,manual break,narrowed viewport,font metric orengine change is used.

All18 old non-ASCII target records have complete ASCII target native planes:ten formerly Japanese sailor speeches,seven punctuation-only/mixed-punctuation cases andone full-width I in B59R56. The corrected I andother leading letters use the normal native font. All12 FE panels pass distinct-consumer alignment,complete glyphs,row membership,bounds andsingle-panel checks,including off-portrait labeled boy speech,knocking,the dock/Remodel instruction,four separate stat results andthree animal cries. No actor254 portrait assignment,new command orFE continuation is introduced. The clean/current speaker commands andruntime tokens remain exact. The FI/FA/FO/FU default macro proof is reused only after matching complete relevant code,font,actor/captain/default-name dependencies;every newly formatted body still hasfresh alignment checks.

The contextual manuscript remains [maria_B58_B70_contextual_review_v2.json](../translations/maria_B58_B70_contextual_review_v2.json). All logical dialogue,source meanings,current comparisons,individual revisions/retentions andfour prose gates are unchanged by layout work. Established Mihwa remains distinct from Maria Huamei;Janus Pasar,Xien Yan,Julian Lopes andMivor Genz match the bound consumers. Item/UI terms include Silla Gold Crown,Ninja Garb,Tomato Seedling,Remodel,Luck andSpirit. Generic metadata does not supply kinship,rank,nationality ornew biography. The wider207-name review remains open.

**Next reconstruct andcheck allten complete SC3 blocks58/59/60/61/62/64/65/66/68/70 on registered Maria310.** There are299 ordinary speech commands (287 progressive/12 FE),four captions intwo menus andno4100 style objects ordynamic source selectors. Use the existing mixed speech/menu whole-block storage pipeline,withcurrent exact source/current commands andthe two compiled choice objects above. The unchanged native body adapter is already in `final_native_v1.json`;do not rerender the294 unchanged pages orrepeat historical source inventory. Bind the full303-object manuscript/plan andnative299-body receipt through a metadata-only storage projection. Preserve menu order,count/pointers,all branch targets,unowned commands andcomplete block/archive/serialized-ROM inverses. Verify allocation,stored parity/terminators,original catalogue lookup,branch behavior andload/cache/parent handoffs. No old pre-market parent bridge ornew FE continuation is required. Source/current packet: `current_v1/current_effective.json`,typed objects: `current_objects_v1/current_objects.json`.

Then use representative initialized gameplay for distinct FE/progressive transitions,normal I/F glyphs,source-labeled unseen boy speech,the short stat-result branches andboth menu selections/cancel returns,withordinary resupply/departure/sailing transitions. All final speeches are one page,so do notinvent a two-page case for this batch. Include full dialogue context andclearly disclose fixtures/inherited battery use andunvisited original conditions. Individual natural activation ofevery conditional line,full routes,full catalogue UI andhardware are not prerequisites. No guide photos.

Register a cumulative successor only after necessary checks pass,including its own startup/protected getters andexact clean-input patch. Current registered candidate isstill `work/maria310_release_v1/all_routes_maria310_candidate.nds`,SHA-256 `465cb3c39c17c08844cbabe3f58e313a6388ea7ec7750877ee9b28eb4de8b05a`,with713 entries/114 accepted layers/48 checks. Reconcile registry/runtime before building andpreserve the market allocation/pointers,six-section ARM9,ASCII right-bound correction,v2 source25 guard andalready registered B54R507 storage amendment. This batch isdisjoint fromB54;do notremove orreapply that amendment. No main promotion without user acceptance.

Integrated totals stay20,058 =12,064 revisions +7,994 retentions;historical meaning/prose/draft total20,061 stays separate. Native story objects remaining stay5,840 (Lil1,805/Maria4,035),including this not-yet-integrated303-object batch. Shared shop/town/random/UI andother prose remain separately tracked. Keep all unfinished storylines,earlier contextual passes,names,wrap/glyph work andremaining player prose in scope. Every ROM,earlier translation,retention andevidence ispreserved. Deferred graphics artwork andthe later older-record technical re-audit remain separate. Full goal active;no new ROM,credit,promotion,commit orpush.
'''
    checkpoint(mutation=ROOT/'offline_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria303 offline/native/visual passed;stored checks andrepresentative gameplay next.',
            proposed_revisions=181,justified_retentions=122,all_current_batch_fifth_gates_pending=True,
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Reconstruct/check ten SC3 blocks,299 speeches/two menus using approved native receipts;representative transitions/glyph/menu gameplay,thenregistered integration.'),
        additional_updates={'Maria_SC3_B58_B70_clean_20261109':dict(new_credit=0,
            offline_native_visual_pass=True,selected_native_pages=299,accepted_wrap_improvements=7,pages_reclaimed=2,
            short_continuation_page_risks=[],resolved_short_continuation_page_records=['DK4_MES_B61_R0023','DK4_MES_B70_R0034'],
            corrected_mixed_width_letters=1,all18_current_nonASCII_targets_native_checked=True,
            distinct_name_strings=24,fresh_name_planes=8,reused_name_planes=16,
            offline_approval=str(approvalpath),offline_approval_sha256=digest(approvalpath),
            final_native=a['final_native'],final_native_sha256=a['final_native_sha256'],
            final_plan=a['final_plan'],final_plan_sha256=a['final_plan_sha256'],
            selected_formatting_input=a['full_formatted_manuscript'],new_native_page_planes=304,
            new_body_native_page_planes=304,selected_alignment_cases=1196,total_executed_alignment_cases=1216,
            actual_gameplay_observations=0,all_fifth_formatting_gates_pending=True,
            stored_andrepresentative_checks_pending=True,registered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria303_offline_20261109.md',document_text=text,completed=20058,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Published303-object offline checkpoint;299 final native pages/7 wrap improvements;20,058 integrated unchanged;full goal active.')

if __name__=='__main__':main()
