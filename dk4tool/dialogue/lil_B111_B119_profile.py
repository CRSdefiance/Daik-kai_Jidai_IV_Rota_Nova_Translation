"""Exact nine-block Lil prose/FE and five variable actor-style selectors."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['0666dc7f1f87875447bd1c52948e3b6b955c56bbf7144dc92cd2e128c3383974', '08ddaafafa273e9aabe985fae95cc09d67e6b59d66f22e42f8f034d517046bef', '20c2ed569e0a29305e3e77848dc7ae210accd0bd4a2801989bdda77ba779ce06', '25abe225b77e71c382c5ed668bb5ea5fd77580b175036af46d42f040454ef489', '372693e04efde8c099fb00b60f603ee0744bcfe7ee3044097d319024a63350a5', '627c5c072bea410e03c62265174677aa2cb927c1f74d7bf264ba11baea44e417', '62d61d7d1584ee7a9f631b03ad686e2a6aef5ae0d11d28c8e207466cd9cc6582', '6dec745bc312823d5f77807190f950266ae8932861b4707d650e1b695861945a', '974a6203b0fbe5df8294be58f5d0707cbb3afba7b3bec065615f6071d9b1394d', 'a1aa8c579ce116057f39ec27b804955d2442876cfd2ad844932036f825927467', 'a954f647e99a2cbade3bcc2c19b9d7e6595d93f72ce6a7797aeaa1dfa0e83647', 'b1d7d6b6b4dfe1638ea2edd2acb4dc959c2945b81e9dcef8d7ae91ea8c53c942', 'b6a745502263170e60137ff9601c63fd486b389225d4198f23174e4748a17683', 'ba4f9ee3280bf010ae48a3f8b580458a476209eda4cd9b58c8b52249df3dbe20', 'cacd59241a23400087a2acc9dded30cd230c37aa1a1299ffd10a0192b3d9d575', 'de525cfe82b75c4e8de17ff4a9525ff765517add0777d9e26990f0296b0f707d', 'e0cd51b4bbf2f3910eb364a7a22fa4124f0c0da16e67e2199c48739d5244e30c', 'ecd9b40aa0ab07b26d08802d3551fe8b5d90d7c50256de420fc44a731ce6f90f'])
SELECTORS=frozenset([2, 4, 9, 14, 19, 20, 104, 137, 163, 170, 179, 198, 207, 208, 209, 214, 215, 220])
DEPENDENCIES={'work\\analysis\\lil_B111_B119_source_v3217b\\complete150_reachable_Lil_clean_current_context.json': 'f169b928e7e812bf5c37555259045207cd777429422cfb231b051b2a9362eb1b', 'work\\analysis\\lil_B111_B119_controls_v3219\\all150_source_current_dispatch_variable_styles_predicates_and_query.json': '3a9e1744e23e1d505a2c26560864facb5592657346c4dea044cf12d3a58bf131', 'work\\analysis\\lil_B111_B119_voices_v3218\\current207_catalog_eight_voices_and_CF_D0_D1_D6_D7_DC_roles.json': '107b9f86c9fc0e776a5ae7d8fd227db32ef1243e56a5acd8cc0928020cd37477', 'work\\analysis\\lil_B111_B119_terms_v3220\\clean_current_items_and_native_actor_role_reconciliation.json': '85d5cda6d5b397f3567bed8f78aa16c7df51000e4078776b33f5c42da5948d5a', 'work\\analysis\\lil_B115_tail_classification_v3216\\source_return0_graph_and_canonical_Maria_copy_classification.json': '46228f24fa16a51476d574a177ea791655cfa479960118f3953a57e5d597e8ba', 'work\\analysis\\lil_B111_B119_controls_v3219\\current_registered_name_catalog_binding.json': '25d6bad5b2c74620e6ac5bb67a3a248128e99e9db4c0062457842d2116453240'}
CONTROL=Path('work/analysis/lil_B111_B119_controls_v3219/all150_source_current_dispatch_variable_styles_predicates_and_query.json')
VOICES=Path('work/analysis/lil_B111_B119_voices_v3218/current207_catalog_eight_voices_and_CF_D0_D1_D6_D7_DC_roles.json')
CLASSIFICATION=Path('work/analysis/lil_B115_tail_classification_v3216/source_return0_graph_and_canonical_Maria_copy_classification.json')
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('B111-B119 requires exact nine clean/current blocks andruntime')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B111-B119 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'))
    voices=json.loads(VOICES.read_text(encoding='utf-8'))
    classification=json.loads(CLASSIFICATION.read_text(encoding='utf-8'))
    if (len(control['speech_and_stored_alternative_dispatch_cases'])!=300
        or len(control['whole_original4100_command_cases'])!=12
        or len(control['all207_actor_style_source_pointer_cases']['cases'])!=2484
        or len(control['current_original_predicate_cases'])!=16
        or len(control['original_event_queries'])!=1
        or control['original_event_queries'][0]['event']!=319
        or not control['one_FE_before_dynamic_fallback208_uses5473C_and24310_null_actor']
        or not voices['all_six_dynamic_selectors_bind_actual_current_original_roles_without_assignment']
        or len(voices['catalog']['rows'])!=207
        or not classification['all12_original_VM_return0_cases_stop_before_cursor_advance']):
        raise ValueError('Complete variable-role/source dispatch/predicate/query/copy contract required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B111-B119-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';exact9blocks/116speech/34actor-stylebodies. VirtualD0/D1/D6/D7/DCprefixmatchesreal4100header andmustnotbestoredinbody;preserve48slots/aliases and20byteheaders. CFcaptain/currentunassignedrolefallback boundwithoutassignment. Unowned32Maria copy excludedfromformatting andpreservedbyteforbyte.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B111-B119-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';oneFE24000goldnotice;originalnullactor24310then5473Cbeforefallback208. Calibrated228x48logical/228x64physical mode1paper,conservative216pxplanning. No inventedname,macro orleadingblankline.')
    raise ValueError('Unknown B111-B119 consumer')
