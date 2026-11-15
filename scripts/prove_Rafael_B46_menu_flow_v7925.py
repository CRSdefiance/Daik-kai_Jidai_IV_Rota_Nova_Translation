"""Bind original typed-menu values to source branches; keep bridged/offline scope explicit."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.research_wedding_command_v676 import walk
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_menu_flow_v7925')
SOURCE=Path('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B46_clean_gloss_v7920b/24_speeches2_choices_fresh_clean_glosses_before_current_English.json')
CONTROL=Path('work/analysis/Rafael_B46_source_controls_v7922/source_EV0_entry_four_relative_sites20_cases25_seeded_ends_menu_scope.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,control=map(read,[SOURCE,GLOSS,CONTROL])
    assert control['source_gloss_sha256']==sha(GLOSS.read_bytes()) and control['current_English_bodies_andtwo_choices_still_unread']
    g=source['groups'][0];block=bytes.fromhex(g['clean_block_hex']);menu=gloss['typed_menu_source']
    raw=bytes.fromhex(menu['whole_command_hex']);assert raw==block[256:292]
    adapter=checked_text(inspect.getsource(original.choice_vm),{
        'p.decode() for p in labels':"p.decode('cp932') for p in labels",
        "'VM_state': state,":"'VM_state': state, 'VM_selection_word': selection,",
    })
    env=dict(original.__dict__);exec(compile(adapter,__file__+'::exact-two-choice-VM','exec'),env)
    versions=[];structural=[]
    for label,path in [('clean-Japanese',source['source_ROM']),('current-runtime-source-Japanese-only',control['candidate'])]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin')
        proof=env['choice_vm'](arm,raw)
        assert proof['labels']==[r['source_Japanese'] for r in gloss['menu_choices']]
        assert [(r['modal_selection'],r['VM_state']) for r in proof['VM_cases']]==[(0,2),(1,2),(-1,0)]
        assert [r['VM_selection_word'] for r in proof['VM_cases'][:2]]==[0,1]
        versions.append(dict(version=label,ARM9_sha256=sha(arm),source_object_hex=raw.hex(),native_VM=proof,
            modal_input_loop_bridged_at_original51FC0=True,not_actual_controller_selection_orbacking_capture=True))
        pairs=[]
        for c in control['five_original_A000_commands']+control['original_resource_6300_andstructural_61FF']:
            value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value
            result=walk(arm,isolated)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
            assert len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent']
            pairs.append(dict(original_offset=c['offset'],original_word=c['word'],source_command_hex=value.hex(),**result))
        structural.append(dict(version=label,cases=pairs))
    assert versions[0]['native_VM']==versions[1]['native_VM']
    for a,b in zip(structural[0]['cases'],structural[1]['cases'],strict=True):
        assert a==b
    commands={c['offset']:c for c in g['commands']};speeches={r['source_reference']['header_offset']:r for r in g['records']}
    relative={c['offset']:c for c in control['source_relative_cases']}
    paths=[]
    for selected in [0,1]:
        pointer=8;visited=[];texts=[];relative_cases=[]
        while pointer<g['clean_logical_end']:
            c=commands[pointer];visited.append(pointer)
            if pointer in speeches:texts.append(speeches[pointer]['id'])
            if pointer in relative:
                case=next(r for r in relative[pointer]['cases'] if r['previous_result_structural_argument']==selected)
                relative_cases.append(dict(source_offset=pointer,**case));pointer=case['next_offset']
            else:pointer+=c['native_extent']
        assert pointer==g['clean_logical_end'] and visited[-1]==1690
        paths.append(dict(menu_selection=selected,original_VM_state=2,original_VM_selection_word=selected,
            visited_source_command_offsets=visited,source_speech_IDs=texts,source_speech_count=len(texts),relative_native_cases=relative_cases,
            composed_from_measured_native_menu_andrelative_cases_not_actual_interpreter_orcontroller_run=True))
    accept,decline=paths
    assert len(accept['source_speech_IDs'])==22 and len(decline['source_speech_IDs'])==7
    assert set(accept['source_speech_IDs'])|set(decline['source_speech_IDs'])=={r['id'] for r in g['records']}
    assert set(decline['source_speech_IDs'])-set(accept['source_speech_IDs'])=={'DK4_MES_B46_R0105','DK4_MES_B46_R0109'}
    ROOT.mkdir(parents=True);save(ROOT/'two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),source_menu_versions=versions,
        paired_source_current_opaque_command_extent_cases=structural,source_paths=paths,
        five_A000_plus6300_plus61FF_seven_pairs14_structural_cases=True,
        A000_operands_preserved_without_assigning_unproven_gameplay_semantics=True,
        original_modal_selection0_1_forwarded_as_state2_value0_1=True,
        modal_cancel_minus1_is_bridged_native_scope_not_actual_B_button_orcancel_behavior=True,
        accept_path22_speeches_includes12_FE_then_check_thanks_skips_caution=True,
        decline_path7_speeches_skips_tutorial_enters_caution_inside_outer0100=True,
        shared_private_unfinished_thought_after_both_paths=True,
        previous_linear_gloss_caution_after_tutorial_is_superseded_by_measured_source_branch_context=True,
        no_current_English_B46_body_orchoice_read=True,no_actual_B46_activation_backing_selection_orfull_mechanics_claim=True,
        source_owned_VM_adapter=adapter,new_emulator_runs=0,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,CONTROL,Path(__file__)]},full_goal_complete=False))
    print('Source menu: two labels/three bridged results each runtime; seven source/current opaque-command pairs. Accept22/decline7; caution belongs to decline. No actual selection claim.')
