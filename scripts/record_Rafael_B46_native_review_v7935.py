"""Record direct review of24 native pages/eight choice planes; actual/stored/release gates stay open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_native_review_v7935')
DOC=Path('translations/rafael_B46_editorial_manuscript_v1.json')
OUTPUT=Path('translations/rafael_B46_editorial_manuscript_v2.json')
PLAN=Path('work/analysis/Rafael_B46_layout_v7932/24_automatic_plans_full_native_width_zero_preamble_separate_body.json')
NATIVE=Path('work/analysis/Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json')
CHOICES=Path('work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json')
REASONS={
15:"One complete relief sentence uses the full original viewport without the inherited Japanese staging break. Hayreddin and the final lives. are complete.",
18:"The quiet trailing acknowledgment is complete on one row. Its brevity is intentional characterization, not a narrow wrap to be filled with invented words.",
23:"Three rows preserve may challenge as a verbal unit. Exhaustive native-budget two-row enumeration yields only a split after may; the selected automatic layout avoids that weak modal ending without narrowing216px or changing the wording.",
27:"Two rows retain the natural offer and complete at sea phrase. What else/you can do is an ordinary complete-word continuation, not a clipped character or extra page.",
41:"Three rows retain all three actions. The last and search. is a complete final action in the coordinated list, not an orphaned function word. No prose was shortened to fit.",
44:"Three rows preserve both targets and both purposes. The first row ends after the target list's comma; the final selection clause remains readable and all final punctuation appears.",
47:"Each complete sentence fits its own row, ending coast. and things. The possibility and variety remain together with no short orphan or early fixed allocation.",
51:"Two rows preserve both nearby target types. Nearby/cities is an ordinary complete-word continuation; cities and fleets stay together. The original216px usable budget is fully available.",
54:"Two rows keep magnifying glass and Inspect mode together. The first row ends at the complete icon description; source Y and all letters survive in the distinct FE renderer.",
58:"Two balanced rows preserve city/fleet, magnifier and A. Aim/the magnifier is an ordinary verb/object continuation across a complete-word boundary, not an authored staging break or missing glyph.",
62:"Two rows preserve the complete ship-attack rule and both target classes. And fleets. is the meaningful second target, not an isolated conjunction.",
65:"Three rows keep Inspect mode and Battle mode intact. The initial mode condition is a complete phrase; the second row explains the sword icon, followed by its complete mode label. No bitmap-width216/228 confusion is allowed.",
68:"Two rows preserve the sword cursor, both battle targets and A confirmation. The complete first row ends with sword; the second supplies the target/confirmation.",
72:"Two rows keep items or supplies and Inspect mode readable. The second row starts with the complete at sea qualification; R remains intact.",
76:"Two short complete sentences explain the gray frame and Search mode. These natural sentences replace inherited Japanese staging without authored hard breaks or redundant prose.",
80:"Two rows preserve searching land inside the gray frame. The frame phrase remains whole and the A instruction and final punctuation render completely.",
83:"Two rows put the complete three-mode list together after the cycling instruction. L/R and all three mode names remain visible; no third row is needed.",
87:"Two rows preserve the exact L order. A normal list boundary follows Inspect, and Battle, then Search. remains readable as the remaining sequence.",
91:"Two rows keep R or Y together and put the entire reverse mode order on the second row. No button or ordering information is sacrificed for width.",
95:"The complete two-question understanding check fits one row. Its conversational brevity is appropriate on the acceptance path.",
98:"One complete polite reply and named thanks fit without a staging break, new title or extra page.",
105:"Two rows keep don't let together and your guard down at sea together. The decline-path caution remains natural; no narrow viewport or expanded threat is introduced.",
109:"The one-word acknowledgment is complete in context and remains on one row.",
117:"The entire parenthesized unfinished private thought fits one row, including both parentheses and all three trailing dots. It is not completed with an invented goal.",
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc,plan,native,choices=map(read,[DOC,PLAN,NATIVE,CHOICES])
    assert plan['manuscript_sha256']==native['manuscript_sha256']==choices['manuscript_sha256']==sha(DOC.read_bytes())
    assert native['plan_sha256']==sha(PLAN.read_bytes()) and not plan['failures']
    assert len(native['records'])==24 and native['fresh_compiled_alignment_cases']==96
    assert native['complete_progressive_pages']==native['complete_FE_logical_andphysical_pages']==12
    assert choices['complete_current_andreviewed_label_style_planes']==8
    assert not any(i['severity'] in ['warning','error'] for p in plan['records'] for i in p['base_QA']['issues'])
    assert sum(len(p['base_QA']['issues']) for p in plan['records'])==14
    sheets=[]
    for s in native['review_sheets']+[choices['review_sheet']]:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append(dict(**s,directly_viewed=True,finding='Complete selected native pages/choices directly viewed; clear full glyphs and punctuation with original bounds. Offline proof, not B46 gameplay.'))
    assert len(sheets)==5
    warning=next(p for p in plan['records'] if p['source_record_index']==23);words=warning['logical_English'].split();two=[]
    for n in range(1,len(words)):
        a,b=' '.join(words[:n]),' '.join(words[n:])
        if len(a)+int(len(a)%2==0)<=36 and len(b)+1<=36:two.append(dict(first=a,second=b,first_length=len(a),second_length=len(b)))
    assert len(two)==1 and two[0]['first'].endswith(' may') and len(warning['lines'])==3
    updated=deepcopy(doc);rows=[]
    for row,p,n in zip(updated['records'],plan['records'],native['records'],strict=True):
        assert row['id']==p['id']==n['id'] and n['compiled_hex']==p['encoded_hex'] and row['english']==n['logical_English']
        assert len(n['pages'])==1 and not row['review']['formatting']
        row.update(compiled_hex=p['encoded_hex'],planned_English_markup=p['planning_record']['english'],formatted_markup=p['formatted_markup'],
            automatic_lines=p['lines'],row_count_reason=REASONS[row['source_record_index']],base_QA_report=p['base_QA'],
            qa_waivers=[],qa_waiver_reason=None,native_page_count=1,complete_native_font_pages=deepcopy(n['pages']),
            complete_native_compiled_alignment=deepcopy(n['native_alignment']),
            native_pages_directly_viewed=True,stored_relocation_actual_andregistered_release_pending=True)
        rows.append(row)
    reviewed=next(c for c in choices['records'] if c['version']=='reviewed-trimmed')
    for row in updated['typed_choice_records']:
        planes=[p for p in reviewed['planes'] if p['index']==row['option_index']]
        assert len(planes)==2 and not row['review']['formatting']
        row.update(compiled_hex=row['english'].encode('ascii').hex(),target_menu_object_hex=choices['target_menu_object_hex'],
            native_caption_width_px=66,native_caption_height_px=12,complete_native_caption_planes=deepcopy(planes),
            native_choice_wording_retained_storage_padding_removed=True,native_caption_directly_viewed=True,
            native_caption_reason='The original constructor sizes both complete trimmed labels at66px. Removing storage-only spaces restores visible centering without manual alignment, abbreviations, order or wording changes.',
            actual_view_backing_highlights_ordinary_input_selection_andbranch_return_pending=True)
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,NATIVE,CHOICES,Path(__file__)]}
    updated.update(prior_manuscript=str(DOC),prior_manuscript_sha256=sha(DOC.read_bytes()),
        native_page_proof=str(NATIVE),native_page_proof_sha256=sha(NATIVE.read_bytes()),
        automatic_layout_plan=str(PLAN),automatic_layout_plan_sha256=sha(PLAN.read_bytes()),
        native_choice_font_proof=str(CHOICES),native_choice_font_proof_sha256=sha(CHOICES.read_bytes()),
        all24_complete_native_single_pages_andindividual_row_reasons_recorded=True,
        all2_choice_wordings_retained8_current_target_planes_original_geometry_andcentering_verified=True,
        original_FE_bitmap228_usable_text216_measured_separately=True,
        actual_review_sheets=sheets,all_five_native_sheets_directly_viewed=True,
        all26_formatting_gates_false=True,formatting_review_pending=True,
        only_remaining_native_stored_controls_reference_actual_policy_andatomic_release_gates_pending=True)
    updated['evidence']=dict(updated['evidence'])|evidence
    ROOT.mkdir(parents=True);save(OUTPUT,updated)
    save(ROOT/'24_pages2_choices_full_native_review_individual_wrap_reasons.json',dict(
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),records=rows,
        typed_choice_records=updated['typed_choice_records'],directly_viewed_sheets=sheets,
        native_page_count=24,complete_FE_pages=12,compiled_alignment_cases=96,native_choice_style_planes=8,
        all_complete_leading_internal_trailing_characters_punctuation_bounds_consumption_andpagination_pass=True,
        R23_two_row_budget_alternatives=two,R23_three_rows_retained_to_avoid_modal_break=True,
        row_count_infos=14,all_original_QA_issues_preserved_no_warnings_orwaivers=True,
        source00_preambles_andbody_NUL_guards_unchanged=True,
        body_andchoice_English_wordings_unchanged_from_v1_seven_revisions19_retentions=True,
        full_source_current_conditional_context_native_names_andmode_order_preserved=True,
        stored_layout_relocation_branches_inverse_loaders_callers_actual_scenes_menu_backing_policy_andrelease_pending=True,
        actual_B46_gameplay_coverage=0,new_emulator_runs=0,new_credit=0,evidence=evidence,full_goal_complete=False))
    print('24 complete pages/two choices/five sheets viewed; individual row reasons14 infos/no waivers. V2 wording unchanged. Stored/actual/release pending; no credit.')
