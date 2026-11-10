"""Exact B189 four-actor source/current progressive and null-actor FE profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['5630898beb2dd2865adedb8ea022236a8cfbc6f822d29e30078d396e8fcf5942', 'd6f4bd35ae90a44ad8f0f4ef4dbdf692effb07f77c03048fa378ee7f095ec1ad'])
SELECTORS=frozenset({82,104,113,147})
DEPENDENCIES={'work\\analysis\\lil_B189_source_v5273b\\all17_clean_current_complete_context.json': '74a37d68595bac5dd505721101cdb8bb08965aec46209ca0cfec649c82995297', 'work/analysis/lil_B189_dispatches_v5275b/all17_source_current_dispatches_no_macros_and3_control_leaves.json': 'daca64964478058679285a9768f1954f786ffd0769122d6cb2aa9d5350e73875', 'work/analysis/lil_B189_voices_v5274b/current207_catalog_eight_voices_and_four_source_selectors.json': '731e635525b7c87dbf6e4334544411dee0e6016c564059ac6bdecdac5dada5d0', 'work/analysis/lil_B189_controls_v5277b/A000_C200_single_end_and_no_relative_or_predicate_contract.json': '422dbe93154f6dacf536013c32da92a52698a0f33a7437a810bd3e6fca2b2ac3', 'work/analysis/lil_B189_entry_v5276b/source_EV2_B189_action_dependency_and_native_getter_binding.json': 'c9457a6fa0c6a78e7acf41a61a797f8b5a80508495d4842084f3cdb09ee4336a', 'work\\analysis\\lil_B189_terms_v5279\\four_roles_Hamburg_ceramics_UI_China_and_two_pair_irony_reconciliation.json': 'd89d1257480a6db8425f3090036ba455296a1dd29df348767945e976a8b814fe', 'work/analysis/lil_B189_names_v5278b/eight_original_progressive_and_catalogue_name_consumers.json': 'e8c2047250014e0a7697ad1669715d1bb89d93e5909a0c44b2f0ffbc63c2f55d'}
CONTROL='work/analysis/lil_B189_dispatches_v5275b/all17_source_current_dispatches_no_macros_and3_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B189 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B189 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=34 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All17 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B189 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B189-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';16 original54020 speeches,clean Shopkeeper82/Trader104/PortWorker113/Guildmaster147,all voice0,eight read-only name consumers. Hex selectors52/68/71/93 are decimal82/104/113/147.20 linear commands,A0008 raw00a0ffff012a05a1,C200764,end766,two tailzeros,no predicates/relative sites. Current V5263 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B189-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Ceramics/Hamburg notice.228x48logical/228x64physical,conservative216px planning. Ceramics is source collective;commodity42 legacy UI China stays unchanged without Chinese-origin claim. No earned boom or earlier location claim;fresh native approval required.')
    raise ValueError('Unknown B189 consumer')
