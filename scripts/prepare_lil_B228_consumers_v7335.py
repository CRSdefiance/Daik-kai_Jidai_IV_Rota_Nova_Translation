"""Bind B228 source names,voices andEV2 entry independently of earlier item rumors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_consumer_tools_v7335')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B227':'B228','source_v7287/nine_clean_current_sword_practice_cloth_rumor_source_references':'source_v7334/thirteen_clean_current_armadillo_shield_rumor_source_references','current_V7277_native_v7282':'current_V7324_native_v7329'}
    consumers={**common,'v7288':'v7335','all9_clean_glosses_precede_old_English':'all13_clean_glosses_precede_old_English','[2,25]':'[2,22]','len(cases)==18':'len(cases)==26','len(effective)==9':'len(effective)==13','all18_source_current_dispatches':'all26_source_current_dispatches','all9_current_templates':'all13_current_templates','nine_effective_bodies18_dispatches_two_actors_four_name_consumers':'thirteen_effective_bodies26_dispatches_two_actors_four_name_consumers','two actors,four original name consumers and nine':'two actors,four original name consumers and thirteen','bodies=9,dispatches=18':'bodies=13,dispatches=26'}
    entry={**common,'v7289':'v7336','in [227]':'in [228]'}
    jobs=[('scripts/prove_lil_B227_consumers_v7288.py','scripts/prove_lil_B228_consumers_v7335.py',consumers),('scripts/prove_lil_B227_entry_v7289.py','scripts/prove_lil_B228_entry_v7336.py',entry)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_consumer_entry_tools.json',dict(tools=rows,strict2b6_own_current_input_andall_native_constants_preserved=True,no_new_name_middle_field_rank_ororiginal_location_assumption=True,new_credit=0,full_goal_complete=False))
