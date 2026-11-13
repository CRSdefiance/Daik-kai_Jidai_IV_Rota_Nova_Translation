"""Bind shipped native callers andall116 mapped commands to the exact research image."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.create_Maria_confrontation_reference_v7805 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_reference_census_v7807')
CURRENT=Path('work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json')
LOADER=Path('work/analysis/maria_confrontation_loaders_v7806/303_whole_native_loads_cache_hits606_initial_parent_modes.json')
PRIOR=Path('work/analysis/maria_B207_reference_census_v7700/Maria_all20_commands_one_entry_one_fresh_shipped_caller_census.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,current,loader,prior=map(read,[PLAN,CURRENT,LOADER,PRIOR])
    assert loader['fresh_native_whole_loads_andcache_hits']==303 and loader['fresh_initial_parent_modes']==606
    assert sha(ROM.read_bytes())==loader['research_ROM_sha256'] and sha(PARENT.read_bytes())==mapping['candidate_sha256']
    for key in ['load','parent_mode']:assert sha(Path(loader[key+'_proof']).read_bytes())==loader[key+'_sha256']
    image,parent=NdsImage.open(ROM),NdsImage.open(PARENT)
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    fresh=census(image);assert fresh==prior['native_call_census']['research']
    groups=[];bank=IlnkContainer.parse(image.read_file(mapping['file_path'])).blocks
    for cg,tg in zip(current['groups'],mapping['groups'],strict=True):
        assert cg['block']==tg['block'];block=bank[tg['block']]
        assert sha(block)==tg['target_block_sha256'] and block[:8].hex()==tg['target_header_hex']
        rows=[]
        for source,before,after,m in zip(cg['all_source_commands'],cg['all_current_commands'],tg['all_target_commands'],tg['command_map'],strict=True):
            assert source['word']==before['word']==after['word']==m['word']
            assert before['offset']==m['old_offset'] and after['offset']==m['new_offset']
            assert before['native_extent']==m['old_extent'] and after['native_extent']==m['new_extent']
            assert before['ancestor_0100_offsets']==m['source_0100_ancestors'] and after['ancestor_0100_offsets']==m['target_0100_ancestors']
            at=after['offset'];assert block[at:at+after['native_extent']].hex()==after['whole_command_hex']
            if source['word'] not in [0x4000,0x100,0x200,0x300,0x400]:assert source['whole_command_hex']==before['whole_command_hex']==after['whole_command_hex']
            rows.append(deepcopy(m))
        assert sum(c['word']==0 for c in rows)==1 and rows[-1]['new_offset']+4==tg['target_logical_end']
        groups.append(dict(file_path=tg['file_path'],block=tg['block'],source_header_hex=cg['source_header_hex'],current_header_hex=cg['current_header_hex'],
            target_header_hex=tg['target_header_hex'],all_command_maps=rows,source_current_target_walks_reused_byexact_whole_block_hashes=True,
            relative_operand_maps=deepcopy(tg['relative_fixups']),relocated_relative_cases=deepcopy(tg['relocated_skip_cases']),
            original_entry_payload_offset=8,source_andtarget_storage_tails_not_interpreted_as_terminal=True))
    assert sum(len(g['all_command_maps']) for g in groups)==22 and sum(len(g['relative_operand_maps']) for g in groups)==0
    ROOT.mkdir(parents=True);save(ROOT/'all22_commands_original_B36_entry_no_relative_sites_shipped_callers.json',dict(
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        groups=groups,native_call_census=dict(research=fresh,exact_prior_same_decoded_units_reference=prior['native_call_census']['research']),
        fresh_caller_censuses=1,all_shipped_decoded_native_units_bound=True,only_original24070_interpreter_call_no_literal_alias=True,
        all_original_EV3_block_indices_and303_load_cache_paths606_parent_modes_verified=True,
        all22_source_current_target_commands_no_relative_sites_bound_to_actual_ROM_bytes=True,
        all16_sixbyte_speech_preambles_six_numeric_leaves_andfourbyte_end_preserved=True,
        no_new_source_current_orrelocated_walk_reexecution_when_hashes_exact=True,
        native_caller_entry_proof_not_ordinary_optional_eligibility_orarbitrary_dynamic_mutation_claim=True,
        actual_button_pagination_headers_scene_transitions_effects_policy_production_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,CURRENT,LOADER,PRIOR,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('22mapped commands/no relative sites/one original block entry;one fresh shipped caller census exact.303native loads606parent modes bound.Actual/policy/release pending.')
