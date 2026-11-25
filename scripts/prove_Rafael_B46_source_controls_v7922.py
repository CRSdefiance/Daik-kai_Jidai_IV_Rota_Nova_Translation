"""Source EV0 entry, four original relative sites and seeded normal ends; not scene activation."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_source_controls_v7922')
SOURCE=Path('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B46_clean_gloss_v7920b/24_speeches2_choices_fresh_clean_glosses_before_current_English.json')
INPUT=Path('work/analysis/current_V7911_Rafael_native_v7914/current_native_input.json')
NAMES=Path('work/analysis/Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,inp,names=map(read,[SOURCE,GLOSS,INPUT,NAMES])
    assert names['source_gloss_sha256']==sha(GLOSS.read_bytes()) and names['current_English_B46_bodies_andtwo_choices_still_unread']
    current,clean=[NdsImage.open(p) for p in [inp['current_ROM'],source['source_ROM']]]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==names['candidate_sha256']
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    arm,ja_arm=[im.read_file('/__arm9__.bin') for im in [current,clean]]
    spans=[(0x23840,0x23A28),(0x293B8,0x2976C),(0x29874,0x29A9C),(0x2A414,0x2A600),(0x24048,0x24118)]
    assert all(arm[a:b]==ja_arm[a:b] for a,b in spans)
    ev=current.read_file('/data/EV0.DK4');assert ev==clean.read_file('/data/EV0.DK4') and sha(ev)==source['EV0_sha256']
    group=source['groups'][0];block=bytes.fromhex(group['clean_block_hex']);commands=group['commands']
    assert len(block)==1696 and group['clean_logical_end']==1694 and block[1694:]==bytes(2)
    assert len(commands)==37 and len(group['records'])==24 and len(gloss['menu_choices'])==2
    assert all(r['current_English_body_unread'] for r in gloss['records']+gloss['menu_choices'])
    assert all(bytes.fromhex(r['source_hex']).count(token)==0 for r in group['records'] for token in [b'FI',b'FA',b'FO'])
    selected=group['source_event_records'];assert len(selected)==1
    assert [(r['event_ID'],r['action_index'],r['script_block'],r['must_be_completed'],r['must_not_be_completed']) for r in selected]==[(46,47,46,[38],[])]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    adapter=checked_text(inspect.getsource(native_entry),{
        'assert get(0x7F244)==2':'assert get(0x7F244)==0',
        'not_current_eligibility_or_selected_B234_activation':'not_current_eligibility_or_selected_B46_activation'})
    env=dict(native_entry.__globals__);exec(compile(adapter,__file__+'::original-EV0-entry','exec'),env)
    entry=ctx.execute(env['native_entry'],ev,selected);ctx.machines.pop()
    boundaries={c['offset'] for c in commands}|{group['clean_logical_end']};branches=[]
    for c in commands:
        if c['word'] not in [0x100,0x200,0x300,0x400]:continue
        result=ctx.execute(native_skip,block,c);ctx.machines.pop()
        assert all(r['next_offset'] in boundaries for r in result['cases'])
        branches.append(dict(block=46,**result))
    assert len(branches)==4 and sum(len(c['cases']) for c in branches)==20
    end=commands[-1];assert end['word']==0 and end['offset']==1690 and end['native_extent']==4 and block[1690:1694]==bytes(4)
    ep=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
    end_adapter=read(ep)['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__)
    exec(compile(end_adapter,__file__+'::source-normal-end-value-carry','exec'),env)
    ends=[env['end_case'](arm,block,1690,p,s) for p in [0,1,2,3,0xFFFFFFFF] for s in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    assert not ctx.machines
    menu=next(c for c in commands if c['word']==0x2100)
    assert menu==gloss['typed_menu_source']
    save(ROOT/'source_EV0_entry_four_relative_sites20_cases25_seeded_ends_menu_scope.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        source_event_records=selected,current_native_EV_entry=entry,source_relative_cases=branches,
        source_terminal=end,normal_seeded_ends=ends,source_typed_menu_command=menu,source_menu_choices=gloss['menu_choices'],
        five_original_A000_commands=[c for c in commands if c['word']==0xA000],
        original_resource_6300_andstructural_61FF=[c for c in commands if c['word'] in [0x6300,0x61FF]],
        native_entry_is_not_prerequisite_satisfaction_orcurrent_eligibility_oractual_activation=True,
        relative_results_are_isolated_native_cases_not_actual_menu_selection=True,
        all_five_A000_effects_menu_owner_geometry_selected_paths_resource_effects_andactual_scene_still_pending=True,
        complete_original_menu_accept_decline_semantics_return_values_andnative_control_flow_pending=True,
        all24_speech_preambles12_FE_selectors_andtwo_choice_source_bytes_retained=True,
        actual_B46_gameplay_observations=0,current_English_bodies_andtwo_choices_still_unread=True,
        measured_default_FI6_FA6_FO10_not_added_to_source_source_macros_zero=True,
        unchanged_source_runtime_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        source_owned_entry_adapter=adapter,source_owned_seeded_end_adapter=end_adapter,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,INPUT,NAMES,ep,Path(__file__)]},
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('B46 source EV entry/four sites20 isolated cases/25 seeded ends pass. Menu owner and actual branches remain pending; current English unread.')
