"""Bind source names,voices andentry independently of the preceding exchange."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_consumer_tools_v7241')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B225':'B226','source_v7178/thirteen_clean_current_children_heroes_exchange_source_references':'source_v7240/twenty_clean_current_Attila_armor_exchange_source_references','current_V7168_native_v7173':'current_V7230_native_v7235'}
    consumers={**common,'v7179':'v7241','all13_clean_glosses_precede_old_English':'all20_clean_glosses_precede_old_English','[2,16,151,162]':'[2,23]',"len(native['rows'])==8":"len(native['rows'])==4",'len(cases)==26':'len(cases)==40','len(effective)==13':'len(effective)==20','all26_source_current_dispatches':'all40_source_current_dispatches','all13_current_templates':'all20_current_templates','thirteen_effective_bodies26_dispatches_four_actors_eight_name_consumers':'twenty_effective_bodies40_dispatches_two_actors_four_name_consumers','four actors,eight original name consumers and thirteen':'two actors,four original name consumers and twenty','native_eight_distinct_name_consumers':'native_four_distinct_name_consumers','all_eight_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_four_original_consumers_and_owned_or_readonly_memory_paths_exact','bodies=13,dispatches=26':'bodies=20,dispatches=40'}
    entry={**common,'v7180':'v7242','in [225]':'in [226]'}
    jobs=[('scripts/prove_lil_B225_consumers_v7179.py','scripts/prove_lil_B226_consumers_v7241.py',consumers),('scripts/prove_lil_B225_entry_v7180.py','scripts/prove_lil_B226_entry_v7242.py',entry)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_consumer_entry_tools.json',dict(tools=rows,strict2b6_own_current_input_andall_native_constants_preserved=True,no_new_surname_kinship_rank_ororiginal_location_assumption=True,new_credit=0,full_goal_complete=False))
