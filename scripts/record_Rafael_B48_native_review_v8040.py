"""Record direct review of final92 native pages andnine names; two exact warnings remain scoped."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_native_review_v8040')
DOC=Path('translations/rafael_B48_editorial_manuscript_v2.json')
OUT=Path('translations/rafael_B48_editorial_manuscript_v3.json')
NAMES=Path('translations/rafael_B48_speaker_name_review_v1.json')
NAMES_OUT=Path('translations/rafael_B48_speaker_name_review_v2.json')
PLAN=Path('work/analysis/Rafael_B48_layout_v8035d/91_automatic_plans_full_native_width_source_preambles4_FE.json')
NATIVE=Path('work/analysis/Rafael_B48_pages_refined_v8038/91_final_native_paragraphs92_pages4_fresh360_reused_alignments.json')
SOURCE=Path('work/analysis/Rafael_B48_source_name_planes_v8037/91_complete_source_pages9_names36_literal_alignments4_FE.json')
NAME_SHEET=Path('work/analysis/Rafael_B48_name_review_assets_v8039/review_sheet_receipt.json')
SPECIAL={
86:"Two readable rows keep the complete Proof of Conquest title together on the second row. The ordinary article/the boundary is complete,with no extra short row,word loss or altered metrics. The original line1 weak-ending warning stays recorded andis waived only for this exact source/id/logical English/compiled plan/boundary.",
140:"Three rows preserve the complete arrival/passsage request andkeep aren't you? together on row2. The earlier generated row2aren't/row3you? split was corrected by an automatic phrase preference,with no added row or prose change. Fresh native checks replace this one compiled record;90 exact records reuse prior proofs.",
171:"The complete intentional silent ellipsis stays as source CP9328163. Its original12px multibyte width andcomplete independent native glyph are retained;no ASCII substitute,staging break ornew dialogue is authored.",
217:"Three rows retain the assistant role,the deliberate young...man hesitation,throat clearing andintroduction. The short dramatic phrase is part ofthe source characterization;ordinary wraps remain formatter-owned.",
247:"Three rows preserve both not-only-academic meaning andthe hesitant young-man presentation. The final young man phrase is intact;it is not shortened or explained away to avoid the third row.",
280:"Three rows retain the full reassurance andcomplete isn't it,Claudio? tag. The natural question is not split inside its short tag or shortened tofit an inherited row count.",
347:"Five full-width rows produce two original native pages. Page1contains four readable rows andpage2the complete continuation sealed on maps ofvarious shapes. The former seven-row plan had manufactured short internal rows solely toend a page at the sentence boundary. The final automatic preference avoids that early wrapping while preserving all words,seven treasures,Seven Sages andsource attribution. Native page2leading s atoriginal[6,0] andfinalshapes. arecomplete;ordinary actual page-turn testing remains required.",
370:"Four rows preserve every effective-predecessor English word andthe exact FI substitution,expanded only toits measured Rafael default for this proof. The ordinary I replaces the old stray full-width I;complete first/internal/final bytes andglyphs pass. No custom player-name coverage isclaimed.",
406:"Three fuller rows preserve the recent,uncertain rumor andsouthern-African direction. The complete ordinary of/Conquest boundary leaves no cropped glyph andavoids manufacturing an extra short row merely toescape a soft preposition warning. The full title remains inone paragraph andevery word survives. The exact original line2weak-ending warning isretained with an id/source/text/compiled/line-bound exception.",
427:"Two rows onthe original FEpaper preserve Hans Letzel's complete surname,including the previously missing final l,andhis naturalist role. Joining you does not imply an assignable navigator. Original216pxusable text/228pxbitmap andnull-actor consumer remain.",
431:"Three FErows preserve the navigator-specific Deck assignment limitation in full. The paper's12pxrow pitch andoriginal logical/physical bounds remain distinct from progressive dialogue.",
435:"Two complete FErows preserve the newly available player action anddetailed item-information function;no new automatic revelation mechanic is implied.",
438:"Two complete FErows retain the exact X instruction andthe item-information context. X andthe finalperiod fit the originalpaper bounds without abbreviated wording.",
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES_OUT.exists()
    doc,names,plan,native,source,name_sheet=map(read,[DOC,NAMES,PLAN,NATIVE,SOURCE,NAME_SHEET])
    assert plan['manuscript_sha256']==native['manuscript_sha256']==sha(DOC.read_bytes()) and native['plan_sha256']==sha(PLAN.read_bytes())
    assert len(native['records'])==91 and sum(len(r['pages']) for r in native['records'])==92
    assert native['fresh_compiled_alignment_cases']==4 and native['reused_compiled_alignment_cases']==360
    assert source['source_complete_native_pages']==91 and len(source['name_planes'])==9
    sheets=deepcopy(native['review_sheets'])+[dict(path=name_sheet['sheet'],sha256=name_sheet['sheet_sha256'])]
    assert len(sheets)==17
    for s in sheets:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        s.update(directly_viewed=True,finding='Complete first/internal/final glyphs andreadable word flow inspected. Final body sheets use the corrected R140 tag layout;the name sheet distinguishes the synthetic full-getter text from actual catalogue UI.')
    infos=[];waivers=[]
    for row,p,n in zip(doc['records'],plan['records'],native['records'],strict=True):
        assert row['id']==p['id']==n['id'] and row['source_hex']==p['source_hex']
        assert p['encoded_hex']==n['compiled_hex'] and not row['review']['formatting']
        assert ' '.join(p['lines'])==row['english']
        assert len(n['pages'])==p['expected_native_pages']
        issues=p['base_QA']['issues'];warnings=[i for i in issues if i['severity']=='warning']
        assert not any(i['severity']=='error' for i in issues)
        reason=SPECIAL.get(row['source_record_index'])
        if reason is None:
            count=len(p['lines']);boundary='; '.join(a['last']+'/'+a['first'] for a in p['automatic_boundaries']) or 'none:complete single-row utterance'
            reason=f"{count} original native row(s) preserve the entire logical paragraph at216pxusable width without Japanese staging breaks. Complete-word boundaries: {boundary}. The selected lines were read with this source-bound character beat: {row['source_meaning']} All words,punctuation andsource substitutions remain;first/internal/final native glyphs,bounds andconsumption match independently."
        row.update(compiled_hex=p['encoded_hex'],planned_English_markup=p['planning_record']['english'],
            formatted_markup=p['formatted_markup'],automatic_lines=p['lines'],row_count_reason=reason,
            base_QA_report=p['base_QA'],qa_waivers=[],qa_waiver_reason=None,qa_waiver_scope=None,
            native_page_count=len(n['pages']),complete_native_font_pages=n['pages'],
            complete_native_compiled_alignment=n['native_alignment'],native_pages_directly_viewed=True,
            stored_relocation_actual_page_transition_policy_andregistered_release_pending=True)
        infos.extend(dict(id=row['id'],issue=i) for i in issues if i['severity']=='info')
        if warnings:
            index=row['source_record_index'];assert index in [86,406] and len(warnings)==1
            line,last,nextword=(1,'the','Proof') if index==86 else (2,'of','Conquest')
            assert warnings[0]==dict(code='weak-line-ending',message=f"line {line} ends with weak wrap word '{last}'",severity='warning')
            assert p['lines'][line-1].split()[-1]==last and p['lines'][line].split()[0]==nextword
            scope=dict(id=row['id'],source_hex=row['source_hex'],logical_English=row['logical_English'],
                compiled_hex=p['encoded_hex'],line=line,last_word=last,next_word=nextword,exact_issue=warnings[0])
            row.update(qa_waivers=['weak-line-ending'],qa_waiver_reason=reason,
                qa_waiver_scope=scope)
            waivers.append(dict(id=row['id'],scope=scope,reason=reason))
    assert len(infos)==37 and all(i['issue']['code']=='line-break-count' for i in infos) and len(waivers)==2
    for row in names['records']:
        plane=next(n for n in source['name_planes'] if n['actor_ID']==row['actor_ID'])
        assert plane['text']==row['name']
        row.update(complete_native_name_plane=plane,native_name_plane_directly_viewed=True,
            native_complete_first_internal_final_characters_width_andbounds_pass=True,
            actual_B48_headers_andcatalogue_UI_still_pending=True)
        if row['actor_ID']==8:row['full_getter_synthetic_original_name_style_proof']=name_sheet['entries'][-1]
    names.update(prior_review=str(NAMES),prior_review_sha256=sha(NAMES.read_bytes()),
        native_source_name_proof=str(SOURCE),native_source_name_proof_sha256=sha(SOURCE.read_bytes()),
        directly_viewed_sheet=sheets[-1],actual_headers_catalogue_UI_custom_names_andfull207_review_pending=True)
    save(NAMES_OUT,names)
    evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,NAMES,PLAN,NATIVE,SOURCE,NAME_SHEET,Path(__file__)]}
    doc.update(prior_manuscript=str(DOC),prior_manuscript_sha256=sha(DOC.read_bytes()),names_packet=str(NAMES_OUT),
        native_page_proof=str(NATIVE),native_page_proof_sha256=sha(NATIVE.read_bytes()),
        source_name_page_proof=str(SOURCE),source_name_page_proof_sha256=sha(SOURCE.read_bytes()),
        automatic_layout_plan=str(PLAN),automatic_layout_plan_sha256=sha(PLAN.read_bytes()),
        native_review_sheets=sheets,all17_final_native_review_sheets_directly_viewed=True,
        all91_native_paragraphs92_pages_complete=True,R347_full_width_five_rows_two_pages_actual_transition_pending=True,
        R140_arent_you_tag_kept_together_no_prose_orrow_count_change=True,
        original_QA_infos=infos,original_exact_ordinary_boundary_warnings=[dict(id=w['id'],issue=w['scope']['exact_issue']) for w in waivers],
        all_original_QA_issues_preserved_two_narrow_documented_exceptions=True,
        inherited_weak_before_row_andpage_sentence_before_readability_retrospective_leads_remain_open=True,
        status='91-source-context-prose-native-pages-names-reviewed-stored-actual-policy-release-pending')
    doc['evidence']=dict(doc['evidence'])|evidence|{str(NAMES_OUT):sha(NAMES_OUT.read_bytes())}
    save(OUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'91_paragraphs92_native_pages9_names_two_scoped_warnings37_infos_wrap_review.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES_OUT),names_sha256=sha(NAMES_OUT.read_bytes()),
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),native_proof=str(NATIVE),native_proof_sha256=sha(NATIVE.read_bytes()),
        records=doc['records'],native_page_count=92,current_native_names=9,
        directly_viewed_sheets=sheets,final_viewed_sheet_count=17,
        historical_superseded_R140_sheet_preserved_andviewed=True,total_sheets_directly_viewed_including_superseded=18,
        original_row_count_infos=37,preserved_warning_exceptions=waivers,
        all91_first_four_review_gates_true_all91_formatting_gates_false=True,
        R347_early_internal_wrap_fixed_without_prose_shortening_andR140_tag_kept_together=True,
        four_FE_geometry_andsource00_4B71_preambles_bodyNULguard_preserved=True,
        no_ROM_registry_completion_credit_ornew_actual_gameplay_change=True,
        stored_reference_actual_policy_atomic_andregistered_release_pending=True,
        evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Native review:91paragraphs/92pages/nine names,17final sheets viewed;37infos/two exactwarning exceptions retained.Allformatting gates false untilstored/actual/release completion.')
