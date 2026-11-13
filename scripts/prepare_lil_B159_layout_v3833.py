"""Create exact B159 progressive-only profile, automatic phrase layout and complete native proof tools."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B159_layout_tools_v3833')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B159_editorial_manuscript_v1.json');source=read(doc['source_context']);terms=read(doc['actor_terminology_reconciliation']);deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation']};deps[terms['source_owned_name_consumer_proof']]=terms['source_owned_name_consumer_proof_sha256'];hashes={g[k] for g in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']};p=Path('dk4tool/dialogue/lil_B159_profile.py');assert not p.exists()
    text='''"""Exact B159 source binding:41 progressive speeches/five original static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,9,14,20,22})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B159 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B159 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B159-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';41 original54020 speeches/five static actors, FI4,24 spans,23 leaves,one A000 andtwo ends;Samwell Khan original progressive name consumer separately bound. No natural eligibility claim.')
''';compile(text,str(p),'exec');p.write_text(text,encoding='utf-8',newline='\n');pairs=[]
    pairs.append(derive('dk4tool/dialogue/lil_B156_layout_v4.py','dk4tool/dialogue/lil_B159_layout_v1.py',{"expected={'lil-B156-progressive-runtime-bound-v1':frozenset({2,9,14,20,21,92,96,152,164,165})}":"expected={'lil-B159-progressive-runtime-bound-v1':frozenset({2,9,14,20,22})}",'source-bound B156 profile':'source-bound B159 profile','def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('roasted','whole'),('step','right'),('right','up'),('bighearted','like'),('knock','you'),('you','flat'),('round','face'),('put','yourself'),('yourself','in'),('my','shoes'),('put','up'),('welcome','aboard'),('every','day')})\n\ndef _word(value):"}))
    pairs.append(derive('scripts/plan_lil_B157_layout_v3753.py','scripts/plan_lil_B159_layout_v3834.py',{'lil_B157_layout_v1':'lil_B159_layout_v1','lil_B157_profile':'lil_B159_profile','lil_B157_layout_v3753':'lil_B159_layout_v3834','lil_B157_editorial_manuscript_v1':'lil_B159_editorial_manuscript_v1','lil_B157_editorial_manuscript_v2':'lil_B159_editorial_manuscript_v2','all75_paragraph':'all41_paragraph','len(reports)==75':'len(reports)==41','plans=75':'plans=41','Plan75':'Plan41'}))
    pairs.append(derive('scripts/verify_lil_B156_fonts_v3707.py','scripts/verify_lil_B159_fonts_v3835.py',{'lil_B156_profile':'lil_B159_profile','lil_B156_layout_v1':'lil_B159_layout_v1','lil_B156_fonts_v3707':'lil_B159_fonts_v3835','lil_B156_editorial_manuscript_v2':'lil_B159_editorial_manuscript_v2','len(cases)==76 and len(qa_reports)==76 and macro_calls==608':'len(cases)==41 and len(qa_reports)==41 and macro_calls==328','blocks[156]':'blocks[159]','blocks[155]':'blocks[158]','[2,9,14,20,21,92,96,152,164,165]':'[2,9,14,20,22]','len(negatives)==29':'len(negatives)==19','all76':'all41','current_original_macro_alignment_calls=608':'current_original_macro_alignment_calls=328','actual_selected_B156_IDs':'actual_selected_B159_IDs','Current608 macro calls,76 progressive planes and76 complete paragraph QA.':'Current328 macro calls,41 progressive planes and41 complete paragraph QA.','76 complete progressive planes,608 macro cases,76 QA plans and29 source-consumer negatives pass;ten sheets':'41 complete progressive planes,328 macro cases,41 QA plans and19 source-consumer negatives pass;six sheets'}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_source_profile_formatter_and_progressive_tools.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),dependencies=deps,tools=pairs,all41_progressive_five_static_actors_FI4_bound=True,source_Samwell_Khan_progressive_label_distinct_from_full_catalogue=True,no_global_profile_or_shared_guard_change=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Exact B159 progressive profile and automatic layout/native tools prepared. No credit.')
