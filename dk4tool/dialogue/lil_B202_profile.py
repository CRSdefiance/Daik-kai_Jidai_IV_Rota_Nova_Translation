"""Exact B202 four-speaker,zero-macro progressive scene;no FE consumer."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='bceb685cd92f2ecf26746999fc7fc5e3c0a82b681f269d4e8a00044bb234360e'
BLOCKS={'1ffb8e51e9fcae8b9bd12bad90ddfde0bb9730f88b56ee2295cae8a31df4064e', 'e5d57ad6cf6886878b47249d5b340be444e6f8bb2a86a3e117f47f8ddf58e4aa'}
SELECTORS=frozenset({2,18,147,157})
DEPENDENCIES={'work\\analysis\\lil_B202_source_v5959\\all19_clean_current_complete_context.json': '20ef996b64aa385952559cb9db97309969ace9a9ed4c336354f78fe0abca6b06', 'work/analysis/lil_B202_voices_v5960/current207_catalog_eight_voices_and_four_source_selectors.json': '00fffe45a31686f0542c1d36192c00d4b6a4fc60bc5fbd9188a36b5d2bebdbd1', 'work/analysis/lil_B202_dispatches_v5963/all19_source_current_dispatches_no_macros_and7_control_leaves.json': '2cb0b58bc6094284ddaf0269f2447a2ea90a0624fe9d814a29cc7cb4b0a3b56b', 'work/analysis/lil_B202_branches_v5965/original_relative_skip_operand_proof.json': 'ba69e329e22971761bedec44ffc4828dc94b6ce2c79df7380c5ab74c9d54c211', 'work/analysis/lil_B202_entry_v5964/source_EV2_B202_action_dependency_and_native_getter_binding.json': 'a5cc35a96699d1996f411ca24092f010932e5ca91828962052096b19dd7b52b2', 'work/analysis/lil_B202_controls_v5966/seven_exact_leaves632A_picture47xx_two_A000_pairs_and_guarded_end.json': 'bc2a6c2746fda6a7776894bb38d0bf53222a9118691bb29708e63f47cea0dc6f', 'work/analysis/lil_B202_names_v5961/eight_original_progressive_and_catalogue_name_consumers.json': '5a8f91230b1f6690e4fbae153a6283accade73d8900a4828973cb0020e3676ed', 'work/analysis/lil_B202_source_names_v5962/four_exact_source_name_fields_voices_and_original_Sailor_alias.json': '53512c1b89c52d6ffc03c124036e62dafe85c64beb773907a86202796e85867f', 'work/analysis/lil_B202_source_reconciliation_v5970/viewed_complete_source_exchange_names_title_and_return_scope.json': '0e4d9cb675307df637f5f3cecf141266e7304dbb1525cf8a5c4abb9523ff7899', 'work/analysis/lil_B202_source_paths_v5969/one_actual_source_path_and_complete_command_intervals.json': '5861fa84df8511e04c9b994dec1a02edcb69002fb23af8a7673b9ccb73aa8893'}
CONTROL='work/analysis/lil_B202_dispatches_v5963/all19_source_current_dispatches_no_macros_and7_control_leaves.json'
TERMS='work/analysis/lil_B202_source_reconciliation_v5970/viewed_complete_source_exchange_names_title_and_return_scope.json'
VOICES='work/analysis/lil_B202_voices_v5960/current207_catalog_eight_voices_and_four_source_selectors.json'
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B202 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B202 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=38 or any(c['source_selector'] not in SELECTORS or c['resolved_actor_ID']!=c['source_selector'] for c in cases):raise ValueError('All19 source/current progressive dispatch pairs required')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B202 has no source runtime name macro')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['all19_source_speeches_observed'] or not terms['all26_source_commands_and9_original_initializers_observed'] or terms['visual_review_pending']:raise ValueError('Complete viewed source context required')
    if terms['source_item14']['Japanese']!='ガラスの製法辞典' or terms['source_item14']['current_English']!='Glassmaking Guide':raise ValueError('Exact source spoken-title/item binding required')
    voices=json.loads(Path(VOICES).read_bytes())
    if {r['actor_ID']:r['original_voice_class'] for r in voices['fresh4_actor_names']['rows']}!={2:3,18:0,147:0,157:4}:raise ValueError('All four source actors/voices required')
    if consumer!='progressive':raise ValueError('B202 has no FE or alternate display consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B202-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';19 original54020 speeches,Lil2 voice3/Charles18 voice0/Guildmaster147 voice0/Sailor157 voice4.Original Sailor alias differs from catalogue Retainer.26 source commands,no FE,choices,predicates,relative sites or macros.One complete end/two tailzeros.Native width,guard,pair phase,four rows and current bceb font unchanged.')
