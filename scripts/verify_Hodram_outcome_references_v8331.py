"""Bind two native SC1 entries,15commands/zerorelatives to one fresh unchanged-code caller census."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_reference_census_v8331')
REFERENCE=Path('work/analysis/Hodram_outcome_reference_v8329/research_image_receipt.json')
CURRENT=Path('work/analysis/Hodram_B47_B48_current_v8317c/six_exact_source_current_effective_refs_after_whole_clean_gloss_andnative_source_view.json')
MAP=Path('work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json')
LOADER=Path('work/analysis/Hodram_outcome_loaders_v8330/325_whole_native_loads_cache_hits650_initial_parent_modes.json')
CONTROLS=Path('work/analysis/Hodram_outcome_final_dispatch_v8328/six_final_dispatches9_exact_nontext_commands_FE_FI_andcomplete_ends.json')
PRIOR=Path('work/analysis/Gerhard_reference_census_v8223/all225_commands44_relative_sites_five_revisions_EV2_entries_shipped_callers.json')
if __name__=='__main__':
    assert not ROOT.exists();reference,current,mapping,loader,controls,prior=map(read,[REFERENCE,CURRENT,MAP,LOADER,CONTROLS,PRIOR])
    assert loader['research_ROM_sha256']==reference['research_ROM_sha256'] and loader['fresh_native_whole_loads_andcache_hits']==325 and loader['fresh_initial_parent_modes']==650
    for key in ['load','parent_mode']:assert sha(Path(loader[key+'_proof']).read_bytes())==loader[key+'_sha256']
    image,parent=[NdsImage.open(reference[k]) for k in ['research_ROM','parent']]
    assert sha(Path(reference['research_ROM']).read_bytes())==reference['research_ROM_sha256'] and sha(Path(reference['parent']).read_bytes())==reference['parent_sha256']
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    assert image.read_file('/data/EV1.DK4')==parent.read_file('/data/EV1.DK4')==NdsImage.open('work/clean.nds').read_file('/data/EV1.DK4')
    fresh=census(image);assert fresh==prior['native_call_census']['research']
    assert sha(image.read_file('/__arm9__.bin'))==sha(parent.read_file('/__arm9__.bin'))==reference['current_ARM9_sha256']
    bank=IlnkContainer.parse(image.read_file(mapping['file_path'])).blocks;loads=read(loader['load_proof']);route=next(r for r in loads['routes'] if r['route']==1)
    groups=[]
    for before,after in zip(current['groups'],mapping['groups'],strict=True):
        number=before['block'];block=bank[number];assert number==after['block'] and sha(block)==after['target_block_sha256'] and block[:8].hex()==after['target_header_hex']
        maps=[]
        for source,old,target,m in zip(before['all_source_commands'],before['all_current_commands'],after['all_target_commands'],after['command_map'],strict=True):
            assert source['word']==old['word']==target['word']==m['word'] and source['offset']==m['clean_offset'] and old['offset']==m['old_offset'] and target['offset']==m['new_offset']
            assert source['native_extent']==m['clean_extent'] and old['native_extent']==m['old_extent'] and target['native_extent']==m['new_extent']
            assert target['ancestor_0100_offsets']==m['target_0100_ancestors'] and block[target['offset']:target['offset']+target['native_extent']].hex()==target['whole_command_hex']
            if target['word']==0x4000:assert source['whole_command_hex'][:12]==old['whole_command_hex'][:12]==target['whole_command_hex'][:12]
            elif target['word'] not in [0x100,0x200,0x300,0x400]:assert source['whole_command_hex']==old['whole_command_hex']==target['whole_command_hex']
            maps.append(deepcopy(m))
        assert maps[-1]['word']==0 and maps[-1]['new_offset']+4==after['target_logical_end']
        selected=[a for a in route['actions'] if a['kind']==2 and a['native_selected_block']==number];assert len(selected)==1 and selected[0]['payload_sha256']==sha(block)
        groups.append(dict(block=number,all_command_maps=maps,relative_operand_maps=deepcopy(after['relative_fixups']),relocated_native_skip_cases=deepcopy(after['relocated_skip_cases']),
            reviewed_text_records=deepcopy(after['text_records']),original_selected_action=selected[0],original_entry_payload_offset=8,no_interior_entry_offset=True))
    assert sum(len(g['all_command_maps']) for g in groups)==15 and sum(len(g['relative_operand_maps']) for g in groups)==0
    assert sum(len(c['cases']) for g in groups for c in g['relocated_native_skip_cases'])==0
    assert len(controls['final_dispatches'])==6 and mapping['source_relative_sites']==0
    ROOT.mkdir(parents=True);save(ROOT/'all15_commands_zero_relative_sites6_records_two_EV1_entries_shipped_callers.json',dict(
        parent=reference['parent'],parent_sha256=reference['parent_sha256'],research_ROM=reference['research_ROM'],research_ROM_sha256=reference['research_ROM_sha256'],
        groups=groups,native_call_census=fresh,fresh_caller_censuses=1,exact_reused_same_complete_code_census=str(PRIOR),exact_reused_same_complete_code_census_sha256=sha(PRIOR.read_bytes()),
        all_shipped_decoded_units_andwhole_ARM9_components_byte_exact_to_registered_parent=True,only_original24070_interpreter_call_no_literal_alias=True,
        all_original_EV1_block_indices325_loads650_parent_modes_verified=True,all15_source_current_target_commands_zero_relative_sites6_complete_preambles_bound=True,
        no_interior_entries_unmapped_nested_targets_orunowned_component_changes=True,external_references_complete=True,
        exact_code_census_reuse_not_a_second_fresh_census=True,source_reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof=True,
        actual_B47_B48_FE_scene_effects_headers_policy_atomic_registered_release_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,CURRENT,MAP,LOADER,CONTROLS,PRIOR,Path(__file__)]}))
    print('Hodramreference:15commands/zerorelatives/6records/twoEV1entries,325load-cache/650modes andonefresh exact-code census pass;actualUI/policy/release pending.')
