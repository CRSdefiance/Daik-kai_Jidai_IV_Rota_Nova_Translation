"""Bind B205's ten progressive and seven FE objects to the measured original consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B205_layout_tools_v6187')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B205_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','effective_current_comparison','control_contract','actor_terminology_reconciliation','actual_source_visual_review','source_prose_module']}
    for p in ['translations/lil_B205_editorial_manuscript_v1.json','work/analysis/lil_FE_row_capacity_v6125/original228px_descriptor_native36_ASCII_row_capacity.json']:deps[p]=sha(Path(p).read_bytes())
    old=Path('dk4tool/dialogue/lil_B204_profile_v2.py').read_text(encoding='utf-8');lines=old.splitlines();literal=lambda key:next(line for line in lines if line.startswith(key+'='))
    profile=derive('dk4tool/dialogue/lil_B204_profile_v2.py','dk4tool/dialogue/lil_B205_profile_v1.py',{
        'B204':'B205','five actors,16 progressive speeches and four actorless letter objects':'two actors,10 progressive speeches and seven actorless sound/echo objects',
        literal('BLOCKS'):'BLOCKS='+repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),
        literal('DEPENDENCIES'):'DEPENDENCIES='+repr(deps),literal('CONTROL'):'CONTROL='+repr(doc['control_contract']),literal('SOURCE'):'SOURCE='+repr(doc['source_context']),
        'frozenset({2,11,124,130,145})':'frozenset({2,15})','current V6110 runtime':'current V6160 runtime','len(cases)!=40':'len(cases)!=34',"sum(r['source_selector']==254 for r in cases)!=8":"sum(r['source_selector']==254 for r in cases)!=14",
        'All20 clean/current speech pairs and four FE letters required':'All17 clean/current speech pairs and seven FE sound/echo objects required','FE letters remain null actor':'FE sound/echo objects remain null actor','All five original static actors required':'Both original static actors required',
        "len(control['source_current_opaque_nonrelative_control_leaves'])!=6":"len(control['source_current_opaque_nonrelative_control_leaves'])!=8",'has six leaves':'has eight leaves',
        "source['ordinary_source_speeches']!=16 or source['system_FE_panels']!=4":"source['ordinary_source_speeches']!=10 or source['system_FE_panels']!=7",'Source16 progressive/four FE consumer split required':'Source10 progressive/seven FE consumer split required',
        '16 source-bound progressive54020 speeches,five static actors':'10 source-bound progressive54020 speeches,two static actors',
        'four original24310 null-actor then5473C letter objects':'seven original24310 null-actor then5473C sound/echo objects',
    })
    planner=derive('dk4tool/dialogue/lil_B204_layout_v4.py','dk4tool/dialogue/lil_B205_layout_v1.py',{
        'B204':'B205','frozenset({2,11,124,130,145})':'frozenset({2,15})',
        '# Exact B204 whole-exchange review:keep short complete clauses and the ship rule intact.':'# Exact B205 whole-exchange review:keep the mimicry and final idiom intact.',
        "frozenset({('sounds','good'),('they','gave'),('gave','me'),('me','this'),('this','to'),('to','thank'),('thank','me'),('something','terrible'),('find','that'),('that','thief'),('one','figurehead'),('figurehead','per'),('per','ship')})":"frozenset({('stop','copying'),('copying','me'),('had','enough'),('finally','got'),('got','it'),('save','face')})",
        "frozenset({('use','figureheads'),('shachihoko','is'),('is','gone')})":"frozenset({(\"i'm\",'going'),('going','to'),('to','catch'),('catch','you'),('trying','to'),('to','save')})",
    })
    verifier=derive('scripts/verify_lil_B204_fonts_v6127.py','scripts/verify_lil_B205_fonts_v6189.py',{
        'B204':'B205','fonts_v6127':'fonts_v6189','lil_B204_profile_v2':'lil_B205_profile_v1','lil_B204_layout_v2':'lil_B205_layout_v1',
        'manuscript_v3':'manuscript_v2','work/analysis/lil_B204_current_v6118/current_native_input.json':'work/analysis/current_V6160_native_v6168/current_native_input.json',
        '160':'136','128':'80','FE_null_actor_alignment_calls=32':'FE_null_actor_alignment_calls=56','complete_progressive_planes=16':'complete_progressive_planes=10','complete_FE_logical_and_physical_planes=4':'complete_FE_logical_and_physical_planes=7',
        '==20':'==17','all20':'all17','All20':'All17',"sum(c['kind']=='system-FE' for c in cases)==4":"sum(c['kind']=='system-FE' for c in cases)==7",'[204]':'[205]','[203]':'[204]',
        '[2,11,124,130,145,254]':'[2,15,254]','format(11 if selector==2 else 2':'format(15 if selector==2 else 2',"r['source_selector']==11":"r['source_selector']==15",'len(negatives)==24':'len(negatives)==18','and24 source-consumer':'and18 source-consumer','all_six_selectors':'all_three_selectors',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_profile_planner_and_native_tools.json',dict(profile=profile,planner=planner,verifier=verifier,dependencies=deps,
        exact10_progressive_seven_FE_two_source_actors_and_eight_leaves=True,FE228px_bitmap_has_measured216px_printable_budget=True,
        original_fonts_addresses_guard_pair_phase_four_rows_and_native_windows_preserved=True,no_old_letter_or_five_actor_assumption=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('B205 exact profile,scoped logical-paragraph planner and fresh136-alignment verifier prepared;measured FE budget216px retained.')
