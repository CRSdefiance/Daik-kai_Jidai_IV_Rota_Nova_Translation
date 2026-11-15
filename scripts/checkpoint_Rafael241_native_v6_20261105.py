"""Save241 complete prose/offline-display reviews while preserving the original live679 build."""
import ctypes as ct
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

DOC=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v4.json')
NATIVE=Path('work/analysis/Rafael241_native_final_v6_20261105/compiled_native_pages.json')
VISUAL=NATIVE.with_name('direct_visual_approval.json')
PLAN=Path('work/analysis/Rafael241_layout_v6_20261105/automatic_plans.json')
IDENTITY=Path('work/analysis/Rafael241_names_terms_20261105/names_terms_roles_andconsumer_dependency_qualification_v1.json')
SEALED=Path('work/analysis/Rafael_B101_B120_clean_20261105/sealed241_v1/all_source_meanings_andindependent_drafts.json')
BUILD=Path('work/analysis/Rafael261_registered_build_20261105')
KEY='Rafael_SC0_B101_B120_clean_20261105'

if __name__=='__main__':
    doc,native,visual,plan,identity,sealed=map(load,[DOC,NATIVE,VISUAL,PLAN,IDENTITY,SEALED])
    assert len(doc['records'])==241 and (doc['proposed_revisions'],doc['justified_retentions'])==(132,109)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert (len(native['records']),native['pages'])==(229,234)
    assert native['all229_body_layouts_approved'] and visual['all234_current_body_pages_andall_generated_readable_sheets_directly_viewed']
    assert native['full241_object_batch_offline_display_complete'] and native['formatting_gates_still_false']
    assert len(visual['body_sheets'])==34 and len(visual['approved_pages'])==234
    assert not plan['failures'] and all(i['severity'] not in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert (identity['fresh_actors'],identity['qualified_reused_actors'],len(identity['actors']))==(11,7,18)
    assert (sealed['source_speech_drafts'],sealed['source_caption_drafts'],sealed['remaining_source_speech_orcaption_drafts'])==(229,12,0)
    assert not (BUILD/'completion.json').exists()
    kernel=ct.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[ct.c_ulong,ct.c_int,ct.c_ulong];kernel.OpenProcess.restype=ct.c_void_p
    kernel.GetExitCodeProcess.argtypes=[ct.c_void_p,ct.POINTER(ct.c_ulong)];kernel.GetExitCodeProcess.restype=ct.c_int
    kernel.CloseHandle.argtypes=[ct.c_void_p];kernel.CloseHandle.restype=ct.c_int
    handle=kernel.OpenProcess(0x1000,False,105028);assert handle
    code=ct.c_ulong();assert kernel.GetExitCodeProcess(handle,ct.byref(code));kernel.CloseHandle(handle);assert code.value==259
    telemetry=json.loads((BUILD/'collections.jsonl').read_text().splitlines()[-1]);assert not telemetry['errors']
    summary=('Rafael early story/all tutorials remain first. Next241 nowhas complete clean-first contextual comparisons:132 proposed revisions/109 justified retentions,allfour prose gates;229 speeches/234 native/viewed pages,12 captions/four menus and18 scoped names pass offline. '
        'Corrected remaining Japanese,wrong certainty/generation/location implications,Julio grandfather joke,Cristina consistency andcorrupted 優usk. Ten ordinary wrap/page refinements andtwo source-scoped FE guard fixes preserve complete glyphs,controls andnative geometry;all34 body sheets/two caption/two name sheets viewed. '
        'Stored script/catalogue/loaders,representative gameplay andregistered integration stillpending;all241 fifth gates/newcredit remainfalse. Original679 build73098/PID105028 remains live;no collector errors,registry11021a16/core27ce0796/all114 accepted layers/eight stages unchanged. '
        'Previous261 research complete;terminal manifest/patch/ownRAM/Fernan getters/once-only credit pending.11845 integrated;verifiedcc71/main unchanged. Fullscope/ROMs/evidence preserved,no guidephotos orpromotion.')
    text=f'''# Rafael241 prose andoffline display complete; original679 build live — November 5,2026

Rafael’s early storyline andall tutorials are first. This reprioritizes the existing full goal;it doesnot restart completed reviews orremove other storylines,earlier unfinished contextual passes,shared shop/town exchanges,random scenes,speaker names/substitutions,glyph consistency orremaining prose. No guide-photo collection,main promotion,pruning orcommit/push.

## Current241: source/context/natural English completed

`{SEALED}` joins229 clean-Japanese speech meanings/independent drafts and12 captions before current-English extraction inthis intake. Both prior partial draft packets remain preserved. `work/analysis/Rafael_B101_B120_current678_20261105/current_effective.json` binds current stored/effective English through the original native catalogue onverified678. The four complete three-choice objects are separately bound bycommand,index andbytes. No blanket historical-English-exposure/amnesia claim.

`{DOC}` has241 individual complete-exchange comparisons: **132 proposed revisions/109 justified retentions**. Allfour prose gates pass;allfifth formatting gates remainfalse. Exact source/current references,clean meanings,individual findings,retention reasons andbranch-aware contexts remain inthe manuscript. B106/B107 are control-only. Alternatives inriddles are not treated assuccessive chronological attempts.

Concrete corrections include the remaining Japanese pilgrim/cross speech;the literal corrupted word`優usk`;Julio’s father/grandfather correction andtentative wish forCristina;hearsay rather thanconfirmed sinking/discovery;the unnamed sword’s trials rather thantrials caused bythe sword;an embedded tablet without aninvented wall;the original clan versusits descendants;anddescendants expected rather thanknown toremain inthe village. Keep the source’s directions,uncertainty,religious/cultural context andunspecified sacrifice victims. The priest dismisses Rafael’s attempted correction before acomplete Trinitarian blessing. The sect leader condemns fearlessness toward thedivine,not a newly asserted lack ofbelief oractive opposition.

`{IDENTITY}` binds18 ordinary public names:11 fresh clean/current getter pairs andseven exact ARM9/COMMON/font/complete actor-array reuses. Twelve source speeches use selector207;the original native dispatch binds runtime role0 toRafael inthis own captain0 startup. It remains dynamic;do not index207 asa static actor-table row orclaim original conditional scene participation. Retain public Sailor,not raw Retainer/nationality metadata. Samwell Khan,Hans Letzel,Arcadius Eudoxios,Margrete,Donna andthe generic roles have individual source-aware retentions. Preserve Clau inits explicit source nickname scope.

Seven actual item-pointer fields andverified own RAM qualify Muramasa,Peacock Mail,Jaguar God’s Vest,Minerva Shield,Hestia’s Pot,Aristarchus Telescope andRigveda. Dialogue uses the established native labels while retaining descriptive source wording;do not insert Rigveda into anunnamed source reference merely because theitem isknown. The complete Ancient Megalithic Civilization Research Society name agrees withthe earlier individually reviewed Hodram/Lil source term. These are lexical/getter proofs,not newly observed item-card orcatalogue UI.

## Native/visual approval — offline only

`{PLAN}` passes all229 plans with234 pages,zero errors/warnings and89 informational source-row-count differences. Ordinary prose remains logical paragraphs;no manual ordinary breaks,shortened prose,font enlargement,viewport expansion orengine changes. `{NATIVE}` and`{VISUAL}` seal all234 current body pages,all12 captions and18 scoped names/17 strings. All34 generated body contact sheets,twocaption sheets andtwo name sheets were directly viewed. Two early partial images are exact duplicates oflater viewed pages. Composite native expansion totals916 alignments;this isnot one run.

Ten ordinary refinements preserve noun/phrasal units andimprove page turns,sparse openings andriddle number/unit continuity. Two exact FE records need36 planning cells within theunchanged native228px viewport:`B113R37` initially wrapped itsfinal period onto another row;the first number/unit refinement of`B118R19` made a37-character row that broke native four-row consumption. Both nowpass theoriginal complete glyph,row,return,canary,pixel andbounds assertions. The failed original runs andplans remain preserved. No assertion orgeometry was relaxed.

Reject the alternative that ended aline withweak`the` andthe alternatives that created sparse middle rows. Retain B120R56’s balanced original rows andcomplete standalone hearsay aside onpage2;forcing itsentire destination after theturn made thefirst page worse. These documented choices do not grant generic wrap waivers. The current source andall words remain intact.

Exact native origins:93 completed original records fromthe run that later failed onFE;133 records fromsuccessful v4 delta;two completed progressive v5 records before itsseparate FE failure;one successful v6 FE record. Every selected row’scompiled bytes,logical prose,source/current refs,allfour expansion outputs,pagination andstored plane/PNG hashes match thefinal plan. Unchanged completed checks are reused.

Four menus pass24 native provider alignments,96 bridged returns and48 caption/style planes,plusall32 compiler negatives. The separately qualified menu proof at`work/analysis/Rafael241_native_final_v6_20261105/qualified_menu.json` keeps theoriginal execution identity andproves thatall12 current captions/objects/gates are unchanged bythe two later body-only prose corrections. This isoffline ABI/pixel evidence,not actual cursor/controller gameplay. Name plane approval isscoped;actual headers andfull catalogue/global207 review remainopen.

**Next:** reconstruct theowned B101–B120 blocks fromthis final manuscript/plan/native/menu proof;run fresh stored paragraph/complete leading-trailing glyphs,bounds,allocation,pagination,branch/catalogue/load/cache checks;then representative initialized gameplay fornew headers,dynamic207,FE periods/riddle four-row panels,allfour three-choice dimensions/highlights andpage transitions. Use complete exchanges where useful;do not require every conditional line orfull route. All241 fifth gates,stored checks,actual gameplay andintegration remainpending. No new research ROM orcapture wascreated thisturn.

## Original679 integration still running — do not restart

The earlier261 already have allfive research gates and111 revisions/150 retentions. Follow[the preceding checkpoint](editorial_Rafael261_build_next241_20261105.md) forits complete qualified storage/gameplay evidence andexact final-release commands;do not repeat those checks. Build session73098/PID105028 remains OS-confirmed live. Latest collector telemetry: {telemetry['elapsed_seconds']}seconds,errors empty. Quiet output isexpected. Registry`11021a16ab4b1157d9e34fc71f214fdb2b9eeb565325122444e59e261d0bcec0`,original core`27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963` andallnine locked drivers/dependencies remain unchanged.

Preserve all114 accepted layers andeight runtime/name/data stages,including ASCII right bounds andFernan’s F. Expected registered candidate SHA-256`7ec12144c3340331ea1c307c0f1ce56f06fb045ce59cd0f03e59de562bd8d150`. Onoriginal terminal0 verify thefull679 manifest,clean-input patch/exact reconstruction,then rebind thesaved own4001-frame startup andFernan getters;credit the261 exactly once. The credit helper isstill unwritten. Do not change thelive registry,core,drivers orconfigs. Do not restart orreplace theprocess based onquiet output.

Integrated totals remain **11845 =6836 revisions+5009 retentions**. Historical source/prose counter11848 remains unchanged. Verified experimental parent`out/all_routes_combined_help97_rafael330_20261105_candidate.nds` SHA-256`cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448`;main`out/raphael_natural_v2_accepted_base.nds` SHA-256`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. Laterrebase onlyowned B101–B120 onto theverified679 successor;do not overwrite a newer wholeSC0 archive withthis678 comparison image. Preserve all ROMs,translations andevidence. Deferred graphics artwork andthe later older-record technical re-audit remain separate. Full goalactive.
'''
    protected={str(p):sha(p.read_bytes()) for p in [DOC,NATIVE,VISUAL,PLAN,IDENTITY,SEALED,
        Path('translations/release_stack.json'),Path('dk4tool/rom/nds.py'),
        Path('out/all_routes_combined_help97_rafael330_20261105_candidate.nds'),Path('out/raphael_natural_v2_accepted_base.nds')]}
    protected.update(load(BUILD/'request.json')['driver_andcanonical_bytes'])
    checkpoint(mutation='work/analysis/Rafael241_native_checkpoint_20261105',completed=11845,protected=protected,
        batch_key=KEY,summary=summary,document='docs/editorial_Rafael241_native_checkpoint_20261105.md',document_text=text,
        batch_updates=dict(new_credit=0,independent_source_speech_drafts=229,remaining_independent_speech_drafts=0,
            caption_drafts=12,remaining_caption_drafts=0,sealed_drafts=str(SEALED),sealed_drafts_sha256=sha(SEALED.read_bytes()),
            contextual_comparisons=241,proposed_revisions=132,justified_retentions=109,all241_four_prose_gates_pass=True,four_gate_passes=241,
            current_English_unconsulted_in_this_intake=False,all_drafts_preceded_current_English_extraction_in_this_intake=True,
            contextual_manuscript=str(DOC),contextual_manuscript_sha256=sha(DOC.read_bytes()),
            scoped_identity=str(IDENTITY),scoped_identity_sha256=sha(IDENTITY.read_bytes()),pending_name_term_holds=0,
            offline_native=str(NATIVE),offline_native_sha256=sha(NATIVE.read_bytes()),offline_body_pages=234,
            offline_complete_speeches=229,offline_choice_captions=12,offline_menus=4,scoped_names=18,
            complete_direct_visual_approval=str(VISUAL),complete_direct_visual_approval_sha256=sha(VISUAL.read_bytes()),
            ten_ordinary_wrap_refinements=10,two_FE_row_guard_fixes=2,
            all_fifth_formatting_gates_pending=True,stored_script_catalogue_loaders_actual_gameplay_andintegration_pending=True,
            term_name_control_formatting_current_comparison_actual_andintegration_pending=False,
            actual_gameplay=False,new_ROMs=0,new_captures=0,guide_photos=False),
        additional_updates={
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch=KEY,next_batch='Rafael261_registered_cumulative_20261105',
                Rafael_early_story_andall_tutorials_first=True,current241_four_gate_passes=241,current241_name_term_holds=0,
                current241_native_pages=234,current241_offline_display_complete=True,current241_fifth_gates_pending=True,
                registered_build_live=True,registered_build_terminal=False,registered_integration_pending=True,
                registered_build_session=73098,registered_build_PID=105028,
                next_focus='Continue241 owned-block stored checks andrepresentative dynamic207/new-name/FE/menu/page gameplay;preserve live679 build. Onterminal0 verifymanifest/clean patch/ownRAM/Fernan getters andcredit261 once.'),
            'Rafael261_registered_cumulative_20261105':dict(new_credit=0,build_live=True,build_session=73098,build_PID=105028,
                latest_verified_collector_elapsed_seconds=telemetry['elapsed_seconds'],collector_errors=[],
                registered_manifest_patch_RAM_binding_andonce_only_credit_pending=True),
        })
    print('Saved241 four-gate prose/offline display approval;11845 integrated unchanged,original679 live,full goalactive.')
