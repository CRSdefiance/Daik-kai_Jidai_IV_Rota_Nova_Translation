"""Retain established build/startup/regression procedures with explicit current-input bindings."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/shady_man_build_tools_v6268')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/build_generic_speaker_labels_v5891.py','scripts/build_shady_man_label_v6270.py',{'generic_speaker_labels_build_v5891':'shady_man_label_build_v6270','v5891':'v6270','generic_speaker_labels_registration_v5890':'shady_man_label_registration_v6269'}))
    tools.append(derive('scripts/run_lil_B205_regressions_v6220.py','scripts/run_shady_man_regressions_v6270.py',{'lil_B205_regressions_v6220':'shady_man_regressions_v6270'}))
    tools.append(derive('scripts/run_generic_speaker_labels_startup_v5893.py','scripts/run_shady_man_startup_v6272.py',{'generic_speaker_labels_runs_v5893':'shady_man_runs_v6272','generic_speaker_labels_v5893':'shady_man_v6272','version=5891':'version=6270'}))
    tools.append(derive('scripts/verify_generic_speaker_labels_startup_v5894.py','scripts/verify_shady_man_startup_v6273.py',{'generic_speaker_labels_startup_v5894':'shady_man_startup_v6273','generic_speaker_labels_runs_v5893':'shady_man_runs_v6272','v5891':'v6270','V5872':'V6220','v5872':'v6220','translations/generic_speaker_labels_release_v1.json':'translations/shady_man_label_release_v1.json','lil_B200_runs_v5874':'lil_B205_runs_v6222','Current5891':'Current6270'}))
    tools.append(derive('scripts/record_generic_speaker_labels_startup_view_v5894.py','scripts/record_shady_man_startup_view_v6273.py',{'generic_speaker_labels_startup_v5894':'shady_man_startup_v6273','V5872':'V6220'}))
    ROOT.mkdir(parents=True);save(ROOT/'current_cumulative_build_regressions_and_startup_tools.json',dict(tools=tools,exact_native_numeric_constants_preserved=True,registered_build_profile='all-routes-unified-v6270',startup_parent='all-routes-unified-v6220',full_goal_complete=False));print('Current registered build,110-regression and two cold-boot verification tools prepared.')
