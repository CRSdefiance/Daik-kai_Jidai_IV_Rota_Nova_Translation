"""Keep the generated acquisition notice as a distinct measured name consumer."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/audit_shachihoko_B204_card_v6084b.py','scripts/audit_shachihoko_B204_card_v6084c.py',{
        'shachihoko_B204_card_actual_v6084b':'shachihoko_B204_card_actual_v6084c',
        'classes=dict(item_title=0,advance_prompt=0)':'classes=dict(item_title=0,acquisition_notice_text=0,advance_prompt=0)',
        "elif 224<=xx<240 and 360<=yy<376:classes['advance_prompt']+=1":"elif 16<=xx<164 and 297<=yy<309:classes['acquisition_notice_text']+=1\n                    elif 224<=xx<240 and 360<=yy<376:classes['advance_prompt']+=1",
        'in [4510,4750]':'in [4510,4750,5530]',
        'len(photos)==4':'len(photos)==6',
        "(1040,1600)":"(1040,2400)",
        'complete_source_path_and_unmasked_title_only_frame_differences.json':'complete_source_path_and_unmasked_title_acquisition_prompt_frame_differences.json',
        'all_measured_RGB_differences_classified_as_item_title_or_advance_prompt=True':'all_measured_RGB_differences_classified_as_item_title_acquisition_notice_or_advance_prompt=True',
        'source_names_portraits_Japanese_text_cultural_item_image_category_and_UI_outside_title_and_prompt_exact_at_same_frames=True':'source_names_portraits_Japanese_text_cultural_item_image_category_and_UI_outside_title_acquisition_notice_and_prompt_exact_at_same_frames=True',
        'no_item_list_acquisition_menu_earned_inventory_full_route_hardware_or_complete_effect_claim=True':'generated_name_substituted_acquisition_notice_observed_at5530_5590_5650_5710=True,no_item_list_menu_earned_inventory_full_route_hardware_or_complete_effect_claim=True',
        'title_or_prompt_differences':'title_notice_or_prompt_differences',
    }))
