"""Exact B203 three actors,21 progressive speeches and one original FE/FI notice."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='bceb685cd92f2ecf26746999fc7fc5e3c0a82b681f269d4e8a00044bb234360e'
BLOCKS={'8ab0080a8a5692f0be9062422923857b6023692feab449fba77e2ebe5f3be9cb', '6f61bede98df13d50e2d66d2d2b410433a05f08963200e7f6da1a1d932629d29'}
SELECTORS=frozenset({2,76,170})
DEPENDENCIES={'work\\analysis\\lil_B203_source_v6010\\all22_clean_current_complete_context.json': '642211240a2d842a5b618ccf57d625465ccabd4cf2ce4888f469d304ff91d51d', 'work/analysis/lil_B203_voices_v6011/current207_catalog_eight_voices_and_three_source_selectors.json': 'eebd6869c085091a78beadf3b68788a11dc67d4448b6a6cc2d942c9b75e0cfad', 'work/analysis/lil_B203_dispatches_v6014/all22_source_current_dispatches_FI_and9_control_leaves.json': '2d65663daa5a3d3d3c53d38c5412fdf889b963eb7f7fd3fd385b9da4347862bb', 'work/analysis/lil_B203_branches_v6016/original_relative_skip_operand_proof.json': '7e8b38def86d67630b2ee94396c867f4382475355be34ef4b5274fabb56b8ab7', 'work/analysis/lil_B203_entry_v6015/source_EV2_B203_action_dependency_and_native_getter_binding.json': 'e0e438466e7bd38588d13aef1211e8bc65d707c35ae22dc7495774ac03b5599a', 'work/analysis/lil_B203_controls_v6017/nine_exact_leaves_resource632E_6003_picture47xx_four_A000_pairs_and_end.json': '7e4d50a84bd8acc10eb7ac110a37ff2b6603133e8227ab620c7833a8312cc4eb', 'work/analysis/lil_B203_names_v6012/six_original_progressive_and_catalogue_name_consumers.json': 'e743ef242f6b4125298b4b7b41ba920e22ed83f42521cea1daafb7a90e98b5bb', 'work/analysis/lil_B203_source_names_v6013/three_exact_source_name_fields_voices_and_distinct_name_consumers.json': '1d3dcddc6368e3d6895ccdff4662aa401cc5f58afd2af19c478c258045a39ade', 'work/analysis/lil_B203_source_reconciliation_v6022/viewed_complete_source_exchange_names_item18_and_return_scope.json': 'bb0c8f6d68fe78ebb90c695aef6ff0c96ae83ca6cd3952a17690555a7f01b272', 'work/analysis/lil_B203_source_paths_v6020/one_actual_source_path_and_complete_command_intervals.json': '833cbb33147d008892b036ae5ccd45ed938a7c0b9592559ba37a4fe84a0b484d'}
CONTROL='work/analysis/lil_B203_dispatches_v6014/all22_source_current_dispatches_FI_and9_control_leaves.json'
TERMS='work/analysis/lil_B203_source_reconciliation_v6022/viewed_complete_source_exchange_names_item18_and_return_scope.json'
VOICES='work/analysis/lil_B203_voices_v6011/current207_catalog_eight_voices_and_three_source_selectors.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B203 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B203 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=44 or sum(c['source_selector']==254 for c in cases)!=2:raise ValueError('All22 source/current dispatch pairs required')
    if any(c['resolved_actor_ID'] is not None for c in cases if c['source_selector']==254):raise ValueError('FE must remain null actor')
    if any(c['source_selector'] not in SELECTORS or c['resolved_actor_ID']!=c['source_selector'] for c in cases if c['source_selector']!=254):raise ValueError('Three exact static actors required')
    if control['source_macro_counts']!={'FI':1,'FA':0,'FO':0}:raise ValueError('B203 has exactly one original FI macro')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['all22_source_objects_observed'] or not terms['all31_source_commands_and9_original_initializers_observed'] or terms['visual_review_pending']:raise ValueError('Complete viewed source context required')
    if terms['source_item18']['Japanese']!='漢方医の聖典' or terms['source_item18']['current_English']!="Herbalist's Bible":raise ValueError('Exact source item18 binding required;no title insertion')
    voices=json.loads(Path(VOICES).read_bytes())
    if {r['actor_ID']:r['original_voice_class'] for r in voices['fresh3_actor_names']['rows']}!={2:3,76:5,170:0}:raise ValueError('All three source actors/voices required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B203-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';21 original54020 speeches,Lil2 voice3/Mikhail76 voice5/MysteriousOldMan170 voice0,six distinct name consumers.31 original commands,no choices,predicates,relative sites or2000 pauses.One complete four-byte end/two tailzeros.Current bceb font,width,guard,pair phase and four rows unchanged.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B203-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';one original24310 null-actor then5473C notice:FI Charm+1. DefaultFI expandsLil3,FA/FO absent.228x48logical/228x64physical,conservative216px planning. Generated item-acquired notice is separate and unchanged. Actual English scene and complete effect semantics remain separate.')
    raise ValueError('Unknown B203 consumer')
