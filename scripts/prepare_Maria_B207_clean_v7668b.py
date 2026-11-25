"""Keep all18 native speeches; legacy metadata omitted the meaningful opening silence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_clean_tools_v7668b')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/inventory_Maria_B207_clean_v7668.py','scripts/inventory_Maria_B207_clean_v7668b.py',{
        'maria_B207_clean_v7668':'maria_B207_clean_v7668b',
        "assert not overlap and {r['id'] for r in lead['records']}=={r['id'] for r in selected['records']}":"assert not overlap and len(selected['records'])==18 and {r['id'] for r in lead['records']} < {r['id'] for r in selected['records']} and {r['id'] for r in selected['records']}-{r['id'] for r in lead['records']}=={'DK4_MES_B207_R0004'}",
        "all_selected_source_keys_uncredited=True":"all_selected_source_keys_uncredited=True,legacy_metadata_has17_refs_but_complete_native_scene_has18=True,legacy_metadata_omitted_opening_silence_id='DK4_MES_B207_R0004',initial_7668_metadata_equality_assertion_failure_preserved_not_rejection_credit=True",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_native18_not_legacy17_inventory.json',dict(tool=tool,all_native_source_objects_retained=True,no_ROM_header_command_orJapanese_body_change=True,first_failed_7668_no_output_orcredit_preserved=True,new_credit=0,full_goal_complete=False))
