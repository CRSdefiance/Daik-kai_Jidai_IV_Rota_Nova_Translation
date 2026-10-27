"""Create an exact B158 typed profile and automatic layout/native proof successors."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B158_layout_tools_v3793')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B158_editorial_manuscript_v1.json');source=read(doc['source_context']);deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation']};hashes={g[k] for g in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']};p=Path('dk4tool/dialogue/lil_B158_profile.py');assert not p.exists()
    text='''"""Exact B158 source binding:15 progressive and4 original null-actor FE panels."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,7,9,14})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B158 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B158-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';15 original54020 speeches/four actors, approved Cristina07, FI1,24 spans and22 source leaves. No natural event eligibility claim.')
    if consumer=='FE-paper':return replace(base,name='lil-B158-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';four original null-actor5473C FE patron/cheering/applause panels with embedded labels;216px conservative plan, separate228x48 logical/228x64 physical painter and complete input/pagination proof required.')
    raise ValueError('Unknown B158 consumer')
''';compile(text,str(p),'exec');p.write_text(text,encoding='utf-8',newline='\n');pairs=[]
    pairs.append(derive('dk4tool/dialogue/lil_B157_layout_v2.py','dk4tool/dialogue/lil_B158_layout_v1.py',{"expected={'lil-B157-progressive-runtime-bound-v1':frozenset({2,9,14,19,20,105,142}),'lil-B157-FE-runtime-bound-v1':frozenset({254})}":"expected={'lil-B158-progressive-runtime-bound-v1':frozenset({2,7,9,14}),'lil-B158-FE-runtime-bound-v1':frozenset({254})}",'source-bound B157 profile':'source-bound B158 profile','def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('patron','1'),('patron','2'),('patrons','1'),('1','&'),('&','2'),('excuse','me'),('quite','a'),('a','bit'),('couldn\'t','help'),('even','more')})\n\ndef _word(value):"}))
    pairs.append(derive('scripts/plan_lil_B157_layout_v3753.py','scripts/plan_lil_B158_layout_v3794.py',{'lil_B157_layout_v1':'lil_B158_layout_v1','lil_B157_profile':'lil_B158_profile','lil_B157_layout_v3753':'lil_B158_layout_v3794','lil_B157_editorial_manuscript_v1':'lil_B158_editorial_manuscript_v1','lil_B157_editorial_manuscript_v2':'lil_B158_editorial_manuscript_v2','all75_paragraph':'all19_paragraph','len(reports)==75':'len(reports)==19','plans=75':'plans=19','Plan75':'Plan19'}))
    pairs.append(derive('scripts/verify_lil_B157_fonts_v3754.py','scripts/verify_lil_B158_fonts_v3795.py',{'lil_B157_profile':'lil_B158_profile','lil_B157_layout_v1':'lil_B158_layout_v1','lil_B157_fonts_v3754':'lil_B158_fonts_v3795','lil_B157_editorial_manuscript_v2':'lil_B158_editorial_manuscript_v2','lil_B157_B160_source_v3744':'lil_B158_B160_source_v3786','len(cases)==75 and len(reports)==75 and macros==600':'len(cases)==19 and len(reports)==19 and macros==152','blocks[157]':'blocks[158]','blocks[156]':'blocks[157]','[2,9,14,19,20,105,142]':'[2,7,9,14]','len(negatives)==24':'len(negatives)==18','all75_native_planes600_macros_and24_consumer_negatives':'all19_native_planes152_macros_and18_consumer_negatives','all75_full_QA_reports':'all19_full_QA_reports','progressive_planes=73,FE_planes=2':'progressive_planes=15,FE_planes=4','all75_complete_native_independent_planes_pass':'all19_complete_native_independent_planes_pass','source13_andFE_are_executable_selectors_not_visible_prose':'source07_andFE_are_executable_selectors_not_visible_prose','actual_selected_B157_IDs':'actual_selected_B158_IDs','73 progressive planes,two FE planes,600 macro cases':'15 progressive planes,four FE planes,152 macro cases','75 complete native planes,600 macro alignments,24 consumer negatives pass. Ten sheets':'19 complete native planes,152 macro alignments,18 consumer negatives pass. Three sheets',"('Carlo / FE recollection' if fe else row['speaker'])":"('Anonymous patrons / applause' if fe else row['speaker'])"}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_source_profile_formatter_and_typed_FE_tools.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),dependencies=deps,tools=pairs,fifteen_progressive_four_FE_consumers_and_FI1_bound=True,source_FE_embedded_labels_and_applause_complete228x48_logical228x64_physical_plane_required=True,no_global_profile_or_shared_guard_change=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Exact B158 profile and automatic layout/native tools prepared;15 progressive/4 FE. No credit.')
