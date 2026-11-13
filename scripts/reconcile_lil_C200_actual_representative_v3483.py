"""Bind existing actual C200 completion to unchanged current code and resources."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_C200_actual_representative_v3483')
ACTUAL=Path('work/analysis/lil_B24_actual_v1838/complete_B24_scene_and_two_coordinate_fixture_audit.json')
CURRENT=Path('out/all_routes_combined_v3450_candidate.nds')
CONTROL=Path('work/analysis/lil_B139_B140_relocated_controls_v3482/all67_relocated_dispatches12_predicates1_query_and_C200_pairs.json')
SOURCE=Path('work/analysis/lil_B139_C200_v3461e/source_C200_UI_request_contract.json')
if __name__=='__main__':
    assert not ROOT.exists();actual,control,source=map(read,[ACTUAL,CONTROL,SOURCE]);oldpath=Path(actual['candidate']);old,current=NdsImage.open(oldpath),NdsImage.open(CURRENT);a,b=[im.read_file('/__arm9__.bin') for im in [old,current]]
    assert sha(oldpath.read_bytes())==actual['candidate_sha256'] and sha(CURRENT.read_bytes())==control['candidate_sha256']==source['candidate_sha256']
    for p,digest in actual['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    pair=next(c for c in actual['all17_original_command_pairs'] if c['word']==0xC200);assert pair['frames']==[47368,47369] and pair['decoded_length']==2 and pair['result_words'][0]==3 and actual['terminal_frame']==47650 and actual['original_docking_event_activation_and_normal_return_not_injected']
    assert actual['only_two_each16_byte_location_fixtures_no_town_event_RNG_outcome_ownership'] and actual['all_readonly_callbacks_zero_errors_mismatches_host_restored']
    cap=next(Path(p) for p in actual['evidence'] if Path(p).name=='capture_report.json');report=read(cap);assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==47650
    tracepath=next(Path(p) for p in actual['evidence'] if Path(p).name=='commands.json');trace=read(tracepath);assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    rows=[r for r in trace['rows'] if r['source'].get('route')==2 and r['source'].get('block')==24 and r['source'].get('first_word')==0xC200];assert len(rows)==2 and [r['frame'] for r in rows]==pair['frames'] and [r['kind'] for r in rows]==['before_command','after_command'] and rows[1]['decoded_length']==2 and rows[1]['result_words'][0]==3
    payload=IlnkContainer.parse(old.read_file('/data/SC2.DK4')).blocks[24];assert payload[pair['actual_offset']:pair['actual_offset']+2]==b'\0\xc2'
    for r in rows:assert r['source']['whole_resident_payload_exact_ROM'] and sha(Path(r['source']['actual_payload_file']).read_bytes())==sha(payload)==r['source']['actual_sha256'] and r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
    spans=[]
    for start,end in [(0x20000,0x30000),(0x7F200,0x7F280),(0x904BC,0x904F4),(0xCB180,0xCB194)]:
        assert a[start:end]==b[start:end];spans.append(dict(start=start,end=end,sha256=sha(b[start:end]),actual_and_current_code_equal=True))
    mutable={'/COMMON/MESFILE.DK4','/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4'};assets=[]
    for _,path,data in old.iter_files():
        if path in mutable:continue
        assert current.read_file(path)==data,path;assets.append(dict(path=path,sha256=sha(data)))
    for path,data in old.iter_components():
        if path=='/__arm9__.bin':continue
        assert current.read_file(path)==data,path
    terminal=actual['terminal_capture'];assert terminal['frame']==47650 and sha(Path(terminal['path']).read_bytes())==terminal['PNG_sha256']
    C200=control['relocated_C200_pairs'];assert len(C200)==1 and C200[0]['block']==139
    for p in C200[0]['cases']:assert p['source_command_hex']=='00c2' and p['native_extent']==2 and p['native_result'][0]==3 and p['source_owned_UI_request_words']==[1,0,13,0,0,0,1] and len(p['source_owned_UI_writes'])==9 and p['native_presentation_resource_bodies_not_executed'] and p['all_other4MiB_actor_roster_event_RNG_and_models_exact']
    ROOT.mkdir(parents=True);save(ROOT/'existing_actual_C200_normal_return_current_code_asset_binding.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),actual_ROM=str(oldpath),actual_ROM_sha256=actual['candidate_sha256'],current_ROM=str(CURRENT),current_ROM_sha256=sha(CURRENT.read_bytes()),current_native_control_proof=str(CONTROL),current_native_control_proof_sha256=sha(CONTROL.read_bytes()),source_native_contract=str(SOURCE),source_native_contract_sha256=sha(SOURCE.read_bytes()),actual_source_C200_pair=pair,actual_normal_return_frame=47650,actual_terminal_capture=terminal,terminal_capture_viewed_current_turn=True,observed_terminal='Amsterdam town screen with complete top town information and lower town/Port UI.',exact_shared_native_code_spans=spans,all_nontext_native_resource_files_exact=assets,source_two_byte_C200_no_translated_operand_or_resource_change=True,actual_B24_gameplay_is_historical_and_not_selected_B139_B140=True,actual_two16_byte_coordinate_fixtures_explicit=True,current_offline_mode1_index0_context13_queue_request_preserved=True,actual_dynamic_queue_arguments_not_inferred_from_later_town_snapshot=True,current_offline_two_resource_bodies_remain_unexecuted=True,shared_C200_result3_extent2_and_normal_return_behavior_class_has_actual_evidence=True,no_fabricated_MMIO_state_or_current_resource_execution_claim=True,type3_result_tail_stale_in_actual_VM_not_semantic=True,no_new_concrete_C200_control_or_resource_change_requires_individual_scene_visit=True,no_selected_map_acquisition_polder_funding_or_outcome_claim=True,new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,CURRENT,CONTROL,SOURCE,cap,tracepath,Path(terminal['path']),Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Historical actual B24 C20047368-47369 and normal return47650 bind to current exact shared code/resources. Two coordinate fixtures disclosed. B139 selected gameplay and current offline resource-body execution remain unclaimed.')
