"""Record directly viewed complete native pages/names andtwo exact ordinary-boundary exceptions."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_native_review_v7988')
DOC=Path('translations/rafael_B47_editorial_manuscript_v1.json')
OUTPUT=Path('translations/rafael_B47_editorial_manuscript_v2.json')
NAME_OLD=Path('translations/rafael_B47_speaker_name_review_v1.json')
NAME_NEW=Path('translations/rafael_B47_speaker_name_review_v2.json')
PLAN=Path('work/analysis/Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json')
NATIVE=Path('work/analysis/Rafael_B47_pages_v7985/15_complete_native_paragraphs16_pages60_compiled_alignments.json')
SOURCE=Path('work/analysis/Rafael_B47_source_name_planes_v7986/15_complete_source_pages4_names16_literal_alignments_all_progressive.json')
NAME_SHEET=Path('work/analysis/Rafael_B47_native_review_assets_v7987/review_sheet_receipt.json')
REASONS={
    5:"Three full-width rows replace the inherited planner's four-row solution. The complete ordinary to/get continuation keeps 'get around' together and avoids a short extra row. The preposition is complete; the first I, Hayreddin and final now. are intact. No words, font metrics, guards or viewport are changed.",
    17:"Two rows preserve Janus's complete measured agreement and conversational danger statement. Pirates/attack is an ordinary complete-word subject/verb continuation. The nearby Mediterranean reference supplies enter's understood object without invented prose.",
    44:"Two balanced rows break at the semicolon between caution and reason. Both clauses are complete and naturally paced; the full original216px width remains available.",
    48:"The complete brief question occupies one row and needs no staging break, padding-created row or added explanation.",
    53:"The complete territory-and-risk explanation requires more than four native rows. Automatic sentence-aware pagination uses four physical rows for the territory description and two on the second page for the complete conditional warning. The page turns after territory., not inside the conditional clause. Both original native pages preserve every glyph; the extra page is not avoided by shortening meaning. Focused actual page-turn validation remains required.",
    63:"Three rows replace the inherited four-row wrap. The ordinary with/Pasha's continuation keeps the complete force reference together while avoiding an extra short row. The preposition is complete, both phrase and punctuation survive, and no global weak-ending rule is changed.",
    70:"Four readable rows preserve both identified forces and the explicit Mediterranean conclusion. The source alternatives stay exclusive. The concluding leave/the Mediterranean continuation is ordinary complete-word flow, with no altered territorial fact or narrowed viewport.",
    77:"Three balanced rows retain the natural contract advice and complete provocation caution. The final sentence occupies its own row after the sentence boundary; no authored dramatic break is needed.",
    81:"Four rows preserve the contrast, possibility and limited recruiting purpose. The complete at least phrase remains together; the final two rows are balanced rather than leaving for some. as a short last fragment.",
    92:"Janus's complete brief approval remains on one row; its brevity is appropriate characterization and needs no invented words.",
    102:"Four rows preserve Claudio's conditional preparation, stronger ships and personal training. Other waters and toughen ourselves up remain readable. The ordinary heading/into continuation is complete and does not lose a glyph.",
    106:"Two rows preserve the complete reminder and navigator target. Large/cities is a normal complete-word adjective/noun wrap; the final recruit navigators. remains intact.",
    110:"The full surprised reaction fits one row, including its first W and final exclamation point. No inherited staging break or extra page remains.",
    122:"Janus's lightly wry complete observation fits one row and remains distinct from Rafael's preceding reaction and following resolve.",
    129:"The complete renewed resolve fits one row, including All right and the final exclamation point, without adding a task or destination.",
}
EXCEPTIONS={
    5:dict(code='weak-line-ending',message="line 2 ends with weak wrap word 'to'",severity='warning'),
    63:dict(code='weak-line-ending',message="line 2 ends with weak wrap word 'with'",severity='warning'),
}
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [OUTPUT,NAME_NEW])
    doc,plan,native,source,names,sheet=map(read,[DOC,PLAN,NATIVE,SOURCE,NAME_OLD,NAME_SHEET])
    assert plan['manuscript_sha256']==native['manuscript_sha256']==sha(DOC.read_bytes()) and native['plan_sha256']==sha(PLAN.read_bytes())
    assert len(native['records'])==15 and native['complete_progressive_pages']==16 and native['fresh_compiled_alignment_cases']==60
    assert source['source_complete_native_pages']==15 and source['current_name_literal_alignment_cases']==16 and len(source['name_planes'])==4
    assert sheet['source_sha256']==sha(SOURCE.read_bytes()) and sha(Path(sheet['sheet']).read_bytes())==sheet['sheet_sha256']
    viewed=[]
    for s in native['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        viewed.append(dict(**s,directly_viewed=True,finding='Complete native body pages directly inspected,including both R53 pages. Offline glyph/bound/pagination evidence,not actual B47 gameplay.'))
    viewed.append(dict(path=sheet['sheet'],sha256=sheet['sheet_sha256'],directly_viewed=True,
        finding='All four complete original-style11 names inspected: Rafael Castor,Janus Pasar,Claudio Manaus,Julio Erneco. No catalogue UI oractual B47 header claim.'))
    assert len(viewed)==4
    updated=deepcopy(doc);info_count=0;warnings=[]
    for row,p,n in zip(updated['records'],plan['records'],native['records'],strict=True):
        index=row['source_record_index']
        assert row['id']==p['id']==n['id'] and row['english']==n['logical_English'] and p['encoded_hex']==n['compiled_hex']
        assert len(n['pages'])==p['expected_native_pages']==(2 if index==53 else 1)
        issues=p['base_QA']['issues'];actual_warnings=[i for i in issues if i['severity']=='warning']
        assert not any(i['severity']=='error' for i in issues)
        assert actual_warnings==([EXCEPTIONS[index]] if index in EXCEPTIONS else [])
        info_count+=sum(i['code']=='line-break-count' for i in issues)
        reason=REASONS[index];waiver_reason=None;waivers=[];scope=None
        if actual_warnings:
            last='to' if index==5 else 'with';first='get' if index==5 else "Pasha's"
            assert p['lines'][1].endswith(' '+last) and p['lines'][2].startswith(first+' ')
            waiver_reason=reason+" This exception is restricted to this exact source-qualified record,unchanged English,compiled plan andline2 boundary. The original warning remains in the QA report. It permits no glyph loss,overflow,blank page,changed source control orother weak boundary."
            waivers=['weak-line-ending'];scope=dict(id=row['id'],source_hex=row['source_hex'],compiled_hex=p['encoded_hex'],
                line=2,last_word=last,next_word=first,exact_issue=EXCEPTIONS[index])
            warnings.append(dict(id=row['id'],issue=EXCEPTIONS[index],scope=scope,reason=waiver_reason))
        row.update(compiled_hex=p['encoded_hex'],planned_English_markup=p['planning_record']['english'],
            formatted_markup=p['formatted_markup'],automatic_lines=p['lines'],row_count_reason=reason,
            base_QA_report=p['base_QA'],qa_waivers=waivers,qa_waiver_reason=waiver_reason,qa_waiver_scope=scope,
            native_page_count=len(n['pages']),complete_native_font_pages=deepcopy(n['pages']),
            complete_native_compiled_alignment=deepcopy(n['native_alignment']),native_pages_directly_viewed=True,
            stored_relocation_actual_page_transition_policy_andregistered_release_pending=True)
        assert not row['review']['formatting']
    assert info_count==6 and len(warnings)==2
    revised_names=deepcopy(names)
    for row in revised_names['records']:
        plane=next(p for p in source['name_planes'] if p['actor_ID']==row['actor_ID'])
        assert plane['text']==row['name'] and sha(Path(plane['native_plane']).read_bytes())==plane['native_plane_sha256']
        row.update(complete_native_name_plane=deepcopy(plane),native_name_plane_directly_viewed=True,
            native_complete_first_internal_final_characters_width_andbounds_pass=True,
            actual_B47_headers_andcatalogue_UI_still_pending=True)
        assert not row['review']['formatting']
    revised_names.update(prior_review=str(NAME_OLD),prior_review_sha256=sha(NAME_OLD.read_bytes()),
        native_source_name_proof=str(SOURCE),native_source_name_proof_sha256=sha(SOURCE.read_bytes()),
        directly_viewed_sheet=viewed[-1],full207_name_role_alias_review_active=True)
    save(NAME_NEW,revised_names)
    updated.update(prior_manuscript=str(DOC),prior_manuscript_sha256=sha(DOC.read_bytes()),
        native_page_proof=str(NATIVE),native_page_proof_sha256=sha(NATIVE.read_bytes()),
        source_name_page_proof=str(SOURCE),source_name_page_proof_sha256=sha(SOURCE.read_bytes()),
        automatic_layout_plan=str(PLAN),automatic_layout_plan_sha256=sha(PLAN.read_bytes()),
        names_packet=str(NAME_NEW),native_review_sheets=viewed,all_four_native_review_sheets_directly_viewed=True,
        all15_native_paragraphs16_pages_complete=True,R53_sentence_boundary_two_pages_requires_actual_transition=True,
        original_QA_infos=6,original_exact_ordinary_boundary_warnings=warnings,
        all_original_QA_issues_preserved_two_narrow_documented_exceptions=True,
        all15_formatting_gates_false=True,formatting_review_pending=True,
        retrospective_weak_before_row_priority_lead_beyond_B47_remains_open=True,
        status='15-source-context-prose-native-pages-reviewed-stored-actual-policy-release-pending')
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,NATIVE,SOURCE,NAME_OLD,NAME_NEW,NAME_SHEET,Path(__file__)]}
    updated['evidence']=dict(updated['evidence'])|evidence
    ROOT.mkdir(parents=True);save(OUTPUT,updated)
    save(ROOT/'15_paragraphs16_native_pages4_names_two_scoped_warnings_individual_wrap_review.json',dict(
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),names=str(NAME_NEW),names_sha256=sha(NAME_NEW.read_bytes()),
        records=updated['records'],directly_viewed_sheets=viewed,native_page_count=16,compiled_alignment_cases=60,
        source_native_pages=15,name_literal_alignment_cases=16,original_row_count_infos=6,
        preserved_warning_exceptions=warnings,no_QA_warning_removed_orrewritten=True,
        all15_wordings_source_controls_and8_revisions7_retentions_unchanged=True,
        R5_R63_early_added_rows_removed_without_shortening_prose=True,
        R53_original_four_row_page_turn_sentence_boundary_all_bytes_andglyphs_complete=True,
        stored_inverse_fullcontrols_actual_page_transition_frozen_policy_atomic_andregistered_release_pending=True,
        actual_B47_gameplay_coverage=0,new_emulator_runs=0,new_credit=0,evidence=evidence,full_goal_complete=False))
    print('15 paragraphs/16 native pages/four names/four sheets reviewed. Six infos andtwo exact warning exceptions retained.V2 prose unchanged;stored/actual/R53 transition/policy/release pending.')
