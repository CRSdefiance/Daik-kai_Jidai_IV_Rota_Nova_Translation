"""Prepare whole-paragraph comparison and viewed eight-panel native approval."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B185_approval_tools_v5103')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/compare_lil_B184_wrap_v5055.py','scripts/compare_lil_B185_wrap_v5103.py',{
        'B184':'B185','wrap_comparison_v5055':'wrap_comparison_v5103',"r['source_record_index']==14":"r['source_record_index']==16",
        'DK4_MES_B184_R0014':'DK4_MES_B185_R0016',
        "[\"It's strange that something this\",\"delicious didn't catch on sooner.\"]":"['I hear furs are selling well in','this cold, and prices are going up.']",
        "r['english'].replace('something','anything')":"r['english'].replace('prices','costs')",
        "r['english'].replace('sooner.','sooner!')":"r['english'].replace('up.','up!')",
        "r['english'].replace(\"It's\",\"IT'S\")":"r['english'].replace('I hear','I HEAR')",
        'all9_unchanged_words_and_exact_R14_boundary':'all8_unchanged_words_and_exact_R16_boundary','all9_words':'all8_words',
        'eight_other_compiled_targets_exact':'seven_other_compiled_targets_exact','R14 only:complete-word soft break after this':'R16 only:complete-word soft break after in',
        'wrap_finding_v5052/exact_R14':'wrap_finding_v5100/exact_R16','Only R14':'Only R16','all9 words':'all8 words','and8 other targets':'and7 other targets'}),
        derive('scripts/approve_lil_B184_native_v5056.py','scripts/approve_lil_B185_native_v5104.py',{
            'B184':'B185','native_approval_v5056':'native_approval_v5104','fonts_v5054':'fonts_v5102',
            'all9_progressive_FE_native_planes_and72_alignment_cases':'all8_progressive_FE_native_planes_and64_alignment_cases',
            "len(font['cases'])==9":"len(font['cases'])==8","font['current_original_macro_alignment_calls']==72":"font['current_original_macro_alignment_calls']==64",
            '==(8,1)':'==(7,1)',"len(font['review_sheets'])==2":"len(font['review_sheets'])==1",'blocks[184]':'blocks[185]',
            "{'revise':4,'retain-wording':5}":"{'revise':4,'retain-wording':4}",'all9':'all8','all72':'all64','All9':'All8','on_two_sheets':'on_one_sheet',
            'four_revisions_and_five_individually_justified_retentions':'four_revisions_and_four_individually_justified_retentions',
            'source_household_tea_request_future_agreement_personal_calm_and_tentative_notice_preserved':'source_reported_fur_sales_rising_prices_cold_coat_wish_and_tentative_notice_preserved',
            'viewed9-panel':'viewed8-panel','4 revisions/5 justified retentions,72':'4 revisions/4 justified retentions,64',
            'wrap_comparison_v5055':'wrap_comparison_v5103','all9_unchanged_words_and_exact_R14_boundary':'all8_unchanged_words_and_exact_R16_boundary',
            'DK4_MES_B184_R0014':'DK4_MES_B185_R0016',
            'R14 exact source/prose only:complete-word soft break after this keeps catch on sooner intact in two safe rows. All words,font,width,guards,phase and pagination remain checked. No global weak-ending exemption.':
            'R16 exact source/prose only:complete-word soft break after in keeps this cold and prices are going up intact in two safe rows. The exact approved shared warning is recorded on this record. All words,font,width,guards,phase and pagination remain checked. No global weak-ending exemption.',
            '        assert row.get(\'qa_waivers\') in [None,[\'line-break-count\']]':
            "        if row['source_record_index']==16:\n            assert len(qa.get('reviewed_ordinary_boundaries',[]))==1\n            row['reviewed_ordinary_boundaries']=qa['reviewed_ordinary_boundaries']\n        assert row.get('qa_waivers') in [None,['line-break-count']]"})]
    ROOT.mkdir(parents=True);save(ROOT/'prepared.json',dict(tools=tools,initial_inline_preparation_quote_syntax_error_created_no_output_files=True,
        exact_shared_warning_reviewed_only_for_source_prose_R16=True,new_review_credit=0,full_goal_complete=False))
