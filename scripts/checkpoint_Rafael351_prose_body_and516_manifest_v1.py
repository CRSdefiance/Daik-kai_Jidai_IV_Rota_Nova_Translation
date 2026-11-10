"""Save complete prose/native-body progress and the terminal separator failure without credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

DOC=Path('translations/rafael_B121_B140_formatting_manuscript_v4.json')
PROSE=Path('translations/rafael_B121_B140_contextual_prose_review_v2.json')
TERMS=Path('work/analysis/Rafael351_item_UI_terms_v1_20261105/term_bindings.json')
NATIVE=Path('work/analysis/Rafael351_native_final_v3_20261105/compiled_native_pages.json')
VISUAL=Path('work/analysis/Rafael351_body_visual_review_v1_20261105/body_visual_review.json')
PLAN=Path('work/analysis/Rafael351_automatic_plans_v6_20261105/automatic_plans.json')
FAILURE=Path('work/analysis/Rafael516_manifest_separator_failure_v1_20261105/failure_analysis.json')
BUILD=Path('work/analysis/Rafael516_registered_build_v1_20261105/completion.json')

if __name__=='__main__':
    doc,prose,native,visual,plan,failure,build=map(load,[DOC,PROSE,NATIVE,VISUAL,PLAN,FAILURE,BUILD])
    assert (len(doc['records']),prose['proposed_revisions'],prose['justified_retentions'])==(351,201,150)
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert not doc['pending_name_term_IDs'] and len(native['records'])==341 and native['pages']==344
    assert native['plan_sha256']==sha(PLAN.read_bytes()) and visual['native_sha256']==sha(NATIVE.read_bytes())
    assert visual['all344_final_body_pages_directly_viewed'] and len(visual['directly_opened_readable_sheets'])==30
    assert not plan['failures'] and failure['only_difference_is_one_Windows_separator_in_same_registered_manuscript_reference']
    assert build['terminal'] and not build['driver_completed_without_exception'] and build['all_original_driver_andregistry_bytes_unchanged']
    summary=('Rafael early story and all tutorials remain first. B121–B140 now has351 complete-exchange prose reviews: '
        '201 proposed revisions/150 justified retentions;all four prose gates pass and126 intake identity/term holds are resolved. '
        'Exact current item/menu/city labels corrected. All341 dialogue bodies/344 final native pages pass and were directly viewed; '
        'scoped phrase/page refinements and one real FE guard-row defect are fixed without shortening prose or changing native geometry. '
        'Captions,names,stored allocation/loader checks,representative gameplay andintegration remain pending;all fifth gates stay false. '
        'Build20868/PID56664 is terminal1:canonical ROM exact andall canonical checks pass,butone Windows separator atmanifest entry670/672 mismatches the frozen expected list. '
        'Preserve that canonical stage for a guarded,versioned registered continuation;do not edit the frozen contract or blindly rebuild. '
        '11845 integrated;verifiedcc71/main3cb8 unchanged. Full scope,ROMs,evidence andtwo pending catalogue de fixes preserved;no guide photos orpromotion.')
    document=f'''# Rafael351 prose and native-body checkpoint — November 5, 2026

Rafael's early story and all tutorials remain the first priority. Every other storyline, unfinished earlier contextual review, shared town/shop exchange, random scene, name, wrap/glyph defect and remaining player-facing prose remains in scope. Preserve all translations, ROMs, coverage credit and evidence. No guide-photo collection, pruning, main promotion or commit/push.

## Completed this checkpoint

`{PROSE}` preserves all351 clean-first, complete-exchange comparisons and exact source/current references: **201 proposed revisions and150 justified retentions**. All four prose gates pass. The126 earlier intake holds are resolved through the existing22-name/six-role qualification and `{TERMS}`. This does not grant global name review, fifth-gate approval or integration credit.

The current data binds **Guiding Staff**, **Snow-Silk Robe**, **Sextant**, **Vels**, **Sao Jorge**, **Verde**, **Auto Move**, **Recruit Crew**, **Flagship** and **Finish**. Auto Sail is a separate sailing-status caption; Route Map is the accepted common-menu caption, distinct from the shorter internal Map heading. Select and Finish are different trading actions. Dialogue now matches the correct consumers. Keep the source's generic knife unnamed rather than guessing between separately bound knife items. Preserve India without adding a Ganges location. All earlier individual factual, voice and retention decisions remain intact.

`{DOC}` is the immutable formatting input. It marks native FI/FA/FO tokens explicitly without changing prose or decisions, and classifies the15 source-FE objects: one whisper, one gold reward and13 sailing instructions. Source selectors, complete preambles,34 physical style variants/six eight-slot objects and10 labels/five menus remain separately bound. No dynamic selector is converted into a fixed actor.

`{PLAN}` passes all341 bodies with344 pages andzero errors/warnings. `{NATIVE}` combines exact compatible records with fresh checks only for changed bytes. `{VISUAL}` records direct review ofall344 final pages through30 opened readable sheets, plus exact duplicate-image reuse for the initial unsealed B128 previews. The final native inputs retain1364 alignment cases across341 bodies;the40 fresh refinement cases replace corresponding earlier results rather than adding coverage.

The initial native run failed the original FE row-membership assertion immediately after B128R85, at B128R89's37-cell opening. Only that exact changed record reserves36 planning cells;the228px native FE viewport andall original validators remain unchanged. It now passes complete glyph,row,canary,pixel andbounds checks. Completed compatible blocks were retained. No failed assertion or unsealed partial B128 record was accepted as a completed proof.

Scoped refinements keep sail handlers,Guiding Staff,out of place,out of this,the alarmed Of all the people idiom,andchoose Finish together. The tablet description fits one complete page. Other longer paragraphs keep coherent destinations/comparisons across a page turn without shortening good prose. A proposed tavern refinement was rejected because it isolated Admiral. on a row;the better original flowing layout is retained with a reason. One short Oh... realization beat in B136R147 is explicitly justified against sourceそうか andRafael's emotional turn toward apologizing;it is not a general exception for sparse openings.

All351 fifth gates remainfalse. The ten typed captions,22 scoped name planes,two catalogue particle fixes,style compiler/allslot checks,stored allocation/reconstruction/catalogue/loader checks andrepresentative gameplay still need their applicable next steps. These are offline native andvisual results;no new natural conditional scene participation orhardware playthrough is claimed.

## Registered516 build: terminal, preserved

`{BUILD}` records terminal1 after6166.7 seconds,withoriginal drivers/core/registry unchanged andno collector errors. `{FAILURE}` proves the precise cause:all672 canonical batch entries represent the same files,butentry670 uses a Windows backslash in the actual manifest and a forward slash in the frozen expected fixture. The required batch list andbase hash match,allcanonical checks pass,andthe canonical ROM is exactly **a97bed78f609bfc76384de4454f0871dd940271c4dbf32c2b613b573f334ae76**.

No final516 candidate or680-entry final manifest was emitted. Do not poll the old live handle or credit516. Preserve the failure,original configuration,expected contract,canonical ROM/manifest andall earlier research. Prepare a narrowly guarded,versioned registered continuation from this completed canonical stage,retaining the original eight runtime/name/data stages,all inverses andown-startup checks. Do not edit the frozen expected contract in place or rerun the102-minute canonical reconstruction merely to change a separator. The already prepared516 target/startup/release proofs remain evidence,not approval ofa final candidate. On successful final registration,require exactly reconstructable clean-input patch,own captain0/route0 andboth Fernan getters beforeonce-only246 revision/270 retention credit.

The two proposed catalogue corrections remain **Dinis デ Albuquerque → Dinis de Albuquerque** and **Garcia デ Oviedo → Garcia de Oviedo**. Public progressive headers are already correct. Qualify the two exclusive pointer fields through an appropriate registered data workflow,not actor35's Fernan-only stage. Unresolved graphics artwork andthe later older-record technical re-audit remain separate.

Integrated totals remain **11845 =6836 revisions+5009 retentions**,historical source/prose11848 unchanged. Verified experimental678/cc71ec06 andmain3cb827e4 remain unchanged. Full goal active.
'''
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,PROSE,TERMS,NATIVE,VISUAL,PLAN,FAILURE,BUILD]}
    checkpoint(mutation='work/analysis/Rafael351_prose_body_checkpoint_20261105',
        batch_key='Rafael_SC0_B121_B140_clean_20261105',
        batch_updates=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),contextual_comparisons=351,
            proposed_revisions=201,justified_retentions=150,four_prose_gate_passes=351,pending_name_term_IDs=[],
            native_body_proof=str(NATIVE),native_body_proof_sha256=sha(NATIVE.read_bytes()),native_body_records=341,native_body_pages=344,
            body_visual_review=str(VISUAL),body_visual_review_sha256=sha(VISUAL.read_bytes()),all_current_body_pages_directly_viewed=True,
            term_bindings=str(TERMS),term_bindings_sha256=sha(TERMS.read_bytes()),all_fifth_formatting_gates_pending=True,
            remaining_name_item_UI_holds_particle_fixes_andall_fifth_gates_pending=False,
            remaining_caption_name_particle_stored_gameplay_andintegration_work_pending=True,evidence=evidence,new_credit=0),
        additional_updates={
            'Rafael516_registered_cumulative_20261105':dict(new_credit=0,current_build_live=False,build_terminal=str(BUILD),
                build_terminal_sha256=sha(BUILD.read_bytes()),build_exit_code=1,manifest_mismatch_analysis=str(FAILURE),
                manifest_mismatch_analysis_sha256=sha(FAILURE.read_bytes()),canonical_stage_exact_andpreserved=True,
                final_candidate_not_emitted=True,registered_continuation_needed=True),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='351 four-prose-gate reviews;341 native/viewed bodies/344 pages',
                registered_build_live=False,registered_build_exit_code=1,
                next_action='Continue351 caption/name/style/stored checks andfocused gameplay. Qualify a guarded registered516 continuation fromthe exact canonical stage;do not rerun completed source/body checks orblindly restartcanonical reconstruction.')},
        summary=summary,document='docs/editorial_Rafael351_prose_body_checkpoint_20261105.md',document_text=document,completed=11845,
        protected={'translations/release_stack.json':'9bc4dd5e408f4e474844d25b1602d2cc4560db371d7c5ee4a92af8b3753cc6c9',
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            'out/all_routes_combined_help97_rafael330_20261105_candidate.nds':'cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448'})
    print('Checkpoint saved:351 prose reviews/341 native bodies/344 viewed pages;516 separator failure isolated,canonical stage preserved.11845 integrated,no newcredit orpromotion.')
