"""Freeze exact B186 conditional/role contracts and prepare current-font checks."""
from pathlib import Path
import json
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B186_native_tools_v5143')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B186_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    predicate='work/analysis/lil_B186_predicate700_v5138/all8_original700_predicate_RNG_ownership_cases.json'
    deps[predicate]=sha(Path(predicate).read_bytes())
    hashes=sorted({g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B186_profile.py');assert not profile.exists()
    text='''"""Exact B186 source/current conditionals, Owner/Cook roles and two text consumers."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({174,175})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B186 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B186 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=24 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All12 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B186 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B186-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';11 original54020 speeches,clean Owner174/Cook175 roles,four read-only name consumers,voice0. All24 commands:raw700 predicate540,six relative operands,three alternative A000s560/572/584,C200644,end646 and2 trailing zeros. Current V5122 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B186-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Sweets/Alexandria notice.228x48logical/228x64physical,conservative216px planning. Sweets is source sweet things,not a single commodity or all Treats. Earlier scene location/earned state not inferred;fresh native approval required.')
    raise ValueError('Unknown B186 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B185_layout_v1.py','dk4tool/dialogue/lil_B186_layout_v1.py',{'B185':'B186'})]
    rows.append(derive('scripts/plan_lil_B185_layout_v5098.py','scripts/plan_lil_B186_layout_v5144.py',{
        'B185':'B186','layout_v5098':'layout_v5144','Plan8':'Plan12','all8':'all12','len(reports)==8':'len(reports)==12','plans=8':'plans=12',
    }))
    rows.append(derive('scripts/verify_lil_B185_fonts_v5099.py','scripts/verify_lil_B186_fonts_v5145.py',{
        'B185':'B186','fonts_v5099':'fonts_v5145','voices_v5088':'voices_v5133',
        'len(cases)==len(qa_reports)==8 and macro_calls==64':'len(cases)==len(qa_reports)==12 and macro_calls==96',
        'blocks[185]':'blocks[186]','blocks[184]':'blocks[185]',
        '[164,165,254]':'[174,175,254]',
        '165 if selector==164 else 164':'175 if selector==174 else 174',
        "r['source_selector']==164":"r['source_selector']==174",
        "b'\\xa4Japanese','{SPEAKER:A4}Hello.'":"b'\\xaeJapanese','{SPEAKER:AE}Hello.'",
        'all8_progressive_FE_native_planes_and64_alignment_cases':'all12_progressive_FE_native_planes_and96_alignment_cases',
        'current_original_macro_alignment_calls=64,progressive_alignment_calls=56,FE_null_actor_alignment_calls=8':'current_original_macro_alignment_calls=96,progressive_alignment_calls=88,FE_null_actor_alignment_calls=8',
        'complete_progressive_planes=7':'complete_progressive_planes=11',
        'B185 current-font progressive/FE planes and64 native alignment cases':'B186 current-font progressive/FE planes and96 native alignment cases',
        'All8 current-font native planes,64 alignment cases and18 source-consumer negatives pass;one sheet needs visual review.':'All12 current-font native planes,96 alignment cases and18 source-consumer negatives pass;two sheets need visual review.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),tools=rows,dependencies=deps,
        inherited_predecessor_is_layout_v1_without_B185_exact_R16_boundary_exception=True,
        source_all24_commands_one700_predicate_six_relative_sites_three_alternative_effects_and_two_tailzeros_bound=True,
        no_prose_shortening_manual_break_metric_font_guard_or_global_weak_word_change=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared source-bound B186 profile,paragraph planner and96-alignment native verifier;no credit.')
