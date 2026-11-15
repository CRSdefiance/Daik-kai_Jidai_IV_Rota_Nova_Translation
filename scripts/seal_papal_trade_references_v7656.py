"""Seal two exact approved exchanges and complete reversible file-qualified relocation maps."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_final_paths_v7655 import *
from scripts.verify_village_wrap_v608 import read,save
FLAGS=['external_references_complete','all40_commands36_complete_preambles_voices_zero_macros_preserved','both1468_predecessor_blocks_andarchives_invert_exactly','both1508_logical1506_tail2_targets_bound','all36_source_current_compiled_stored_andactual_refs_bound','all668_native_loads1336_parent_modes_andshipped_caller_bound','all_measured_late_differences_andnatural_activation_limits_preserved','four_scoped_name_retentions_no_assets_orfull207_approval','full_four_storyline_editorial_names_andretrospective_wrapping_objective_open']
if __name__=='__main__':
    assert not SEAL.parent.exists() and not MAP.exists() and all(not p.exists() for p in SEALED.values())
    plan,approval,loader,census,entry,actual,later,view=map(read,[PLAN,APPROVAL,LOADER,CENSUS,ENTRY,ACTUAL,LATER,VIEW])
    assert approval['all36_individual_five_gates_approved'] and loader['fresh_native_whole_loads_andcache_hits']==668 and loader['fresh_initial_parent_modes']==1336
    assert census['only_original_24070_interpreter_call_no_literal_alias'] and view['all72_complete_source_English_speech_panes_individually_viewed']
    assert sha(PARENT.read_bytes())==plan['candidate_sha256'] and [(g['selected_source_events'][0]['event_ID'],g['selected_source_events'][0]['action_index']) for g in entry['groups']]==[(246,247),(237,238)]
    for g in entry['groups']:assert g['selected_source_events'][0]['must_be_completed']==g['selected_source_events'][0]['must_not_be_completed']==[]
    before,after=[NdsImage.open(p) for p in [PARENT,ROM]];source=read(CURRENT);groups=[];observed=[]
    for route,path in APPROVED.items():
        doc=read(path);assert all(all(r['review'].values()) for r in doc['records']) and approval['manuscripts'][route]['sha256']==sha(path.read_bytes())
        spec=deepcopy(plan['groups'][route]);file=spec['file_path'];n=spec['block']
        old,new=[IlnkContainer.parse(im.read_file(file)).blocks[n] for im in [before,after]]
        assert (len(old),spec['source_logical_end'],spec['source_tail_bytes'],len(new),spec['research_logical_end'],spec['research_tail_bytes'])==(1468,1468,0,1508,1506,2)
        rows={r['id']:r for r in doc['records']};refs=[]
        for ref in spec['text_records']:
            row=rows[ref['id']];raw=bytes.fromhex(row['current_hex']);value=bytes.fromhex(ref['target_hex']);compiled=bytes.fromhex(row['compiled_hex'])
            assert old[ref['old_offset']:ref['old_offset']+len(raw)+1]==raw+b'\0' and new[ref['new_offset']:ref['new_offset']+len(value)+1]==value+b'\0' and value in [compiled,compiled+b' ']
            assert old[ref['old_offset']-5:ref['old_offset']+1].hex()==new[ref['new_offset']-5:ref['new_offset']+1].hex()==row['source_complete_preamble_hex'];refs.append(deepcopy(ref))
        assert len(refs)==18 and not any(spec[k] for k in ['choice_commands','actor_style_commands','relative_skip_fixups','target_native_skip_cases','original_C200_map','original_630B_map'])
        spec.update(clean_block_sha256=source['groups'][route]['clean_block_sha256'],target_block_sha256=sha(new),target_bytes=1508,target_logical_end=1506,target_tail_bytes=2,entry_point_offset=8,external_references_complete=True,no_external_interior_byte_aliases_from_shipped_census=True,all_object_references=refs,mapped_native_commands=deepcopy(census['groups'][route]['mapped_commands']),approved_manuscript=str(path),approved_manuscript_sha256=sha(path.read_bytes()))
        groups.append(spec);l=later['groups'][route];ag=next(g for g in actual['groups'] if g['route']==route and g['version']=='English')
        observed.append(dict(route=route,source_English_exits=l['source_English_exits'],body_holds=ag['complete_body_holds'],name_holds=ag['complete_name_holds'],command_difference_rows=len(l['command_comparison_differences']),duration_changes=len(l['duration_differences']),later_samples=l['later_sample_count'],later_RGB_differences=len(l['later_RGB_differences']),component_equality=l['five_native_component_equality'],actors_equal=l['whole_actors_equal'],captains=l['captain_IDs'],PRNG_seeds=l['final_PRNG_seeds']))
    assert [(g['later_RGB_differences'],g['later_samples'],g['command_difference_rows'],g['duration_changes']) for g in observed]==[(3,133,19,7),(53,133,19,7)]
    paths=[*APPROVED.values(),PLAN,APPROVAL,*map(Path,proofs().values()),Path(__file__)];evidence={str(p):sha(p.read_bytes()) for p in paths}
    save(MAP,dict(format='dk4-papal-trade-source-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=read(source['source_packet'])['source_ROM_sha256'],groups=groups,preserve_record_parity=True,required_runtime_ARM9_sha256=source['current_ARM9_sha256'],observed_comparison_contract=observed,evidence=evidence,registered_integration_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False,**{k:True for k in FLAGS}))
    sealed=[]
    for route,path in APPROVED.items():
        doc=deepcopy(read(path));doc.update(previous_manuscript=str(path),previous_manuscript_sha256=sha(path.read_bytes()),native_approved_manuscript=str(path),native_approved_manuscript_sha256=sha(path.read_bytes()),native_approval_sha256=sha(APPROVAL.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(SEAL),reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),all18_source_native_reference_andactual_decisions_sealed=True,status='all18 exact decisions sealed;atomic registered integration pending')
        save(SEALED[route],doc);sealed.append(dict(route=route,path=str(SEALED[route]),sha256=sha(SEALED[route].read_bytes()),approved_manuscript=str(path),approved_manuscript_sha256=sha(path.read_bytes())))
    SEAL.parent.mkdir(parents=True)
    save(SEAL,dict(manuscripts=sealed,reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),all36_five_gates_andexact_references_approved=True,all40_commands_both_A000_ends_andfull_predecessor_inverse_bound=True,observed_comparison_contract=observed,all_measured_late_differences_andnatural_activation_limits_preserved=True,full207_names_andearlier_consumer_review_open_no_assets_orcredits=True,source_item106_no_asset_card_mechanic_other_consumer_approval=True,source_prose_or_completion_credit_added=0,evidence=evidence,full_goal_complete=False))
    print('36 decisions sealed in two manuscripts/one file-qualified map;all40 commands,both1508/logical1506/tail2 targets andmeasured late limits bound. Zero credit;atomic registered integration pending.')
