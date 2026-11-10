"""Reconcile completed Help integration and Rafael research without extra credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

def main():
    root=Path('work/analysis/Help59_Rafael330_actual_checkpoint_20261105')
    approval=Path('work/analysis/Rafael330_actual_progress_20261105/actual_visual_andscope_approval_v1.json')
    proof=load(approval)
    assert proof['initialized_fixture_runs']==4 and proof['total_frames']==58004
    assert proof['current_wording_compatible_actual_source_speeches']==74
    manuscript=Path(proof['latest_manuscript']);doc=load(manuscript)
    assert len(doc['records'])==330
    summary=('Rafael/tutorial priority continues.59 Help articles are registered,verified and credited once;'
        '11418 integrated completions(6645 revisions/4773 retentions),experimental81511dde,main unchanged.'
        '675 manifests/114 accepted layers/eight stages/exact clean patch/own startup andFernan getters pass;no live build.'
        'All202 Help research remains complete;97 new articles pluszero-credit Coerce33 amendment awaitone ordered successor.'
        'Rafael330 nowhas174 revisions/156 retentions/four prose gates. Prototype327 speech commands/336 pages/five captions '
        'pass stored lookups,140 branch cases andarchive loaders;source-owned FE pagination solves both held paragraphs.'
        'Four initialized fixture runs(58004 frames) coverall16 headers,allmenu indices/returns,FE transitions andseven page fixes.'
        'Latest wording-compatible coverage is74 source speeches/85 body pages plusfive captions;old EmilioR220 capture '
        'isnot credited asnew wording. Its fresh native page passes;incremental stored/actual checks andRafael integration remain.'
        'No newRafael credit,no guide photos;all scope/ROMs/evidence preserved.')
    text='''# Help59 integrated and Rafael330 actual checkpoint — November 5, 2026

Rafael’s early story and all tutorials remain first. Preserve the complete all-route editorial objective, earlier translations, justified retentions, town/shop/random scenes, names, glyphs and wrapping. No guide-photo collection, promotion, pruning or commit/push. Earlier checkpoint entries are historical; reuse their exact compatible proofs.

## Registered Help completion

`out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds` is the verified experimental cumulative candidate, SHA-256 `81511dde6bc4cd81dee799e8ce893ba06f1fa44d96bbd541ac86ca67ae2d9635`. Its adjacent xdelta reconstructs it exactly from clean input. All 675 manifest entries, 114 accepted layers, eight final stages and 26 checks pass. Registry `82a17be4` and original ROM core `27ce0796` remain unchanged. Own 4001-frame startup and both Fernan name getters pass. No release build or emulator remains live.

`work/analysis/Sea22_Fleet66_release_verified_20261105/` contains release, exact source/stored bindings, composite page coverage, own startup/name and completion receipts. `translations/help_shipyard_sea59_integrated_final_review_v1.json` records all five gates. The 59 new source articles (44 revisions/15 retentions) were credited once; Command66 is an amendment with no duplicate credit. Total integrated: **11418 = 6645 revisions + 4773 retentions** (historical source/prose totals retain their three-record offset). Actual Help coverage is 39 pages/38 articles across three research-ROM groups, with 21 offline-only pages; it is not a complete final-ROM playthrough. The final identity-bound startup is separate.

All 202 source Help topics retain completed research. Remaining integration is 30 new articles plus the zero-credit Coerce33 correction, followed by 67 articles. Use one successor with two ordered extensions, optionally together with Rafael330 when qualified. Keep `help_deck30_Coerce33_active_terms_final_review_v1.json` and `help_remaining67_contextual_final_review_v1.json` proofs; do not repeat their completed research.

## Rafael330 and fresh prose revision

`translations/rafael_B81_B84_contextual_editorial_manuscript_v2.json` has 330 contextual decisions, **174 revisions/156 retentions**, four prose gates. It covers bullfight/Emilio, Cristina/Mivor, rescue and Gerhard/combat training, including five choice labels. All 16 scoped name/role retentions have exact source/current references and reasons. Four Latin artifacts are corrected. Other 255 speeches in the B81–100 source packet remain drafts/comparisons pending; no Rafael330 credit or integration yet.

The prototype reconstruction in `work/analysis/Rafael_B81_B84_rebuilt_20261105/` contains 327 native speech commands/336 body pages plus five captions. Both previously held FE paragraphs are solved by source-owned native continuation commands with exact repeated controls, preserved prose, relative branches and full inverse. All menu styles/captions, stored dispatch/catalogue, 140 controlled branch cases and archive loaders pass. Those proofs still contain the older R220 prose. Latest changes must not inherit old text checks as though freshly executed.

After reviewing the complete food/recruitment exchange, B81R220 now reads: “R-really? All kinds, and lots of it? Then I'm in! I'll go anywhere, even to sea!” This restores the stammer and natural food-driven excitement without invented story facts. All other 329 objects remain exact. `work/analysis/Rafael_Emilio_food_acceptance_20261105/` binds source/current context and the fresh one-page native proof; the page was directly viewed. Next compose this single changed record into the existing cache, refresh affected stored/relocated references and archive loads, and observe the short complete food/recruitment exchange. Do not repeat the entire 51-speech scene solely for this prose change. Current corrections are seven page turns/eleven other phrase wraps plus this prose revision; retain the historical 19-layout proof as history.

## Actual coverage and limits

`work/analysis/Rafael330_actual_progress_20261105/actual_visual_andscope_approval_v1.json` seals four initialized targeted emulator runs/58004 frames, all directly viewed compact pages and menu/response sheets. The full B81 scene retains all 101 commands; one natural branch visits 49 of 51 speeches. Two conditional asides are separately observed in the focused fixture, with original guards preserved. The static Emilio CG does not prove who throws whom; the Japanese agent/object-implicit throw wording is retained faithfully.

Prototype coverage is 75 source speeches/86 body pages plus all five captions. Latest-wording-compatible coverage is **74 source speeches/85 body pages plus five captions**, excluding the old R220 page. All 16 nameplates, nine two-page cases, four FE panels, three FI notice texts, every two-/three-choice cursor position and A returns are observed. Numeric choice return registers, original story response branches, actual stat-reward effects, full route and hardware remain unvisited. Offline proofs are explicitly separate. These are targeted initialized fixtures, not exhaustive natural playthroughs.

`work/analysis/Rafael330_current675_dependency_qualification_20261105.json` proves ARM9, COMMON, font, SC0/EV0 and captain/actor dependencies exact between the earlier research parent and current675; reuse compatible proofs. Main remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. Graphics artwork and the later older-record technical re-audit remain separate. Full goal active.
'''
    protected={
        'translations/release_stack.json':'82a17be4f7610abef225fa39c2059cd4180511af5683f519aec8171de3df5f4e',
        'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
        'out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds':'81511dde6bc4cd81dee799e8ce893ba06f1fa44d96bbd541ac86ca67ae2d9635',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        str(approval):sha(approval.read_bytes()),str(manuscript):sha(manuscript.read_bytes()),
    }
    checkpoint(mutation=root,batch_key='Rafael_SC0_B81_B100_clean_20261105',completed=11418,protected=protected,
        summary=summary,document='docs/editorial_help59_integrated_Rafael330_actual_20261105.md',document_text=text,
        batch_updates=dict(new_credit=0,manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
            proposed_revisions=174,justified_retentions=156,pending_source_action_IDs=[],held_FE_source_IDs=[],typed_labels_pending=0,
            prototype_native_speech_commands=327,prototype_native_body_pages=336,prototype_stored_andbranches_andloaders_pass=True,
            source_owned_FE_pagination_pass=True,all16_headers_actual=True,new_gameplay_runs=4,total_frames=58004,
            latest_wording_compatible_actual_source_speeches=74,latest_wording_compatible_actual_body_pages=85,
            actual_choice_labels=5,final_layout_refinements=18,phrase_wrap_fixes=11,
            new_Emilio_prose_ID='DK4_MES_B81_R0220',new_Emilio_native_page_pass=True,new_Emilio_stored_andactual_pending=True,
            actual_approval=str(approval),actual_approval_sha256=sha(approval.read_bytes()),
            actual_headers_stored_branches_andregistered_release_pending=False,all_registered_integration_pending=True),
        additional_updates={
            'editorial_execution_priority_20261104':dict(new_credit=0,build_live=False,registered_build_live=False,
                registered_cumulative_build_live=False,registered_integration_pending=False,build_terminal=True,build_exit_code=0,
                new_Rafael_proposed_revisions=174,new_Rafael_justified_retentions=156,
                remaining_HELP_new_source_articles_to_integrate=97,new_Rafael_actual_source_speeches_compatible=74,
                previous37_registered_technically_verified_butcredit_held=False,
                next_focus='Refresh one Emilio paragraph stored/actual checks;finalizeRafael330 andcombine ordered97 Help successor.'),
            'sea22_fleet66_registered_cumulative_20261105':dict(new_credit=0,
                all_registered_build_patch_own_startup_andcredit_pending=False,
                final_verifier_andonce_only_completion_not_yet_prepared=False),
        })
    print('Checkpoint saved:11418 integrated;Rafael330 research/current-wording limits preserved;no extra credit.')

if __name__=='__main__':main()
