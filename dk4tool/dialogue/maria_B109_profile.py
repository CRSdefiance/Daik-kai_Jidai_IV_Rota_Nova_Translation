"""Exact B109 progressive metrics,with separate source UI restoration/actual gates."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['a7021783122684ee09eaad0b1932fd553b8927b289b6cb887c7b508b42c47457', '097bf7472d32718ced887cd2ee0c56ab130f93c711207cf17d929522b5cae1b5', 'c33cff9a3ab7f883bbccb078457985d9dca0439f461c0f3df2c2d1bc856a20ed'])
SELECTORS=frozenset({3,11,21,74})
DEPENDENCIES={'work\\analysis\\maria_B109_source_v3498\\all26_clean_current_complete_context.json': '7f979eb36fa90171a24dcaac1268806691491d8cf53478302d088adfa6a1eafa', 'work\\analysis\\maria_B109_controls_v3502\\source_restored_UI_prefix_pause_C200_and34_commands_contract.json': '221624ee6ae72ba825e5cdbc0b16cc886d90020d4986a080027b2cbd2ef98d92', 'work\\analysis\\maria_B109_voices_v3499\\current_four_Maria_static_names_voices_and_native_context.json': '973f964ff3dc498dab143546229b7502fbed16cb26be5b55cee2c610e2259d64', 'work\\analysis\\maria_B109_dispatches_v3500\\all26_source_current_Maria_dispatches_and_catalog.json': 'e490ea3881fbd14a7e5a078ce53e0e4af2278929b1d9e3e22d75d5024e1e8ecf', 'work\\analysis\\maria_B109_entry_v3501\\source_EV3_B109_action_dependency_and_native_getter_binding.json': 'f991f6d1ccd64526722882f8ed48f16e63b8ea1089a4e019d1c7134f9e535ee5', 'work\\analysis\\maria_B109_terms_v3504b\\current_approved_Admiral_Ming_Netherlands_and_source_culture.json': '862419f544d1b864367d7ab62817a2bc0064668f73adfe3cb8a118d07281e533', 'work\\analysis\\maria_B109_macro_profile_v3507\\four_static_actors_default_macro_lengths16_alignment_cases.json': '679de948e69572175b385d7a0dfbc3e2ab91131b86aa53cc8f0649afbc0faf8d'}
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS or consumer!='progressive':raise ValueError('Exact Maria B109 source/current block and progressive runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Maria B109 source contract changed:'+path)
    base=get_dialogue_profile('maria-story-shared-events-live')
    return replace(base,name='maria-B109-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,balanced_wrapping=True,literal_prefix_policy='native-guard-v255',macro_widths={'FI':30,'FA':12,'FO':42,'I':12},macro_ascii_lengths={'FI':5,'FA':2,'FO':7},metrics_source=base.metrics_source+';B10926 progressive speeches,four static actors in actual Maria captain3 context.52 native dispatches and16 default macro cases bind5/2/7 lengths;source macros0. Original CS0101/4500/4684 prefix restoration,pause andC200 are separate source controls;focused actual display/transition approval remains required.')
