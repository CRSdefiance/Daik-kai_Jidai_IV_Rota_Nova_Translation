"""Exact B194 source/current native profile,with default FI-to-Lil binding."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['3356a310a39843601093b18bd877f5ba56456347d33ef680003c3582abdc84cf', 'f38288f3975db43a6e60fa080952f76b00610aee6b4fabea6e8b19e90b06a767'])
SELECTORS=frozenset({6,117,156})
DEPENDENCIES={'work\\analysis\\lil_B194_source_v5489\\all11_clean_current_complete_context.json': '0b939d615c8ac681d01db9388f16c34a0f58589faa70a67a0d2529f35013f033', 'work/analysis/lil_B194_dispatches_v5491/all11_source_current_dispatches_one_FI_and6_control_leaves.json': '60c2a7ddfa4dffe4797d6f35f1aa42cf0d19b38dc2f4c55035c9c7d2044dc905', 'work/analysis/lil_B194_voices_v5490/current207_catalog_eight_voices_and_three_source_selectors.json': '392bfce392e9b753e73eabca6b1e25a0f1fbc963d700381af153431dc744095a', 'work/analysis/lil_B194_branches_v5493/original_relative_skip_operand_proof.json': 'ed215f329fcd221868a3f461b81e51837b755bd1d3900b092c4b814cd9f38b3f', 'work/analysis/lil_B194_entry_v5492/source_EV2_B194_action_dependency_and_native_getter_binding.json': 'cceb399256af43398d204c614715441e2afe34fe6713a902e9fa068017fe01ee', 'work/analysis/lil_B194_controls_v5495/one_unforced_predicate_resource42_two_C200_paths_and6_source_leaves.json': '039caa37daa8de5c18f09525bcf61689cc2eaff67b6dbe4cae57c856ad696d0a', 'work\\analysis\\lil_B194_terms_v5496\\Julio_Sailor_Port_Worker_Hangzhou_Sake_and_FI_title_reconciliation.json': '11d1d9680802acf73cd13308d54dfef9db876adc5265030e43feb220a5cf521b', 'work/analysis/lil_B194_names_v5494/six_original_progressive_and_catalogue_name_consumers.json': '24d4605ef7c3a259c88aa0a943918431f168444488cc5ef7c543f43468d9f1cc'}
CONTROL='work/analysis/lil_B194_dispatches_v5491/all11_source_current_dispatches_one_FI_and6_control_leaves.json'
TERMS='work\\analysis\\lil_B194_terms_v5496\\Julio_Sailor_Port_Worker_Hangzhou_Sake_and_FI_title_reconciliation.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B194 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B194 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=22 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All11 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':1,'FA':0,'FO':0}:raise ValueError('B194 has exactly one source FI')
    terms=json.loads(Path(TERMS).read_bytes())
    if terms['FI_default_expansion']!='Lil' or terms['FI_default_ASCII_bytes']!=3:raise ValueError('Exact current default FI name/parity required')
    if any(bytes.fromhex(r['output_hex'])!=b'Lil' for r in terms['original_default_captain_FI_four_alignment_cases']['cases']):raise ValueError('Original FI expansion differs')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B194-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';10 original54020 speeches,Julio6 voice5/PortWorker117 voice0/Sailor156 voice4,six original names with two owned Julio scratch paths. One FI expands to default Lil in four original alignments;Admiral title is source-explicit.21 commands,one conditional,four spans,resource42,two C200 and one end. Current V5478 font/guards. Custom name lengths and actual scene remain outside this proof.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B194-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C prospective Sake/Hangzhou notice.228x48logical/228x64physical,conservative216px planning. Sake37 and one Hangzhou alias unchanged;no earned fashion or earlier location claim;fresh approval required.')
    raise ValueError('Unknown B194 consumer')
