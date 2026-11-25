"""Record direct review of all twelve complete native pages; keep actual/release gates open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_native_review_v7883')
BEFORE=Path('work/analysis/Rafael_B45_layout_v7881/12_automatic_plans_full_native_width_zero_preamble_separate_body.json')
PLAN=Path('work/analysis/Rafael_B45_layout_v7881b/12_automatic_plans_full_native_width_zero_preamble_separate_body.json')
NATIVE=Path('work/analysis/Rafael_B45_pages_v7882/12_complete_native_pages48_compiled_alignments_distinct_FE.json')
MANUSCRIPT=Path('translations/rafael_B45_editorial_manuscript_v2.json')
OUTPUT=Path('translations/rafael_B45_editorial_manuscript_v3.json')
REASONS={
    5:"One complete natural question. No inherited source staging break is needed; Julio's following call answers it.",
    9:"One short emphatic call is appropriate dialogue, not an unnecessarily narrow wrap.",
    13:"One complete realization with the trailing pause intact. Market remains together.",
    18:"Four full-width rows preserve the complete conditional instruction. The break after you is an ordinary complete-word boundary. The final But remember... is a coherent warning that leads to R21, not an isolated orphan or new page.",
    21:"One complete explanatory sentence uses the available width and leads naturally to Rafael's question.",
    24:"The short questioning echo is complete in context and should not be artificially lengthened.",
    29:"Four rows keep contract fee, local ruler and Governor's Office readable as units. The first row ends at the complete local-ruler phrase; the lower fill follows those units, not a narrowed viewport. Palace/or Governor's Office remains one continuous alternative across the wrap. All payment, destination and trading-rights facts remain.",
    33:"Four rows align the recommendation and early-stage qualification as coherent phrases. The final minimum-fee sentence remains intact; no manual break or narrowed-width rule is added.",
    37:"Three rows retain Julio's responsibility and Rafael's future role. Next/ones is an ordinary complete-word continuation within the instruction; ones yourself. is a meaningful two-word conclusion, not a dropped or isolated glyph.",
    52:"Four rows fit the measured216px text budget inside the original228px FE bitmap. Market share, 20 percent and local stock remain coherent units; determines how much forms a complete phrase. All words, FO and the final buy. render in one complete native page without the failed extra blank row.",
    58:"Two rows preserve the optional invitation. Want/to sell is a normal complete-word continuation, not authored early wrapping or an invented deadline.",
    61:"One complete brief assent ends the exchange. It does not assert that a sale has already occurred.",
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();before,plan,native,doc=map(read,[BEFORE,PLAN,NATIVE,MANUSCRIPT])
    assert before['records']==plan['records'] and before['failures']==plan['failures']==[]
    assert native['plan_sha256']==sha(BEFORE.read_bytes()) and native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert native['fresh_compiled_alignment_cases']==48 and len(native['records'])==12
    assert native['complete_progressive_pages']==11 and native['complete_FE_logical_andphysical_pages']==1
    sheets=[]
    for s in native['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append(dict(**s,directly_viewed=True,
            finding='All twelve complete source-contextual English panes viewed across both sheets;complete leading/internal/trailing letters and punctuation,legible automatic wraps andsingle-page consumption.No actual B45 gameplay approval.'))
    assert len(sheets)==2
    updated=deepcopy(doc)
    for row,p,n in zip(updated['records'],plan['records'],native['records'],strict=True):
        assert row['id']==p['id']==n['id'] and row['english']==n['logical_English']
        assert not row['review']['formatting'] and not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        assert len(n['pages'])==1
        for page in n['pages']:
            assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
        row.update(compiled_hex=p['encoded_hex'],automatic_formatted_markup=p['formatted_markup'],
            automatic_lines=p['lines'],automatic_line_lengths=p['line_lengths'],automatic_row_review=REASONS[row['source_record_index']],
            complete_native_page_proof=n,native_pages_androw_boundaries_directly_viewed=True,
            actual_scene_andstored_parity_tail_display_not_yet_approved=True)
    updated.update(prior_manuscript=dict(path=str(MANUSCRIPT),sha256=sha(MANUSCRIPT.read_bytes())),
        native_page_proof=str(NATIVE),native_page_proof_sha256=sha(NATIVE.read_bytes()),
        automatic_layout_plan=str(PLAN),automatic_layout_plan_sha256=sha(PLAN.read_bytes()),
        all12_complete_native_pages_andindividual_row_reasons_recorded=True,
        original_FE_bitmap228_usable_text216_measured_separately=True,
        all12_formatting_gates_false_until_stored_source_controls_policy_actual_andrelease_checks=True)
    save(OUTPUT,updated)
    ROOT.mkdir(parents=True);rebound=deepcopy(native)
    rebound.update(plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        original_native_proof=str(NATIVE),original_native_proof_sha256=sha(NATIVE.read_bytes()),
        no_new_native_runs_same12_encoded_records_andall_QA_objects_exact=True,
        direct_visual_review=sheets,visual_review_pending=False,
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()))
    save(ROOT/'12_exact_native_pages_rebound_with_individual_row_review.json',rebound)
    save(ROOT/'native_visual_review_andexact_plan_guard_rebinding.json',dict(
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        source_plan=str(BEFORE),source_plan_sha256=sha(BEFORE.read_bytes()),current_plan=str(PLAN),current_plan_sha256=sha(PLAN.read_bytes()),
        all12_encoded_records_planning_records_lines_andQA_objects_exact=True,
        original_native_proof=str(NATIVE),original_native_proof_sha256=sha(NATIVE.read_bytes()),
        reused_native_pages=12,reused_compiled_alignment_cases=48,new_native_runs=0,
        direct_visual_review=sheets,all12_individual_row_reasons=True,all12_formatting_false=True,
        whole_controls_relocation_stored_parity_actual_policy_andregistered_release_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('All12 complete native pages andtwo sheets viewed;individual wrap reasons recorded. Same encoded/QA objects rebound;no duplicated native run. Formatting,actual andintegration remain open.')
