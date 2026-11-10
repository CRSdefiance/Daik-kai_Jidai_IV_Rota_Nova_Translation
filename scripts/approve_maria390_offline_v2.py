"""Carry372 exact body proofs and all menu/name checks; approve the one fresh wine reply."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/approve_maria390_offline_v1.py').read_text(encoding='utf-8'),{
    'formatting_v1/formatting_input.json':'formatting_v2/formatting_input.json',
    'plan_continuity_v3/automatic_plans.json':'plan_wine_v4/automatic_plans.json',
    'native_final_selection_v1/resume_selection.json':'native_wine_final_selection_v1/resume_selection.json',
    'native_pages_v3/compiled_native_pages.json':'native_wine_pages_v1/compiled_native_pages.json',
    "['initial_body_visual_review_v1.json','refined_body_visual_review_v1.json','farewell_body_visual_review_v1.json']":
        "['initial_body_visual_review_v1.json','refined_body_visual_review_v1.json','farewell_body_visual_review_v1.json','wine_body_visual_review_v1.json']",
    '[1,10,362]':'[1,1,10,361]',
    "'body_visual_review_v1.json'":"'body_visual_review_v2.json'",
    "'final_native_v1.json'":"'final_native_v2.json'",
    "'mixed_visual_review_v1.json'":"'mixed_visual_review_v2.json'",
    "'menu_native_approved_v1.json'":"'menu_native_approved_v3.json'",
    'compiled_styles_v1/compiled_style_objects.json':'compiled_styles_v2/compiled_style_objects.json',
    "'offline_display_approval_v1.json'":"'offline_display_approval_v2.json'",
    'superseded_twelve_receipts_preserved_not_reused_for_changed_pages':'superseded_thirteen_receipts_preserved_not_reused_for_changed_pages',
    'completed_executed_alignment_cases_including_superseded=1540,superseded_completed_alignment_cases_not_selected=48':
        'completed_executed_alignment_cases_including_superseded=1544,superseded_completed_alignment_cases_not_selected=52',
    "save(menupath,dict(runtime=doc['runtime'],menus=approvedmenus":
        "save(menupath,dict(runtime=doc['runtime'],manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),menus=approvedmenus",
    'dialogue_revisions=153,dialogue_retentions=237':'dialogue_revisions=154,dialogue_retentions=236',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-visual-menu-name-guards-one-source-faithful-reply-amendment','exec'),globals())
