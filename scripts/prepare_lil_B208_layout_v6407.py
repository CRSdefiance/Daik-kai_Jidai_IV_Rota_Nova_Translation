"""Bind B208's23 progressive objects/one FE to the measured current native consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B208_layout_tools_v6407')
if __name__=='__main__':
    assert not ROOT.exists();docpath=Path('translations/lil_B208_editorial_manuscript_v2.json');doc=read(docpath);packet=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','effective_current_comparison','control_contract','actor_terminology_reconciliation','actual_source_visual_review','source_prose_module','speaker_name_contextual_review','name_native_font_and_actual_proof']}
    for p in [str(docpath),'work/analysis/lil_FE_row_capacity_v6125/original228px_descriptor_native36_ASCII_row_capacity.json','scripts/shady_man_font_oracles_v6263.py','work/analysis/lil_B208_name_approval_v6406/two_name_retentions91_headers_no_asset_change.json']:deps[p]=sha(Path(p).read_bytes())
    lines=Path('dk4tool/dialogue/lil_B205_profile_v2.py').read_text('utf-8').splitlines();literal=lambda k:next(x for x in lines if x.startswith(k+'='))
    profile=derive('dk4tool/dialogue/lil_B205_profile_v2.py','dk4tool/dialogue/lil_B208_profile_v1.py',{
        'B205':'B208','two actors,10 progressive speeches and seven actorless sound/echo objects':'two actors,23 progressive objects incl private thought and one actorless named attribute notice',
        literal('ARM9_SHA'):'ARM9_SHA='+repr(doc['required_runtime_ARM9_sha256']),literal('BLOCKS'):'BLOCKS='+repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),
        literal('DEPENDENCIES'):'DEPENDENCIES='+repr(deps),literal('CONTROL'):'CONTROL='+repr(doc['control_contract']),literal('SOURCE'):'SOURCE='+repr(doc['source_context']),
        'frozenset({2,15})':'frozenset({7,170})','current V6160 runtime':'current V6380 runtime','len(cases)!=34':'len(cases)!=48',"sum(r['source_selector']==254 for r in cases)!=14":"sum(r['source_selector']==254 for r in cases)!=2",
        'All17 clean/current speech pairs and seven FE sound/echo objects required':'All24 clean/current pairs and one FE named notice required','FE sound/echo objects remain null actor':'FE named notice remains null actor',
        "len(control['source_current_opaque_nonrelative_control_leaves'])!=8":"len(control['source_current_opaque_nonrelative_control_leaves'])!=5",'has eight leaves':'has five leaves',
        "source['ordinary_source_speeches']!=10 or source['system_FE_panels']!=7":"source['ordinary_source_speeches']!=23 or source['system_FE_panels']!=1",'Source10 progressive/seven FE consumer split required':'Source23 progressive/one FE consumer split required',
        '10 source-bound progressive54020 speeches,two static actors':'23 source-bound progressive54020 objects including a parenthesized private thought,two static actors with voices3/0',
        'seven original24310 null-actor then5473C sound/echo objects':'one original24310 null-actor then5473C named attribute notice',
    })
    planner=derive('dk4tool/dialogue/lil_B205_layout_v2.py','dk4tool/dialogue/lil_B208_layout_v1.py',{
        'B205':'B208','frozenset({2,15})':'frozenset({7,170})',
        '# Exact B205 whole-exchange review:keep the mimicry and final idiom intact.':'# Exact B208 whole-exchange review:keep the resemblance,reported clue and limited commitment intact.',
        "frozenset({('stop','copying'),('copying','me'),('had','enough'),('finally','got'),('got','it'),('got','caught'),('save','face')})":"frozenset({('to','be'),('be','reckoned'),('reckoned','with'),('air','about'),('about','you'),('get','stronger'),('get','even'),('even','stronger'),('look','for'),('prized','sword'),('took','part'),('great','naval'),('naval','battle'),('keep','it'),('it','in'),('in','mind'),('see','it')})",
        "frozenset({(\"i'm\",'going'),('going','to'),('to','catch'),('catch','you'),('trying','to'),('to','save')})":"frozenset()",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_profile_and_planner.json',dict(profile=profile,planner=planner,dependencies=deps,exact23_progressive_one_FE_private_thought_two_source_actors_and_five_leaves=True,FE_original228_logical_bitmap_measured216_printable_capacity_preserved=True,current_strict_input=doc['current_strict_native_input'],current_font_oracle='scripts/shady_man_font_oracles_v6263.py',no_inherited_B207_it_if_exception_or_B205_echo_sound_rule=True,original_fonts_native_addresses_guard_pair_phase_four_rows_and_windows_preserved=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('B208 current-bound profile and logical-paragraph planner prepared;23 progressive/one FE,original measured36-cell capacity,all words unchanged.')
