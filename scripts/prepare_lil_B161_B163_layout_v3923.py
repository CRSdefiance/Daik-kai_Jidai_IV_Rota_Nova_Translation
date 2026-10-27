"""Create the exact three-block progressive profile and complete45-plane native proof tools."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B161_B163_layout_tools_v3923')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B161_B163_editorial_manuscript_v1.json');source=read(doc['source_context']);terms=read(doc['actor_terminology_reconciliation']);deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation']};deps[terms['source_owned_name_consumer_proof']]=terms['source_owned_name_consumer_proof_sha256'];hashes={g[k] for g in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']};P=Path('dk4tool/dialogue/lil_B161_B163_profile.py');assert not P.exists();text='''"""Exact B161-B163 source binding:45 progressive speeches/six original static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,9,11,15,20,116})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B161-B163 clean/current source and runtime required')
    if consumer!='progressive':raise ValueError('Only original B161-B163 progressive consumer is source-bound')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B161-B163-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';45 original54020 speeches/six static actors,FI1,32 spans,29 leaves,eight predicates,two C200,one A000,one two-byte pause andfour ends;Jam Ludwyan progressive/Jam Jack Ludwyan full-name consumers bound. No natural eligibility claim.')
''';compile(text,str(P),'exec');P.write_text(text,encoding='utf-8',newline='\n');pairs=[]
    pairs.append(derive('dk4tool/dialogue/lil_B160_layout_v2.py','dk4tool/dialogue/lil_B161_B163_layout_v1.py',{"expected={'lil-B160-progressive-runtime-bound-v1':frozenset({2,9,14,15,116,151})}":"expected={'lil-B161-B163-progressive-runtime-bound-v1':frozenset({2,9,11,15,20,116})}",'source-bound B160 profile':'source-bound B161-B163 profile','def _word(value):':'''PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('strawberry','jam'),('jam','jack'),('jack','ludwyan'),('live','large'),('life','is'),('is','short'),('kindhearted','jam'),('picked','her'),('her','up'),('lying','around'),('looking','lonely'),('all','right'),('the','head'),('get','back'),('a','will'),('a','way'),("it's",'all'),('all','good'),('hoping','for'),('what','a'),('out','to'),('to','sea'),('all','weird')})

def _word(value):'''}))
    pairs.append(derive('scripts/plan_lil_B160_layout_v3882.py','scripts/plan_lil_B161_B163_layout_v3924.py',{'lil_B160_layout_v2':'lil_B161_B163_layout_v1','lil_B160_profile':'lil_B161_B163_profile','lil_B160_layout_v3882':'lil_B161_B163_layout_v3924','lil_B160_editorial_manuscript_v2':'lil_B161_B163_editorial_manuscript_v1','lil_B160_editorial_manuscript_v3':'lil_B161_B163_editorial_manuscript_v2','all22_paragraph':'all45_paragraph','len(reports)==22':'len(reports)==45','plans=22':'plans=45','Plan22':'Plan45'}))
    pairs.append(derive('scripts/verify_lil_B160_fonts_v3883.py','scripts/verify_lil_B161_B163_fonts_v3925.py',{'lil_B160_profile':'lil_B161_B163_profile','lil_B160_layout_v2':'lil_B161_B163_layout_v1','lil_B160_fonts_v3883':'lil_B161_B163_fonts_v3925','lil_B160_editorial_manuscript_v3':'lil_B161_B163_editorial_manuscript_v2','len(cases)==22 and len(qa_reports)==22 and macro_calls==176':'len(cases)==45 and len(qa_reports)==45 and macro_calls==360','blocks[160]':'blocks[163]','blocks[159]':'blocks[164]','[2,9,14,15,116,151]':'[2,9,11,15,20,116]','all22':'all45','current_original_macro_alignment_calls=176':'current_original_macro_alignment_calls=360','actual_selected_B160_IDs':'actual_selected_B161_B163_IDs','Current176 macro calls,22 progressive planes and22 complete paragraph QA.':'Current360 macro calls,45 progressive planes and45 complete paragraph QA.','22 complete progressive planes,176 macro cases,22 QA plans and21 source-consumer negatives pass;three sheets':'45 complete progressive planes,360 macro cases,45 QA plans and21 source-consumer negatives pass;six sheets'}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_three_block_profile_formatter_and_native_tools.json',dict(profile=str(P),profile_sha256=sha(P.read_bytes()),dependencies=deps,tools=pairs,source_blocks=[161,162,163],all45_progressive_six_static_actors_FI1_bound=True,source_Jam_short_full_intro_and_original_progressive_label_distinguished=True,no_global_profile_or_shared_guard_change=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
