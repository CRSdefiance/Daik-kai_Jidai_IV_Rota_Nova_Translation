"""Seal exact source/current/compiled/stored references without granting registered completion credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_reference_approval_v6481')
INPUT=Path('translations/lil_B209_editorial_manuscript_v2.json')
OUTPUT=Path('translations/lil_B209_editorial_manuscript_v3.json')
MAP=Path('translations/lil_B209_editorial_relocation_map_v1.json')
PLAN=Path('work/analysis/lil_B209_relocation_research_v6466/nested20_object_relocation_RESEARCH_ONLY.json')
ENTRY=Path('work/analysis/lil_B209_entry_v6471/source_EV2_B209_action_dependency_and_native_getter_binding.json')
LOADER=Path('work/analysis/lil_B209_loader_v6472/whole_SC2_and_B209_initial_entry_proof.json')
CENSUS=Path('work/analysis/lil_B209_reference_census_v6473/all18_commands_four_relative_sites_and_shipped_entry_census.json')
CONTROL=Path('work/analysis/lil_B209_relocated_controls_v6476/all20_dispatches_two_whole_styles414_slots_predicate_staging_and_complete_ends.json')
ACTUAL=Path('work/analysis/lil_B209_actual_v6474/six_English_objects_eight_native_pages24_commands_and_source_differences.json')
VIEW=Path('work/analysis/lil_B209_actual_view_v6477/eight_actual_pages25_complete_holds_names_returns_and_later_scope_viewed.json')
ROM=Path('out/lil_B209_reference_v6468_RESEARCH_ONLY.nds')
PARENT=Path('out/all_routes_combined_v6439_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not MAP.exists();doc,plan,entry,loader,census,controls,actual,view=map(read,[INPUT,PLAN,ENTRY,LOADER,CENSUS,CONTROL,ACTUAL,VIEW]);approval=read(doc['native_approval'])
    assert approval['manuscript_sha256']==sha(INPUT.read_bytes()) and approval['all20_five_gates_approved'] and all(all(r['review'].values()) for r in doc['records'])
    assert loader['all336_whole_blocks_and672_modes_each_pass'] and census['all18_clean_current_target_commands_and_four_relative_sites_reexecuted'] and len(controls['relocated_dispatch_cases'])==20 and len(controls['whole_relocated4100_commands'])==2 and len(controls['all207_actor_two_style_command_pointer_cases']['cases'])==414
    assert controls['predicate_type2_Boolean0_preserved'] and len(controls['structural_source4500_4621_A000_cases'])==5 and len(controls['target_five_complete_end_cases'])==5
    assert not actual['failures'] and not actual['command_result_differences'] and not actual['command_UI_word_differences'] and not view['upper_scene_and_portrait_differences'] and not view['visual_review_pending']
    assert [(r['event_ID'],r['script_block'],r['action_index'],r['must_be_completed']) for r in entry['selected_B209_source_events']]==[(209,209,210,[85])]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256'] and sha(ROM.read_bytes())==controls['research_ROM_sha256']==census['research_ROM_sha256']
    source=read(doc['source_context']);spec=deepcopy(plan['blocks'][0]);old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[209] for p in [PARENT,ROM]];rows={r['id']:r for r in doc['records']};refs=[]
    for r in spec['text_records']:
        row=rows[r['id']];r.update(kind='progressive',source_reference=deepcopy(row['source_reference']),current_reference=deepcopy(row['current_reference']),current_record_index=row['current_record_index'],compiled_hex=row['compiled_hex'],source_preamble_hex=row['source_complete_preamble_hex']);refs.append(r)
    for obj in spec['actor_style_commands']:
        for r in obj['alternative_records']:
            row=rows[r['id']];r.update(kind='typed-4100-actor-style-alternative',source_reference=deepcopy(row['source_reference']),current_reference=deepcopy(row['current_reference']),current_record_index=row['current_record_index'],compiled_hex=row['compiled_hex'],source_selector=208,old_command_offset=obj['old_offset'],new_command_offset=obj['new_offset'],virtual_formatter_selector_not_stored=True);refs.append(r)
    assert len(refs)==len({r['id'] for r in refs})==20
    for r in refs:
        row=rows[r['id']];before=bytes.fromhex(row['current_hex']);after=bytes.fromhex(r['target_hex']);assert old[r['old_offset']:r['old_offset']+len(before)+1]==before+b'\0' and new[r['new_offset']:r['new_offset']+len(after)+1]==after+b'\0'
        compiled=bytes.fromhex(row['compiled_hex']);compiled=compiled if row['kind']=='progressive' else compiled[1:];assert after in [compiled,compiled+b' ']
    mapped=[dict(word=m['word'],old_offset=m['old_offset'],new_offset=m['new_offset'],old_native_extent=m['old_extent'],new_native_extent=m['new_extent']) for m in spec['command_map']]
    assert len(mapped)==18 and len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20 and spec['inverse_recovers_every_original1148_byte']
    spec.update(file_path='/data/SC2.DK4',clean_block_sha256=source['blocks'][0]['clean_block_sha256'],target_block_sha256=spec['research_block_sha256'],target_bytes=1336,target_logical_end=1334,target_tail_bytes=2,entry_point_offset=8,text_records=refs,mapped_native_commands=mapped,all20_clean_current_compiled_stored_references_bound=True,all18_original_command_types_preambles_opaque_operands_and_aliases_preserved=True,external_references_complete=True,no_external_interior_byte_aliases_from_shipped_census=True,natural_event209_dependency85_and_outer_eligibility_not_executed=True)
    proofpaths=[INPUT,PLAN,ENTRY,LOADER,CENSUS,CONTROL,ACTUAL,VIEW,Path(doc['native_approval']),Path(doc['native_font_proof']),Path(doc['native_stored_proof']),Path(doc['native_policy_validation']),Path(doc['speaker_names_review']),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths};ROOT.mkdir(parents=True)
    save(MAP,dict(format='dk4-source-bound-nested-relocation-map-v1',file_path='/data/SC2.DK4',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),clean_ROM='work/clean.nds',clean_ROM_sha256=doc['source_ROM_sha256'],source_SC2_sha256=plan['source_SC2_sha256'],target_SC2=plan['target_SC2'],target_SC2_sha256=plan['target_SC2_sha256'],manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),blocks=[spec],external_references_complete=True,all20_records5_speeches15_stored_alternatives16_slots_two_typed_objects_bound=True,all_four_relative_source_target_operands_and20_native_cases_bound=True,source1148_full_inverse_target1336_logical1334_tail2_complete_end1330=True,native_original_four_row_pagination_and_source_names_controls_preserved=True,representative_English6_objects8_pages25_holds_and14_offline_objects_explicit=True,all_measured_later_limits_preserved=True,evidence=evidence,registered_integration_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    previous=deepcopy(doc);doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),native_approved_manuscript=str(INPUT),native_approved_manuscript_sha256=sha(INPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),reference_approval=str(ROOT/'approval_receipt.json'),all20_source_prose_native_reference_and_representative_decisions_sealed=True,registered_integration_pending=True,status='all20 decisions sealed;atomic registered integration clean-input patch and current startup pending',source_prose_or_completion_credit_added=0)
    assert doc['records']==previous['records'] and doc['current_ROM']==str(PARENT) and doc['current_ROM_sha256']==sha(PARENT.read_bytes());save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),native_approved_manuscript=str(INPUT),native_approved_manuscript_sha256=sha(INPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),all20_five_gates_and_exact_reference_obligations_approved=True,twenty_disjoint_objects17_revisions3_retentions_uncredited=True,all_names_controls_slots_aliases_relative_spans_bounds_and_native_pages_bound=True,actual6_objects8_pages25_body_name_holds_not_all20_gameplay=True,all12_timing12_RNG_two_duration187_broader_RGB_and_final_state_limits_preserved=True,original_event209_dependency85_not_natural_activation_or_earned_progress=True,source_prose_or_completion_credit_added=0,atomic_registered_integration_clean_input_patch_and_current_startup_pending=True,evidence=evidence,full_goal_complete=False))
    print('B20920 decisions sealed in manuscriptv3/mapv1:all1148 predecessor bytes reversible;1336stored/1334logical/tail2;18commands,15typed bodies/16slots,four relatives/20cases. Atomic registered integration/patch/startup pending;zero credit.')
