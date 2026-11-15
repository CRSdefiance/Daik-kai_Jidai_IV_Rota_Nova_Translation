"""Seal the complete B221 source/current/final references after native and actual checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.lil_B221_profile_v1 import contract
from dk4tool.patch.grand_race_menu_release import sha
from scripts.create_lil_B221_reference_v6997 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_reference_approval_v7007')
OLD=Path('translations/lil_B221_editorial_manuscript_v2.json');OUTPUT=Path('translations/lil_B221_editorial_manuscript_v3.json')
OLD_MENU=Path('translations/lil_B221_choice_manuscript_v2.json');OUTPUT_MENU=Path('translations/lil_B221_choice_manuscript_v3.json')
MAP=Path('translations/lil_B221_editorial_relocation_map_v1.json')
ENTRY=Path('work/analysis/lil_B221_entry_v6969/source_EV2_B221_action_dependency_and_native_getter_binding.json')
LOADER=Path('work/analysis/lil_B221_loader_v6998/whole_SC2_and_B221_initial_entry_proof.json')
CENSUS=Path('work/analysis/lil_B221_reference_census_v6999/all21_commands_four_relatives_one_menu_and_shipped_census.json')
FLAGS=['all16_exact_clean_current_compiled_stored_references_bound','complete1208_byte_predecessor_inverse',
       'all21_commands_preambles_four_relatives_one_menu_A000_and_normal_end_preserved',
       'all335_other_SC2_blocks_exact','native_stored_complete_glyphs_zero_macros_bounds_and_pages_pass',
       'external_references_complete','all14_actual_English_speeches_both_choice_paths_explicit',
       'only_R46_R60_two_pages_with_original_A_advancement','both_choice_value_words0_1_preserved_at_normal_end',
       'two_personal_name_retentions_current_role_preservation_and_all_later_limits_preserved',
       'seven_individual_row_reasons25_boundaries_and_all_QA_diagnostics_retained','exact_R67_had_gone_boundary_carried_per_record']

if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [OUTPUT,OUTPUT_MENU,MAP])
    doc,choices,plan,loader,census=map(read,[OLD,OLD_MENU,PLAN,LOADER,CENSUS])
    actual=read(doc['actual_English_proof']);view=read(doc['actual_English_view']);c=contract()
    assert len(doc['records'])==14 and len(choices['records'])==2
    assert all(all(r['review'].values()) for r in doc['records']+choices['records'])
    assert not actual['failures'] and actual['actual_unique_speeches']==14 and actual['actual_complete_native_page_observations']==30
    assert actual['all30_stored_commands_executed_in_union'] and not view['visual_review_pending']
    assert loader['all336_whole_blocks_and672_modes_each_pass'] and census['all21_clean_current_target_commands_bound']
    assert [(v['normal_terminal_result'],v['exit_frame']) for v in actual['versions']]==[([0,0],6693),([0,1],6693)]
    mapping=deepcopy(plan);mapping.update(format='dk4-lil-B221-source-relocation-map-v1',
        required_runtime_ARM9_sha256=doc['current_ARM9_sha256'],target_ROM=str(ROM),target_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),
        choice_manuscript=str(OLD_MENU),choice_manuscript_sha256=sha(OLD_MENU.read_bytes()),not_release_map_or_candidate=False)
    spec=mapping['blocks'][0]
    spec['clean_block_sha256']=read(mapping['source_context'])['blocks'][0]['clean_block_sha256']
    for name in ['block_sha256','bytes','logical_end','tail_bytes','block']:spec['target_'+name]=spec['research_'+name]
    assert (spec['source_bytes'],spec['source_logical_end'],spec['source_tail_bytes'],spec['target_bytes'],spec['target_logical_end'],spec['target_tail_bytes'])==(1208,1208,0,1224,1224,0)
    assert len(spec['text_records'])==14 and len(spec['choice_commands'])==1 and len(spec['all_object_references'])==16
    assert len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20
    assert spec['original_A000_map']==[dict(source_offset=1196,target_offset=1212,extent=8,source_hex='00a0ffff47000110')]
    assert spec['complete_end_map']==[dict(source_offset=1204,target_offset=1220,extent=4,source_hex='00000000',source_four_zero_bytes_exact=True)]
    spec['external_references_complete']=True
    for row in doc['records']:
        binding=c['record_bindings'][row['id']]
        assert row['reviewed_ordinary_boundaries']==binding['ordinary_wrap_reasons']
        assert row['reviewed_native_page_boundary']==binding['page_boundary_reason']
        assert row['informational_row_count_reason']==binding['row_count_reason']
        assert row['native_page_count']==binding['native_page_count']
    for flag in FLAGS:mapping[flag]=True
    paths=[PLAN,OLD,OLD_MENU,ENTRY,LOADER,CENSUS,Path(doc['actual_source_proof']),Path(doc['actual_English_proof']),Path(doc['actual_English_view']),
        Path(doc['native_font_proof']),Path(doc['native_stored_proof']),Path(doc['native_name_proof']),Path(doc['relocated_control_proof']),
        Path(doc['speaker_name_review']),Path(doc['policy_validation']),Path(doc['later_scope_proof']),
        Path('work/analysis/lil_B221_stored_choices_v6996/one_final_typed_object_two_references_and_both_even_alignments.json'),
        Path('scripts/create_lil_B221_reference_v6997.py'),Path(__file__)]
    mapping['evidence'].update({str(p):sha(p.read_bytes()) for p in paths});save(MAP,mapping);ROOT.mkdir(parents=True)
    seal=ROOT/'all16_five_gates_and_exact_references_approved.json'
    for old,path,value in [(OLD,OUTPUT,doc),(OLD_MENU,OUTPUT_MENU,choices)]:
        final=deepcopy(value);final.update(native_approved_manuscript=str(old),native_approved_manuscript_sha256=sha(old.read_bytes()),
            reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(seal),
            reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),
            status='all16 contextual/source/native/reference/actual gates approved;registered release patch and startup pending')
        save(path,final)
    save(seal,dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        choice_manuscript=str(OUTPUT_MENU),choice_manuscript_sha256=sha(OUTPUT_MENU.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),all16_five_gates_and_exact_references_approved=True,
        flags=FLAGS,all_actual_offline_natural_gameplay_and_unresolved_name_limits_preserved=True,
        source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('Sealed B221 manuscriptsv3/mapv1:16 records,1208-byte inverse,21 commands,four relatives,one menu,16 pages and actual paths. No credit yet.')
