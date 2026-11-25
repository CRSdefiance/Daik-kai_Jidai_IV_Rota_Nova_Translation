"""Prepare bounded actual scene/final-state comparison without replay orretiming."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_comparison_tools_v8743');assert not root.exists()
    source=Path('scripts/compare_Hodram_B52_actual_v8655.py').read_text('utf-8')
    a=source.index('    for case,proofpath,return_key,selected in [');z=source.index('        reports=[read(',a)
    prefix='''    for number,proofpath,value in [
        (31,'work/analysis/Hodram_B31_B53_actual_v8742/B31/paired_actual_dialogue_headers_flow_returns.json',1),
        (53,'work/analysis/Hodram_B31_B53_actual_v8742b/B53/paired_actual_dialogue_headers_flow_returns.json',0)]:
        case='default';path=Path(proofpath);proof=read(path)
        assert not proof['unresolved'] and proof['all_observed_complete_body_name_holds_andnative_flow_pass'];evidence[str(path)]=sha(path.read_bytes())
        old,new=[{**g,'script_return':g['normal_return']} for g in proof['groups']]
        assert old['version']=='clean_Japanese' and new['version']=='revised_English'
        assert all(g['script_return']['native_result']==[0,value] for g in [old,new])
        expectedIDs=['DK4_MES_B31_R0018'] if number==31 else ['DK4_MES_B53_R0007']
        expectedMissing=['DK4_MES_B31_R0013'] if number==31 else []
        expectedPath=[8,10,18,22,90,188,192] if number==31 else [8,10,12,98,106,114,122,130,132]
        for g in [old,new]:
            assert g['unvisited_conditional_text_IDs']==expectedMissing and len(g['speeches'])==1 and [s['id'] for s in g['speeches']]==expectedIDs
            assert len(g['command_pairs'])==8+len(expectedPath) and all(s['kind']=='progressive' and s['source_selector']==(34 if number==31 else 113) for s in g['speeches'])
            assert [c['canonical_source_offset'] for c in g['command_pairs'] if c['source_command_ordinal'] is not None]==expectedPath
            assert not [c for c in g['command_pairs'] if c['word']==0x2100]
            assert [c['native_result'] for c in g['command_pairs'] if c['word']==0x8000]==([[2,1]] if number==31 else [])
'''
    receipt=derive('scripts/compare_Hodram_B52_actual_v8655.py','scripts/compare_Hodram_B31_B53_actual_v8743.py',{
        source[a:z]:prefix,
        'Hodram_B52_comparison_v8655':'Hodram_B31_B53_comparison_v8743',
        'ordinary_menu_selection=selected':'ordinary_default_input_case=True',
        'source_has_no_picture_orhide_sites=True':'opaque_effect_semantics_not_inferred_from_structural_preservation=True',
        'total_actual_frames=40004':'total_actual_frames=24004',
        'current_registered_V8609_andmainV4701_unchanged':'current_registered_V8704_andmainV4701_unchanged',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        all_original_native_state_models_persistentobjects_tasks_calendar_wholeactors_captain_RNG_RGB_andreadonly_guards_preserved=True,
        no_command_duration_UI_request_seed_calendar_state_orfollowing_command_difference_suppressed=True,
        source31_long_path_selected_unforced_short_variant_offline_only=True,source53_all9commands_observed=True,
        actual_end_results31_0_1_and53_0_0_separate_from_interpreter_carried_mode=True,
        no_replay_retiming_opaque_effect_invention_future_simulation_orcredit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
