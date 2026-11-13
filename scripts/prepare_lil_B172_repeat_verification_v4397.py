"""Bind B172's focused repeats to exact current native state and original code."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_repeat_verify_tools_v4397')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/verify_lil_B171_repeat_v4344.py','scripts/verify_lil_B172_repeat_v4397.py',{
        'B171':'B172','source_event171':'source_event172',
        'v4344':'v4397','v4343':'v4395','v4340':'v4389','v4341':'v4390',
        'all53':'all47','==53':'==47','2112':'1880','first_end':'single_end',
        '3130':'3010','7510':'6610','11770':'9370','16450':'14050',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(tool=tool,whole_scene47_commands_and_single_end1880=True,
        native_state_samples=[3010,6610,9370,14050,19990],post_C200_A000_town_sample=9370,
        no_new_causal_trace_or_equal_world_claim=True,full_goal_complete=False))
    print('Prepared B172 focused repeat verification,including post-C200/A000 actor/captain and five persistent components.')
