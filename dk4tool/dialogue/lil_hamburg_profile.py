"""B74-only original progressive/Gerhard and separate FE paper consumers."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha

PROOF = Path('work/analysis/lil_Hamburg_controls_v1953b/source_bound_B74_presenter_and_control_contract.json')
PROOF_SHA = '5cfde262d710257099e083b7d3c0f1143721ae92bc238920f8e30dd27b32089f'
ARM9_SHA = '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
BLOCKS = {'5d5d8845f149c83b61b0b8e4c35ee688a79b43ac8e541d9adcad77a64a06e07b',
          '88884af4d54b369a701fd6e9141aea6d872d50c96720be2215b6f5f73e00421f'}


def profile_for(arm, source_block, consumer='progressive'):
    if sha(arm) != ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Hamburg requires exact proven runtime and original B74 source')
    if sha(PROOF.read_bytes()) != PROOF_SHA:
        raise ValueError('Hamburg source/presenter proof differs')
    proof = json.loads(PROOF.read_text(encoding='utf-8'))
    flags = ('native_selector_preserves16_and_all4MiB',
             'Gerhard10_actual_portrait_full_nameplate_and_following_dialogue_viewed',
             'three_FE_actual_anonymous_portrait_free_paper_panels_viewed',
             'FE_uses_original_separate_consumer_and_null_actor_macro_caller',
             'FE_not_reinterpreted_via_fallback_actor_selector',
             'all79_original_speeches_individually_observed',
             'original_capture_B74_and_ARM9_exact_current')
    if proof['ARM9_sha256'] != ARM9_SHA or not all(proof.get(k) is True for k in flags):
        raise ValueError('Hamburg complete scoped presentation evidence required')
    for prefix, count in ((2,20),(9,23),(14,2),(16,30),(20,1),(254,3)):
        if source_block.count(bytes.fromhex('0040ffff00') + bytes([prefix])) != count:
            raise ValueError('Hamburg complete original preamble inventory differs')
    base = get_dialogue_profile('lil-opening-editorial-native-v1')
    if any(v in base.leading_speaker_bytes for v in (16,254)):
        raise ValueError('Global Lil profile changed; review original scoped contract again')
    if consumer == 'progressive':
        return replace(base, name='lil-hamburg-progressive-runtime-bound-v1',
            leading_speaker_bytes=base.leading_speaker_bytes | frozenset({16}),
            metrics_source=base.metrics_source + '; exact B74 original54020/Gerhard16 control proofV1953b')
    if consumer == 'FE-paper':
        return replace(base, name='lil-hamburg-FE-runtime-bound-v1', leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source + '; B74 original FE5473C; conservative216px planning. Separate228x48 mode1 native font/pagination proof required.')
    raise ValueError('Unknown Hamburg presentation consumer')
