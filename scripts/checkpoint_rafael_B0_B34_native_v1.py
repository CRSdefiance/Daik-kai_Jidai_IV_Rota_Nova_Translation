"""Save completed prose, native pages, viewed sheets and the remaining wrap candidates."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael4903_v1 import RELEASE, REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import FORMATTING, IDENTITY, MACROS, ROOT
from scripts.qualify_rafael_B0_B34_names_v1 import LABELS
from scripts.review_rafael_B0_B34_contextual_v1 import OUT as REVIEW
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE


BATCH='Rafael_SC0_B0_B34_clean_20261106'
FINAL=ROOT/'final_native_pages_v1.json'
PLAN=ROOT/'refined_plan_v3/automatic_plans.json'
SHEETS=ROOT/'body_review_sheets_v1/sheet_index.json'
NAMES=ROOT/'retained_name_planes_v2/native_name_planes.json'
MIDDLE=ROOT/'owned_middle_fields_visual_v1.json'
PREFS=ROOT/'ordinary_visual_preferences_v5.json'
VIEW=ROOT/'initial_complete_visual_review_v1.json'


def main():
    assert not VIEW.exists()
    doc,native,plan,sheets,names,middle,prefs,ledger,release,package=map(load,
        (REVIEW,FINAL,PLAN,SHEETS,NAMES,MIDDLE,PREFS,LEDGER,RELEASE,PACKAGE))
    assert doc['records_count']==283 and doc['counts']=={'revision':162,'retention':121}
    assert doc['remaining_current_comparisons']==0 and doc['first49_decisions_exactly_preserved']
    assert native['pages']==sheets['pages']==284 and len(native['records'])==283
    assert len(sheets['sheets'])==12 and sheets['native_receipt_sha256']==digest(FINAL)
    assert native['plan_sha256']==digest(PLAN) and plan['manuscript_sha256']==digest(FORMATTING)
    assert not plan['failures'] and not any(i['severity'] in ('error','warning') for r in plan['records'] for i in r['base_QA']['issues'])
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and not native['actual_gameplay']
    assert native['fresh_visual_delta_records']==4 and native['reused_unchanged_visual_records']==279
    assert names['scoped_actors']==39 and names['distinct_strings']==38 and len(names['review_sheets'])==4
    assert names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert middle['offline_visual_approved'] and not middle['direct_view_pending']
    assert len(middle['planes'])==18 and len(middle['negative_cases_rejected'])==8
    assert middle['name_data_plan']['changed_bytes']==9 and middle['name_data_plan']['complete_parent_inverse_exact']
    assert len(prefs['records'])==20 and prefs['additional_visual_findings']==16
    assert ledger['records_editorially_completed']==16748 and ledger[BATCH]['new_credit']==0
    reviewed_sheets=[*sheets['sheets'],*names['review_sheets'],middle['review_sheet']]
    assert all(digest(s['path'])==s['sha256'] for s in reviewed_sheets)
    save(VIEW,dict(body_pages=284,body_sheets=12,scoped_actors=39,distinct_progressive_name_strings=38,
        progressive_name_sheets=4,changed_middle_name_planes=18,changed_middle_name_sheets=1,
        all_listed_initial_body_andname_sheets_directly_viewed=True,sheets=reviewed_sheets,
        native=str(FINAL),native_sha256=digest(FINAL),name_planes=str(NAMES),name_planes_sha256=digest(NAMES),
        changed_name_visual=str(MIDDLE),changed_name_visual_sha256=digest(MIDDLE),
        four_refined_layouts_andfive_pages_native_andvisually_reviewed=True,
        further16_observed_wrap_candidates_pending=str(PREFS),further_candidates_sha256=digest(PREFS),
        all_final_formatting_gates_still_pending=True,actual_gameplay=False,new_credit=0))
    summary=('All 283 Rafael B0–B34 contextual decisions are saved: 162 revisions and 121 justified retentions. '
        'All 284 initial body pages and scoped name sheets passed native checks and direct visual review. '
        'Four wrap refinements pass; 16 further boundary candidates remain. Three exclusive full-name repairs '
        'pass offline glyph and ownership checks. Stored integration, representative gameplay and registration remain. '
        'Integrated coverage is 16,748 in Rafael4903.')
    text=f'''# Rafael B0–B34 prose and native checkpoint

{summary}

[283 contextual decisions](../{REVIEW.as_posix()}) preserve every one of the 49 earlier decisions exactly. The remaining 234 comparisons are complete. The ledger keeps each exact clean/current reference, gloss, finding, revision or justified retention and five explicit gates; formatting remains false until the final display and integration checks pass.

Corrections include the obsolete Proof name and omitted Indian Ocean destination; Plett Perrault, Kuhn and Xien consistency; the invented French Oui in a drunken hiccup; spying described as suspicion; unsupported chains and Lord Al; lost maneuver direction; and Aziza's reciprocal rescue changed into the feeling is mutual. Her keepsake realization remains comparative rather than denying that she ever wanted pirate greatness. The stray Japanese character at the start of B26 R33 and the full-width I in B5 R52 are corrected in the proposed text. Retentions have individual contextual reasons, including Claudio's rough Old man address to Pereira as familiarity rather than kinship.

The validated formatter planned all 283 ordinary speeches as 284 pages. There are no FE, style or caption objects in this batch. All 16 macro-bearing paragraphs, including combined FI/FA, pass the original native wrapper in four alignments. [Scoped macro proof](../{MACROS.as_posix()}). [Runtime identity](../{IDENTITY.as_posix()}). [Initial complete native proof](../work/Rafael_B0_B34_clean_20261106/native_pages_v1/compiled_native_pages.json).

Four phrase refinements were rerendered as five pages; the other 279 records retain byte-identical native evidence. The cabin question keeps its verb/object and destination together. Gerhard's seamanship line uses two readable rows. Rafael's musical offer stays together. The unchanged poem cannot fit any four-row word partition, so it retains two pages while carrying the complete memory image onto page two. Earlier cabin candidates created an orphaned word or a weak in ending; those failed trials are preserved and excluded. [Current clean plan](../{PLAN.as_posix()}). [Combined native proof](../{FINAL.as_posix()}).

All 12 complete body contact sheets, four progressive-name sheets and the changed-middle-name sheet were directly inspected. No clipped or mismatched leading/trailing glyphs were found in these new planes. The review identified 16 additional split-expression and isolated-tag candidates, now source/current/prose-hash bound in [preferences v5](../{PREFS.as_posix()}). Test those through the formatter, reject regressions, then rerender only byte-changed records and inspect their pages. Reuse the current complete native proofs for exact unchanged dependencies. [Visual receipt](../{VIEW.as_posix()}). This is offline coverage, not gameplay.

All 39 scoped speaker/role labels have individual decisions: 36 retentions and three full-name revisions. Both original clean/current name getters passed for all 39. The progressive labels remain unchanged. The three proposed middle fields produce Dinis de Albuquerque, Garcia de Oviedo and Antony von Kuhn. Each field is exclusively owned, fits its current allocation and has no unexpected aligned pointer references; only nine bytes change, with all other ARM9 bytes, sections, pointers and allocations exact and a complete parent inverse. Both getters and 18 old/new planes in two styles pass, including complete glyphs and bounds; eight negative proposal checks reject invalid edits. [Name decisions](../{LABELS.as_posix()}). [Owned-field/native/visual evidence](../{MIDDLE.as_posix()}). Style 1 is a second native plane test, not observed catalogue UI. Startup and deployment of these repairs remain pending.

The publisher's [Japanese rival introduction](https://www.gamecity.ne.jp/products/products/ee/new/dai4/dai4_06.htm) corroborates the Japanese フォン・クーン name and merchant context. Von is the source-based editorial rendering of フォン, not a claim that the publisher provides that Latin spelling or an added noble biography. The clean デ particles become de consistently with the retained source particles in Pedro de Valdes and Alonso de Rosa. No graphics artwork is changed.

Next finish the 16 wrap candidates, compile stored dialogue, apply the approved field proposal through its owned-name path, check exact reconstruction and stored pagination/branches, then run a focused display sequence covering the poem's page turn, corrected leading glyphs and names, battle/tavern transitions and representative conditional prose. Register only after necessary checks pass. No research ROM has been created in this checkpoint; the proposed ARM9 is a binary reference only. Current Rafael4903, promoted main, weekend package and all earlier ROMs remain unchanged. Full wider scope, separate artwork and the later older-record technical re-audit remain open. No guide photographs are requested.
'''
    evidence={str(p):digest(p) for p in (REVIEW,FINAL,PLAN,FORMATTING,MACROS,IDENTITY,VIEW,NAMES,MIDDLE,PREFS,LABELS,Path(__file__))}
    checkpoint(mutation=ROOT/'prose_native_checkpoint_v1',batch_key=BATCH,
        batch_updates=dict(new_credit=0,contextual_decisions=283,four_prose_gate_records=283,
            proposed_revisions=162,justified_retentions=121,remaining_current_comparisons=0,
            initial_native_speech_objects=283,initial_native_pages=284,initial_body_sheets_directly_viewed=12,
            refined_layouts_checked=4,remaining_wrap_candidates=16,scoped_names_reviewed=39,
            name_revisions=3,name_retentions=36,owned_name_changed_bytes=9,scoped_name_field_leads=0,
            current_name_data_repairs_offline_qualified_not_deployed=True,remaining_display_checks=283,
            native_job_live=False,representative_gameplay_pending=True,registered_integration_pending=True,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael B0–B34: all prose/native initial checks complete; final wrap refinements remain.',
            next_action='Test 16 observed wrap candidates, then stored scripts, representative gameplay and registered release.',
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,
            registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael_B0_B34_native_20261106.md',document_text=text,
        completed=16748,protected={str(REGISTRY):release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved complete prose and initial native/visual coverage; 16 wrap candidates and integration remain. No new credit.')


if __name__=='__main__':main()
