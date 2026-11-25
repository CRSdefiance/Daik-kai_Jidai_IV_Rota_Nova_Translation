"""Bind the shipped caller census andall20 Maria clean/current/relocated command boundaries."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.create_Maria_B207_reference_v7698 import ROM,PARENT,PLAN
from scripts.draft_Maria_B207_prose_v7687 import CURRENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_reference_census_v7700')
LOADER=Path('work/analysis/maria_B207_loaders_v7699/303_whole_native_loads_cache_hits606_initial_parent_modes.json')
PRIOR=Path('work/analysis/lil_B234_reference_census_v7596/all20_commands_no_relative_or_typed_sites_and_shipped_census.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,loader,prior,current=map(read,[PLAN,LOADER,PRIOR,CURRENT])
    assert loader['fresh_native_whole_loads_andcache_hits']==303 and loader['fresh_initial_parent_modes']==606
    for key in ['load','parent_mode']:assert sha(Path(loader[key+'_proof']).read_bytes())==loader[key+'_sha256']
    target,old=NdsImage.open(ROM),NdsImage.open(PARENT);assert sha(PARENT.read_bytes())==mapping['candidate_sha256']
    previous=NdsImage.open(prior['research_ROM']);assert sha(Path(prior['research_ROM']).read_bytes())==prior['research_ROM_sha256']
    assert old.read_file('/__arm9__.bin')==target.read_file('/__arm9__.bin')==previous.read_file('/__arm9__.bin')
    assert all(target.read_file(p)==v for p,v in old.iter_components())
    assert old.rom.arm9OverlayTable==target.rom.arm9OverlayTable==previous.rom.arm9OverlayTable
    for row in prior['native_call_census']['research']['units']:
        if row['name'].startswith('overlay'):
            from ndspy.code import loadOverlayTable
            overlays=loadOverlayTable(target.rom.arm9OverlayTable,lambda _,f:target.rom.files[f])
            n=int(row['name'][7:]);assert sha(bytes(overlays[n].data))==row['sha256']
    fresh=census(target);assert fresh==prior['native_call_census']['research']
    inventory,_,_=scoped_inventory();groups=[]
    for g,source in zip(mapping['groups'],[current],strict=True):
        block=IlnkContainer.parse(target.read_file(g['file_path'])).blocks[g['block']]
        assert sha(block)==g['research_block_sha256'];walk=inventory(target.read_file('/__arm9__.bin'),block)[0]
        assert len(walk)==20 and not g['relative_skip_fixups'] and not g['choice_commands'] and not g['actor_style_commands'];rows=[]
        for jp,before,after,mapped in zip(source['all_clean_native_commands'],source['all_current_native_commands'],walk,g['command_map'],strict=True):
            assert jp['word']==before['word']==after['word']==mapped['word'] and jp['offset']==before['offset']==mapped['old_offset']
            assert jp['native_extent']==before['native_extent']==mapped['old_extent'] and after['offset']==mapped['new_offset'] and after['native_extent']==mapped['new_extent']
            assert jp['ancestor_0100_offsets']==before['ancestor_0100_offsets']==after['ancestor_0100_offsets']==[]
            if after['word']!=0x4000:assert jp['whole_command_hex']==before['whole_command_hex']==after['whole_command_hex']
            rows.append(deepcopy(mapped))
        groups.append(dict(route=g['route'],file_path=g['file_path'],block=g['block'],all20_commands_clean_current_target_bound=True,native_walks=dict(clean=source['all_clean_native_commands'],current=source['all_current_native_commands'],research=walk),mapped_commands=rows,entry_point_offset=8,no_relative_typed_choice_oractor_style_sites=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'Maria_all20_commands_one_entry_one_fresh_shipped_caller_census.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),groups=groups,native_call_census=dict(research=fresh,current_exact_code_units_reuse=deepcopy(prior['native_call_census']['research']),clean_exact_reference=deepcopy(prior['native_call_census']['clean'])),fresh_caller_censuses=1,exact_reused_caller_censuses=2,all_shipped_decoded_native_units_bound_no_new_alias=True,only_original_24070_interpreter_call_no_literal_alias=True,source_current_walks_exact_hash_reuse_not_reexecution=True,fresh_target_walks=1,original_EV3_block_index_loader_andtwo_parent_modes_verified=True,all20_commands_complete_preambles_opaque_operands_andnormal_end_preserved=True,no_source_eligibility_activation_location_earned_progress_orfull_effect_claim=True,actual_control_pixels_andregistered_release_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,CURRENT,LOADER,PRIOR,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('All20 Maria clean/current/relocated commands andoriginal block entry pass;one fresh shipped caller census matches exact native units. Actual/release pending.')
