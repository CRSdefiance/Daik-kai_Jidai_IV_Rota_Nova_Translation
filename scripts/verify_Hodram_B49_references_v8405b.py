"""Bind all B49 commands/entries and a fresh shipped-code caller census to the research ROM."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_references_v8405b')
REFERENCE=Path('work/analysis/Hodram_B49_reference_v8403/research_image_receipt.json')
CURRENT=Path('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')
MAP=Path('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')
LOADER=Path('work/analysis/Hodram_B49_loaders_v8404/325_whole_native_loads_cache_hits650_initial_parent_modes.json')
CONTROLS=Path('work/analysis/Hodram_B49_controls_v8401d/stored_controls.json')
PRIOR=Path('work/analysis/Hodram_outcome_reference_census_v8331/all15_commands_zero_relative_sites6_records_two_EV1_entries_shipped_callers.json')

if __name__=='__main__':
    assert not ROOT.exists();reference,current,mapping,loader,controls,prior=map(read,[REFERENCE,CURRENT,MAP,LOADER,CONTROLS,PRIOR])
    assert loader['research_ROM_sha256']==reference['research_ROM_sha256']
    assert loader['fresh_native_whole_loads_andcache_hits']==325 and loader['fresh_initial_parent_modes']==650
    for key in ['load','parent_mode']:assert sha(Path(loader[key+'_proof']).read_bytes())==loader[key+'_sha256']
    image,parent=[NdsImage.open(reference[k]) for k in ['research_ROM','parent']]
    assert all(sha(Path(reference[k]).read_bytes())==reference[k+'_sha256'] for k in ['research_ROM','parent'])
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    assert image.read_file('/data/EV1.DK4')==parent.read_file('/data/EV1.DK4')==NdsImage.open('work/clean.nds').read_file('/data/EV1.DK4')
    fresh=census(image);assert fresh==prior['native_call_census']
    bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    a,b=current['groups'][0],mapping['groups'][0];block=bank[49]
    assert sha(block)==b['target_block_sha256'] and block[:8].hex()==b['target_header_hex']
    maps=[]
    for source,old,target,m in zip(a['all_source_commands'],a['all_current_commands'],b['all_target_commands'],b['command_map'],strict=True):
        assert source['word']==old['word']==target['word']==m['word']
        assert old['offset']==m['old_offset'] and target['offset']==m['new_offset']
        assert old['native_extent']==m['old_extent'] and target['native_extent']==m['new_extent']
        assert old['ancestor_0100_offsets']==m['source_0100_ancestors'] and target['ancestor_0100_offsets']==m['target_0100_ancestors']
        assert block[target['offset']:target['offset']+target['native_extent']].hex()==target['whole_command_hex']
        if target['word']==0x4000:assert source['whole_command_hex'][:12]==old['whole_command_hex'][:12]==target['whole_command_hex'][:12]
        elif target['word']==0x2100:
            menu=b['choice_commands'][0]
            assert source['whole_command_hex']==menu['clean_hex'] and old['whole_command_hex']==menu['old_hex'] and target['whole_command_hex']==menu['target_hex']
        elif target['word'] not in [0x100,0x200,0x300,0x400]:assert source['whole_command_hex']==old['whole_command_hex']==target['whole_command_hex']
        maps.append(deepcopy(m))
    assert len(maps)==36 and maps[-1]['word']==0 and maps[-1]['new_offset']+4==b['target_logical_end']
    assert len(b['relative_fixups'])==8 and sum(len(r['cases']) for r in b['relocated_skip_cases'])==40
    loads=read(loader['load_proof']);route=next(r for r in loads['routes'] if r['route']==1)
    selected=[r for r in route['actions'] if r['kind']==2 and r['native_selected_block']==49]
    assert len(selected)==1 and selected[0]['payload_sha256']==sha(block)
    events=a['source_event_records'];assert [(e['event_ID'],e['script_block'],e['must_be_completed']) for e in events]==[(49,49,[48])]
    assert len(controls['final_dispatches'])==14 and len(controls['normal_seeded_ends'])==25
    ROOT.mkdir(parents=True);save(ROOT/'references.json',dict(parent=reference['parent'],parent_sha256=reference['parent_sha256'],research_ROM=reference['research_ROM'],research_ROM_sha256=reference['research_ROM_sha256'],file_path='/data/SC1.DK4',block=49,all_command_maps=maps,relative_operand_maps=b['relative_fixups'],relocated_native_skip_cases=b['relocated_skip_cases'],all14_text_records=b['text_records'],typed_choice_records=b['choice_commands'],source_event_records=events,original_selected_action=selected[0],native_call_census=fresh,fresh_caller_censuses=1,exact_prior_census=str(PRIOR),all_shipped_decoded_native_units_andcomponents_bound=True,only_original24070_interpreter_call_no_literal_alias=True,all_original_EV1_block_indices325_loads650_parent_modes_verified=True,all36_commands14_full_preambles8_relatives2_choices_query_picture_hide_effects_andterminal_bound=True,original_entry_payload_offset=8,no_interior_entry_offsets_orunmapped_nested_relative_targets=True,event49_requires48_not_natural_eligibility_location_orfull_chronology_proof=True,external_references_complete=True,reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof=True,actual_B49_backing_controller_transitions_policy_atomic_registered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,CURRENT,MAP,LOADER,CONTROLS,PRIOR,Path(__file__)]}))
    print('B49:36 command maps/8 relative sites40cases/14 speeches2choices,originalEV1entry,325load-cache/650modes andfresh shipped-code census pass.Actual UI/policy/release pending.')
