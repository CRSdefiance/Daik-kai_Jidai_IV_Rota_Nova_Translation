"""Exact three-Lady cooking-scene progressive/FE profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['cebc5f4c3641acc0fda8358f52dafaf8df45cb9e67188942f014dfb6ab8c0b12', 'e9f8ae7fa5d95fcf9f82bbd20b9c80f82642918a4dacfb6e0e024a86578408e2'])
SELECTORS=frozenset({166,167,168})
DEPENDENCIES={'work\\analysis\\lil_B193_source_v5447\\all15_clean_current_complete_context.json': 'd6335d5b09f79a890e09d4c002a2f2edcd34aa111b75b3160b3822ac19478b9a', 'work/analysis/lil_B193_dispatches_v5449/all15_source_current_dispatches_no_macros_and3_control_leaves.json': 'd9121c3d94d6e17261e7c6d19a6fde6eaf3a90e44d6e240f253d21cadc320855', 'work/analysis/lil_B193_voices_v5448/current207_catalog_eight_voices_and_three_source_selectors.json': 'e57772b3cd8fc86878be1c912084d2df539722e6b19fb4ecbe7f37de83b8b537', 'work/analysis/lil_B193_controls_v5451/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '670db30c48741374bf9e41529449323c968b80fe6e6c9e7227b92fc7cba8d140', 'work/analysis/lil_B193_entry_v5450/source_EV2_B193_action_dependency_and_native_getter_binding.json': '76d0af04267b4771157550136482c290edf855b244bde067656916b7199e949d', 'work\\analysis\\lil_B193_terms_v5453\\three_Ladies_Seoul_Chili_and_cooking_friendship_reconciliation.json': '5d8977f41ff70d4e797b34ad711049dec5e8d41fe365f3b08dfc8a3a91a32e63', 'work/analysis/lil_B193_names_v5452/six_original_progressive_and_catalogue_name_consumers.json': 'b78eb060c3d3c33a47226c99660f79cb1e3dbd1041b7a6bc917a762e461624dc'}
CONTROL='work/analysis/lil_B193_dispatches_v5449/all15_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B193 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B193 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=30 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All15 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B193 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B193-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';14 original54020 speeches,three distinct source Ladies166/167/168 voice0,six original read-only names. HexA6/A7/A8 exact.18 linear commands,A0008,C200660,end662,two source tailzeros. Current V5437 font/guards;fresh approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B193-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C prospective chili/Seoul notice.228x48logical/228x64physical,conservative216px planning. Chili29 and both Seoul aliases unchanged;source cooking and explicit friendship,not trade advice or earned fashion;fresh approval required.')
    raise ValueError('Unknown B193 consumer')
