"""Exact B191 two-actor mixed-predicate progressive/FE formatting profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
BLOCKS=frozenset(['6fdd9664b7119bdea920f4d317b9e8dfe90e10975385632266bcf2f36a563889', 'bdde69a51ec6e45f38f249b01a408548ae06d1cde638c8d8cb531ef2d49e67a3'])
SELECTORS=frozenset({86,154})
DEPENDENCIES={'work\\analysis\\lil_B191_source_v5356\\all13_clean_current_complete_context.json': 'f5ed44108b65bb1cb6a978d8056217f3cc0d97a80c6e002d381dfcdad43d1110', 'work/analysis/lil_B191_dispatches_v5358/all13_source_current_dispatches_no_macros_and9_control_leaves.json': '87a3b8997ab12e5b8998be9cf429ed4d04f0c2ee9cab4ffe32249e4cd2c328a0', 'work/analysis/lil_B191_voices_v5357/current207_catalog_eight_voices_and_two_source_selectors.json': '0db9d0e2b13da6d48ae36a742aec82862ecf96e96aa0d46d3f7c2865618c90ef', 'work/analysis/lil_B191_branches_v5360/original_relative_skip_operand_proof.json': '8971d6ef9f346624b29df3742d56431518004b490bd16a24dc1638cd14ddc10a', 'work/analysis/lil_B191_entry_v5359/source_EV2_B191_action_dependency_and_native_getter_binding.json': '416c53a36cff43281fd68a0857b6d4a775d52296fbf16bb0c51716f40889e8eb', 'work/analysis/lil_B191_controls_v5363/three_predicates_four_A000_C200_sixteen_relative_sites_and_single_end.json': '34c5396248687cb2ae88f6267af2008c46563ba5b791b3a75f32f01104df960b', 'work\\analysis\\lil_B191_terms_v5364b\\Square_Shopkeeper_Sailor_Calicut_Dyes_and_persuasive_claims.json': '5651c42ff14fb798fb2a9176fa2b54a9725a0918e01acdd4d37c889c77ef06ea', 'work/analysis/lil_B191_names_v5361/four_original_progressive_and_catalogue_name_consumers.json': 'ff89b1bba623287aada21c805689c33cc82766070df6f6f95e8887f16e5d324d', 'work/analysis/lil_B191_predicates_v5362/all24_original_mixed_predicate_RNG_ownership_cases.json': '613c6de1a27986f967bd224b816512184e5a780dacbc45ef2aafa7c7b395c5be'}
CONTROL='work/analysis/lil_B191_dispatches_v5358/all13_source_current_dispatches_no_macros_and9_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B191 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B191 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=26 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All13 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B191 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B191-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';12 original54020 speeches,Shopkeeper86 voice0/Sailor154 voice4,distinct full Retainer154,four original read-only names. Hex56/9A equal decimal86/154.38 commands,three500/700/500 predicates at8/28/76,16relatives,four alternatives and no-effect paths,C200728,end730,two tailzeros. Current V5346 font/guards;fresh approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B191-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C:prospective Dyes/Calicut notice.228x48logical/228x64physical,conservative216px planning. Category14 Dyes/two Calicut aliases unchanged. No single pigment,earned fashion,earlier location or guaranteed profit inferred;fresh approval required.')
    raise ValueError('Unknown B191 consumer')
