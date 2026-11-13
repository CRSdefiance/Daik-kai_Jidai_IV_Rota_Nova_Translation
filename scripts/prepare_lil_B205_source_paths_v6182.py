"""Derive complete B205 source observation audit from independently counted source."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_source_path_tools_v6182')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/audit_lil_B204_source_paths_v6072.py','scripts/audit_lil_B205_source_paths_v6182.py',{
        'B204':'B205','source_paths_v6072':'source_paths_v6182','source_fixture_v6070':'source_fixture_v6180','source_run_v6071':'source_run_v6181',
        '[9,13,16,19,29,33,36,45,48,52,55,58,62,66,69,72]':'[5,9,13,17,20,24,28,32,36,40,44,47,51,55,59,63,67]',
        '1308':'616','len(selected)==20':'len(selected)==17','len(pairs)==35':'len(pairs)==34','stored_source_objects=20':'stored_source_objects=17',
        'all26_source_plus9_original_initializer_commands_stored':'all25_source_plus9_original_initializer_commands_stored',
        'initialized_Amsterdam_fixture_not_natural_event204_activation_or_original_location':'initialized_Amsterdam_fixture_not_natural_event205_activation_or_original_location',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_observation_audit_derivation.json',dict(tool=tool,source_objects=17,source_commands=25,initializers=9,new_review_credit=0,full_goal_complete=False))
