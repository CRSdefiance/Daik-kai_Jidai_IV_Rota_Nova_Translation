"""Keep both actors' full and progressive names distinct,with exact source fields."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_name_tools_v6174')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/prove_lil_B204_names_v6064.py','scripts/prove_lil_B205_names_v6174.py',{
        'B204':'B205','names_v6064':'names_v6174','source_v6062':'source_v6172','voices_v6063':'voices_v6173','all20_clean_current_complete_context':'all17_clean_current_complete_context','current207_catalog_eight_voices_and_five_source_selectors':'current207_catalog_eight_voices_and_two_source_selectors','scripts.current_build_native_context_v4774':'scripts.current_build_native_context_v6097',
        '[2,11,124,130,145]':'[2,15]','native_ten_consumer_cases':'native_four_consumer_cases','ten_original_progressive_and_catalogue_name_consumers':'four_original_progressive_and_catalogue_name_consumers','len(native[\'rows\'])==10':'len(native[\'rows\'])==4','Ten source-owned name consumers':'Four source-owned name consumers','fresh5_actor_names':'fresh2_actor_names','work/analysis/lil_B204_voices_v6063/current_native_input.json':'work/analysis/current_V6160_native_v6168/current_native_input.json',
    })]
    tools.append(derive('scripts/bind_lil_B204_source_names_v6065.py','scripts/bind_lil_B205_source_names_v6175.py',{
        'B204':'B205','source_names_v6065':'source_names_v6175','source_v6062':'source_v6172','names_v6064':'names_v6174','voices_v6063':'voices_v6173','all20_clean_current_complete_context':'all17_clean_current_complete_context','ten_original_progressive_and_catalogue_name_consumers':'four_original_progressive_and_catalogue_name_consumers','current207_catalog_eight_voices_and_five_source_selectors':'current207_catalog_eight_voices_and_two_source_selectors','[2,11,124,130,145]':'[2,15]','len(payload)==123040':'len(payload)==123264','fresh5_actor_names':'fresh2_actor_names','five_exact_source_name_fields_voices_and_distinct_name_consumers':'two_exact_source_name_fields_voices_and_distinct_name_consumers',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_name_tools.json',dict(tools=tools,two_clean_source_actors_six_fields_four_native_consumers_required=True,no_whole_207_entry_editorial_closure=True,full_goal_complete=False));print('Four B205 name consumers and two exact source-field binders prepared;old producers preserved.')
