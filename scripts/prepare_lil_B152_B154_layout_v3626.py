"""Create exact three-block/eight-actor automatic layout scope with source pause/control locks."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B152_B154_layout_tools_v3626')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B152_B154_editorial_manuscript_v1.json');packet=read(doc['source_context']);deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','item_terminology_reconciliation']};hashes={g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']};p=Path('dk4tool/dialogue/lil_B152_B154_profile.py');assert not p.exists();text='''"""Exact B152-B154 original progressive consumers and eight static selectors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,9,14,17,20,92,115,148})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B152-B154 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B152-B154 has no FE or dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B152-B154-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';59 ordinary54020 messages/eight static actors,including Barkeep92,PortWorker115,Guildmaster148 andAl17. Source FI3/FA1,2000pause/eightrelative sites andother source controls bound separately. No source scene eligibility claim.')
''';compile(text,str(p),'exec');p.write_text(text,encoding='utf-8');a=Path('dk4tool/dialogue/lil_B142_B145_layout_v2.py');b=Path('dk4tool/dialogue/lil_B152_B154_layout_v1.py');assert not b.exists();t=a.read_text(encoding='utf-8');old="expected={'lil-B142-B145-progressive-runtime-bound-v1':frozenset({2,4,9,13,16,20,23,109,171}),'lil-B142-B145-FE-runtime-bound-v1':frozenset({254})}";assert old in t;t=t.replace(old,"expected={'lil-B152-B154-progressive-runtime-bound-v1':frozenset({2,9,14,17,20,92,115,148})}").replace('source-bound B142-B145 profile','source-bound B152-B154 profile');old='def _word(value):';assert old in t;t=t.replace(old,"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('ancient','kingdom'),('kingdom','coin'),('lotion','jar'),('al','ferid'),('ferid','shin'),('guard','you'),('carry','your'),('your','bags'),('run','errands'),('your','wages'),('more','obedient'),('something','special'),('fighting','skills'),('limited','vocabulary'),('have','you'),('with','us')})\n\ndef _word(value):");compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');ROOT.mkdir(parents=True);save(ROOT/'exact_source_profile_and_formatter_provenance.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),previous_formatter=str(a),previous_formatter_sha256=sha(a.read_bytes()),formatter=str(b),formatter_sha256=sha(b.read_bytes()),dependencies=deps,no_global_profile_or_shared_guard_change=True,source_eight_static_selectors_including_printable5C_73_and94_bound=True,no_FE_consumer_allowed=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Exact three-block/eight-actor profile and automatic phrase planner created;FI3/FA1 andsource pause stay separate from prose.')
