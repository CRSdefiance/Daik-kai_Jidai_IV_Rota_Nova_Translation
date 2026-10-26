"""Exact B28/B29 source-bound progressive and separate FE planning profiles."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha

PROOF=Path('work\\analysis\\lil_Seville_controls_v2706b\\source_bound_B28_B29_presenter_and_control_contract.json')
PROOF_SHA='db72e0b16edfe0981118910faf21e6511d07d8178bd3f939e0b8c95cb532cf08'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset({'a9a3e9c8a409a85b503749634342c1d10e708c8c35acff300843917e562a1a7c', '9858f3629f4b032ae48e33a8c8dd7dd7a90c2dfff855fb564561da3770d1b30d', '482931caad6cac9cc19da4b668670da8d2876e0432c3850b8c28d72a7f4d956e', '1b755f68c827ed37c1447caf87c8b238599fa68ac9ad1595e8d4753a1a1b0bf3'})

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Seville requires exact reviewed B28/B29 source and current runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA:
        raise ValueError('Seville source control proof changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'))
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all18_complete_preambles_bound']
        or len(proof['all36_source_current_text_contexts_dispatch_to_correct_actor_or_FE'])!=36
        or proof['ordinary_native_actor_selectors']!={'2':2,'4':4,'16':16,'20':20,'31':31}
        or not proof['ordinary_selector_on_FE_would_return208_but_original_dispatch_selects_FE_first']):
        raise ValueError('Seville complete ordinary actor/FE dispatch contract required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-seville-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset({2,4,16,20,31}),
            metrics_source=base.metrics_source+'; exact B28/B29source/ordinary selector54020proof2712. Individual Janus/Valdes visits not claimed;current native fonts/macro/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-seville-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exact B28/B29FE5473Cbeforefallback208;conservative216px planning,separate228x48mode1/native pagination proof required.')
    raise ValueError('Unknown Seville presentation consumer')
