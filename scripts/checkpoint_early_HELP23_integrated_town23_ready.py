"""Preserve verified/credited first Help23 andmetadata-rebound town23 ready forregistered integration."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v4 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

RELEASE=Path('work/analysis/Early_HELP23_release_verified_20261104/registered_release_verification.json')
FINAL=Path('translations/help_town23_contextual_final_review_v2.json')
ROOT=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104')
KEY='shared_HELP_T21_T43_contextual_20261104'
DOC=Path('docs/editorial_early_help23_integrated_town23_ready_20261104.md')
if __name__=='__main__':
    release,doc=map(load,[RELEASE,FINAL]);completion=load(RELEASE.with_name('completion_checkpoint.json'))
    assert completion['new_credit']==23 and completion['counts']==dict(completed=11336,revised=6582,retained=4754)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert doc['all23_individual_five_gates_pass'] and not doc['registered_parent_still_pending']
    assert doc['current_ROM_sha256']==release['candidate_sha256']
    summary='First Help23 isregistered,verified andcredited once:11336 completions/6582 revisions/4754 retentions. Experimental d61af913 passes671 entries/114 accepted layers/eight stages/exact clean patch/own Rafael startup. Next23 town-help reviews arefive-gate research-ready:19 revisions/4 retentions,28 checked/viewed pages,15 observed/13 offline-only;six display refinements removeone needless page. Parent metadata isbound toverified d61 withall page bytes unchanged;next registered integration remains. No live jobs. Rafael/tutorial priority,full scope/all ROMs/main preserved;no guide photos.'
    text=f'''# First Help23 integrated; town23 ready — 2026-11-04

Rafael early storyline andall tutorial/help prose remain first. Preserve the full all-story/earlier-translation/shared town-shop/random/name-role/player-prose objective andall translations,retentions,credit,ROMs andevidence. No main promotion,pruning,commit/push orguide photos. Graphics artwork andlater older-record technical re-audit remain separate. The previous goal turn wasprogress;this turn isprogress (next23 source/control/layout/actual checks plusfirst23 registered release andonce-only credit). The full goal isnot complete.

## Newly verified cumulative release

`{release['candidate']}`, SHA256 `{release['candidate_sha256']}`, profile `{release['profile']}`. Registry remains `{release['registry_sha256']}`. Build61834/PID102816 wasobserved terminal0;do not restart it. All671 manifest entries/114 accepted layers/26 checks/eight final runtime-name-data stages pass. ASCII right bounds,Fernan F,all older accepted layers andprofiles remain. Relative toverified9ace,only `/COMMON/HELP.DK4` changes;all other files/components/runtime/code/names/fonts/graphics areexact. The baseline-wide changed-path list stillcontains earlier accepted assets,asexpected.

Patch `{release['patch']}`, SHA256 `{release['patch_sha256']}`, reconstructs the exact image fromclean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. (Authoritative clean hash isrecorded inthe release proof;the exact reconstruction passed.) Registered proof,own startup,both original Fernan getters andcompletion checkpoint areunder `work/analysis/Early_HELP23_release_verified_20261104`. Own4001-frame Rafael captain0/route0 startup matchesall10 reviewed RGB frames andbinds its fresh RAM/payload/protected names;changed HELP isseparately bound toits25 actual pages. Main3cb827e4 isunchanged;this isexperimental,not promoted.

First Help0–20/181/184 nowadds23 credits once:16 revisions/seven justified retentions. Totals11336 completed/6582 revised/4754 retained;source/draft counter11339 preserves the historical3-record offset. All23 original articles/25 native andordinary-UI pages/original links/continuation returns/history arebound. Do not recount202/211 continuations assource articles orre-credit these23. `scripts/verify_early_HELP23_registered_release.py`, `verify_registered_early_HELP23_startup.py`,the frozen own-Fernan getter verifier and`complete_early_HELP23_review.py` all actually ran terminal0;their earlier prepared-only status isnow historical. All generated/intermediate/reconstruction ROMs arepinned.

## Next town Help23: ready forregistration

Authoritative manuscript `{FINAL}`,production plan `work/analysis/Shared_HELP_T21_T43_formatting_20261104/production_plan_v2.json`. It covers21–43,23 complete articles/19 revisions/four word-exact body retentions23/37/40/43. All five individual gates pass. Metadata nowreferences the verified d61 parent;all28 encoded pages,English,native proofs,actual captures andruntime dependencies areunchanged. Receipt `registered_parent_metadata_rebinding_v1.json` records the exact metadata-only rebind;do not repeat source/native/visual/gameplay checks. The v1 final review andold comparisons remain historical. All next23 credit remainszero untilregistered integration/patch/own startup pass.

Reuse the complete detailed evidence in `docs/editorial_town_help23_research_ready_20261104.md` andits linked source packets. Its statement thatfirst build islive/parent unverified isnow superseded. Inn34 cancel intent islocalized withverified B input fromhistorical actual/captured code matching current control spans;physicalX wasnot tested andisnot called broken. Trends andMarket Info use exact native labels. First Mate/Purser roles,Friendship versusrelation state,atleast200 Persuasion,guild selling,profit margin,red purchase prices andactual-contract conditions arereviewed. Source21's working market prose iskept;its24 link isaligned toMarket Info,therefore19 revisions/four retentions. Four body retentions retain the entire working word chain;headings/links/context arenoted separately.

Final28 pages use41 planning cells/252px/ten native rows. Six display refinements keep tips andmarkers together,letter instructions/100-percent conditions whole,press B together andshorten onlyredundant continuation-header context. Body prose isnot shortened. Military37 nowuses37↔204 in two pages;old205 isretained exact butunreferenced,withforeign ownership checks. Other continuations22↔212,25↔213,38↔214,39↔215;target216 topics. Original29 native pages/all eight sheets remain;final28 uses10 fresh native checks/18 exact byte-runtime-font proof reuses andall seven refined sheets directly viewed. Four new semantic ownership/paragraph guards reject invalid proposals. Frozen first-help compiler/producers areunchanged;town formatter uses `reviewed_help_pages_v3.py` withits frozen v2/v1 ancestry.

Focused ordinary31641-frame coldboot isterminal0. Fifteen actual pages/ten articles passcomplete text masks,native child targets,all five two-page returns,two-row heading andL/R history. All four actual sheets were directly viewed. Thirteen pages/thirteen articles remain offline-only,explicit perrecord;no full story route,hardware ornew actual-town Inn/Square command activation claim. The Help-only research ROM isqualified andpinned under `preview_qualification_v2`;do not hand itoff asregistered. Reusable parameterized navigation planning/verification scripts nowavoid per-batch test-code copies.

## Next actions

Register andintegrate the complete town23 batch next. Use a new pure late adapter delegating tothe already qualified v3 compiler;qualify partial actual coverage honestly (15 observed/13 offline-only),not the first-help adapter's all25-observed assumption. Clone verified `all-routes-early-help23-20261104`,preserving all114 accepted layers,all prior profiles andall eight stages. Rebase onlywhole parent/target identities andthe canonical manifest/dependency additions needed forHELP,asinthe existing preparation scripts. Expect672 final manifest entries withthe additional town manuscript;no new source credit forpage/continuation changes. The target mustexactlymatch the pinned216-topic research image. Qualify direct/shared plans,new changed guards andstage contracts,reusing unchanged runtime/name/renderer proofs. Build through `build_integrated_release_with_Fernan_field.py` on a short work path;verifyexact source/current/stored refs,whole parent inverse,all mandatory stages,baseline andclean-input patch. Bind an own Rafael startup beforecrediting23 once. Ifonlyparent metadata changes,all28 page bytes remain reviewed andmustnot berendered/re-tested again without a concrete dependency change.

Continue remaining early help/tutorial work andRafael storyline whilethe next long build runs. The next clean help group canstart at44 (Shipyard) through80 (Ruins),but read source beforecurrent English anddisclose earlier heading/body exposure ratherthan claiming everything unseen. Preserve all later-route checkpoints,includingHodram's queued work. Do not restart completed batches orbroaden technical investigations without changed behavior/failed checks/concrete risks. No live jobs remain atthis checkpoint;full objective stays active.
'''
    # Substitute the authoritative full clean hash toavoid hand-transcription drift.
    text=text.replace('f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',release['clean_input_sha256'])
    protected={str(p):sha(p.read_bytes()) for p in [Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path(release['candidate']),Path(release['patch']),Path(doc['reviewed_parent_research_ROM']),Path('out/raphael_natural_v2_accepted_base.nds')]}
    checkpoint(mutation='work/analysis/Editorial_early_HELP23_integrated_town23_ready_20261104',batch_key=KEY,
        batch_updates=dict(new_credit=0,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
            formatting_plan=str(ROOT/'production_plan_v2.json'),registered_parent_andintegration_pending=False,
            registered_parent_verified=True,registered_parent_release=str(RELEASE),registered_parent_release_sha256=sha(RELEASE.read_bytes()),
            registered_integration_pending=True,research_checks_complete=True,all23_individual_five_gates_pass=True,
            current_ROM=release['candidate'],current_ROM_sha256=release['candidate_sha256'],main_unchanged=True),
        summary=summary,document=DOC,document_text=text,completed=11336,protected=protected,
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,current_batch=KEY,next_batch=KEY,next_help_batch=KEY,
            previous_first_HELP23_registered_verified_andcredited_once=True,registered_cumulative_build_live=False,
            registered_cumulative_integration_next=True,next23_all_five_gates_research_ready=True,current_batch_not_yet_integrated=True,
            current_body_pages_native_andvisually_reviewed=28,Rafael_early_story_andall_tutorials_first=True,full_editorial_scope_preserved=True)},
        coverage_unit_updates={'help-and-other-player-facing-prose':dict(status='in-progress',active_batch=KEY,
            progress_evidence=str(FINAL),progress_evidence_sha256=sha(FINAL.read_bytes()))})
    print('Saved verified d61/11336 completions andnext town23 ready forregistration;no live jobs/full goal active/main preserved.')
