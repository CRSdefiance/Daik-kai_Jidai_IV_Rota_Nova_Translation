"""Exact B135/B136 progressive speakers;no FE,source00,choices orpauses."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['5677c6275378ffef7cf60865220cf6f695c7c97df45340b73dd79ab178dde614', '5aa9f7934582b07c4840e01cddea98395bfceade743306ddd9470041396f7fbb', 'b5791241f80daf6f39820b215b24a9328e4d5f716163cb99d15aca932f73cc8a', 'b9c6b51a01f0031375273eb1ef5cefceabc8942d01da526eb31ee0f9adf6dd58'])
SELECTORS=frozenset({2,9,14,36,47,96})
DEPENDENCIES={'work\\analysis\\lil_remaining_B135_B140_source_v3345b\\next35_B135_B136_clean_current_context.json': '2c5b4c86ebb60a1daf8565d1d33bf0d268bdd500726af233b6d9c9f721625bec', 'work\\analysis\\lil_B135_B136_controls_v3347\\all35_source_current_dispatches_and1_predicate.json': '2317a40a7eeb25565dcb02bcf8e2ade0d4cb4208c85a420d59e03ec60b4670a2', 'work\\analysis\\lil_B135_B136_voices_v3346b\\current_six_static_names_voices_and207_catalog_rebind.json': '2f50655e90b55c1b3f1430ddfa4083a00a92ac2788b3a842ccec9c1a4fe4fb81', 'work\\analysis\\lil_B135_B136_terms_v3352\\clean_current_tablets_narcotic_names_and_wordplay_reconciliation.json': '1e602175117c6dde89e100c16e015cefce1a1730e035d78ee7aac45d7b16bdab', 'work\\analysis\\lil_B135_B136_branches_v3348b\\original_relative_skip_operand_proof.json': 'cbbdcb3dacbd3adf0d42f46dc1631df358b9a5412ae27c741409acb8b4f2f4bf', 'work\\analysis\\lil_B135_B136_controls_v3347\\current_registered_name_catalog_binding.json': '1432ebc7d7f911c2e9dccc81a8475a6bbfa854bb5ff10f700a4d93a7b4ca0bcb'}
CONTROL=Path('work\\analysis\\lil_B135_B136_controls_v3347\\all35_source_current_dispatches_and1_predicate.json')
VOICE=Path('work\\analysis\\lil_B135_B136_voices_v3346b\\current_six_static_names_voices_and207_catalog_rebind.json')
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('B135/B136 exact clean/current block andruntime required')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B135/B136 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'));voice=json.loads(VOICE.read_text(encoding='utf-8'))
    if consumer!='progressive' or len(control['speech_dispatch_cases'])!=70 or len(control['current_original_predicate_cases'])!=1 or control['original_event_queries'] or control['source_macro_counts']!={'FI':0,'FA':0,'FO':1} or len(voice['fresh_six_actor_names']['rows'])!=6:raise ValueError('Complete static actors,predicate andLil-context macro contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B135-B136-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';35 progressive speeches,six static actors. FI3/FA5/FO9 use Lil captain2. No FE/source00/dynamic/4100/2000/2100 inthis source scope.')
