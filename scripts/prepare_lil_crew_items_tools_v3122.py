"""Create exact fourteen-block speech/FE profile and local immutable planner successor."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Crew_Items_tools_v3122')
PROFILE=Path('dk4tool/dialogue/lil_crew_items_profile.py')
LAYOUT=Path('dk4tool/dialogue/lil_crew_items_layout_v1.py')
SOURCE=Path('work/analysis/lil_Crew_Items_source_v3112/complete200_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Crew_Items_controls_v3114/source_bound198_preambles_FE_and_original_conditional_predicates.json')
TERMS=Path('work/analysis/lil_Crew_Items_terms_v3116/clean_current_ten_items_stat_UI_and_native_actor_terms.json')
PARENT=Path('dk4tool/dialogue/lil_recruits_julian_layout_v1.py')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,PROFILE,LAYOUT]);source,control=map(read,[SOURCE,CONTROL])
    hashes=sorted({b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']});assert len(hashes)==28
    selectors=[2,4,6,7,12,14,15,16,18,20,22,108,114,152,188]
    assert control['ordinary_native_actor_selectors']=={str(k):k for k in selectors}
    text='''"""Exact fourteen-block crew/item speech and seven FE consumers."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path(@CONTROL@)
PROOF_SHA=@CONTROL_SHA@
TERMS=Path(@TERMS@)
TERMS_SHA=@TERMS_SHA@
ARM9_SHA=@ARM@
BLOCKS=frozenset(@HASHES@)
SELECTORS=frozenset(@SELECTORS@)

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Crew/Items requires exact fourteen reviewed clean/current source blocks/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(TERMS.read_bytes())!=TERMS_SHA:
        raise ValueError('Crew/Items source-control or item/stat/native name terminology changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));terms=json.loads(TERMS.read_text(encoding='utf-8'))
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all198_complete_preambles_and396_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=396 or proof['ordinary_native_actor_selectors']!={str(k):k for k in SELECTORS}
        or proof['current_original_predicate_cases'] or proof['original_event_queries']
        or not proof['all7_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['all7_FE_source_stat_notices_and_unlabeled_monkey_calls_preserved_by_original_dispatcher']
        or not terms['all10_clean_current_pointer_strings_equal_registered_names']
        or terms['approved_stat_terms']['Luck']['English']!='Luck'
        or terms['approved_stat_terms']['Spirit']['English']!='Spirit'):
        raise ValueError('Complete ordinary/seven FE/item/stat contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-crew-items-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+'; exact14blocks/198complete preambles/15 ordinary54020 selectors. No new individual nameplate or earned item/stat claim; current fonts/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-crew-items-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exact7FEbeforefallback208and5473C,original24310nullactor,fourstat notices/twoFI andthreeunlabeledmonkeycalls. Inherited228x48mode1paper,conservative216pxplanning;complete freshfont/pagination required.')
    raise ValueError('Unknown Crew/Items presentation consumer')
'''
    replacements={'@CONTROL@':repr(CONTROL.as_posix()),'@CONTROL_SHA@':repr(sha(CONTROL.read_bytes())),'@TERMS@':repr(TERMS.as_posix()),'@TERMS_SHA@':repr(sha(TERMS.read_bytes())),'@ARM@':repr(source['current_ARM9_sha256']),'@HASHES@':repr(hashes),'@SELECTORS@':repr(selectors)}
    for old,new in replacements.items():assert old in text;text=text.replace(old,new)
    assert '@' not in text
    planner=PARENT.read_text(encoding='utf-8')
    old="'lil-recruits-julian-progressive-runtime-bound-v1':frozenset({2,4,9,12,14,18,20,22,26,41,109,158})"
    new="'lil-crew-items-progressive-runtime-bound-v1':frozenset({2,4,6,7,12,14,15,16,18,20,22,108,114,152,188})"
    assert planner.count(old)==1
    planner=planner.replace(old,new).replace('lil-recruits-julian-FE-runtime-bound-v1','lil-crew-items-FE-runtime-bound-v1').replace('Recruits/Julian','Crew/Items')
    anchor='PROTECTED_BOUNDARIES=frozenset({';assert planner.count(anchor)==1
    pairs=[('tomato','seedling'),('miracle','bullet'),('bullet','charm'),('peacock','mail'),('ninja','garb'),('jaguar',"god's"),("god's",'vest'),('minerva','shield'),("hestia's",'pot'),('aristarchus','telescope'),('cape','of'),('of','good'),('good','hope'),('give','back'),('come','back'),('get','your'),('your','hopes'),('hopes','up'),('covert','operations'),('back','to'),('to','work')]
    planner=planner.replace(anchor,anchor+','.join(repr(p) for p in pairs)+',')
    compile(text,str(PROFILE),'exec');compile(planner,str(LAYOUT),'exec')
    PROFILE.write_text(text,encoding='utf-8');LAYOUT.write_text(planner,encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'new_scoped_tools_provenance.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),layout=str(LAYOUT),layout_sha256=sha(LAYOUT.read_bytes()),parent_layout=str(PARENT),parent_layout_sha256=sha(PARENT.read_bytes()),dependencies={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,TERMS,Path(__file__)]},exact_14_clean_and_current_block_hashes=hashes,ordinary_selectors=selectors,FE_selector=254,no_global_or_previous_module_change=True,no_editorial_or_completion_credit=True,full_goal_complete=False))
    print('New exact28-hash/15-selector profile andbatch-local item/phrase planner created;prior modules preserved.')
