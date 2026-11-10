"""Record viewed native paragraphs and individual scoped QA decisions; no final display approval."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.draft_papal_trade_prose_v7631 import MANUSCRIPTS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_native_review_v7635')
PLAN=Path('work/analysis/papal_trade_layout_v7632b/two_routes36_automatic_full_width_plans_all_base_QA_preserved.json')
NATIVE=Path('work/analysis/papal_trade_native_pages_v7634/two_routes36_complete_pages144_fresh_compiled_alignments_exact_logical_andfont_reuse.json')
ROW_REASONS={
9:"The complete familiar question and Daydreaming? fit one 35-cell row. The Japanese staging break is not necessary in English; all source words and intended teasing survive.",
12:"The retained startled recognition and return question fit one 32-cell row, keeping When did together. Three Japanese rows do not require three English rows.",
33:"Four complete rows retain all territorial and direct-rule facts within one original page. The exact complete-word break after the on line1 keeps Papal States whole on line2. This is the same frozen text and boundary previously reviewed for B234; scope the ordinary article continuation only to each exact SC0/SC1 record, not to a global weak-word rule.",
37:"Three full rows of31/31/35 cells preserve both hearing/reporting layers, territorial prosperity and peak papal power without copying four Japanese staging rows.",
40:"Three full rows of34/28/35 cells preserve agreement, past setting, lords, competition, donation kinds and amounts. No word is cut to imitate four source rows.",
47:"The retained cooperative historical response fits two rows of35/26 cells. The natural complete-word break before with the Church preserves the institutional phrase; the source's three rows are not required.",
51:"Three rows of28/29/35 cells preserve agreement, making one's own way and great-grandfather envy. How lucky remains together and every word is retained.",
64:"Three rows of35/33/30 cells preserve the tentative courteous transition and explicit if-found condition. The ordinary complete-word we/found continuation allows the full paragraph to remain within one original page; adding a fourth row solely for that pair would leave a less balanced paragraph. No global weak-boundary or page rule changes.",
}
if __name__=='__main__':
    assert not ROOT.exists();plan,native=map(read,[PLAN,NATIVE]);assert native['layout_plan_sha256']==sha(PLAN.read_bytes())
    assert native['fresh_native_page_renders']==6 and native['distinct_prior_exact_reused_native_page_renders']==12 and native['second_route_exact_shared_page_reuse']==18
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    groups=[];warnings=[];infos=0
    for pg,ng in zip(plan['groups'],native['groups'],strict=True):
        route=pg['route'];path=MANUSCRIPTS[route];doc=read(path);assert sha(path.read_bytes())==pg['manuscript_sha256']
        rows=[]
        for row,p,n in zip(doc['records'],pg['records'],ng['records'],strict=True):
            assert row['id']==p['id']==n['id'] and n['compiled_hex']==p['encoded_hex'] and len(n['pages'])==1
            issues=p['base_QA']['issues'];actual=[i for i in issues if i['severity']=='warning'];info=[i for i in issues if i['severity']=='info'];assert not any(i['severity']=='error' for i in issues)
            index=row['source_record_index'];assert (index in ROW_REASONS)==bool(info)
            if actual:
                assert index==33 and actual==[dict(severity='warning',code='weak-line-ending',message="line 1 ends with weak wrap word 'the'")]
                assert p['lines']==['It was about trade in the',"Papal States. The pope's",'direct rule once stretched','almost to Venice.']
                warnings.append(dict(file_path=doc['file_path'],id=row['id'],compiled_hex=p['encoded_hex'],exact_warning=actual,reason=ROW_REASONS[33]))
            infos+=len(info)
            rows.append(dict(id=row['id'],file_path=doc['file_path'],source_record_index=index,English=row['english'],compiler_source_hex=row['source_hex'],compiled_hex=p['encoded_hex'],lines=p['lines'],base_QA_issues=issues,exact_reviewed_base_warnings=actual,qa_waivers=['weak-line-ending'] if actual else [],qa_waiver_reason=ROW_REASONS[33] if actual else None,row_count_reason=ROW_REASONS.get(index),complete_native_page_reference=dict(path=str(NATIVE),route=route,id=row['id'],plane=n['pages'][0]['native_plane'],plane_sha256=n['pages'][0]['native_plane_sha256']),visually_reviewed_complete_paragraph=True,all_logical_words_andpunctuation_preserved=True,formatting_gate_still_false_stored_actual_policy_andrelease_pending=True))
        groups.append(dict(route=route,route_identity=doc['route_identity'],records=rows))
    assert len(warnings)==2 and infos==16
    ROOT.mkdir(parents=True)
    save(ROOT/'all36_native_paragraphs_viewed_two_exact_R33_boundaries16_row_infos_stored_actual_pending.json',dict(groups=groups,all_three_distinct_native_page_sheets_individually_viewed=True,all18_distinct_paragraphs_visually_reviewed_in_complete_exchange_order=True,review_sheets=native['review_sheets'],exact_file_qualified_R33_ordinary_article_boundaries=warnings,informational_row_count_changes=16,all_unmodified_base_QA_issues_preserved=True,no_global_font_viewport_weak_ending_literal_I_F_orpairphase_change=True,retained_R5_complete_original_three_CP932_ellipses_native_plane_exact_reuse=True,offline_R5_generic_index15_preview_shade_not_counterpart_actual_palette_claim=True,Carlo_Sinat_andTrader_contextual_name_decisions_not_full_catalogue_UI_approval=True,stored_bytes_policy_relocation_representative_actual_andregistered_release_pending=True,all36_formatting_gates_remain_false=True,no_current_ROM_registry_orledger_mutation=True,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,NATIVE,*MANUSCRIPTS.values(),Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('All3 native sheets/18 distinct paragraphs viewed;36 file-qualified reviews preserve all QA,16 row infos andtwo exact R33 warnings. Stored/actual/policy/release still pending;zero credit.')
