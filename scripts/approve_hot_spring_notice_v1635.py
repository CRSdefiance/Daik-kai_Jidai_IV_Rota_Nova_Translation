"""Native approval of notice310;original optional gameplay remains required."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.hot_spring_notice_plan_v1632 import compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_notice_native_review_v1635')
SOURCE=Path('translations/hot_spring_notice_editorial_manuscript_v1.json')
OUT=Path('translations/hot_spring_notice_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    doc=deepcopy(read(SOURCE));font_path=Path('work/analysis/hot_spring_notice_fonts_v1633/native_font_proof.json');copy_path=Path('work/analysis/hot_spring_notice_copies_v1634/all_native_copies_and_prefix_cache_sequence.json')
    fonts,copies=read(font_path),read(copy_path)
    assert fonts['manuscript_sha256']==sha(SOURCE.read_bytes()) and len(fonts['cases'])==1 and len(fonts['invalid_compiler_inputs_rejected'])==12
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert copies['ARM9_sha256']==fonts['ARM9_sha256'] and copies['COMMON_sha256']==fonts['COMMON_sha256']
    assert fonts['cases'][0]['compiled_hex']==compiled(doc['records'][0]).hex()
    assert fonts['cases'][0]['literal_modal_origin_x0_native_preserved'] and fonts['cases'][0]['complete_first_final_letters_single_line_bounds_and_blank_paper_pass']
    assert sha(Path(fonts['review_sheet']).read_bytes())==fonts['review_sheet_sha256']
    ROOT.mkdir(parents=True);visual=ROOT/'notice_native_panel_visual_review.json'
    save(visual,{'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],'notice_native_panel_actually_viewed':True,
        'complete_T_full_Experience_final_period_original_x0_bounds_and_blank_paper_pass':True,'remaining_layout_findings':0,'no_actual_modal_release_or_completion_credit':True})
    doc.update(formatting_review_pending=False,native_font_proof=str(font_path),native_copy_proof=str(copy_path),visual_review=str(visual),
        reviewed_research_manuscript=str(SOURCE),reviewed_research_manuscript_sha256=sha(SOURCE.read_bytes()),status='source-native-approved;registered-release-and-original-optional-notice-pending')
    for row in doc['records']:row['review']['formatting']=True;row['compiled_hex']=compiled(row).hex();row['status']='source-native-approved;release-actual-pending'
    validate_natural_dialogue_batch(doc);save(OUT,doc)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-hot-spring-Experience-notice1-source-prose');unit.update(status=doc['status'],native_approved_manuscript=str(OUT))
    drafts=ledger['active_source_prose_drafts'];drafts['manuscripts'].append(str(OUT));drafts['manuscript_record_subsets_pending'][str(SOURCE)]=[];drafts['manuscript_record_subsets_pending'][str(OUT)]=[310]
    ledger['formatting_watchlist']['hot_spring_Experience_notice310'].update(native_approved_manuscript=str(OUT),native_font_proof=str(font_path),native_visual_review=str(visual),native_font_pending=False)
    ledger['research_checkpoints'].append({'id':'V1635-hot-spring-notice-native-approved','proof':str(ROOT/'native_approval_receipt.json'),'source_prose_reviews_added':0,'completed_entries_added':0,'full_goal_complete':False})
    for k in ['records_editorially_completed','records_with_source_and_prose_pass','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work']:assert ledger[k]==before[k]
    save(lp,ledger);save(ROOT/'native_approval_receipt.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),'native_fonts':str(font_path),'copies':str(copy_path),'visual_review':str(visual),
        'completed':1350,'source_prose':1508,'reviewed_incomplete_COMMON':158,'completed_entries_added':0,'full_goal_complete':False})
    print('Notice310 native-approved:complete T/Experience/period,x0 margin,7336 copies180 cache pass;registered ROM and original optional scene pending.')
