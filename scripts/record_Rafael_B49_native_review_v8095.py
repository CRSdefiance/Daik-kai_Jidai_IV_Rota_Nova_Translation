"""Record directly viewed final native pages/names andthree exact source-bound soft boundaries."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_native_review_v8095')
DOC=Path('translations/rafael_B49_editorial_manuscript_v1.json')
OUT=Path('translations/rafael_B49_editorial_manuscript_v2.json')
NAMES=Path('translations/rafael_B49_speaker_name_review_v1.json')
NAMES_OUT=Path('translations/rafael_B49_speaker_name_review_v2.json')
PLAN=Path('work/analysis/Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json')
NATIVE=Path('work/analysis/Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json')
SOURCE=Path('work/analysis/Rafael_B49_source_name_planes_v8093/61_complete_source_pages7_names8_fresh20_reused_literal_alignments.json')
NAME_SHEET=Path('work/analysis/Rafael_B49_name_review_assets_v8094b/review_sheet_receipt.json')
SPECIAL={
43:'Three rows preserve the complete incredulous Need something?! question,then Who gave you permission,then the trading location. The earlier legal break left Who stranded. The automatic phrase refinement keeps the subject/verb together with no added row,word change ormanual break.',
142:'Three rows keep navy guy andHodram Ber... something together. The shorter final For now,anyway. is a complete qualifier,not missing text. Preserve the deliberately forgotten surname andthe source uncertainty;do not expand to Bergstrom oradd an uncle relationship.',
213:'Two rows keep the idiom fight out of me together onrow2 rather than leaving out of me isolated. The exact line1warning after the is a reviewed complete-word soft boundary. All words andnative glyphs remain;no extra row,manual break,viewport change orglobal warning relaxation is allowed.',
244:'Four rows retain the full first exclamation as a natural sentence pause,keep Head west together,andkeep the New World andfar East names intact. The exact line2to/the boundary is preferable to breaking Head/west. A proposed single row Head west to the New World, or solve needs36text cells plusone phase cell andone continuation guard,38against36available;do not weaken guards,drop words oradd a fifth row to force it.',
405:'Two rows keep the complete North Sea name together onrow2 andretain the remaining-region qualification. The exact line1the/North soft boundary is preferable to splitting North/Sea. This exception is source/id/text/compiled/line/issue-bound anddoesnot permit another warning,extra rows orlost glyphs.',
311:'Three rows preserve Julio\'s first-name address andtentative practical advice. FI expands to the measured default Rafael in this context;the source substitution remains incompiled text. Do not claim custom player-name coverage orpromise profit.',
388:'Three complete rows preserve the effective catalogue-selected words,ASCII I andI\'ll,andthe source FI substitution. The ordinary continuation guards andnative alignment prove the complete first/internal/final characters;no narrator,name literal ornew macro is added.',
}
WARNINGS={213:(1,'the','fight'),244:(2,'to','the'),405:(1,'the','North')}
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES_OUT.exists()
    doc,names,plan,native,source,name_sheet=map(read,[DOC,NAMES,PLAN,NATIVE,SOURCE,NAME_SHEET])
    assert plan['manuscript_sha256']==native['manuscript_sha256']==sha(DOC.read_bytes()) and native['plan_sha256']==sha(PLAN.read_bytes())
    assert len(native['records'])==61 and sum(len(r['pages']) for r in native['records'])==61
    assert native['fresh_compiled_alignment_cases']==20 and native['reused_compiled_alignment_cases']==224
    assert source['source_complete_native_pages']==61 and len(source['name_planes'])==7
    sheets=deepcopy(native['review_sheets'])+[dict(path=name_sheet['sheet'],sha256=name_sheet['sheet_sha256'])];assert len(sheets)==12
    for s in sheets:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];s.update(directly_viewed=True,
            finding='Complete first/internal/final glyphs andword flow inspected. Final body sheets use five phrase refinements;the name sheet clearly separates progressive names from synthetic full-getter strings,which arenot catalogue UI.')
    infos=[];waivers=[]
    for row,p,n in zip(doc['records'],plan['records'],native['records'],strict=True):
        assert row['id']==p['id']==n['id'] and row['source_hex']==p['source_hex'] and p['encoded_hex']==n['compiled_hex']
        assert not row['review']['formatting'] and ' '.join(p['lines'])==row['english'] and len(n['pages'])==p['expected_native_pages']==1
        issues=p['base_QA']['issues'];warnings=[i for i in issues if i['severity']=='warning'];assert not any(i['severity']=='error' for i in issues)
        boundaries='; '.join(a['last']+'/'+a['first'] for a in p['automatic_boundaries']) or 'none:complete single-row utterance'
        reason=SPECIAL.get(row['source_record_index'],f"{len(p['lines'])} original native row(s) retain the whole logical paragraph at216px. Complete-word boundaries: {boundaries}. Read with the source-bound beat: {row['source_meaning']} Every word,punctuation mark andsource substitution survives;independent native masks,bounds andcomplete consumption pass.")
        row.update(compiled_hex=p['encoded_hex'],planned_English_markup=p['planning_record']['english'],formatted_markup=p['formatted_markup'],automatic_lines=p['lines'],row_count_reason=reason,
            base_QA_report=p['base_QA'],qa_waivers=[],qa_waiver_reason=None,qa_waiver_scope=None,native_page_count=1,complete_native_font_pages=n['pages'],
            complete_native_compiled_alignment=n['native_alignment'],native_pages_directly_viewed=True,stored_relocation_actual_transition_policy_andregistered_release_pending=True)
        infos.extend(dict(id=row['id'],issue=i) for i in issues if i['severity']=='info')
        if warnings:
            index=row['source_record_index'];assert index in WARNINGS and len(warnings)==1;line,last,nextword=WARNINGS[index]
            assert warnings[0]==dict(code='weak-line-ending',message=f"line {line} ends with weak wrap word '{last}'",severity='warning')
            assert p['lines'][line-1].split()[-1]==last and p['lines'][line].split()[0]==nextword
            scope=dict(id=row['id'],source_hex=row['source_hex'],logical_English=row['logical_English'],compiled_hex=p['encoded_hex'],line=line,last_word=last,next_word=nextword,exact_issue=warnings[0])
            row.update(qa_waivers=['weak-line-ending'],qa_waiver_reason=reason,qa_waiver_scope=scope);waivers.append(dict(id=row['id'],scope=scope,reason=reason))
    assert len(infos)==22 and all(i['issue']['code']=='line-break-count' for i in infos) and len(waivers)==3
    for row in names['records']:
        plane=next(n for n in source['name_planes'] if n['actor_ID']==row['actor_ID']);assert plane['text']==row['name']
        row.update(complete_native_name_plane=plane,native_name_plane_directly_viewed=True,native_complete_first_internal_final_characters_width_andbounds_pass=True,actual_B49_headers_andcatalogue_UI_still_pending=True)
        if row['actor_ID'] in [8,9]:row['full_getter_synthetic_original_name_style_proof']=next(e for e in name_sheet['entries'] if e['actor_ID']==row['actor_ID'] and e.get('synthetic_full_getter_text_in_original_name_style_only'))
    names.update(prior_review=str(NAMES),prior_review_sha256=sha(NAMES.read_bytes()),native_source_name_proof=str(SOURCE),native_source_name_proof_sha256=sha(SOURCE.read_bytes()),
        directly_viewed_sheet=sheets[-1],actual_headers_catalogue_UI_custom_names_andfull207_review_pending=True)
    save(NAMES_OUT,names)
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,NAMES,PLAN,NATIVE,SOURCE,NAME_SHEET,Path(__file__)]}
    doc.update(prior_manuscript=str(DOC),prior_manuscript_sha256=sha(DOC.read_bytes()),names_packet=str(NAMES_OUT),native_page_proof=str(NATIVE),native_page_proof_sha256=sha(NATIVE.read_bytes()),
        source_name_page_proof=str(SOURCE),source_name_page_proof_sha256=sha(SOURCE.read_bytes()),automatic_layout_plan=str(PLAN),automatic_layout_plan_sha256=sha(PLAN.read_bytes()),
        native_review_sheets=sheets,all12_final_native_review_sheets_directly_viewed=True,initial11_sheets_andfive_updated_sheets_plus_name_sheet_total17_direct_views=True,
        all61_native_paragraphs61_single_pages_complete=True,five_phrase_refinements_no_prose_orrow_count_change=True,
        original_QA_infos=infos,original_exact_ordinary_boundary_warnings=[dict(id=w['id'],issue=w['scope']['exact_issue']) for w in waivers],
        all_original_QA_issues_preserved_three_narrow_documented_exceptions=True,
        inherited_weak_before_row_page_before_readability_andphrase_coherence_retrospective_leads_remain_open=True,
        status='61-source-context-prose-native-pages-names-reviewed-stored-actual-policy-release-pending')
    doc['evidence']=dict(doc['evidence'])|evidence|{str(NAMES_OUT):sha(NAMES_OUT.read_bytes())};save(OUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES_OUT),names_sha256=sha(NAMES_OUT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        native_proof=str(NATIVE),native_proof_sha256=sha(NATIVE.read_bytes()),source_name_proof=str(SOURCE),source_name_proof_sha256=sha(SOURCE.read_bytes()),
        records=doc['records'],native_page_count=61,current_native_names=7,directly_viewed_sheets=sheets,narrow_warning_exceptions=waivers,all_original_infos=infos,
        all61_formatting_gates_false_pending_stored_actual_reference_andrelease=True,no_new_prose_words_orname_assets_from_layout=True,
        native_only_not_actual_gameplay_catalogue_UI_orfull207_name_approval=True,evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B49:61native pages/seven names/12final viewed sheets;22original infos/three exact scoped warnings retained. Draftv2/namesv2;allformatting gates false,stored/actual/release pending,no credit.')
