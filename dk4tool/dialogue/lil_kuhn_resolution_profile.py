"""Exact eleven-block Kuhn-resolution ordinary andFE planning profiles."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Kuhn_Resolution_controls_v2925/source_bound358_preambles_FE_and_original_conditional_predicates.json')
PROOF_SHA='ff35c179fbb27278530caeb8de943622a7b4ad7039b6232be20785fde01f2c5e'
FE_RULE=Path('work/analysis/lil_Seville_FE_v2713/current_FE_macro_font_and_typed_paper_proof.json')
FE_RULE_SHA='eec677a7a5558d2dfddba929389c30a45c8eff94a158121ecae30d6a9870a677'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['0b7a74bf573887e0c90998952efe52e412083763df7f7cd7dbb414110a846aec', '1c774c9484a3a46776e0ecab52b542287947c5cb0c0de2e3876ab1abd2de2694', '1ce9f27926f8b6e7fae2e25c52b63eb574c5466c5e0f1f45b3ef7e5a04dd0bc1', '1e144765fd4a1bb14d580da97b676133431f1335a3af841d1b4b2b60579981ca', '26474a4b8744f3a70f92ecddf858649af0e033bdfade43f8dc0ec91d935517dc', '303238f78f6b31fe574cd395d577e1283d6884a0c6f1503a2bcffbd1c66472dc', '347dfc6c3f6268775c3bedc01ee4d42308ab476d321d9c4a9379ed9edcd83742', '45356ff9322aa3d609700a608d00655a2db12bdc6ee61fc699476183383bcab7', '54f566eb5f315b15cf324a4ffd82e586d558940ece40b005bd49437dee6413a8', '55ef5ca6697600ea782a59c67c7028faeb47497c89142745c9589826eea3303d', '6c71800ec88bcbd06898fc40be9ad79eb9f72f3372ff98cb85b0fb14e4383f8b', '6de43663ef7f6ca1c1ee27e428b56e23fbb2ecc4ef6baae4a5aa20214ca3e80d', '72da376e023f51df850f24001d2bbddf4d3e9eedbf79945b57a7c8b5ae9ea76c', '82b480991d0974e7fbca30e0ce2f202b0cb49a454f2da1832488ecccd74e4f5a', '8c41da907704b9510e19619138303c9db375433c54233a24a6f2b2cb26f7ff6e', '8e33aebec67dd99d22e1b49cbe424802825b4ebaf12abf8a4399224b96ef9b4c', 'a9e3e313936a00490ab8534f4875ebf85b4f876994685e5209f585e8358ee7f5', 'ab18b0883fcc6aae62e24161910b70ebd20a36c7777aff526cbf9e905067f280', 'b12079f55c40913e926ec38401b6c2d1f6fdc95e31cca5dde063bc98718797dd', 'be61ff3338848ab862333f818d5e8f8c89dfba5437ab9c4c092b57baadf9c9ec', 'd5ec61fa5c9768f9922e3b45608ab9f5d81075bd11a5686ff2134b0cfdcaa983', 'd5fde1dc9de2ca3c587ba72ff127dae05e2c2c1228ab73121a2e44b0f71a2b5e'])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Kuhn-resolution requires exact reviewed eleven-block source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(FE_RULE.read_bytes())!=FE_RULE_SHA:
        raise ValueError('Kuhn-resolution source-control or FE rule changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));fe=json.loads(FE_RULE.read_text(encoding='utf-8'))
    expected={str(k):k for k in [1,2,3,6,7,9,11,12,14,16,19,20,21,28,40,43,56,151]}
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all358_complete_preambles_and716_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=716 or proof['ordinary_native_actor_selectors']!=expected
        or len(proof['current_original_predicate_cases'])!=84
        or not proof['all16_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['FE_FI_substitution_original_dispatcher_output_bound']
        or fe['ARM9_sha256']!=ARM9_SHA or not fe['one_native_page_consumes_complete_target']
        or not fe['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']):
        raise ValueError('Complete ordinary and inherited FE contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-kuhn-resolution-progressive-runtime-bound-v1',leading_speaker_bytes=frozenset(expected.values()),
            metrics_source=base.metrics_source+'; exactB57/58/59/60/61/62/63/64/65/66/121complete preambles andordinary54020selectors. No individual new nameplate/activation claim;current fonts/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-kuhn-resolution-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exactsource FEbeforefallback208and5473C,withsame-ARM inherited null-actor/228x48mode1paper rule. Conservative216pxplanning;fresh completeFEfont/pagination required.')
    raise ValueError('Unknown Kuhn-resolution presentation consumer')
