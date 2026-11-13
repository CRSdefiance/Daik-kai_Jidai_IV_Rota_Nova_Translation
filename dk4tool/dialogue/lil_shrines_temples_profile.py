"""Exact ten-block speech/FE and virtual actor-style context."""
from pathlib import Path
from dataclasses import replace
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA = 'd9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS = frozenset(['077441e40db4306618dcfd2452f6773fc773b54740858b81577d0f277b38d921', '19f56cb2371717ccd8180d15d30d8829df68c7932da5047d114179fb87c16e0e', '1a5a12d68a350f0fc7dc90b8e5b0271affc4375ff7b7a994611937911a2481bb', '264e118d2ad30ccf7bf8128a1325b5e1599630dc0a3b2382d4d60ba16358ab4e', '3176833dceb80b5ba2f3b96af1ea9a4b1675d4efeaced4981d31c282297448e9', '375fdf1615aaa39b70a003a5ffe43594fe755ac70775e264c33333ded683e999', '44231a246a55d83c0abd64ef2b707b52322a9d7d434ec8283571bfccc1e46ff4', '48fe62b0b0062244e2771a38e6a4b6896f5b77db0961ec36823a195a62d8ab14', '5b39d6b332b6e5d9050af990f308c4dd583b20993468f7ccab583f2974c9d87c', '720682d5bf8812aad95465be8fb403df5f58c8f081ee7bdcf4b8f85b8b9e9e73', '764395887827545e78c66e6199fcf6e490df5eb48bd22ed22ca6517b685e1236', '781186c712c7e81f2a6eef2d875d94dedf945898f6446016820ac4a76054d856', '8786f4471c7c28f3edf0f9bb4ba7294d503d9f869e99876012f0bc56b6ee18b3', '8a4ef4a08a28c2bc2c45849bb2be447556e3eca5dafed25a38b09c10d3668ef6', 'a3b26f8a1949fcb58db4619f4f32213e956e8d9dff0f490fec4ce7e45d09ed42', 'bc1ecab3236bd3300a82352f0ec9468482e7902a7e2202325d1279d0ec6634b2', 'c052e29c6a18228323dcbfe88648b38f8ffcb2f10d734f2808cf59aff99b7986', 'cf652faca6d682f926638f09de3ce5248ddf38c95d97c68c34170fdb6425a42b', 'e84b58198acb5e5d010a57e18630065232e940fb3062cec00a124cd78e5373b7', 'f36710c0173ca5ebee01ef3707ce057e19804125c0daebf88e3baf3518328278'])
SELECTORS = frozenset([2, 9, 16, 20, 139, 151, 160, 177, 178, 191, 207, 208])
DEPENDENCIES = {'work\\analysis\\lil_Shrines_Temples_source_v3163\\complete235_clean_current_native_context.json': 'eb4491dae5e324128e9ccafb146147a56aaac946b4f3bddb55603dd2ef35fa9c', 'work\\analysis\\lil_Shrines_Temples_controls_v3168c\\all235_source_current_dispatch_dynamic_styles_and_predicates.json': '24f0e45e64b2dcac48daca8f8c0ed73cd01287706a9d1ba7601525fb410b5576', 'work\\analysis\\lil_Shrines_Temples_terms_v3170\\clean_current_items_cathedral_and_source_roles.json': 'dca6520ebfea84a95e9a355806362c3279074da7b93f5d83b8615c42b919c20d', 'work\\analysis\\lil_Shrines_Temples_voices_v3167\\current_catalog207_eight_voice_groups_and_dynamic_CF_D0.json': 'eee4b73afceb84d43a9c66a966560b4f8bd3500702ca11148d2cc60a5e29f49c', 'work\\analysis\\lil_Shrines_Temples_controls_v3168c\\current_registered_name_catalog_binding.json': '1045ec7a90e655ac432fd74fe2df695c0982f8b0cd0b33b9fa2ecb48cbd19fb8'}
CONTROL = Path('work/analysis/lil_Shrines_Temples_controls_v3168c/all235_source_current_dispatch_dynamic_styles_and_predicates.json')
VOICES = Path('work/analysis/lil_Shrines_Temples_voices_v3167/current_catalog207_eight_voice_groups_and_dynamic_CF_D0.json')

def profile_for(arm, source_block, consumer='progressive'):
    if sha(arm) != ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Shrines/Temples requires exact ten reviewed clean/current blocks and runtime')
    for p, digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes()) != digest:
            raise ValueError('Shrines/Temples source contract changed:' + p)
    control = json.loads(CONTROL.read_text(encoding='utf8'))
    voices = json.loads(VOICES.read_text(encoding='utf8'))
    if (len(control['speech_and_stored_alternative_dispatch_cases']) != 440
        or len(control['whole_original4100_command_cases']) != 16
        or len(control['all207_actor_style_source_pointer_cases']['cases']) != 3312
        or len(control['current_original_predicate_cases']) != 21
        or control['original_event_queries']
        or not control['all30_FE_before_fallback208_use5473C_and24310_null_actor']
        or not control['source_current_effective_runtime_English_distinguished_from_storage']
        or not voices['dynamic_CF_is_original_role0_captain_and_D0_role1_with_original_fallback']
        or len(voices['catalog']['rows']) != 207):
        raise ValueError('Complete current speech, FE, dynamic actor-style and predicate contract required')
    base = get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer == 'progressive':
        return replace(base, name='lil-shrines-temples-progressive-runtime-bound-v1',
            leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source + '; exact10blocks/164preambles/56stored actor-style alternatives. CFcaptain/D0role1fallback source bound. VirtualD0prefix is formatter-only; typed4100 packing must remove it and preserve the source20byte header/eight alias slots. Current fonts and three-choice geometry still required.')
    if consumer == 'FE-paper':
        return replace(base, name='lil-shrines-temples-FE-runtime-bound-v1',
            leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source + '; exact30FE before fallback208; original24310 null actor then5473C. Inherited228x48logical/228x64physical mode1paper, conservative216px planning. English starts first line; source vertical staging breaks are not authored. Complete per-record glyph/pagination proof required.')
    raise ValueError('Unknown Shrines/Temples consumer')
