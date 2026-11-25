"""Exact B19720 progressive speeches and one common-tail null-actor FE."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS={'5fe938304f75e92152a41a117ed4cd5331533f00af497db7702fde75e5dc9f94', '821a2bfe04a016105d1cef1d4fefab9d635b94157d294dd65efd7f10653b8222'}
SELECTORS=frozenset({21,169})
DEPENDENCIES={'work\\analysis\\lil_B197_source_v5647\\all24_clean_current_complete_context_with_three_choice_labels.json': '2eeb91e447eda8299679fd0d27ea2f9a70c63d675725ed07f6571cc78863eab0', 'work/analysis/lil_B197_voices_v5648/current207_catalog_eight_voices_and_two_source_selectors.json': '46bfec3d919f6d7872ed0d0b022b50d7e57cc007fee3ce6b8de648b7375ae038', 'work/analysis/lil_B197_dispatches_v5649/all21_source_current_dispatches_no_macros_and11_control_leaves.json': '696fac8da83c82cfd77b0a6e840737563e96201719451ba5736e52a9f86f9bbe', 'work/analysis/lil_B197_branches_v5651/original_relative_skip_operand_proof.json': '7812a82e446a6c6ea87a84ec2b68f08e4d351b11dbc4f7138b30a0d7be719e5b', 'work/analysis/lil_B197_entry_v5650/source_EV2_B197_action_dependency_and_native_getter_binding.json': 'e1fd4ed660704c61040c70b5563caf6f41813eba11b57308dd417222faed2f0b', 'work/analysis/lil_B197_controls_v5654/eleven_exact_leaves_five_effect_two47xx_pairs_picture_resource_6003_and_end_cases.json': '765edbc1c59a001766ce9d911b9a5e57cb166272e249c3f97654151d57c0bd9c', 'work/analysis/lil_B197_names_v5652/four_original_progressive_and_catalogue_name_consumers.json': 'be4bfce646d3474a090702cf59cfb7db8c253562dd2fc3839b60d32444718b30', 'work/analysis/lil_B197_source_names_v5653/two_source_name_fields_four_current_consumers_and_literal_scope.json': '03949840da60778edbbec8c4d145477924c8e5076a352263ffad75d263c9fbe7', 'work\\analysis\\lil_B197_funds_v5660\\one_exact8500_source_price_one_unforced_and_five_offline_payment_boundaries.json': 'f1f887e79224b1b1866c716aecdcaf3045c5a88b95f1d4dc07bd6d4302e5c1e3', 'work\\analysis\\lil_B197_context_v5662\\clean_first_context_original_three_paths_gold_and_Charm.json': 'e1be98bafd16e948e21d07d3fbd42695ccf53976a4e41bc9935a36463647d6eb', 'work\\analysis\\lil_B197_source_paths_v5661\\three_actual_source_menu_paths_and_original_response_intervals.json': '36e27ea465a6aef30ec2085e246c12c3d5aad60168ba10379d9b4915909499ba'}
CONTROL='work/analysis/lil_B197_dispatches_v5649/all21_source_current_dispatches_no_macros_and11_control_leaves.json'
TERMS='work\\analysis\\lil_B197_context_v5662\\clean_first_context_original_three_paths_gold_and_Charm.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B197 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B197 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=42 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All21 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B197 has no source name macros')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['source_FE_R109_common_tail_observed_after_all_three_choices']:raise ValueError('Common-tail notice context required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B197-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';20 original54020 speeches,Ian21 voice1 and woman169 voice0,four name consumers.39 source commands/one2200/six relative sites/one end. No source macros. V5637 unchanged font,width,guard and pair phase.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B197-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C common-tail Ian Charm-plus-one notice,no FI.228x48logical/228x64physical,conservative216px planning. Actual Japanese paths bound;no English scene or effect-body claim.')
    raise ValueError('Unknown B197 consumer')
