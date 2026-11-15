"""Exact-runtime/original-B25/B128 private progressive presentation scope."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha

PROOF = Path('work/analysis/lil_Speyer_controls_v1936/source_bound_B25_B128_progressive_control_contract.json')
PROOF_SHA = 'e816a5f1f99b2e5874fd68255fa89961fa53d72e76dd6b33887cf8794142e3b3'
ARM9_SHA = '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
BLOCKS = {
    'b5b0b776ce9513b4c421bdbf4060ad0ce2e080da7bdb0aa55d40bd8746fd73f4':25,
    'a7d145c37c3b53d6d35155e9e5ba4c67a6fa8a93fd95586f6406604603804527':25,
    '4289e262e31e26412201fab0a83ccb1c36837847423db0980746ff33668ec134':128,
    '3b74465173e3de6d2c3861657a93fad5f1dea223fc58c630c5c4e3c815ebc599':128,
}

def profile_for(arm,source_block):
    number = BLOCKS.get(sha(source_block))
    if sha(arm)!=ARM9_SHA or number is None:
        raise ValueError('Speyer requires exact proven runtime and original B25/B128 source')
    if sha(PROOF.read_bytes())!=PROOF_SHA:
        raise ValueError('Speyer source/presenter proof differs')
    proof = json.loads(PROOF.read_text(encoding='utf-8'))
    flags = ('native_selector_preserves29_151_152_and_all4MiB',
        'Speyer29_actual_portrait_full_Martin_Speyer_nameplate_body_and_transitions_viewed',
        'actor152_actual_Sailor_portrait_nameplate_Japanese_body_and_following_Lil_transition_viewed',
        'native_catalog_full_name_not_assumed_to_equal_actual_nameplate',
        'source151_unidentified_player_side_voice_uses_same_original_progressive_presenter',
        'Retainer151_fallback_not_individually_activated','all57_complete_source_preambles_bound',
        'all_Speyer_speeches_use_same_original_progressive_presenter','no_FE_or_new_modal_geometry_in_Speyer_blocks')
    if proof['ARM9_sha256']!=ARM9_SHA or not all(proof.get(k)is True for k in flags):
        raise ValueError('Speyer complete scoped presentation evidence required')
    counts = ({2:1,9:1,20:1} if number==25 else {2:18,9:21,14:1,20:3,29:7,151:1,152:3})
    for prefix,count in counts.items():
        if source_block.count(bytes.fromhex('0040ffff00')+bytes([prefix]))!=count:
            raise ValueError('Speyer complete source preamble inventory differs')
    base = get_dialogue_profile('lil-opening-editorial-native-v1')
    if any(p in base.leading_speaker_bytes for p in (29,151,152,254)):
        raise ValueError('Global Lil presentation profile changed; review scope again')
    return replace(base,name='lil-speyer-progressive-runtime-bound-v1',
        leading_speaker_bytes=base.leading_speaker_bytes|frozenset({29,151,152}),
        metrics_source=base.metrics_source+'; B25/B128-only original54020/selector proofV1936. Actor152 displays Sailor although its catalog says Retainer. Six speeches have offline coverage without individual activation.')
