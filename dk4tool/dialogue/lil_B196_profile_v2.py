"""Exact B196 runtime,source commands,actors and default-FI contracts."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS={'9936685c61c1adf55655cb1a121975baa99902f446ca0aa47761a09e317aeff1', '3736c69036bd8318af1311027c75aa7c60fdd9e8323e8dd600643a097f9137fd'}
SELECTORS=frozenset({2,6,19,20,25,173})
DEPENDENCIES={'work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json': '81472db4345a3aa4166138fd852419fdc7c8ff6590cd435abf78753e66632c05', 'work/analysis/lil_B196_voices_v5591/current207_catalog_eight_voices_and_six_source_selectors.json': '6f3fdbee3401af487fc231537b45f9cf9b1a72e02eee3ab7fd5db418b4c90af1', 'work/analysis/lil_B196_dispatches_v5592/all24_source_current_dispatches_FI1_and37_control_leaves.json': 'd5a81cc719e6a2c4f995354429f1596c997f951c9f5cfe7f7f4d51694d31f6c3', 'work/analysis/lil_B196_branches_v5595/original_relative_skip_operand_proof.json': '2e170d4185e631655e17e22374c5765fe73bbe35c5465519907239d87fca49f7', 'work/analysis/lil_B196_entry_v5593/source_EV2_B196_action_dependency_and_native_getter_binding.json': 'c52354d08f23f11766403feed3f17fe8879031ef69b5f4a2e1c929959c67ba36', 'work/analysis/lil_B196_controls_v5596/seven_unforced_predicates_six_picture_pairs_twenty_resource_cases_fourteen_opaque_effect_pairs.json': '7fee4f8862b8db4b6be6aed4912309318eb1db126bef84724da2dca71cbef18c', 'work/analysis/lil_B196_6003_ends_v5597/source6003_ten_boundary_cases_and_seventy_guarded_end_cases.json': '6a8dcf4be5bbb96ed83872d393453c68f665d4ff1d553d98582d0269473bb289', 'work/analysis/lil_B196_names_v5594/twelve_original_progressive_and_catalogue_name_consumers.json': '5efd238b39dcf54b545207ba734bee812184084a4bd83643d11486419a506bc2', 'work/analysis/lil_B196_source_names_v5598/six_source_name_fields_twelve_current_consumers_and_literal_scope.json': 'eaff3d2a873d2379ad36346df7ed19ee02d44bfe44f193b639efcec39d1faeae', 'work\\analysis\\lil_B196_funds_v5601b\\six_exact_source_prices_six_unforced_and_thirty_offline_payment_boundaries.json': '544cbfd8ddbf623a1cfd1c5bcab82b7c9bc12019bb6a15f2c13068351e2840b2', 'work\\analysis\\lil_B196_terms_v5602\\six_roles_gold_Charm_FI_and_six_prices_without_invented_item_identity.json': '354ca2815aa3f96de4604a36f89dc99fb132afcb8996795d1a2a0c7f21bc0e07'}
CONTROL='work/analysis/lil_B196_dispatches_v5592/all24_source_current_dispatches_FI1_and37_control_leaves.json'
TERMS='work\\analysis\\lil_B196_terms_v5602\\six_roles_gold_Charm_FI_and_six_prices_without_invented_item_identity.json'
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B196 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B196 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=48 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All24 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':1,'FA':0,'FO':0}:raise ValueError('B196 has exactly one source FI')
    terms=json.loads(Path(TERMS).read_bytes())
    if terms['current_source_FI_expansion']!='Lil' or terms['current_default_captain_ID']!=2:raise ValueError('Exact current default FI name/parity required')
    token=terms['native_FE_macro_pipelines'][1]
    if len(token['cases'])!=4 or any(bytes.fromhex(r['output_hex'])!=b'Lil' for r in token['cases']):raise ValueError('Original FI expansion differs')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B196-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';23 original54020 speeches,six original actor/voice bindings,twelve name consumers. Source119 commands/six menus/52 relative sites/seven predicates/seven ends. No font,width,guard,phase or custom-name claim. Current V5580 font and native guards.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B196-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C branch-specific FI Charm-plus-one notice. FI expands to current default Lil in four source alignments.228x48logical/228x64physical,conservative216px planning. No item-effect,custom-player-name or actual scene claim.')
    raise ValueError('Unknown B196 consumer')
