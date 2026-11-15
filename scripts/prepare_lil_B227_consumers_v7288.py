"""Bind B227's two source actors and independent EV2 entry without inherited identities."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_consumer_tools_v7288')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B226':'B227','source_v7240/twenty_clean_current_Attila_armor_exchange_source_references':'source_v7287/nine_clean_current_sword_practice_cloth_rumor_source_references','current_V7230_native_v7235':'current_V7277_native_v7282'}
    consumers={**common,'v7241':'v7288','all20_clean_glosses_precede_old_English':'all9_clean_glosses_precede_old_English','[2,23]':'[2,25]','len(cases)==40':'len(cases)==18','len(effective)==20':'len(effective)==9','all40_source_current_dispatches':'all18_source_current_dispatches','all20_current_templates':'all9_current_templates','twenty_effective_bodies40_dispatches_two_actors_four_name_consumers':'nine_effective_bodies18_dispatches_two_actors_four_name_consumers','two actors,four original name consumers and twenty':'two actors,four original name consumers and nine','bodies=20,dispatches=40':'bodies=9,dispatches=18'}
    entry={**common,'v7242':'v7289','in [226]':'in [227]'}
    jobs=[('scripts/prove_lil_B226_consumers_v7241.py','scripts/prove_lil_B227_consumers_v7288.py',consumers),('scripts/prove_lil_B226_entry_v7242.py','scripts/prove_lil_B227_entry_v7289.py',entry)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_consumer_entry_tools.json',dict(tools=rows,strict2b6_own_current_input_andall_native_constants_preserved=True,no_new_surname_rank_kinship_ororiginal_location_assumption=True,new_credit=0,full_goal_complete=False))
