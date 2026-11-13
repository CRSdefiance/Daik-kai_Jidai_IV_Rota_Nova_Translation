"""Prepare exact current consumers and event binding without assigning child roles."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_consumer_tools_v7179')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B224':'B225','source_v7130/fifteen_clean_current_Medusa_flirtation_exchange_source_references':'source_v7178/thirteen_clean_current_children_heroes_exchange_source_references','current_V7118_native_v7123':'current_V7168_native_v7173'}
    consumers={**common,'v7131':'v7179','all15_clean_glosses_precede_old_English':'all13_clean_glosses_precede_old_English','[26,197]':'[2,16,151,162]',"len(native['rows'])==4":"len(native['rows'])==8",'len(cases)==30':'len(cases)==26','len(effective)==15':'len(effective)==13','all30_source_current_dispatches':'all26_source_current_dispatches','all15_current_templates':'all13_current_templates','fifteen_effective_bodies30_dispatches_two_actors_four_name_consumers':'thirteen_effective_bodies26_dispatches_four_actors_eight_name_consumers','two actors,four original name consumers and fifteen':'four actors,eight original name consumers and thirteen','native_four_distinct_name_consumers':'native_eight_distinct_name_consumers','all_four_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_eight_original_consumers_and_owned_or_readonly_memory_paths_exact','bodies=15,dispatches=30':'bodies=13,dispatches=26'}
    entry={**common,'v7132':'v7180','in [224]':'in [225]'}
    jobs=[('scripts/prove_lil_B224_consumers_v7131.py','scripts/prove_lil_B225_consumers_v7179.py',consumers),('scripts/prove_lil_B224_entry_v7132.py','scripts/prove_lil_B225_entry_v7180.py',entry)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_consumer_entry_tools.json',dict(tools=rows,strict2b6_own_current_input_and_all_native_constants_preserved=True,static_source_selectors_not_renamed_or_given_new_roles=True,actual_child_labels_630B_and_entry_eligibility_not_assumed=True,new_credit=0,full_goal_complete=False))
