"""Create exact-source profiles for nine actors and a distinct FE consumer."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_layout_tools_v3584')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B142_B145_editorial_manuscript_v1.json');packet=read(doc['source_context']);deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_finance_contract','source_effect_boundary_contract','source_predicate_contract','item_terminology_reconciliation']};hashes={g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']};p=Path('dk4tool/dialogue/lil_B142_B145_profile.py');assert not p.exists()
    text='''"""B142-B145 exact runtime/source consumers;0D and6D remain executable selectors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,4,9,13,16,20,23,109,171})
DEPENDENCIES='''+repr(deps)+'''
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B142-B145 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':return replace(base,name='lil-B142-B145-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';37 ordinary54020 messages;Cesare13 andShipwright109 original static dispatch,not CR or m glyph. Nine actor names/FI2 source-bound. No selected event eligibility claim.')
    if consumer=='FE-paper':return replace(base,name='lil-B142-B145-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),metrics_source=base.metrics_source+';one FE null-actor5473C armor-capability notice. Conservative216px planning;separate228x48 logical/228x64 physical native painter proof required.')
    raise ValueError('Unknown B142-B145 consumer')
''';compile(text,str(p),'exec');p.write_text(text,encoding='utf-8')
    a=Path('dk4tool/dialogue/lil_B141_layout_v2.py');b=Path('dk4tool/dialogue/lil_B142_B145_layout_v1.py');assert not b.exists();t=a.read_text(encoding='utf-8');old="expected={'lil-B141-progressive-runtime-bound-v1':frozenset({2,9,20,171})}";new="expected={'lil-B142-B145-progressive-runtime-bound-v1':frozenset({2,4,9,13,16,20,23,109,171}),'lil-B142-B145-FE-runtime-bound-v1':frozenset({254})}";assert old in t;t=t.replace(old,new).replace('source-bound B141 profile','source-bound B142-B145 profile')
    old='def _word(value):';assert old in t;t=t.replace(old,"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('patterned','cloth'),('brass','lamp'),('mediterranean','proof'),('300,000','gold'),('research','funds'),('extra','armor'),('hidden','writing'),('long','shot'),('since','then'),('as','soon'),('soon','as'),('all','right')})\n\ndef _word(value):")
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');ROOT.mkdir(parents=True);save(ROOT/'exact_source_profile_and_formatter_provenance.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),previous_formatter=str(a),previous_formatter_sha256=sha(a.read_bytes()),formatter=str(b),formatter_sha256=sha(b.read_bytes()),dependencies=deps,no_global_profile_or_shared_guard_change=True,source13_109_static_and254_null_actor_bound=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Exact four-block/nine-static-plus-FE profiles and scoped automatic planner created.')
