"""Exact fourteen-block crew/item speech and seven FE consumers."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path('work/analysis/lil_Crew_Items_controls_v3114/source_bound198_preambles_FE_and_original_conditional_predicates.json')
PROOF_SHA='dce2efd98c16ae5e46b53f044e820d5539faed9c1c7d669c67c9a247d737ef11'
TERMS=Path('work/analysis/lil_Crew_Items_terms_v3116/clean_current_ten_items_stat_UI_and_native_actor_terms.json')
TERMS_SHA='2869cc27aca05670b98a7e1be26bc8045315eeb700cb85209e91a7b66b5530bd'
ARM9_SHA='d9415c1e0eb18c9eec9b76329f3dedb724a1a754a4829be103c6b958f927b9aa'
BLOCKS=frozenset(['0060bdbbe2416e3e36869e45c52b0ac043346e64d719e0f260998af4df648a46', '042fbc688c723a556fd045ae19d60b42bd9a57addd764828a04d91828bd782fe', '067c76d79f647107f6b1ed3cef027535e7e93289d87ef011c5e83d7b7566402f', '068acee726366e542f7cae4cbab1119b0f9bedf9443582d55c410b52c8169493', '1346e467aa47365697f460b283545973ae90885cb77a7656638745b8e1f25d7d', '136d91f56d9046fa9ec3078127c3691a1ee5ae21a2cd81eba60db385f9f6d335', '1443f7e230c18cfed36a2ade9938a5f8bff1a76ca7747ea0e40010e440e98a6c', '35d8f6fcfc25bfc1e13f9e526f96193e5b06df438eb6dc322e4a609f03dadd2c', '3a06aca26fbecbf61fd8d6c2a36cfb8f879c22d763df349bd57efbda52107e3f', '4104a6f0c2bb5b9c2ff34a8a56a5fb1202edd42adeaa614b5fe53e915afb1255', '58972d7156c8262126d12d40d0997a03ff7b7afc138786324ed29673dc9aab6c', '5b942f7cdf810efc7dde990451e88d2522feca7b3c445b7f51882f5086577bcf', '5db96ff5a54a2248fe9e84348fff33fd6240fc041e4b2f125518f9326d08cc73', '68a171727b618095500d04db1ac20fb682e87e9d81490d195193c3b4846e6535', '6ea20bc5a4f326b4229b741f8b60b589871325e5a06aaac5137ba5988fa744d7', '76400fe440851f8ccb61a09b01c239450b7beec0f02155ce54610984bbe7a78e', '8415b10a7a4f1380e372e155b14cad0b9204db4f25f7f1db0c614d4266650b3e', '847758277107e4ccb9effa050ad3ec360eb222985b7be2667dc29dce99faf319', '987c1f86a4e4f201c7816b2ab6118367f6f78d3db0acf571c1461712644bb4e6', '988567c6c5f4eb845d407a54c129849be5a9ba75b934d0d852ce13928e62355f', '9a4f69afbff516bb04d271acc678e2f833c38cb08fb048c9a3f460cf6231e909', 'a2584ae0e3b829aafab4eaa8faf46338f742457a1a9f5d21de994da7f9a6ee98', 'a83fc3c2b02f7b1032ba745e420741fc4504e742dc408822f08ad99c75cb553e', 'b5c1520e9955076351972ed4357991cafc5c9a852c16d7c621031f9ea7855d80', 'b792fa322e02b557ff2dc95db4e8ccfd8ba112063015cbc0fea230b8d9d0d040', 'cc10f95a1e638d19a9f0549ea8d1fb6c24a9fd7accd193ec70dbb4029f7bec55', 'ec635b581f4661d11874c665ccae51a121e454f7a41bf338a240c9eb6ac9e6ba', 'f07398848040c381836e4c1ada90f394441fc030fa499e2dc7ce5a913ffeeb08'])
SELECTORS=frozenset([2, 4, 6, 7, 12, 14, 15, 16, 18, 20, 22, 108, 114, 152, 188])

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Crew/Items requires exact fourteen reviewed clean/current source blocks/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(TERMS.read_bytes())!=TERMS_SHA:
        raise ValueError('Crew/Items source-control or item/stat/native name terminology changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));terms=json.loads(TERMS.read_text(encoding='utf-8'))
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all198_complete_preambles_and396_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=396 or proof['ordinary_native_actor_selectors']!={str(k):k for k in SELECTORS}
        or proof['current_original_predicate_cases'] or proof['original_event_queries']
        or not proof['all7_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['all7_FE_source_stat_notices_and_unlabeled_monkey_calls_preserved_by_original_dispatcher']
        or not terms['all10_clean_current_pointer_strings_equal_registered_names']
        or terms['approved_stat_terms']['Luck']['English']!='Luck'
        or terms['approved_stat_terms']['Spirit']['English']!='Spirit'):
        raise ValueError('Complete ordinary/seven FE/item/stat contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-crew-items-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+'; exact14blocks/198complete preambles/15 ordinary54020 selectors. No new individual nameplate or earned item/stat claim; current fonts/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-crew-items-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exact7FEbeforefallback208and5473C,original24310nullactor,fourstat notices/twoFI andthreeunlabeledmonkeycalls. Inherited228x48mode1paper,conservative216pxplanning;complete freshfont/pagination required.')
    raise ValueError('Unknown Crew/Items presentation consumer')
