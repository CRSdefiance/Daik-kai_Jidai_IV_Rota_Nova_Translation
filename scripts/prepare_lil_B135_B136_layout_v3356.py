"""Scope the established progressive planner to35 source-bound speeches."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B135_B136_layout_tools_v3356');profile=Path('dk4tool/dialogue/lil_B135_B136_profile.py');formatter=Path('dk4tool/dialogue/lil_B135_B136_layout_v1.py');planner=Path('scripts/plan_lil_B135_B136_layout_v3356b.py');assert not any(p.exists() for p in [root,profile,formatter,planner])
    from scripts.author_lil_B135_B136_v3355 import SOURCE,CONTROL,VOICE,TERMS,BRANCH
    catalog=Path('work/analysis/lil_B135_B136_controls_v3347/current_registered_name_catalog_binding.json');source=read(SOURCE);deps={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,VOICE,TERMS,BRANCH,catalog]};hashes=sorted({b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    text='''"""Exact B135/B136 progressive speakers;no FE,source00,choices orpauses."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_REPLACE
BLOCKS=frozenset(BLOCK_REPLACE)
SELECTORS=frozenset({2,9,14,36,47,96})
DEPENDENCIES=DEP_REPLACE
CONTROL=Path(CONTROL_REPLACE)
VOICE=Path(VOICE_REPLACE)
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('B135/B136 exact clean/current block andruntime required')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B135/B136 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'));voice=json.loads(VOICE.read_text(encoding='utf-8'))
    if consumer!='progressive' or len(control['speech_dispatch_cases'])!=70 or len(control['current_original_predicate_cases'])!=1 or control['original_event_queries'] or control['source_macro_counts']!={'FI':0,'FA':0,'FO':1} or len(voice['fresh_six_actor_names']['rows'])!=6:raise ValueError('Complete static actors,predicate andLil-context macro contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B135-B136-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';35 progressive speeches,six static actors. FI3/FA5/FO9 use Lil captain2. No FE/source00/dynamic/4100/2000/2100 inthis source scope.')
'''
    for a,b in [('ARM_REPLACE',repr(source['current_ARM9_sha256'])),('BLOCK_REPLACE',repr(hashes)),('DEP_REPLACE',repr(deps)),('CONTROL_REPLACE',repr(str(CONTROL))),('VOICE_REPLACE',repr(str(VOICE)))]:text=text.replace(a,b)
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8')
    old=Path('dk4tool/dialogue/lil_B122_B127_layout_v2.py');text=old.read_text(encoding='utf-8').replace('B122-B127','B135-B136');text=text.replace('frozenset({2,6,9,20,26,92,95,151})','frozenset({2,9,14,36,47,96})')
    text=text.replace(",'lil-B135-B136-FE-runtime-bound-v1':frozenset({254})",'')
    anchor='PROTECTED_BOUNDARIES=frozenset({';assert anchor in text;text=text.replace(anchor,anchor+"('goddess','temptation'),('cheese','tart'),('upper','stone'),('lower','stone'),('stone','tablets'),")
    compile(text,str(formatter),'exec');formatter.write_text(text,encoding='utf-8')
    oldplan=Path('scripts/prepare_lil_B122_B127_layout_v3281.py');text=oldplan.read_text(encoding='utf-8');a=text.index('SOURCE=Path(');z=text.index('INPUTS=[',a)
    text=text[:a]+f'SOURCE=Path({str(SOURCE)!r})\nPROFILE=Path({str(profile)!r})\nFORMATTER=Path({str(formatter)!r})\nOLD=Path({str(old)!r})\n'+text[z:]
    changes={'lil_B122_B127_layout_v3281':'lil_B135_B136_layout_v3356b',"INPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v2.json'),Path('translations/lil_B122_B127_choice_manuscript_v1.json')]":"INPUTS=[Path('translations/lil_B135_B136_editorial_manuscript_v1.json')]","OUTPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v4.json'),Path('translations/lil_B122_B127_choice_manuscript_v3.json')]":"OUTPUTS=[Path('translations/lil_B135_B136_editorial_manuscript_v2.json')]",'dk4tool.dialogue.lil_B122_B127_profile_v2':'dk4tool.dialogue.lil_B135_B136_profile','dk4tool.dialogue.lil_B122_B127_layout_v2':'dk4tool.dialogue.lil_B135_B136_layout_v1','all159_paragraph_and_label_layout_QA':'all35_paragraph_layout_QA','len(reports)==159':'len(reports)==35','plans=159':'plans=35'}
    for a,b in changes.items():assert a in text,a;text=text.replace(a,b)
    compile(text,str(planner),'exec');planner.write_text(text,encoding='utf-8');root.mkdir(parents=True)
    save(root/'provenance.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),formatter=str(formatter),formatter_sha256=sha(formatter.read_bytes()),previous_formatter=str(old),previous_formatter_sha256=sha(old.read_bytes()),planner=str(planner),planner_sha256=sha(planner.read_bytes()),global_codec_encoder_QA_and_previous_profiles_unchanged=True,no_source00_exception_in_this_profile=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
