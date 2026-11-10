"""Bind exact Maria consumers and a source72-only two-native-page planning budget."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_B97_layout_tools_v5009')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/maria_B97_editorial_manuscript_v1.json');source=read(doc['source_context']);r72=next(r for r in doc['records'] if r['source_record_index']==72)
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','source_dispatch_proof','source_entry_proof','item_terminology_reconciliation','name_consumer_proof','macro_contract']}
    p=Path('dk4tool/dialogue/maria_B97_profile.py');assert not p.exists()
    t='''"""Exact B97 consumers;physical216x64/4rows,source72-only two-page planning."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(source['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted({source['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}))+''')
SELECTORS=frozenset({3,10,180})
PAGED_SOURCE_SHA='''+repr(sha(bytes.fromhex(r72['source_hex'])))+'''
DEPENDENCIES='''+repr(deps)+'''

def profile_for(arm,source_block,consumer='progressive',source_raw=None):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact Maria B97 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Maria B97 source contract changed:'+path)
    base=get_dialogue_profile('maria-story-shared-events-live')
    common=dict(balanced_wrapping=True,literal_prefix_policy='native-guard-v255',macro_widths={'FI':30,'FA':12,'FO':42,'I':12},macro_ascii_lengths={'FI':5,'FA':2,'FO':7})
    if consumer=='progressive':
        return replace(base,name='maria-B97-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,**common,metrics_source='B97 current captain3 Maria/Xien/Bandit voices3/5/0 and64 source/current dispatches.216x64 physical viewport,four16px rows.20 measured default macro cases bindMaria5/Li2/Li Clan7;one real FO. All40 commands/eight source leaves preserved. Current native and actual approval required.')
    if consumer=='progressive-two-page':
        if source_raw is None or sha(source_raw)!=PAGED_SOURCE_SHA:raise ValueError('Two-page plan is restricted to exact clean B97R72')
        return replace(base,name='maria-B97-progressive-two-page-runtime-bound-v1',leading_speaker_bytes=SELECTORS,max_lines=8,**common,metrics_source='Exact source72 only. max_lines8 is a bounded two-page host plan,not a taller native viewport. Original216x64 physical viewport,four16px rows per page and A continuation stay unchanged. Complete current native planes and fresh actual page advance remain required;historicalV288 is a lead,not current Maria proof.')
    if consumer=='FE-paper':
        return replace(base,name='maria-B97-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),**common,metrics_source='One original24310 null actor then5473C whisper sound.228x48 logical/228x64 physical;conservative216px host planning. No FE speech actor. Current font and focused actual approval required.')
    raise ValueError('Unknown B97 consumer')
'''
    compile(t,str(p),'exec');p.write_text(t,encoding='utf-8',newline='\n')
    old=Path('dk4tool/dialogue/lil_B183_layout_v3.py').read_text(encoding='utf-8')
    start=old.index('STRONG_ENDINGS=frozenset(');end=old.index('def _word(value):')
    constants="""STRONG_ENDINGS=frozenset({'a','an','as','at','for','from','in','of','the','to','with','and','or','but','so','that','which','than','because','if','like','by','into','not','i','you','he','she','it','its','we','they','my','your','our','his','her','their','is','are','was','were','be','been','being','can','could','will','would','shall','should','may','might','must','have','has','had',"don't","doesn't","didn't","can't","couldn't","won't","wouldn't","shouldn't","isn't","aren't","wasn't","weren't","i'll","you'll","we'll","they'll","i'm","you're","we're","they're","it's","that's","there's","i've","you've","we've","they've","it'll"})
BASE_WEAK=frozenset({'a','an','as','at','for','from','in','of','the','to','with'})
PROTECTED_BOUNDARIES=frozenset({('sao','jorge'),('great','powers'),('whole','world'),('slave','traders'),('stone','tablet'),('of','conquest'),('put','us'),('out','of'),('of','business'),('all','over'),('over','again'),('equal','terms'),('take','a'),('a','chance'),('make','a'),('a','move'),('what','it'),('it','takes'),('give','up'),('up','on'),('at','least'),('to','blame'),('think','about'),('in','our'),('our','hands')})

"""
    t=old[:start]+constants+old[end:]
    a="expected={'lil-B183-progressive-runtime-bound-v1':frozenset({85,110,132,148,153}),'lil-B183-FE-runtime-bound-v1':frozenset({254})}"
    b="expected={'maria-B97-progressive-runtime-bound-v1':(frozenset({3,10,180}),4),'maria-B97-progressive-two-page-runtime-bound-v1':(frozenset({3,10,180}),8),'maria-B97-FE-runtime-bound-v1':(frozenset({254}),4)}"
    changes={a:b,'profile.leading_speaker_bytes!=expected[profile.name]':'profile.leading_speaker_bytes!=expected[profile.name][0]','profile.max_lines!=4':'profile.max_lines!=expected[profile.name][1]',"[('FI',3),('FA',5),('FO',9)]":"[('FI',5),('FA',2),('FO',7)]",'exact source-bound B183 profile':'exact source-bound Maria B97 profile',"    # Bind every source prefix":"    if profile.name=='maria-B97-progressive-two-page-runtime-bound-v1' and sha(source_raw)!="+repr(sha(bytes.fromhex(r72['source_hex'])))+":\n        raise ValueError('Two-page encoding requires exact clean B97R72 source')\n    # Bind every source prefix"}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    t=t.replace('"""Source-bound relocated prose planner;preserve reviewed words and byte guards.','"""Maria B97 source-bound logical prose planner;preserve complete words and byte guards.')
    q=Path('dk4tool/dialogue/maria_B97_layout_v1.py');assert not q.exists();compile(t,str(q),'exec');q.write_text(t,encoding='utf-8',newline='\n')
    tools=[derive('scripts/plan_lil_B183_layout_v4944.py','scripts/plan_maria_B97_layout_v5010.py',{'lil_B183_layout_v3':'maria_B97_layout_v1','lil_B183_profile':'maria_B97_profile','lil_B183_layout_v4944':'maria_B97_layout_v5010','lil_B183_editorial_manuscript_v1':'maria_B97_editorial_manuscript_v1','lil_B183_editorial_manuscript_v6':'maria_B97_editorial_manuscript_v2','/data/SC2.DK4':'/data/SC3.DK4',"profile=profile_for(arm,blocks[r['block']],'FE-paper' if r['kind']=='system-FE' else 'progressive')":"profile=profile_for(arm,blocks[r['block']],'FE-paper' if r['kind']=='system-FE' else ('progressive-two-page' if r['source_record_index']==72 else 'progressive'),raw)",'all25_paragraph':'all32_paragraph','len(reports)==25':'len(reports)==32','plans=25':'plans=32','Plan25':'Plan32',"dialogue_profile='lil-opening-editorial-native-v1'":"dialogue_profile='maria-story-shared-events-live'"})]
    ROOT.mkdir(parents=True);save(ROOT/'profile_formatter_and_planner_provenance.json',dict(profile=str(p),profile_sha256=sha(p.read_bytes()),formatter=str(q),formatter_sha256=sha(q.read_bytes()),tools=tools,dependencies=deps,source72_only_two_native_pages_pending_fresh_actual_A_advance=True,physical_viewport_font_metrics_guards_and_native_code_unchanged=True,no_historical_compiler_changed=True,no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Exact B97 profile/planner created;source72-only two-page budget leaves physical216x64 unchanged. Native and actual page approval pending.')
