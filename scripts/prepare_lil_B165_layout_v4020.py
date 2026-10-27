"""Bind the exact24-speech/three-actor source andcreate complete native layout tools."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B165_layout_tools_v4020')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B165_editorial_manuscript_v1.json');source=read(doc['source_context']);terms=read(doc['actor_terminology_reconciliation']);deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation']};deps[terms['source_owned_name_consumer_proof']]=terms['source_owned_name_consumer_proof_sha256'];hashes={g[k] for g in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']};p=Path('dk4tool/dialogue/lil_B165_profile.py');assert not p.exists();text='''"""Exact B165 source binding:24 progressive speeches,three static actors,FI3."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,6,9})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B165 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B165 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B165-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';24 original54020 speeches,three static actors including Julio06,FI3,20spans,five Camille membership sites,12opaque leaves,resource6329,oneA000 andone end. Firstsolo remark differs fromoptional three-line Camille exchange. No natural eligibility ornewrelationship claim.')
''';compile(text,str(p),'exec');p.write_text(text,encoding='utf-8',newline='\n');pairs=[]
    pairs.append(derive('dk4tool/dialogue/lil_B164_layout_v2.py','dk4tool/dialogue/lil_B165_layout_v1.py',{"expected={'lil-B164-progressive-runtime-bound-v1':frozenset({2,9,13})}":"expected={'lil-B165-progressive-runtime-bound-v1':frozenset({2,6,9})}",'source-bound B164 profile':'source-bound B165 profile','def _word(value):':'''PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('julio','erneco'),('good','drink'),('decent','drink'),('good','long'),('long','life'),('young','people'),('some','manners'),('formerly','active'),('active','navigator'),('not','again'),('show','me'),('to','the'),('the','ship'),('give','in'),('calm','down')})

def _word(value):'''}))
    pairs.append(derive('scripts/plan_lil_B164_layout_v3982.py','scripts/plan_lil_B165_layout_v4021.py',{'lil_B164_layout_v2':'lil_B165_layout_v1','lil_B164_profile':'lil_B165_profile','lil_B164_layout_v3982':'lil_B165_layout_v4021','lil_B164_editorial_manuscript_v7':'lil_B165_editorial_manuscript_v1','lil_B164_editorial_manuscript_v8':'lil_B165_editorial_manuscript_v2','all47_paragraph':'all24_paragraph','len(reports)==47':'len(reports)==24','plans=47':'plans=24','Plan47':'Plan24'}))
    pairs.append(derive('scripts/verify_lil_B164_fonts_v3983.py','scripts/verify_lil_B165_fonts_v4022.py',{'lil_B164_profile':'lil_B165_profile','lil_B164_layout_v2':'lil_B165_layout_v1','lil_B164_fonts_v3983':'lil_B165_fonts_v4022','lil_B164_editorial_manuscript_v8':'lil_B165_editorial_manuscript_v2','len(cases)==47 and len(qa_reports)==47 and macro_calls==376':'len(cases)==24 and len(qa_reports)==24 and macro_calls==192','blocks[164]':'blocks[165]','blocks[165]':'blocks[166]','[2,9,13]':'[2,6,9]','all47':'all24','current_original_macro_alignment_calls=376':'current_original_macro_alignment_calls=192','actual_selected_B164_IDs':'actual_selected_B165_IDs','no_FE_objects_and_typed_choice_requires_separate_consumer_proof=True':'no_FE_or_typed_choice_objects_in_this_source_scope=True','Current376 macro calls,47 progressive planes and47 complete paragraph QA.':'Current192 macro calls,24 progressive planes and24 complete paragraph QA.','47 complete progressive planes,376 macro cases,47 QA plans and15 source-consumer negatives pass;six sheets':'24 complete progressive planes,192 macro cases,24 QA plans and15 source-consumer negatives pass;three sheets'}));ROOT.mkdir(parents=True);save(ROOT/'exact_B165_profile_formatter_and_native_tools.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),dependencies=deps,tools=pairs,source_scope=dict(speeches=24,actors=[2,6,9],FI=3,relative_sites=20,Camille_queries=5,opaque_leaves=12),no_global_profile_guard_change=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Exact B165 profile,24-paragraph planner andcomplete192-case native font tools created.')
