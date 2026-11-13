"""Exact B131/B133 static speakers andFE;source00 is actor0,not a terminator."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['6c439afb57244a70a207bfa5e9a19c191c9379b44ebc99dce1885dbe4039a984', '6fd63f08858a025ea6b24d54c798d65dace5e4c1938247c4dce0c3401fc9b8e6', '9e836d3703c482703254daac1a6cd36ddf9132d1a53ff4a8885cca3712c55003', 'a00391d091293de202c3b569b7936ce09cc2ebd2fc5bd29e6d05d377094d4cf2'])
SELECTORS=frozenset({0,2,5,9,20})
DEPENDENCIES={'work\\analysis\\lil_remaining_B131_B140_source_v3306b\\next63_B131_B133_clean_current_context.json': '16ae615ee3c21d61cb15830e89f98927fb71fe67985e5f11f4ef0da93969ed66', 'work\\analysis\\lil_B131_B133_controls_v3308b\\all61_source_current_dispatch_selector00_FE_and5_predicates.json': 'c171643475bf35b3a0b08a5cfc22481250d66f80cccec566551b9d302e06cc32', 'work\\analysis\\lil_B131_B133_voices_v3307b\\current_five_static_names_voices_selector00_and207_catalog_rebind.json': 'cbcaa5c8bdc26ee8761b35ce5c231a05f42e52065697377efa41537ed6af152e', 'work\\analysis\\lil_B131_B133_terms_v3313\\clean_current_items_names_and_share_ratio_reconciliation.json': '3bc383d30fd89f5a318e4b81cd89dc24dc6b756c23d8948694ad8ac44e16a0e8', 'work\\analysis\\lil_B131_B133_branches_v3309b\\original_relative_skip_operand_proof.json': '9c580170047da4a94410cf1716971fba5059920584e04af79c5b34b334498517', 'work\\analysis\\lil_B131_B133_controls_v3308b\\current_registered_name_catalog_binding.json': '28a27e03e6b9f01dc0559c45e7a5955524070d807a7582e699ba959b771b1943'}
CONTROL=Path('work\\analysis\\lil_B131_B133_controls_v3308b\\all61_source_current_dispatch_selector00_FE_and5_predicates.json')
VOICE=Path('work\\analysis\\lil_B131_B133_voices_v3307b\\current_five_static_names_voices_selector00_and207_catalog_rebind.json')
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('B131/B133 requires exact clean/current blocks andruntime')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B131/B133 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'));voice=json.loads(VOICE.read_text(encoding='utf-8'))
    if (len(control['speech_dispatch_cases'])!=122 or sum(r['source_selector']==0 for r in control['speech_dispatch_cases'])!=36
        or len(control['current_original_predicate_cases'])!=5 or control['original_event_queries']
        or control['source_macro_counts']!={'FI':6,'FA':0,'FO':1}
        or not control['all2_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback']
        or not control['source00_is_static_actor0_Rafael_Castor_without_role_assignment']
        or len(voice['fresh_five_actor_names']['rows'])!=5 or not voice['source00_is_static_actor0_not_empty_text_or_dynamic_role']):
        raise ValueError('Complete source00/static actor/FE/predicate/macro contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B131-B133-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';60progressive speeches,18source00 actor0/Rafael. Complete speaker00 precedes a nonempty C-string body;only this source-bound prefix may containzero. FI3/FA5/FO9 use Lil captain2 context,not Rafael route macros. No dynamic selector/4100/2000;one2100 menu separate.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B131-B133-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one unlabeled share-exchange notice;original24310null actor before5473C/fallback208.228x48logical/228x64physical paper,conservative216px planning.No leading staging orinvented name/macro.')
    raise ValueError('Unknown B131/B133 consumer')
