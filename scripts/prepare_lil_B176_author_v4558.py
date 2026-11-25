"""Prepare ten B176 complete-context decisions; native formatting approval remains separate."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_author_tools_v4558')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/author_lil_B175_v4514.py','scripts/author_lil_B176_v4558.py',{
        'Record all32 B175 contextual decisions':'Record all10 B176 contextual decisions',
        'lil_B175_prose_v4513':'lil_B176_prose_v4557','lil_B175_author_v4514':'lil_B176_author_v4558',
        'lil_B175_comparison_v4511/all32_current_effective_comparison_packet':'lil_B176_comparison_v4556/all10_current_effective_comparison_packet',
        'lil_B175_clean_context_v4502/all32_complete_B175_exchange':'lil_B176_clean_context_v4547/all10_complete_B176_exchange',
        'lil_B175_editorial_manuscript_v1':'lil_B176_editorial_manuscript_v1',
        'all32_clean_source':'all10_clean_source','len(prose.REVISIONS)==19 and len(prose.RETAIN_NOTES)==13':'len(prose.REVISIONS)==5 and len(prose.RETAIN_NOTES)==5',
        'lil_B175_voices_v4504/current5_static_names':'lil_B176_voices_v4549/current2_static_names',
        'lil_B175_branches_v4506':'lil_B176_branches_v4551','lil_B175_entry_v4507/source_EV2_B175':'lil_B176_entry_v4552/source_EV2_B176',
        'lil_B175_controls_v4509/one_resource_three_presentations_C200_two_ends_and7_source_leaves':
            'lil_B176_controls_v4554/one_A000_C200_single_end_and3_source_leaves',
        'lil_B175_names_v4508/ten_original_name_consumers_owned_and_readonly_paths':
            'lil_B176_names_v4553/four_original_Owner_Cook_name_consumers_readonly_paths',
        "{2:'Lil',9:'Camille',183:'Angel',184:'Snake',185:'Dandy',254:'Woman pirate (anonymous)'}":
            "{174:'Owner',175:'Cook',254:'Impersonal fashion notice'}",
        "{'revise':19,'retain-wording':13}":"{'revise':5,'retain-wording':5}",
        "sum(r['kind']=='system-FE' for r in rows)==9 and len(rows)==32":"sum(r['kind']=='system-FE' for r in rows)==1 and len(rows)==10",
        'revised=19,retained=13':'revised=5,retained=5','all32_clean_first_contextual_decisions':'all10_clean_first_contextual_decisions',
        'all32_clean_then_current_whole_exchange_read':'all10_clean_then_current_whole_exchange_read',
        'all13_retentions_individually_justified':'all5_retentions_individually_justified',
        'five_static_names_bound_and_FE_woman_and_sword_unnamed=True':'Owner_Cook_native_names_bound_and_FE_notice_impersonal=True',
        'source_FI4_FA1_FO0_preserved=True,admiral_source_rank_preserved_without_new_commission=True':
            'source_FI0_FA0_FO0_preserved=True,Seville_pointer_bound_in_clean_and_current_staged_pool=True',
        'recognition_danger_pirate_pride_defiance_sword_mystery_relief_teasing_and_worry_progression_preserved=True':
            'enthusiasm_taste_reason_doubt_imperious_insistence_compliance_order_offhand_reply_grand_laugh_and_forecast_preserved=True',
        'no_boss_Captain_relationship_sword_power_or_earned_pursuit_added=True':
            'no_royal_rank_formal_relationship_quantity_price_completed_purchase_or_earned_boom_added=True',
        'objects=32,progressive=23,FE=9':'objects=10,progressive=9,FE=1','FI=4,FA=1,FO=0':'FI=0,FA=0,FO=0',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,revisions=5,retentions=5,
        no_formatting_approval_orledger_credit=True,full_goal_complete=False))
    print('Prepared ten B176 decisions,five revisions/five justified retentions;formatting/native/release approval pending.')
