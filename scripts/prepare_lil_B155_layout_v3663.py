"""Derive exact B155/five-actor layout,with automatic phrase flow andunchanged native metrics."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B155_layout_tools_v3663')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B155_editorial_manuscript_v1.json');packet=read(doc['source_context']);deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation']};hashes={g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']};p=Path('dk4tool/dialogue/lil_B155_profile.py');assert not p.exists();text='''"""Exact B155 original progressive consumers andfive static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,6,9,15,20})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B155 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B155 has no FE or dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B155-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';50 original54020 speeches/five static actors includingAngelo0F;sourceFI5/FA1,sevenpredicates,29relative sites,sixresource sites andtwoendwords bound. No natural event eligibility claim.')
''';compile(text,str(p),'exec');p.write_text(text,encoding='utf-8',newline='\n');a=Path('dk4tool/dialogue/lil_B152_B154_layout_v4.py');b=Path('dk4tool/dialogue/lil_B155_layout_v1.py');assert not b.exists();t=a.read_text(encoding='utf-8');old="expected={'lil-B152-B154-progressive-runtime-bound-v1':frozenset({2,9,14,17,20,92,115,148})}";assert old in t;t=t.replace(old,"expected={'lil-B155-progressive-runtime-bound-v1':frozenset({2,6,9,15,20})}").replace('source-bound B152-B154 profile','source-bound B155 profile');needle='def _word(value):';assert needle in t;t=t.replace(needle,"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('small','fry'),('rude','queen'),('no','queen'),('butt','out'),('run','along'),('someone','like'),('like','you'),('of','line'),('camille','overijssel'),('angelo','puccini'),('cute','boys'),('too','nice'),('your','own'),('own','good'),('eye','for'),('for','people'),('a','read'),('read','on'),('on','him'),('little','lady'),('trade','routes'),('contract','fees'),('big','powers'),('big','return'),('tidy','fortune'),('room','to'),('to','grow'),('time','to'),('to','waste'),('putting','you'),('you','to')})\n\ndef _word(value):");compile(t,str(b),'exec');b.write_text(t,encoding='utf-8',newline='\n');pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x in changes:assert x in t,x
        pattern='|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True));t=re.sub(pattern,lambda m:changes[m.group(0)],t);compile(t,str(b),'exec');b.write_text(t,encoding='utf-8',newline='\n');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('scripts/plan_lil_B152_B154_layout_v3627.py','scripts/plan_lil_B155_layout_v3664.py',{'lil_B152_B154_layout_v1':'lil_B155_layout_v1','lil_B152_B154_profile':'lil_B155_profile','lil_B152_B154_layout_v3627':'lil_B155_layout_v3664','lil_B152_B154_editorial_manuscript_v1':'lil_B155_editorial_manuscript_v1','lil_B152_B154_editorial_manuscript_v2':'lil_B155_editorial_manuscript_v2','all59_paragraph':'all50_paragraph','len(reports)==59':'len(reports)==50','plans=59':'plans=50','Plan59':'Plan50'})
    make('scripts/verify_lil_B152_B154_fonts_v3628.py','scripts/verify_lil_B155_fonts_v3665.py',{'lil_B152_B154_profile':'lil_B155_profile','lil_B152_B154_layout_v1':'lil_B155_layout_v1','lil_B152_B154_fonts_v3628':'lil_B155_fonts_v3665','lil_B152_B154_editorial_manuscript_v2':'lil_B155_editorial_manuscript_v2','len(cases)==59 and len(qa_reports)==59 and macro_calls==472':'len(cases)==50 and len(qa_reports)==50 and macro_calls==400','blocks[152]':'blocks[155]','blocks[151]':'blocks[154]','selectors=[2,9,14,17,20,92,115,148]':'selectors=[2,6,9,15,20]','len(negatives)==25':'len(negatives)==19','all59':'all50','current_original_macro_alignment_calls=472':'current_original_macro_alignment_calls=400','actual_selected_B152_B154_IDs':'actual_selected_B155_IDs','Current472 macro calls,59 progressive planes and59 complete paragraph QA.':'Current400 macro calls,50 progressive planes and50 complete paragraph QA.','59 complete progressive planes,472 macro cases,59 QA plans and25 source-consumer negatives pass;eight sheets need visual review.':'50 complete progressive planes,400 macro cases,50 QA plans and19 source-consumer negatives pass;seven sheets need visual review.'})
    ROOT.mkdir(parents=True);save(ROOT/'exact_profile_formatter_and_tools_provenance.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),previous_formatter=str(a),previous_formatter_sha256=sha(a.read_bytes()),formatter=str(b),formatter_sha256=sha(b.read_bytes()),dependencies=deps,tools=pairs,no_global_profile_or_shared_guard_change=True,source_five_static_actors_and_FI5_FA1_bound=True,no_FE_consumer_allowed=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('B155 exact-source/five-actor profile,automatic planner andnative font tools created. No credit.')
