"""Exact-runtime/original-B26 private progressive and FE presentation scope."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha

PROOF=Path('work/analysis/lil_London_controls_v1893b/source_bound_B26_presenter_and_control_contract.json')
PROOF_SHA='0aed4295db606799c29e1f169fe9cc2f3a478373530c146ff7701dd8e68814c9'
ARM9_SHA='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
BLOCKS={'3d331aef166a5b7ca61f5f5f0e75db0f37af7342734d7078d6345acf3ed019cb',
        '9387603d1fee1faea1d9c9fcb35613ef2f692e26775ffe9dfb00f13c612966e6'}

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('London requires exact proven runtime and original B26 source')
    if sha(PROOF.read_bytes())!=PROOF_SHA:
        raise ValueError('London source/presenter proof differs')
    p=json.loads(PROOF.read_text(encoding='utf-8'))
    flags=('native_selector_preserves16_28_and151_and_all4MiB',
        'Clifford28_actual_portrait_full_nameplate_body_and_following_Camille_transition_viewed',
        'three_FE_actual_anonymous_portrait_free_paper_panels_viewed',
        'Gerhard10_shared_preamble_matches_actual_SC1B42_proof',
        'Retainer97_uses_same_original_progressive_presenter_and_actor151_catalog',
        'Retainer97_not_individually_activated_no_portrait_or_nameplate_live_claim')
    if p['ARM9_sha256']!=ARM9_SHA or not all(p.get(k) is True for k in flags):
        raise ValueError('London complete scoped presentation evidence required')
    for prefix,count in ((16,5),(28,34),(151,1),(254,3)):
        if source_block.count(bytes.fromhex('0040ffff00')+bytes([prefix]))!=count:
            raise ValueError('London complete preamble inventory differs')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if any(v in base.leading_speaker_bytes for v in (16,28,151,254)):
        raise ValueError('Global Lil presentation profile changed;review scope again')
    if consumer=='progressive':
        return replace(base,name='lil-london-progressive-runtime-bound-v1',
            leading_speaker_bytes=base.leading_speaker_bytes|frozenset({16,28,151}),
            metrics_source=base.metrics_source+'; B26-only original54020/selector proofV1893b. Six conditional objects have source/native coverage,not individual visits.')
    if consumer=='FE-paper':
        return replace(base,name='lil-london-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; B26-only original FE5473C. Conservative216px paragraph planning;separate actual-mode228x48 native paper glyph/pagination proof required.')
    raise ValueError('Unknown London presentation consumer')
