"""Source-lock complete B50 scene fixtures; preserve all source commands and controls."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_fixture_tools_v8504');assert not root.exists()
    proof=derive('scripts/create_Hodram_B49_fixtures_v8406.py','scripts/create_Hodram_B50_fixtures_v8504.py',{
        'Hodram_B49_fixtures_v8406':'Hodram_B50_fixtures_v8504',
        'work/analysis/Hodram_B49_reference_v8403/research_image_receipt.json':'work/analysis/Hodram_B50_reference_v8502/research_image_receipt.json',
        'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json':'work/analysis/Hodram_B50_references_v8503/source_current_final_map.json',
        'work/analysis/Hodram_B49_references_v8405b/references.json':'work/analysis/Hodram_B50_references_v8503/references.json',
        'all36_commands14_full_preambles8_relatives2_choices_query_picture_hide_effects_andterminal_bound':'all12_commands3_full_preambles_source_FE_item_hide_effects_terminal_andtails_bound',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B50_current_v8488/current_effective.json',
        "group=dict(group,all_source_commands=current['groups'][0]['all_source_commands'])":"assert group['all_source_commands']==current['groups'][0]['all_source_commands']",
        '_v8406_RESEARCH_ONLY.nds':'_v8504_RESEARCH_ONLY.nds',
        "sum(len(f['all_original_exchange_commands']) for f in fixtures)==72":"sum(len(f['all_original_exchange_commands']) for f in fixtures)==24",
        'B49':'B50',
        'all36_commands14_speeches8_relative_sites_two_typed_labels_preserved_perversion':'all12_commands3_speeches_zero_relative_query_choice_sites_preserved_perversion',
        'registered_current_V8377_mainV4701_unchanged':'registered_current_V8475_mainV4701_unchanged',
        'all36commands14speeches8relatives2typedlabels perversion':'all12commands3speeches0relatives perversion',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=proof,all_native_high_integer_constants_andmultiplicity_preserved=True,whole_B50_exchange_no_runtime_state_forcing=True,new_credit=0,full_goal_complete=False))
