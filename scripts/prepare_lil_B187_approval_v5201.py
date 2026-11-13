"""Prepare viewed sixteen-panel approval with no inherited paragraph exception."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_approval_tools_v5201')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/approve_lil_B185_native_v5104b.py');text=source.read_text(encoding='utf-8')
    a=text.index("    comparison=read('work/analysis/lil_B185_wrap_comparison_v5103b/")
    b=text.index('    validate_natural_dialogue_batch(doc)',a)
    comparison=text[a:b]
    boundary="""        if row['source_record_index']==16:
            assert len(qa.get('reviewed_ordinary_boundaries',[]))==1
            row['reviewed_ordinary_boundaries']=qa['reviewed_ordinary_boundaries']
"""
    row=derive(source,'scripts/approve_lil_B187_native_v5201.py',{
        comparison:'',boundary:"        assert not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries')\n",
        'B185':'B187','viewed8-panel':'viewed16-panel','native_approval_v5104b':'native_approval_v5201',
        'lil_B185_layout_v2':'lil_B187_layout_v1','editorial_manuscript_v3':'editorial_manuscript_v2','editorial_manuscript_v4':'editorial_manuscript_v3',
        'fonts_v5102/all8_progressive_FE_native_planes_and64_alignment_cases':'fonts_v5200/all16_progressive_FE_native_planes_and128_alignment_cases',
        "len(font['cases'])==8":"len(font['cases'])==16",
        "font['current_original_macro_alignment_calls']==64":"font['current_original_macro_alignment_calls']==128",
        '==(7,1)':'==(15,1)','blocks[185]':'blocks[187]',"len(font['review_sheets'])==1":"len(font['review_sheets'])==2",
        "{'revise':4,'retain-wording':4}":"{'revise':7,'retain-wording':9}","('progressive',164)":"('progressive',87)",
        'all8_current_native_previews_viewed_on_one_sheet':'all16_current_native_previews_viewed_on_two_sheets',
        'complete_exact_source_prose_ordinary_boundary_reviewed':'no_record_specific_ordinary_boundary_exception_required',
        'all8_source_prose_current_native_approval':'all16_source_prose_current_native_approval',
        'all8_complete_native_panels_read_as_one_exchange':'all16_complete_native_panels_read_as_one_exchange',
        'four_revisions_and_four_individually_justified_retentions':'seven_revisions_and_nine_individually_justified_retentions',
        'source_reported_fur_sales_rising_prices_cold_coat_wish_and_tentative_notice_preserved':
        'source_reported_remedy_effectiveness_sales_forgotten_name_memory_trigger_search_intentions_and_tentative_notice_preserved',
        'all64_current_native_alignment_cases_and_complete_planes_pass':'all128_current_native_alignment_cases_and_complete_planes_pass',
        'All8 source/prose/current-native reviews approved:4 revisions/4 justified retentions,64 alignments':
        'All16 source/prose/current-native reviews approved:7 revisions/9 justified retentions,128 alignments',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_native_approval.json',dict(derivation=row,
        all16_current_native_previews_already_viewed_on_two_sheets=True,
        no_inherited_B185_or_B186_record_specific_boundary_review=True,
        no_manual_break_prose_shortening_font_metric_width_guard_or_shared_rule_change=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared16-panel B187 native approval;no record-specific boundary exception is needed.')
