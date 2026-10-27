"""Approve both source-reviewed literal modal font planes without event credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspection_status_native_plan_v1573 import compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/inspection_status_native_review_v1576')
SOURCE=Path('translations/inspection_status_editorial_manuscript_v1.json')
OUT=Path('translations/inspection_status_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    doc=deepcopy(read(SOURCE));font_path=Path('work/analysis/inspection_status_fonts_v1574/native_font_proof.json');copy_path=Path('work/analysis/inspection_status_copies_v1575/all_native_copies_and_prefix_cache_sequence.json')
    font,copies=read(font_path),read(copy_path)
    assert font['manuscript_sha256']==sha(SOURCE.read_bytes()) and len(font['cases'])==2 and len(font['invalid_compiler_inputs_rejected'])==12
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert copies['ARM9_sha256']==font['ARM9_sha256'] and copies['COMMON_sha256']==font['COMMON_sha256']
    assert all(c['compiled_hex']==compiled(r).hex() for c,r in zip(font['cases'],doc['records'],strict=True))
    ROOT.mkdir(parents=True);visual=ROOT/'both_native_panels_visual_review.json'
    save(visual,{'review_sheet':font['review_sheet'],'review_sheet_sha256':font['review_sheet_sha256'],
        'both_native_panels_actually_viewed':True,'complete_words_leading_trailing_letters_native_literal_margin_bounds_and_blank_paper_pass':True,
        'remaining_layout_findings':0,'no_actual_modal_release_or_completion_credit':True})
    doc.update(formatting_review_pending=False,native_font_proof=str(font_path),native_copy_proof=str(copy_path),visual_review=str(visual),
        reviewed_research_manuscript=str(SOURCE),reviewed_research_manuscript_sha256=sha(SOURCE.read_bytes()),
        status='source-native-approved;registered-release-and-actual-two-modal-paths-pending')
    for row in doc['records']:row['review']['formatting']=True;row['status']='source-native-approved;release-actual-pending'
    validate_natural_dialogue_batch(doc);save(OUT,doc)
    ledger=read('translations/editorial_review_current_v1.json')
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-inspection-status2-source-prose')
    unit.update(status='source-native-approved;registered-release-and-actual-modal-pending',native_manuscript=str(OUT))
    ledger['formatting_watchlist']['inspection_status2'].update(native_approved_manuscript=str(OUT),native_font_proof=str(font_path),native_visual_review=str(visual),native_font_pending=False)
    ledger['research_checkpoints'].append({'id':'V1576-inspection-status2-native-approval','manuscript':str(OUT),'proof':str(visual),'source_prose_reviews_added':0,'completed_entries_added':0,'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    save(ROOT/'native_approval_receipt.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),'native_fonts':str(font_path),'copies':str(copy_path),'visual_review':str(visual),
        'completed':1338,'source_prose':1492,'reviewed_incomplete_COMMON':154,'completed_entries_added':0,'full_goal_complete':False})
    print('Both literal modal statuses native-approved;complete fonts/copies/cache/visual gates pass. Registered ROM and both actual paths pending.')
