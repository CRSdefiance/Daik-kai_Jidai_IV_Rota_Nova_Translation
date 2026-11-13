"""Seal34 prose/native formatting reviews;reference and release still pending."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_post_Seville_font_approval_v2740')
OLD=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v3.json')
DOC=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v4.json')
FONTS=Path('work/analysis/lil_post_Seville_fonts_v2739/current_macro_QA_and_progressive_font_proof.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));font=read(FONTS);prior=read(font['reused_proof'])
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and font['all34_full_QA_and_complete_native_fonts_pass']
    assert len(font['cases'])==len(font['all34_full_QA_reports'])==34 and font['current_original_macro_alignment_calls']==272
    assert font['newly_executed_current_macro_alignment_calls']==32 and font['reused_current_macro_alignment_calls']==240
    assert font['newly_executed_font_cases']==4 and font['reused_unchanged_font_cases']==30
    assert font['candidate_sha256']==doc['current_ROM_sha256'] and font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    assert len(font['review_sheets'])==5
    for sheet in font['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert [s['sha256'] for s in font['review_sheets'][:2]]==[s['sha256'] for s in prior['review_sheets'][:2]]
    # All five2737sheets andchanged2739sheets3/4/5were viewed in this turn.
    cases={r['id']:r for r in font['cases']};reports={r['id']:r for r in font['all34_full_QA_reports']}
    for row in doc['records']:
        case=cases[row['id']];assert case['encoded_hex']==reports[row['id']]['encoded_hex']
        assert case['complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert case['all_visible_origins_zero_and16px_rows_within4rows']
        row['review']['formatting']=True
        row.update(compiled_hex=case['encoded_hex'],native_font_case=case,record_index=row['current_record_index'],current_text_hex=row['current_hex'],
            native_display_consumer='original_progressive_54020',status='source-prose-current-native-formatting-approved;reference-representative-release-pending')
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),native_font_proof=str(FONTS),native_font_proof_sha256=sha(FONTS.read_bytes()),
        formatting_review_pending=False,all34_current_native_cases_and272_macro_calls_bound=True,
        all5_review_sheets_viewed_or_identical_to_previously_viewed=True,
        four_detected_phrase_flow_findings_resolved_without_waiver=True,
        status='source-prose-current-native-formatting-approved;reference-representative-release-pending')
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':22,'retain-wording':12}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==11
    validate_natural_dialogue_batch(doc)
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_font_proof=str(FONTS),native_font_proof_sha256=sha(FONTS.read_bytes()),
        all34_five_per_record_review_gates_true=True,all34_complete_current_fonts_and272_macro_calls_bound=True,new_macro_calls32_reused240=True,
        all5_review_sheets_viewed_or_exact_previously_viewed=True,phrase_flow_refinements=doc['phrase_flow_refinements'],
        narrow_line_count_notes=11,no_orphan_predicate_weak_ending_missing_glyph_or_blank_page_waivers=True,
        actual_B30_B31_B132_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,
        source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('34source/prose/native reviews sealed:22revisions/12retentions;all5gates,272current macro calls/34fonts;four phrase-flow findings resolved. References/release pending.')
