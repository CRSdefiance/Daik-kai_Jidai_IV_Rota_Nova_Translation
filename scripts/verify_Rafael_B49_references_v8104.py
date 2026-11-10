"""Bind154commands,56relative spans,C281 andoriginal EV0entry to a fresh shipped caller census."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.create_Rafael_B49_reference_v8102 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_reference_census_v8104')
CURRENT=Path('work/analysis/Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json')
LOADER=Path('work/analysis/Rafael_B49_loaders_v8103/343_whole_native_loads_cache_hits686_initial_parent_modes.json')
PRIOR=Path('work/analysis/Rafael_B48_reference_census_v8048/all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json')
CONTROLS=Path('work/analysis/Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,current,loader,prior,controls=map(read,[PLAN,CURRENT,LOADER,PRIOR,CONTROLS])
    assert loader['fresh_native_whole_loads_andcache_hits']==343 and loader['fresh_initial_parent_modes']==686
    assert sha(ROM.read_bytes())==loader['research_ROM_sha256'] and sha(PARENT.read_bytes())==mapping['candidate_sha256']
    for key in ['load','parent_mode']:assert sha(Path(loader[key+'_proof']).read_bytes())==loader[key+'_sha256']
    image,parent=NdsImage.open(ROM),NdsImage.open(PARENT)
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    fresh=census(image);assert fresh==prior['native_call_census']['research']
    assert image.read_file('/data/EV0.DK4')==parent.read_file('/data/EV0.DK4')==NdsImage.open('work/clean.nds').read_file('/data/EV0.DK4')
    bank=IlnkContainer.parse(image.read_file(mapping['file_path'])).blocks
    cg,tg=current['groups'][0],mapping['groups'][0];block=bank[49]
    assert cg['block']==tg['block']==49 and sha(block)==tg['target_block_sha256'] and block[:8].hex()==tg['target_header_hex']
    rows=[]
    for source,before,after,m in zip(cg['all_source_commands'],cg['all_current_commands'],tg['all_target_commands'],tg['command_map'],strict=True):
        assert source['word']==before['word']==after['word']==m['word']
        assert before['offset']==m['old_offset'] and after['offset']==m['new_offset']
        assert before['native_extent']==m['old_extent'] and after['native_extent']==m['new_extent']
        assert before['ancestor_0100_offsets']==m['source_0100_ancestors'] and after['ancestor_0100_offsets']==m['target_0100_ancestors']
        at=after['offset'];assert block[at:at+after['native_extent']].hex()==after['whole_command_hex']
        if source['word']==0x4000:
            assert source['whole_command_hex'][:12]==before['whole_command_hex'][:12]==after['whole_command_hex'][:12]
        elif source['word'] not in [0x100,0x200,0x300,0x400]:
            assert source['whole_command_hex']==before['whole_command_hex']==after['whole_command_hex']
        rows.append(deepcopy(m))
    assert len(rows)==154 and sum(c['word']==0 for c in rows)==1 and rows[-1]['new_offset']+4==tg['target_logical_end']==3792
    assert len(tg['relative_fixups'])==56 and sum(len(r['cases']) for r in tg['relocated_skip_cases'])==280
    assert len(controls['final_dispatches'])==61 and len(controls['relocated_predicates_andqueries'])==14 and len(controls['normal_seeded_ends'])==25
    source=read(current['source_packet']);events=source['groups'][0]['source_event_records']
    assert [(e['event_ID'],e['action_index'],e['script_block'],e['must_be_completed']) for e in events]==[(49,50,49,[39])]
    ROOT.mkdir(parents=True)
    save(ROOT/'all154_commands56_relative_sites61_speeches_C281_EV0_entry_shipped_callers.json',dict(
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        file_path=mapping['file_path'],block=49,source_header_hex=cg['source_header_hex'],current_header_hex=cg['current_header_hex'],
        target_header_hex=tg['target_header_hex'],all_command_maps=rows,relative_operand_maps=tg['relative_fixups'],
        relocated_relative_cases=tg['relocated_skip_cases'],all61_text_records=deepcopy(tg['text_records']),
        native_call_census=dict(research=fresh,exact_prior_same_decoded_units_reference=prior['native_call_census']['research']),
        fresh_caller_censuses=1,all_shipped_decoded_native_units_bound=True,only_original24070_interpreter_call_no_literal_alias=True,
        all_original_EV0_block_indices_and343_load_cache_paths686_parent_modes_verified=True,
        all154_source_current_target_commands56_relative_sites_bound_to_research_ROM=True,
        all61_preambles_source00_02_09_thirteen_raw_predicates_one_query_sevenA000_C281_andcomplete_end_preserved=True,
        original_entry_payload_offset=8,no_interior_entry_offsets_orunmapped_nested_relative_targets=True,
        source_event49_action50_requires39_not_natural_eligibility=True,no_FE_or_typed_menu_source_consumers=True,
        no_repeated_walk_execution_when_exact_block_hashes_andcommand_maps_bound=True,
        caller_entry_checks_not_actual_event_selection_orarbitrary_dynamic_reference_proof=True,
        actual_body_seven_headers_C281_transitions_return_policy_production_andrelease_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,CURRENT,LOADER,PRIOR,CONTROLS,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B49 full reference:154commands/56relative sites/61speeches/C281,originalEV0entry/shippedcallers bound.Actual scenes/policy/production/release pending.')
