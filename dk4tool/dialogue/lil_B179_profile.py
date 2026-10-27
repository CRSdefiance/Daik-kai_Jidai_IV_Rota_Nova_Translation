"""B179 exact controls:thirteen progressive speeches,one impersonal FE,A000 and end only."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['735463ff68a796a53b230db59c993f7a20b0e93a4649f722b5fdd036933bf3b7', 'c430628d8ee957e7b54dee2d7bf7020a7e5d22e7c0a6727c8de24fe51fdf1b3b'])
SELECTORS=frozenset({92,96,152})
DEPENDENCIES={'work\\analysis\\lil_B179_source_v4708\\all14_clean_current_complete_context.json': '31ab075a45ccfaf453d9cfb0d350760ed1e074879f165f53626a19fc03922db5', 'work\\analysis\\lil_B179_dispatches_v4710\\all14_source_current_dispatches_no_macros_and2_control_leaves.json': '2dc1dffbf7241ef603bfa98c26082a47e5e7a8a7256809c96f65750fe339127a', 'work/analysis/lil_B179_voices_v4709/current3_static_names_voices_and207_catalog_rebind.json': '04cedbd5d6eb2a8ea086a8ea3d999210cdad6157a8f9e41de095abf237b93123', 'work/analysis/lil_B179_branches_v4711/original_relative_skip_operand_proof.json': '001339671f1c3c0dc6583df49da6f288af1cc95a98b864ff028a3553f764f6d8', 'work/analysis/lil_B179_entry_v4712/source_EV2_B179_action_dependency_and_native_getter_binding.json': '58c09ad6be61e706eb65c3280b4aedff0dce4a0e206e3963c1a4e752968351f6', 'work/analysis/lil_B179_controls_v4714/one_A000_no_C200_single_end_and2_source_leaves.json': '0db593cd93085893f9868f31e6dd5232e42db80441e19e25f17d27cb43c880a0', 'work\\analysis\\lil_B179_terms_v4718\\Barkeep_Patron_Sailor_Sao_Jorge_Wine_and_prospective_fashion_reconciliation.json': 'd141856b80bde470b992f682919c3f2a4b19e1f5146aba2d3407109a54779ad6', 'work/analysis/lil_B179_names_v4713b/six_original_Barkeep_Patron_Retainer_name_consumers.json': '8ae8147dda0b6a688aeecb1112918738557ea7eb17445ecef066a2eaa31f1699'}
CONTROL='work\\analysis\\lil_B179_dispatches_v4710\\all14_source_current_dispatches_no_macros_and2_control_leaves.json'

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B179 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B179 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=28 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All fourteen source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE notice must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B179 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B179-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';thirteen original54020 speeches,Barkeep92/Patron96/Sailor152. Catalog Retainer152 is a distinct getter and does not override dialogue identity. Zero FI/FA/FO. Exact16 commands,opaque A0008,single end508;no C200. Six read-only name paths;no resource,presentation,predicate,relative or typed object. No natural eligibility or earned fashion-state claim.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B179-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one impersonal prospective Sao Jorge wine-fashion notice,original24310null actor then5473C before fallback.228x48logical/228x64physical paper;conservative216px planning. No invented speaker/name label;complete-page native approval remains separate. The separate Japanese city alias reference lead stays open.')
    raise ValueError('Unknown B179 consumer')
