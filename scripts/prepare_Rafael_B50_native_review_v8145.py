"""Record six directly viewed final B50 sheets and preserve two exact soft-boundary diagnostics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
SPECIAL={
 23:'Three rows preserve the full map-deciphering aid andthe gift. Key/to is an ordinary complete-word continuation;treasure map stays together andthe short final It\'s yours. is a complete offer. Do not shorten the object into a new map,remove words orfill the final row with invented dialogue.',
 37:'Two full-width rows retain Camille\'s complete greeting andunnamed preparations. After a standalone Lil! There you are! the remaining We haven\'t finished getting ready yet! has38text cells,plusone continuation guard,39against36available. Keep the ordinary auxiliary/verb continuation instead of stranding We,adding a third row solely for phrase preference orweakening guards.',
 49:'Two rows nowkeep it\'s been together;the earlier legal auxiliary break is refined with no added row,page orprose change. Camille\'s tentative reunion andlaugh remain complete;no date orchronology is invented.',
 61:'Two rows preserve the complete Mr. FA address andthe whole North Sea name onrow2. The exact line1the/North warning remains;avoiding it would need another row orsplit the place name under these words andnative guards. All words anddefault Castor glyphs survive. This is an id/source/text/compiled/line/issue-bound exception,not a wider viewport orwarning relaxation.',
 69:'Two rows keep the self-correction andthe complete You\'re as easygoing as ever. phrase together onrow2. The refinement removes an avoidable copula break without changing the working prose,row count orpage count.',
 73:'Two full-width rows preserve Lil\'s personal discovery andits deliberately unspecified content. The first row ends there\'s andthe second begins more;after the earlier found boundary,the remainder there\'s more to life than making money. would need39text cells plusone continuation guard,40against36available. Do not add a third row orrewrite the meaning solely toavoid this legal complete-word boundary.',
 86:'Two rows retain the complete parenthesized inner bluff before the spoken That\'s wonderful! sentence. All opening/closing parentheses andfirst/internal/final glyphs pass;the line doesnot explain the hidden occasion.',
 103:'Two rows nowkeep no idea together. The stammer,open parenthesis andcomplete private confusion survive without moving the final celebration question earlier. No prose orrow/page count change.',
 108:'Two rows nowkeep Come on together onrow2. The source FI remains a native substitution andexpands toRafael bydefault;no Commander rank orfixed-name replacement is added. Retain polite dismissal anddeparture.',
 114:'Three rows nowend the first at the complete thanks,keep I\'ll do together,andkeep live up to your expectations! as the final phrase. The exact line2to/live warning remains. This preserves both addressees,the promise totry andall source meaning without a short extra row,prose abbreviation ormanual staging.',
 119:'One complete full-width row preserves both parentheses andthe deliberately unresolved final question. No extra blank page orhidden life-event explanation is introduced.',
}
if __name__=='__main__':
    source=Path('scripts/record_Rafael_B49_native_review_v8095.py').read_text('utf8')
    start=source.index('SPECIAL=');end=source.index("if __name__",start)
    print(derive('scripts/record_Rafael_B49_native_review_v8095.py','scripts/record_Rafael_B50_native_review_v8145.py',{
        source[start:end]:'SPECIAL='+repr(SPECIAL)+"\nWARNINGS={61:(1,'the','North'),114:(2,'to','live')}\n",
        'Rafael_B49_native_review_v8095':'Rafael_B50_native_review_v8145',
        'Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json':'Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json',
        'Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json':'Rafael_B50_pages_refined_v8143/28_final_native_pages20_fresh92_reused_alignments.json',
        'Rafael_B49_source_name_planes_v8093/61_complete_source_pages7_names8_fresh20_reused_literal_alignments.json':'Rafael_B50_source_name_planes_v8142/28_complete_source_pages3_names0_fresh12_reused_literal_alignments.json',
        'Rafael_B49_name_review_assets_v8094b':'Rafael_B50_name_review_assets_v8144','B49':'B50',
        "len(native['records'])==61":"len(native['records'])==28", "for r in native['records'])==61":"for r in native['records'])==28",
        "native['reused_compiled_alignment_cases']==224":"native['reused_compiled_alignment_cases']==92",
        "source['source_complete_native_pages']==61 and len(source['name_planes'])==7":"source['source_complete_native_pages']==28 and len(source['name_planes'])==3",
        'len(sheets)==12':'len(sheets)==6','len(infos)==22':'len(infos)==18','len(waivers)==3':'len(waivers)==2',
        "row['actor_ID'] in [8,9]":"row['actor_ID']==9",
        'all12_final_native_review_sheets_directly_viewed':'all6_final_native_review_sheets_directly_viewed',
        'initial11_sheets_andfive_updated_sheets_plus_name_sheet_total17_direct_views':'initial5_sheets_andfour_updated_sheets_plus_name_sheet_total10_direct_views',
        'all61_native_paragraphs61_single_pages_complete':'all28_native_paragraphs28_single_pages_complete',
        'all_original_QA_issues_preserved_three_narrow_documented_exceptions':'all_original_QA_issues_preserved_two_narrow_documented_exceptions',
        '61-source-context-prose-native-pages-names-reviewed-stored-actual-policy-release-pending':'28-source-context-prose-native-pages-names-reviewed-stored-actual-policy-release-pending',
        '61_native_pages7_names_three_scoped_warnings22_infos_wrap_review':'28_native_pages3_names_two_scoped_warnings18_infos_wrap_review',
        'native_page_count=61,current_native_names=7':'native_page_count=28,current_native_names=3',
        'all61_formatting_gates_false_pending_stored_actual_reference_andrelease':'all28_formatting_gates_false_pending_stored_actual_reference_andrelease',
        'Record directly viewed final native pages/names andthree exact source-bound soft boundaries.':'Record six directly viewed final native pages/names andtwo exact source-bound soft boundaries.',
        'B49:61native pages/seven names/12final viewed sheets;22original infos/three exact scoped warnings retained. Draftv2/namesv2;allformatting gates false,stored/actual/release pending,no credit.':'B50:28native pages/three names/six final viewed sheets;18original infos/two exact scoped warnings retained.Draftv2/namesv2;allformatting gates false,stored/actual/release pending,no credit.',
    }))
