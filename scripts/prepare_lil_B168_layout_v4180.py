"""Bind B168's progressive/FE consumers to unchanged native metrics and automatic wrapping."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B168_layout_tools_v4180')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B168_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes={b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']}
    p=Path('dk4tool/dialogue/lil_B168_profile.py');assert not p.exists()
    text='''"""Exact B168 source consumers:51 progressive speeches and three null-actor FE notices."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,6,9,20,76,87,165,166})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B168 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B168-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';51 original54020 speeches/eight static actors,FI7/FA1/FO1,twelve relative sites,three predicates and sixteen source leaves;printable57/4C/A5/A6 are mapped actors. No natural eligibility claim.')
    if consumer=='FE-paper':return replace(base,name='lil-B168-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';three original null-actor5473C naturalist/nonofficer/Deck/item-information/X notices;216px conservative plan,separate228x48 logical/228x64 physical painter and complete input/pagination proof required.')
    raise ValueError('Unknown B168 consumer')
'''
    compile(text,str(p),'exec');p.write_text(text,encoding='utf-8',newline='\n')
    boundaries=[('old','mikhail'),('this','town'),('tropical','tree'),('grind','it'),('it','up'),('rabbit','droppings'),('bust','size'),('put','all'),('all','that'),('that','knowledge'),('good','use'),('come','aboard'),("ship's",'officer'),('shipboard','work'),('item','information'),('detailed','item'),('the','deck'),('fountain','of'),('of','knowledge'),('made','up'),('up','my'),('my','mind'),('dirty','old'),('old','man'),('how','come'),('young','lady'),('you','worry'),('bear','with'),('press','x')]
    tools=[derive('dk4tool/dialogue/lil_B167_layout_v6.py','dk4tool/dialogue/lil_B168_layout_v1.py',{
        "expected={'lil-B167-progressive-runtime-bound-v1':frozenset({2,4,13,23,109})}":"expected={'lil-B168-progressive-runtime-bound-v1':frozenset({2,6,9,20,76,87,165,166}),'lil-B168-FE-runtime-bound-v1':frozenset({254})}",
        'source-bound B167 profile':'source-bound B168 profile',
        'def _word(value):':'PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset('+repr(boundaries)+')\n\ndef _word(value):'
    })]
    tools.append(derive('scripts/plan_lil_B158_layout_v3797.py','scripts/plan_lil_B168_layout_v4181.py',{
        'lil_B158_layout_v2':'lil_B168_layout_v1','lil_B158_profile':'lil_B168_profile','lil_B158_layout_v3797':'lil_B168_layout_v4181',
        'lil_B158_editorial_manuscript_v2':'lil_B168_editorial_manuscript_v1','lil_B158_editorial_manuscript_v3':'lil_B168_editorial_manuscript_v2',
        'all19_paragraph':'all54_paragraph','len(reports)==19':'len(reports)==54','plans=19':'plans=54','Plan19':'Plan54'}))
    tools.append(derive('scripts/verify_lil_B158_fonts_v3795.py','scripts/verify_lil_B168_fonts_v4182.py',{
        '15 progressive planes,four FE planes,152 macro cases':'51 progressive planes,three FE planes,432 macro cases',
        'lil_B158_profile':'lil_B168_profile','lil_B158_layout_v1':'lil_B168_layout_v1',
        'lil_B158_fonts_v3795':'lil_B168_fonts_v4182','lil_B158_editorial_manuscript_v2':'lil_B168_editorial_manuscript_v2',
        'lil_B158_B160_source_v3786':'lil_B168_voices_v4170',
        'len(cases)==19 and len(reports)==19 and macros==152':'len(cases)==54 and len(reports)==54 and macros==432',
        'blocks[158]':'blocks[168]','blocks[157]':'blocks[167]','[2,7,9,14]':'[2,6,9,20,76,87,165,166]',
        'len(negatives)==18':'len(negatives)==26','all19_native_planes152_macros_and18_consumer_negatives':'all54_native_planes432_macros_and26_consumer_negatives',
        'all19_full_QA_reports':'all54_full_QA_reports','progressive_planes=15,FE_planes=4':'progressive_planes=51,FE_planes=3',
        'all19_complete_native_independent_planes_pass':'all54_complete_native_independent_planes_pass',
        'source07_andFE_are_executable_selectors_not_visible_prose':'source57_4C_A5_A6_andFE_are_executable_selectors_not_visible_prose',
        'actual_selected_B158_IDs':'actual_selected_B168_IDs',
        '19 complete native planes,152 macro alignments,18 consumer negatives pass. Three sheets':'54 complete native planes,432 macro alignments,26 consumer negatives pass. Seven sheets',
        "'Anonymous patrons / applause'":"'System notice'"}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_source_profile_formatter_and_typed_FE_tools.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),dependencies=deps,tools=tools,source_51_progressive_three_FE_consumers_and_FI7_FA1_FO1_bound=True,complete_FE228x48_logical228x64_physical_and_progressive216x64_planes_required=True,no_global_profile_shared_guard_metric_orwaiver_change=True,no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B168 exact progressive/FE profile and automatic layout/native tools prepared;no credit.')
