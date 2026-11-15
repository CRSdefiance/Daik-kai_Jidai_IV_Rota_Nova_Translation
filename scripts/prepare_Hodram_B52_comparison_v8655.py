"""Compare both actual B52 paths without retiming; retain all timing/RNG/UI/component/RGB differences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_comparison_tools_v8655');assert not root.exists()
    source=Path('scripts/compare_Hodram_B51_actual_v8577.py').read_text(encoding='utf-8')
    a=source.index('    for number in [51]:');b=source.index('        reports=',a)
    cases="""    for case,proofpath,return_key,selected in [
        ('withdrawal','work/analysis/Hodram_B52_actual_v8651/B52/paired_actual_dialogue_headers_flow_returns.json','normal_return',0),
        ('opposition','work/analysis/Hodram_B52_opposition_actual_v8653/B52/paired_actual_dialogue_headers_flow_returns.json','script_return',1)]:
        number=52;path=Path(proofpath);proof=read(path)
        assert not proof['unresolved'] and proof['all_observed_complete_body_name_holds_andnative_flow_pass'];evidence[str(path)]=sha(path.read_bytes())
        old,new=[{**g,'script_return':g[return_key]} for g in proof['groups']]
        assert old['version']=='clean_Japanese' and new['version']=='revised_English'
        assert all(g['script_return']['native_result']==[selected,0] for g in [old,new])
        expectedIDs=['DK4_MES_B52_R0006','DK4_MES_B52_R0021' if selected==0 else 'DK4_MES_B52_R0033']
        expectedMissing=['DK4_MES_B52_R0033' if selected==0 else 'DK4_MES_B52_R0021']
        expectedPath=[8,68,104,112,164,166] if selected==0 else [8,68,104,108,174,178,200,208,216,224]
        for g in [old,new]:
            assert g['unvisited_conditional_text_IDs']==expectedMissing and len(g['speeches'])==2 and [s['id'] for s in g['speeches']]==expectedIDs
            assert len(g['command_pairs'])==8+len(expectedPath) and all(s['kind']=='progressive' and s['source_selector']==113 for s in g['speeches'])
            assert [c['canonical_source_offset'] for c in g['command_pairs'] if c['source_command_ordinal'] is not None]==expectedPath
            assert [c['native_result'] for c in g['command_pairs'] if c['word']==0x2100]==[[2,selected]]
            assert not [c for c in g['command_pairs'] if c['word'] in [0x8000,0x8100]]
"""
    result=derive('scripts/compare_Hodram_B51_actual_v8577.py','scripts/compare_Hodram_B52_actual_v8655.py',{
        source[a:b]:cases,'Hodram_B51_comparison_v8577':'Hodram_B52_comparison_v8655',
        "g['normal_return']":"g['script_return']",'normal_returns=':'script_returns=',
        "f'B{number}_full_scene_transition_pairs.png'":"f'B{number}_{case}_full_scene_transition_pairs.png'",
        'dict(block=number,scene_pairs=':'dict(block=number,case=case,ordinary_menu_selection=selected,scene_pairs=',
        'total_actual_frames=20002':'total_actual_frames=40004','current_registered_V8543_andmainV4701_unchanged':'current_registered_V8609_andmainV4701_unchanged',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,exact_source_controller0_normal_andcontroller1_flagged_paths_bound=True,all_original_scene_header_native_state_query_five_components_wholeactors_RNG_calendar_followingcommands_andfull_RGB_guards_preserved=True,no_capture_replay_retiming_orfalse_future_equivalence_claim=True,new_credit=0,full_goal_complete=False))
