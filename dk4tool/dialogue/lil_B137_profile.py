"""Exact B137 progressive speakers;no FE,source00,choices orpauses."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['3cab88f183ef2da1b51b4bf3e6e8a1abde8053fee4c9146fa79b478f63354522', 'bbbc2d4837485d1c3938cce70be31af4049bf9ad38ed9128456e035a1e029a5c'])
SELECTORS=frozenset({2,9,14,16,17,20,22,23,38,92,198})
DEPENDENCIES={'work\\analysis\\lil_remaining_B137_B140_source_v3380b\\next48_B137_clean_current_context.json': 'd3b6ba92afb7a311e7f510ad64c68d0c2f3d26efb9c10093f38447dc81a08f14', 'work\\analysis\\lil_B137_controls_v3384\\all48_source_current_dispatches_and12_predicates.json': 'dac33373bb5d41df188d13610aa0557978e31b51938647f2e3027f91a91105a7', 'work\\analysis\\lil_B137_voices_v3383b\\current_eleven_static_names_voices_and207_catalog_rebind.json': 'd0fe44f2fb8e4e1fc92de75f84aa6f81ef23c2063f3ab8d0417588c049da29c7', 'work\\analysis\\lil_B137_terms_v3387\\clean_current_names_addresses_thought_and_fivefold_wages.json': '3b3d84132a4298e02c2eefe3a09cf06b8a3b10aae5f6025fa5e28ba371d4f0b6', 'work\\analysis\\lil_B137_branches_v3385b\\original_relative_skip_operand_proof.json': '0e2f093dc27244d90e03ca99cff55ca27d61a936a2327b4c905f312d302400f4', 'work\\analysis\\lil_B137_controls_v3384\\current_registered_name_catalog_binding.json': '147f33e5b0021763adc5efee2e49e6eb5662f9d400a7f916ac71237247a7ede0'}
CONTROL=Path('work\\analysis\\lil_B137_controls_v3384\\all48_source_current_dispatches_and12_predicates.json')
VOICE=Path('work\\analysis\\lil_B137_voices_v3383b\\current_eleven_static_names_voices_and207_catalog_rebind.json')
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('B137 exact clean/current block andruntime required')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B137 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'));voice=json.loads(VOICE.read_text(encoding='utf-8'))
    if consumer!='progressive' or len(control['speech_dispatch_cases'])!=96 or len(control['current_original_predicate_cases'])!=12 or control['original_event_queries'] or control['source_macro_counts']!={'FI':3,'FA':0,'FO':0} or len(voice['fresh_eleven_actor_names']['rows'])!=11:raise ValueError('Complete static actors,predicate andLil-context macro contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B137-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';48 progressive speeches,eleven static actors. FI3/FA5/FO9 use Lil captain2. No FE/source00/dynamic/4100/2000/2100 inthis source scope.')
