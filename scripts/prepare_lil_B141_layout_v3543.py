"""Create a source-bound automatic formatter and complete native-font successor."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_layout_tools_v3543')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json');packet=read(source)
    control=Path('work/analysis/lil_B141_controls_v3538b/all14_source_current_dispatches_FI_C200_and630A_contract.json');voice=Path('work/analysis/lil_B141_voices_v3533/current_four_static_names_voices_and207_catalog_rebind.json');funds=Path('work/analysis/lil_B141_funds_v3537b/source_million_threshold_and900000_payment_seven_boundary_cases.json');branch=Path('work/analysis/lil_B141_branches_v3539/original_relative_skip_operand_proof.json');entry=Path('work/analysis/lil_B141_entry_v3536/source_EV2_B141_action_dependency_and_native_getter_binding.json');terms=Path('work/analysis/lil_B141_terms_v3541/source_current_polder_and_distinct_monetary_amounts.json')
    profile=Path('dk4tool/dialogue/lil_B141_profile.py');assert not profile.exists();deps={str(p):sha(p.read_bytes()) for p in [source,control,voice,funds,branch,entry,terms]};hashes={packet['blocks'][0]['clean_block_sha256'],packet['blocks'][0]['current_block_sha256']}
    text='''"""Exact B141 progressive consumers,source monetary contracts and relative controls."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(sorted(hashes))+''')
SELECTORS=frozenset({2,9,20,171})
DEPENDENCIES='''+repr(deps)+'''
CONTROL=Path('''+repr(str(control))+''')
VOICE=Path('''+repr(str(voice))+''')
FUNDS=Path('''+repr(str(funds))+''')
BRANCH=Path('''+repr(str(branch))+''')
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B141 clean/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    c,v,f,b=[json.loads(p.read_text(encoding='utf-8')) for p in [CONTROL,VOICE,FUNDS,BRANCH]]
    if consumer!='progressive' or len(c['speech_dispatch_cases'])!=28 or c['source_macro_counts']!={'FI':1,'FA':0,'FO':0} or len(c['source_C200_cases'])!=2 or len(c['source_630A_cases'])!=10 or len(v['fresh_four_actor_names']['rows'])!=4 or len(f['cases'])!=7 or f['source_threshold_gold']!=1000000 or f['source_payment_gold']!=900000 or len(b['cases'])!=130:raise ValueError('Complete four-actor,FI1,source monetary,C200/630A and relative contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B141-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';14 B141 progressive speeches,four static actors,Lil captain2 and FI1. One-million threshold and900000 payment are source-bound. Opaque630A/resource bodies and selected scene are not executed by this profile.')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8');pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('dk4tool/dialogue/lil_B139_B140_layout_v2.py','dk4tool/dialogue/lil_B141_layout_v1.py',[
        ('lil-B139-B140-progressive-runtime-bound-v1','lil-B141-progressive-runtime-bound-v1'),('frozenset({2,4,9,16,20,21,171})','frozenset({2,9,20,171})'),('B139/B140','B141'),
        ('def _word(value):',"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('million','gold'),('900,000','gold'),('save','up'),('work','hard'),('wish','you'),('you','well'),('went','all'),('all','over'),('different','people'),('a','tenth'),('polder','soon')})\n\ndef _word(value):")])
    make('scripts/verify_lil_B139_B140_fonts_v3472.py','scripts/verify_lil_B141_fonts_v3544.py',[
        ('lil_B139_B140_profile','lil_B141_profile'),('lil_B139_B140_layout_v1','lil_B141_layout_v1'),('lil_B139_B140_fonts_v3472','lil_B141_fonts_v3544'),('lil_B139_B140_editorial_manuscript_v4','lil_B141_editorial_manuscript_v2'),
        ('len(cases)==67 and len(qa_reports)==67 and macro_calls==536','len(cases)==14 and len(qa_reports)==14 and macro_calls==112'),('blocks[139]','blocks[141]'),('blocks[137]','blocks[140]'),('selectors=[2,4,9,16,20,21,171]','selectors=[2,9,20,171]'),('format(4 if selector==2 else 2','format(9 if selector==2 else 2'),('len(negatives)==23','len(negatives)==17'),('all67','all14'),('current_original_macro_alignment_calls=536','current_original_macro_alignment_calls=112'),('actual_selected_B139_B140_IDs','actual_selected_B141_IDs'),('67 complete progressive planes,536 macro cases,67 QA plans and23source-consumer','14 complete progressive planes,112 macro cases,14 QA plans and17 source-consumer'),('nine sheets','two sheets')])
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),tools=pairs,all_predecessors_preserved=True,source_finance_and_UI_control_contracts_distinguished=True,no_global_profile_or_guard_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
