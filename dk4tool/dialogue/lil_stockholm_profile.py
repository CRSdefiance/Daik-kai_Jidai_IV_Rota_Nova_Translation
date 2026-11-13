"""Exact-runtime/B27-only Gerhard control extension;global profiles unchanged."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha

PROOF=Path('work/analysis/Gerhard_story_control_proof_v1857/original4000_prefix10_Gerhard_live_mapping.json')
PROOF_SHA='d52ac7f0487586a2b2f25ab57fa0e2537ae558df2f28a64c38f3816cd41d4dd6'
ARM9_SHA='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
BLOCKS={'83465e8cab8124547f26aa6299b113d546e5fe924035849aa5bcfa2a054e9b92',
        '5e1041e21a231e96c4329888acb651a5c3d98f65e2d04a0941569a2727a45e3a'}

def profile_for(arm,source_block):
    if sha(arm)!=ARM9_SHA or sha(source_block)not in BLOCKS:
        raise ValueError('Stockholm profile requires exact proven runtime and original B27 source')
    if sha(PROOF.read_bytes())!=PROOF_SHA:
        raise ValueError('Stockholm original Gerhard control proof differs')
    proof=json.loads(PROOF.read_text(encoding='utf-8'))
    if (proof['ARM9_sha256']!=ARM9_SHA or proof['native_actor_ID']!=16
        or proof['mapped_source_preamble_hex']!='0040ffff0010'
        or not proof['actor16_lookup_exact_on_actual_Hodram1_and_Lil2_snapshots']
        or not proof['actual_Gerhard_portrait_full_nameplate_body_and_normal_next_Hodram_portrait_viewed']
        or len(proof['eligible_B27_record_IDs'])!=9):
        raise ValueError('Stockholm live source-control mapping incomplete')
    if source_block.count(bytes.fromhex('0040ffff0010'))!=9:
        raise ValueError('Stockholm original Gerhard preamble inventory differs')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if 0x10 in base.leading_speaker_bytes:
        raise ValueError('Global profile changed;original scoped contract must be reviewed again')
    return replace(base,leading_speaker_bytes=base.leading_speaker_bytes|frozenset({0x10}),
        metrics_source=base.metrics_source+'; exact B27 leading10/Gerhard mapping proven by V1857;no other control or global profile change')
