"""Source/runtime-bound B30/B31/B132 ordinary progressive speech profile."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_post_Seville_controls_v2734c/source_bound_34_preambles_and_B132_warning_predicate.json')
PROOF_SHA='867a83e37988d206078e209accd0ee30bc781146782bd8a2242fcfdb1064526e'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['4016494183e150863511afb7270214cefc690dba01f675ceb0c6eaeb63ae1a6f', '57cd7be0de8f4cf7dbbc9999c21b659bcfd4fdfb95ec5c1a692b372036129d2b', '704b94a0a6dc89f9a3471c2ede3e2bdef5e25d38a9f4c7b5ab0cbb5746bd5b76', 'b643a07beeac74ce33200a894a1e31a2a1927d630a2fa4197a32ab5b89bf7fe0', 'c65543841598459856a03c6b5f5b04b3ada085153e577cdd21efa632a4876af6', 'd823392f90c185d3f2420957f3bf2e3ad9200be3a1634db64c48dbdf89a6c0a7'])


def profile_for(arm,source_block):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Post-Seville requires exact reviewed B30/B31/B132 source and runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA:
        raise ValueError('Post-Seville source control proof changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'))
    expected={'2':2,'4':4,'9':9,'16':16,'20':20,'28':28,'31':31,'92':92,'113':113}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all34_complete_preambles_and68_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=68 or proof['ordinary_native_actor_selectors']!=expected
        or not proof['warning_reference_is_B132_Barkeep_not_Clifford']):
        raise ValueError('Post-Seville complete ordinary actor/control contract required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-post-seville-progressive-runtime-bound-v1',
        leading_speaker_bytes=frozenset({2,4,9,16,20,28,31,92,113}),
        metrics_source=base.metrics_source+'; exact B30/B31/B132complete preambles,ordinary selector54020andB132warning predicate. No individual new portrait/activation claim;current native fonts,representative andrelease gates required.')
