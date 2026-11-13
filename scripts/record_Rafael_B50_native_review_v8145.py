"""Record six directly viewed final native pages/names andtwo exact source-bound soft boundaries."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_native_review_v8145')
DOC=Path('translations/rafael_B50_editorial_manuscript_v1.json')
OUT=Path('translations/rafael_B50_editorial_manuscript_v2.json')
NAMES=Path('translations/rafael_B50_speaker_name_review_v1.json')
NAMES_OUT=Path('translations/rafael_B50_speaker_name_review_v2.json')
PLAN=Path('work/analysis/Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json')
NATIVE=Path('work/analysis/Rafael_B50_pages_refined_v8143/28_final_native_pages20_fresh92_reused_alignments.json')
SOURCE=Path('work/analysis/Rafael_B50_source_name_planes_v8142/28_complete_source_pages3_names0_fresh12_reused_literal_alignments.json')
NAME_SHEET=Path('work/analysis/Rafael_B50_name_review_assets_v8144/review_sheet_receipt.json')
SPECIAL={23: "Three rows preserve the full map-deciphering aid andthe gift. Key/to is an ordinary complete-word continuation;treasure map stays together andthe short final It's yours. is a complete offer. Do not shorten the object into a new map,remove words orfill the final row with invented dialogue.", 37: "Two full-width rows retain Camille's complete greeting andunnamed preparations. After a standalone Lil! There you are! the remaining We haven't finished getting ready yet! has38text cells,plusone continuation guard,39against36available. Keep the ordinary auxiliary/verb continuation instead of stranding We,adding a third row solely for phrase preference orweakening guards.", 49: "Two rows nowkeep it's been together;the earlier legal auxiliary break is refined with no added row,page orprose change. Camille's tentative reunion andlaugh remain complete;no date orchronology is invented.", 61: 'Two rows preserve the complete Mr. FA address andthe whole North Sea name onrow2. The exact line1the/North warning remains;avoiding it would need another row orsplit the place name under these words andnative guards. All words anddefault Castor glyphs survive. This is an id/source/text/compiled/line/issue-bound exception,not a wider viewport orwarning relaxation.', 69: "Two rows keep the self-correction andthe complete You're as easygoing as ever. phrase together onrow2. The refinement removes an avoidable copula break without changing the working prose,row count orpage count.", 73: "Two full-width rows preserve Lil's personal discovery andits deliberately unspecified content. The first row ends there's andthe second begins more;after the earlier found boundary,the remainder there's more to life than making money. would need39text cells plusone continuation guard,40against36available. Do not add a third row orrewrite the meaning solely toavoid this legal complete-word boundary.", 86: "Two rows retain the complete parenthesized inner bluff before the spoken That's wonderful! sentence. All opening/closing parentheses andfirst/internal/final glyphs pass;the line doesnot explain the hidden occasion.", 103: 'Two rows nowkeep no idea together. The stammer,open parenthesis andcomplete private confusion survive without moving the final celebration question earlier. No prose orrow/page count change.', 108: 'Two rows nowkeep Come on together onrow2. The source FI remains a native substitution andexpands toRafael bydefault;no Commander rank orfixed-name replacement is added. Retain polite dismissal anddeparture.', 114: "Three rows nowend the first at the complete thanks,keep I'll do together,andkeep live up to your expectations! as the final phrase. The exact line2to/live warning remains. This preserves both addressees,the promise totry andall source meaning without a short extra row,prose abbreviation ormanual staging.", 119: 'One complete full-width row preserves both parentheses andthe deliberately unresolved final question. No extra blank page orhidden life-event explanation is introduced.'}
WARNINGS={61:(1,'the','North'),114:(2,'to','live')}
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES_OUT.exists()
    doc,names,plan,native,source,name_sheet=map(read,[DOC,NAMES,PLAN,NATIVE,SOURCE,NAME_SHEET])
    assert plan['manuscript_sha256']==native['manuscript_sha256']==sha(DOC.read_bytes()) and native['plan_sha256']==sha(PLAN.read_bytes())
    assert len(native['records'])==28 and sum(len(r['pages']) for r in native['records'])==28
    assert native['fresh_compiled_alignment_cases']==20 and native['reused_compiled_alignment_cases']==92
    assert source['source_complete_native_pages']==28 and len(source['name_planes'])==3
    sheets=deepcopy(native['review_sheets'])+[dict(path=name_sheet['sheet'],sha256=name_sheet['sheet_sha256'])];assert len(sheets)==6
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
    assert len(infos)==18 and all(i['issue']['code']=='line-break-count' for i in infos) and len(waivers)==2
    for row in names['records']:
        plane=next(n for n in source['name_planes'] if n['actor_ID']==row['actor_ID']);assert plane['text']==row['name']
        row.update(complete_native_name_plane=plane,native_name_plane_directly_viewed=True,native_complete_first_internal_final_characters_width_andbounds_pass=True,actual_B50_headers_andcatalogue_UI_still_pending=True)
        if row['actor_ID']==9:row['full_getter_synthetic_original_name_style_proof']=next(e for e in name_sheet['entries'] if e['actor_ID']==row['actor_ID'] and e.get('synthetic_full_getter_text_in_original_name_style_only'))
    names.update(prior_review=str(NAMES),prior_review_sha256=sha(NAMES.read_bytes()),native_source_name_proof=str(SOURCE),native_source_name_proof_sha256=sha(SOURCE.read_bytes()),
        directly_viewed_sheet=sheets[-1],actual_headers_catalogue_UI_custom_names_andfull207_review_pending=True)
    save(NAMES_OUT,names)
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,NAMES,PLAN,NATIVE,SOURCE,NAME_SHEET,Path(__file__)]}
    doc.update(prior_manuscript=str(DOC),prior_manuscript_sha256=sha(DOC.read_bytes()),names_packet=str(NAMES_OUT),native_page_proof=str(NATIVE),native_page_proof_sha256=sha(NATIVE.read_bytes()),
        source_name_page_proof=str(SOURCE),source_name_page_proof_sha256=sha(SOURCE.read_bytes()),automatic_layout_plan=str(PLAN),automatic_layout_plan_sha256=sha(PLAN.read_bytes()),
        native_review_sheets=sheets,all6_final_native_review_sheets_directly_viewed=True,initial5_sheets_andfour_updated_sheets_plus_name_sheet_total10_direct_views=True,
        all28_native_paragraphs28_single_pages_complete=True,five_phrase_refinements_no_prose_orrow_count_change=True,
        original_QA_infos=infos,original_exact_ordinary_boundary_warnings=[dict(id=w['id'],issue=w['scope']['exact_issue']) for w in waivers],
        all_original_QA_issues_preserved_two_narrow_documented_exceptions=True,
        inherited_weak_before_row_page_before_readability_andphrase_coherence_retrospective_leads_remain_open=True,
        status='28-source-context-prose-native-pages-names-reviewed-stored-actual-policy-release-pending')
    doc['evidence']=dict(doc['evidence'])|evidence|{str(NAMES_OUT):sha(NAMES_OUT.read_bytes())};save(OUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'28_native_pages3_names_two_scoped_warnings18_infos_wrap_review.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES_OUT),names_sha256=sha(NAMES_OUT.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        native_proof=str(NATIVE),native_proof_sha256=sha(NATIVE.read_bytes()),source_name_proof=str(SOURCE),source_name_proof_sha256=sha(SOURCE.read_bytes()),
        records=doc['records'],native_page_count=28,current_native_names=3,directly_viewed_sheets=sheets,narrow_warning_exceptions=waivers,all_original_infos=infos,
        all28_formatting_gates_false_pending_stored_actual_reference_andrelease=True,no_new_prose_words_orname_assets_from_layout=True,
        native_only_not_actual_gameplay_catalogue_UI_orfull207_name_approval=True,evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B50:28native pages/three names/six final viewed sheets;18original infos/two exact scoped warnings retained.Draftv2/namesv2;allformatting gates false,stored/actual/release pending,no credit.')
