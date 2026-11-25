"""Exact B195 cheese-specialty source/current native profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['1ba8b8828012be6a178836b7fa3baf4ac9eae0f263b0b4bffcaaf084ec9ecfb1', '698fbd1b016dcc5eb2f7168bde5158977fddb90ee9d1c93ad4a150f06fe66a3f'])
SELECTORS=frozenset({92,103,119})
DEPENDENCIES={'work\\analysis\\lil_B195_source_v5541\\all20_clean_current_complete_context.json': 'ab6e02a10c2cba772f92f4fe815987d6a709d256ef63d9cd0c803aa70cdc0033', 'work/analysis/lil_B195_dispatches_v5543/all20_source_current_dispatches_no_macros_and3_control_leaves.json': '7fcac682d09809ec9e304737a935501bba2010f62227a62c8e5938aa0ae60f29', 'work/analysis/lil_B195_voices_v5542/current207_catalog_eight_voices_and_three_source_selectors.json': 'd99a98aa194978da85b3dfe7cdc399b731f52554da2d64572f449acdc20073cd', 'work/analysis/lil_B195_controls_v5545/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '5bc96d1883aab5e25d0ce9fc850e7ed324803d0ef3922cfe1297c1a5869e25d6', 'work/analysis/lil_B195_entry_v5544/source_EV2_B195_action_dependency_and_native_getter_binding.json': 'e0952ac4b0c2fea2f6d40ee55c611826500bd9357f3b607092732059401ca0e2', 'work\\analysis\\lil_B195_terms_v5547\\three_roles_both_Veracruz_aliases_Cheese8_and_unnamed_specialty_reconciliation.json': '3dcaccf7f9a62ce94e024cb97b425461768228080be18c42eb0e6668b6c4055c', 'work/analysis/lil_B195_names_v5546/six_original_progressive_and_catalogue_name_consumers.json': '58a6dab28bd8d0df0a70707b30b63f690db1279049776d43078299e87f253351'}
CONTROL='work/analysis/lil_B195_dispatches_v5543/all20_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B195 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B195 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=40 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All20 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B195 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B195-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';19 original54020 speeches,Barkeep92/Patron103/PortWorker119 voice0,six original readonly names.23 linear commands,A0008,C200704,end706,two source tailzeros. Current V5531 font/guards;fresh approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B195-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C prospective Cheese/Veracruz notice.228x48logical/228x64physical,conservative216px planning. Cheese8 and both Veracruz aliases unchanged;unnamed house specialty and character popularity prediction,not narrator fact or earned fashion;fresh approval required.')
    raise ValueError('Unknown B195 consumer')
