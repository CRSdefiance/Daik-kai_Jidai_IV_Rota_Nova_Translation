"""Seal the complete approved Maria exchange andits exact reversible file-qualified map."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Maria_B207_final_paths_v7712 import *
from scripts.verify_village_wrap_v608 import read,save
FLAGS=['external_references_complete','all20_commands18_complete_preambles_voices_zero_macros_preserved','complete_clean_block_andpredecessor_archive_inverse_exact','target1472_logical1470_tail2_bound','all18_source_current_compiled_stored_andactual_refs_bound','all303_native_loads606_parent_modes_andshipped_caller_bound','distinct_CS0101_header_preserved','all_measured_late_differences_andnatural_activation_limits_preserved','two_scoped_name_retentions_no_assets_orfull207_approval','full_four_storyline_editorial_names_andretrospective_wrapping_objective_open']
if __name__=='__main__':
    assert not SEAL.parent.exists() and not MAP.exists() and all(not p.exists() for p in SEALED.values())
    plan,approval,loader,census,entry,actual,later,view=map(read,[PLAN,APPROVAL,LOADER,CENSUS,ENTRY,ACTUAL,LATER,VIEW])
    assert approval['all18_individual_five_gates_approved'] and loader['fresh_native_whole_loads_andcache_hits']==303 and loader['fresh_initial_parent_modes']==606
    assert census['only_original_24070_interpreter_call_no_literal_alias'] and view['all36_complete_source_English_speech_panes_individually_viewed']
    assert sha(PARENT.read_bytes())==plan['candidate_sha256']
    event=entry['selected_source_event'];assert (event['event_ID'],event['action_index'],event['script_block'],event['must_be_completed'],event['must_not_be_completed'])==(207,208,207,[],[])
    before,after,clean=[NdsImage.open(p) for p in [PARENT,ROM,'work/clean.nds']];source=read(CURRENT);groups=[];observed=[]
    for route,path in APPROVED.items():
        assert route==3;doc=read(path);assert all(all(r['review'].values()) for r in doc['records'])
        ap=next(r for r in approval['manuscripts'] if r['route']==3);assert ap['sha256']==sha(path.read_bytes())
        spec=deepcopy(plan['groups'][0]);file=spec['file_path'];n=spec['block'];assert (spec['route'],file,n)==(3,'/data/SC3.DK4',207)
        old,new,jp=[IlnkContainer.parse(im.read_file(file)).blocks[n] for im in [before,after,clean]]
        assert (len(old),spec['source_logical_end'],spec['source_tail_bytes'],len(new),spec['research_logical_end'],spec['research_tail_bytes'])==(1468,1468,0,1472,1470,2)
        assert old[:8].hex()==jp[:8].hex()=='43530101b4050000' and new[:4]==old[:4] and new[6:8]==old[6:8]
        rows={r['id']:r for r in doc['records']};refs=[]
        for ref in spec['text_records']:
            row=rows[ref['id']];raw=bytes.fromhex(row['current_hex']);value=bytes.fromhex(ref['target_hex']);compiled=bytes.fromhex(row['compiled_hex'])
            assert old[ref['old_offset']:ref['old_offset']+len(raw)+1]==raw+b'\0' and new[ref['new_offset']:ref['new_offset']+len(value)+1]==value+b'\0' and value in [compiled,compiled+b' ']
            assert old[ref['old_offset']-5:ref['old_offset']+1].hex()==new[ref['new_offset']-5:ref['new_offset']+1].hex()==row['source_complete_preamble_hex']
            assert new[:ref['new_offset']].count(b'\0')==ref['new_record_index'];refs.append(deepcopy(ref))
        assert len(refs)==18 and not any(spec[k] for k in ['choice_commands','actor_style_commands','relative_skip_fixups','target_native_skip_cases','original_C200_map','original_630B_map'])
        inverse,sourceinverse=bytearray(new[:1470]),bytearray(new[:1470]);struct.pack_into('<H',inverse,4,1460);struct.pack_into('<H',sourceinverse,4,1460)
        for ref in reversed(sorted(refs,key=lambda r:r['new_offset'])):
            at=ref['new_offset'];inverse[at:at+ref['new_length']]=bytes.fromhex(ref['old_hex']);sourceinverse[at:at+ref['new_length']]=bytes.fromhex(rows[ref['id']]['source_hex'])
        assert bytes(inverse)==old and bytes(sourceinverse)==jp
        targetbank=IlnkContainer.parse(after.read_file(file));restored=list(targetbank.blocks);restored[n]=bytes(inverse)
        assert IlnkContainer(restored).to_bytes()==before.read_file(file) and [i for i,(a,b) in enumerate(zip(IlnkContainer.parse(before.read_file(file)).blocks,targetbank.blocks,strict=True)) if a!=b]==[207]
        spec.update(clean_block_sha256=source['clean_block_sha256'],target_block_sha256=sha(new),target_bytes=1472,target_logical_end=1470,target_tail_bytes=2,entry_point_offset=8,external_references_complete=True,no_external_interior_byte_aliases_from_shipped_census=True,all_object_references=refs,mapped_native_commands=deepcopy(census['groups'][0]['mapped_commands']),approved_manuscript=str(path),approved_manuscript_sha256=sha(path.read_bytes()))
        groups.append(spec);l=later['groups'][0];ag=next(g for g in actual['groups'] if g['route']==3 and g['version']=='English')
        observed.append(dict(route=3,source_English_exits=l['source_English_exits'],body_holds=ag['complete_body_holds'],name_holds=ag['complete_name_holds'],command_difference_rows=len(l['command_comparison_differences']),duration_changes=len(l['duration_differences']),later_samples=l['later_sample_count'],later_RGB_differences=len(l['later_RGB_differences']),component_equality=l['five_native_component_equality'],actors_equal=l['whole_actors_equal'],captains=l['captain_IDs'],PRNG_seeds=l['final_PRNG_seeds']))
    assert len(groups)==1 and [(r['later_RGB_differences'],r['later_samples'],r['command_difference_rows'],r['duration_changes']) for r in observed]==[(104,123,19,8)]
    paths=[*APPROVED.values(),PLAN,APPROVAL,*map(Path,proofs().values()),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths}
    save(MAP,dict(format='dk4-Maria-B207-source-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),groups=groups,preserve_record_parity=True,required_runtime_ARM9_sha256=source['current_ARM9_sha256'],observed_comparison_contract=observed,evidence=evidence,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,registered_integration_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False,**{k:True for k in FLAGS}))
    sealed=[]
    for route,path in APPROVED.items():
        doc=deepcopy(read(path));doc.update(previous_manuscript=str(path),previous_manuscript_sha256=sha(path.read_bytes()),native_approved_manuscript=str(path),native_approved_manuscript_sha256=sha(path.read_bytes()),native_approval_sha256=sha(APPROVAL.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(SEAL),reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),all18_source_native_reference_andactual_decisions_sealed=True,status='all18 exact decisions sealed;atomic registered integration pending')
        save(SEALED[route],doc);sealed.append(dict(route=route,path=str(SEALED[route]),sha256=sha(SEALED[route].read_bytes()),approved_manuscript=str(path),approved_manuscript_sha256=sha(path.read_bytes())))
    SEAL.parent.mkdir(parents=True);save(SEAL,dict(manuscripts=sealed,reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),all18_five_gates_andexact_references_approved=True,all20_commands_A000_end_full_clean_andpredecessor_inverse_bound=True,distinct_CS0101_preserved=True,observed_comparison_contract=observed,all_measured_late_differences_andnatural_activation_limits_preserved=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,full207_names_andearlier_consumer_review_open_no_assets_orcredits=True,source_item106_no_asset_card_mechanic_other_consumer_approval=True,source_prose_or_completion_credit_added=0,evidence=evidence,full_goal_complete=False))
    print('Maria18 sealed inone manuscript/map;all20 commands,CS0101,target1472/logical1470/tail2,full clean/predecessor inverse andmeasured limits bound. Zero credit;atomic integration pending.')
