"""Six exact clean/current blocks; static actors, FE and original UI pauses."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['04a0ed0efd0be70c5db9f0c5961475a6138bf7eb4596cfd74ce5dcbaeac5f418', '369cacde069478192d02f4c39c167cfc660c51f3e0dec7b0755ccb4a8e0a01dd', '5b0038222e5f247b8dba2bc17be9cd140efc182be1772892ee038cb2aecb8f9d', '60aa166d494f4fe4b3b16d9326f33bdba1cbffd6ffbdbb5635935d491cc2e0e3', '75224c2b450e9d6374aed515612fa1059204e48d74f208a234aed2b4f32923c9', '8104ae3358d96d4f5d795fbc3bca557ac5e7809724609b18607c23f33d4e9496', '8af1ad141b29e9626e79e44fa10676f0e140a9f2c06c81e9d32c91a11db5d122', 'cb47d89c56407ce24af8132eea207228313977e39dcbc18dd1b0ad224e09467e', 'cd3ad8e1b8247393ae3508c0994c62ee41b0ab95574df0b2efbf387f823558c2', 'd066f6606fb6c593ac91ec278677cc89cb1d6edc6d7db4cf8ed3a4c2a7230d3a', 'd8a787222cd2f05b9db52c47dd1e6b27f5881008032e7caaa4034ad99a5d4816', 'fbd16251cde3bd17f9d3082f069130b0099027fd2872565b80f2951f854fa845'])
SELECTORS=frozenset({2,6,9,20,26,92,95,151})
DEPENDENCIES={'work\\analysis\\lil_B122_B127_source_v3260c\\complete159_clean_current_native_context.json': '3eed258827402e10595a5ef52c6a1a9370b0022c60ee58b7f41006bb091b94aa', 'work\\analysis\\lil_B122_B127_controls_v3266\\all155_source_current_dispatch_FE_null_actor_and14_predicates.json': '67e45f3cbbc078c7e9ed55bfdbb094a7c444714ff21fb78f00c89115aa1cc7c6', 'work\\analysis\\lil_B122_B127_voices_v3264\\current_eight_static_names_voices_and207_catalog_rebind.json': '7e14dda84635da7c36ed32826f032bbc4c8214d323812acfcc94cd9415c58ca2', 'work\\analysis\\lil_B122_original2000_waits_v3265\\original2000_actual_rule_and_current_source_binding.json': '5f59813a336e996bd2ef6c1d616486d922d0c01438087853904b23ce0f5ca107', 'work\\analysis\\lil_B122_B127_terms_v3267\\clean_current_items_Spirit_static_actors_and_related_terms.json': 'fc16beb2103f61ceefe65e3077c4b102b81ced75a9e913f4dccd61de6fe0a0ee', 'work\\analysis\\lil_B122_B127_controls_v3266\\current_registered_name_catalog_binding.json': '7737308af4672fc2445bb9019cde71795a8e21570e65fd684eacea2e77598606'}
CONTROL=Path('work\\analysis\\lil_B122_B127_controls_v3266\\all155_source_current_dispatch_FE_null_actor_and14_predicates.json')
VOICE=Path('work\\analysis\\lil_B122_B127_voices_v3264\\current_eight_static_names_voices_and207_catalog_rebind.json')
WAIT=Path('work\\analysis\\lil_B122_original2000_waits_v3265\\original2000_actual_rule_and_current_source_binding.json')

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('B122-B127 requires exact six clean/current blocks and runtime')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B122-B127 source contract changed:'+path)
    control=json.loads(CONTROL.read_text(encoding='utf-8'))
    voice=json.loads(VOICE.read_text(encoding='utf-8'))
    wait=json.loads(WAIT.read_text(encoding='utf-8'))
    if (len(control['speech_dispatch_cases'])!=310 or len(control['current_original_predicate_cases'])!=14
        or control['original_event_queries'] or control['source_macro_counts']!={'FI':12,'FA':0,'FO':0}
        or not control['all20_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback']
        or len(voice['fresh_eight_actor_names'])!=8
        or not voice['source_97_is_static_retainer151_not_dynamic_D0_fallback']
        or not wait['current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence']):
        raise ValueError('Complete original speech/FE/actor/predicate/UI2000 source contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B122-B127-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';145 progressive static actor speeches. Static97 is Retainer151. No dynamic selector or4100 body. Preserve original2000 pauses and2100 choices separately.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B122-B127-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';10 unlabeled FE panels;original24310 null actor before5473C/fallback208.228x48 logical/228x64 physical paper;conservative216px planning. Seven Japanese leading-LF staging cases are not authored English blank rows. No invented name/caption;source FI exact.')
    raise ValueError('Unknown B122-B127 consumer')
