"""Seal all viewed pages and exact compiled objects for this 234-record scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/approve_hodram_B281_B300_display_v5.py').read_text(encoding='utf-8'),{
    'prepare_hodram_B281_B300_formatting_v1':'prepare_hodram_B301_B310_formatting_v1',
    'review_hodram_B281_B300_contextual_v1':'review_hodram_B301_B310_contextual_v1',
    'formatting_v1/visual_plan_v5/':'formatting_v1/final_plan_v6/',
    'final_native_v5/':'native_final_v6/',
    'native_styles_v5/':'native_style_delta_v6/',
    'final_visual_approval_v5.json':'final_visual_approval_v6.json',
    "ROOT/'storage_inputs_v5'":"ROOT/'storage_inputs_v6'",
    'initial_visual_review_v2.json':'initial_visual_review_v3.json',
    'layout_trial_retentions_v5.json':'layout_trial_retention_v5.json',
    'name_planes_v2/':'name_planes_v1/',
    'layout_delta_v5/':'layout_delta_v6/',
    'changed_body_sheets_v5/':'final_delta_sheets_v6/',
    "len(doc['records'])==384":"len(doc['records'])==234",
    "len(native['records'])==373 and native['pages']==374":"len(native['records'])==225 and native['pages']==228",
    "native['all_current_placement_alignments']==1492 and native['current_version_fresh_alignments']==112":
        "native['all_current_placement_alignments']==900 and native['current_version_fresh_alignments']==72",
    'all375_initial_body_pages_directly_viewed':'all229_initial_body_pages_directly_viewed',
    'all_five_menu_sheets_directly_viewed':'all_four_menu_sheets_directly_viewed',
    'all17_name_strings_directly_viewed':'all8_name_strings_directly_viewed',
    "len(delta['changed_record_IDs'])==28 and delta['fresh_pages']==29":
        "len(delta['changed_record_IDs'])==18 and delta['fresh_pages']==21",
    "len(sheets['sheets'])==2 and sum(len(s['included']) for s in sheets['sheets'])==29":
        "len(sheets['sheets'])==1 and sum(len(s['included']) for s in sheets['sheets'])==21",
    "styles['physical_alternatives']==131 and styles['native_target_slot_cases']==144":
        "styles['physical_alternatives']==152 and styles['native_target_slot_cases']==184",
    "styles['changed_voice_objects']==11 and styles['exact_reused_voice_objects']==7":
        "styles['changed_voice_objects']==5 and styles['exact_reused_voice_objects']==18",
    'formatting_v1/visual_preferences_v5.json':'formatting_v1/visual_preferences_v6.json',
    'all29_new_native_pages_directly_viewed=True':'all21_new_native_pages_directly_viewed=True',
    'final_pages=374,visual_layout_revisions=28,visual_candidate_retentions=2':
        'final_pages=228,visual_layout_revisions=18,visual_candidate_retentions=1',
    "corrected_FE_blank_rows=1,FE_record='DK4_MES_B290_R0148',scoped_punctuation_glyph_fixes=5":
        "corrected_FE_split_words=1,FE_record='DK4_MES_B309_R0294',scoped_punctuation_glyph_fixes=1",
    'scoped_actors=18,scoped_name_strings=17':'scoped_actors=8,scoped_name_strings=8',
    'all131_style_inputs_match_final_native_plan':'all152_style_inputs_match_final_native_plan',
    "len(groups)==5 and sum(len(g['record_IDs']) for g in groups)==11":
        "len(groups)==4 and sum(len(g['record_IDs']) for g in groups)==9",
    '374 final native pages approved; 28 wrap revisions, two layout retentions, one FE blank row and five glyph fixes.':
        '228 final native pages approved;18 wrap revisions, one layout retention, one FE split-word repair and one glyph fix.',
})
exec(compile(source,__file__+'::same-source-bound-native-visual-and-storage-bridge-contract','exec'),globals())
