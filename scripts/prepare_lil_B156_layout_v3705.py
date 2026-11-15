"""Bind B156's ten original static actors to the unchanged native layout geometry."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B156_layout_tools_v3705')
def derive(a,b,changes):
    a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
    for x in changes:assert x in t,x
    t=re.sub('|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],t)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8',newline='\n')
    return dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()))
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B156_editorial_manuscript_v1.json');packet=read(doc['source_context']);deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation']};hashes={g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']}
    p=Path('dk4tool/dialogue/lil_B156_profile.py');assert not p.exists();t='''"""Exact B156 original progressive consumers and ten static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,9,14,20,21,92,96,152,164,165})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B156 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B156 has no FE or dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B156-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';76 original54020 speeches/ten static actors including Ian15 and Retainer98;sourceFI2,three predicates,12 relative sites,14resource sites andtwo endwords bound. No natural event eligibility claim.')
''';compile(t,str(p),'exec');p.write_text(t,encoding='utf-8',newline='\n')
    pairs=[derive('dk4tool/dialogue/lil_B155_layout_v4.py','dk4tool/dialogue/lil_B156_layout_v1.py',{'lil-B155-progressive-runtime-bound-v1': 'lil-B156-progressive-runtime-bound-v1','frozenset({2,6,9,15,20})':'frozenset({2,9,14,20,21,92,96,152,164,165})','source-bound B155 profile':'source-bound B156 profile','def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('ian','dukov'),('give','it'),('it','a'),('a','rest'),('give','me'),('leave','a'),('let','you'),('you','go'),('right','up'),('close','to'),('saving','my'),('my','life'),('on','my'),('my','own'),('take','me'),('me','aboard'),('come','with'),('turn-on','')})\n\ndef _word(value):"})]
    pairs.append(derive('scripts/plan_lil_B155_layout_v3675.py','scripts/plan_lil_B156_layout_v3706.py',{'lil_B155_layout_v4':'lil_B156_layout_v1','lil_B155_profile':'lil_B156_profile','lil_B155_layout_v3675':'lil_B156_layout_v3706','lil_B155_editorial_manuscript_v6':'lil_B156_editorial_manuscript_v1','lil_B155_editorial_manuscript_v7':'lil_B156_editorial_manuscript_v2','all50_paragraph':'all76_paragraph','len(reports)==50':'len(reports)==76','plans=50':'plans=76','Plan50':'Plan76'}))
    pairs.append(derive('scripts/verify_lil_B155_fonts_v3670.py','scripts/verify_lil_B156_fonts_v3707.py',{'lil_B155_profile':'lil_B156_profile','lil_B155_layout_v3':'lil_B156_layout_v1','lil_B155_fonts_v3670':'lil_B156_fonts_v3707','lil_B155_editorial_manuscript_v3':'lil_B156_editorial_manuscript_v2','len(cases)==50 and len(qa_reports)==50 and macro_calls==400':'len(cases)==76 and len(qa_reports)==76 and macro_calls==608','blocks[155]':'blocks[156]','blocks[154]':'blocks[155]','selectors=[2,6,9,15,20]':'selectors=[2,9,14,20,21,92,96,152,164,165]','len(negatives)==19':'len(negatives)==29','all50':'all76','current_original_macro_alignment_calls=400':'current_original_macro_alignment_calls=608','actual_selected_B155_IDs':'actual_selected_B156_IDs','Current400 macro calls,50 progressive planes and50 complete paragraph QA.':'Current608 macro calls,76 progressive planes and76 complete paragraph QA.','50 complete progressive planes,400 macro cases,50 QA plans and19 source-consumer negatives pass;seven sheets need visual review.':'76 complete progressive planes,608 macro cases,76 QA plans and29 source-consumer negatives pass;ten sheets need visual review.'}))
    old=Path('work/analysis/lil_B156_author_v3704/all50_contextual_revision_or_retention_receipt.json');receipt=read(old);assert receipt['complete_speech_objects']==76 and receipt['decisions']=={'revise':41,'retain-wording':35}
    ROOT.mkdir(parents=True);save(ROOT/'all76_author_receipt_filename_clarification.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),explanation='Frozen author producer retained a historical all50 filename. Its actual asserted contents are76 speech objects,41 revisions and35 justified retentions;no data or credit changed.',receipt=receipt));save(ROOT/'exact_profile_formatter_and_tools_provenance.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),dependencies=deps,tools=pairs,no_global_profile_or_shared_guard_change=True,source_ten_static_actors_and_FI2_bound=True,no_FE_consumer_allowed=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Exact B156 profile, planner and native tools created; no credit.')
