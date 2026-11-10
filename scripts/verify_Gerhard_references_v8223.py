"""Bind all225 commands,44 relative sites and two original entries to fresh decoded caller censuses."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_reference_census_v8223')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
CURRENT=Path('work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json')
MAP=Path('work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json')
LOADER=Path('work/analysis/Gerhard_loaders_v8222/336_whole_native_loads_cache_hits672_initial_parent_modes.json')
CONTROLS=Path('work/analysis/Gerhard_final_controls_v8214/5_final_dispatches51_controls30_raw_evaluations150_seeded_ends.json')
OWNERSHIP=Path('work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json')
if __name__=='__main__':
    assert not ROOT.exists();reference,current,mapping,loader,controls,ownership=map(read,[REFERENCE,CURRENT,MAP,LOADER,CONTROLS,OWNERSHIP])
    assert loader['fresh_native_whole_loads_andcache_hits']==336 and loader['fresh_initial_parent_modes']==672
    assert loader['research_ROM_sha256']==reference['research_ROM_sha256'] and loader['parent_sha256']==reference['parent_sha256']==mapping['candidate_sha256']
    for key in ['load','parent_mode']:assert sha(Path(loader[key+'_proof']).read_bytes())==loader[key+'_sha256']
    rom,parentpath=Path(reference['research_ROM']),Path(reference['parent'])
    assert sha(rom.read_bytes())==reference['research_ROM_sha256'] and sha(parentpath.read_bytes())==reference['parent_sha256']
    image,parent=NdsImage.open(rom),NdsImage.open(parentpath)
    original,target=parent.read_file('/__arm9__.bin'),image.read_file('/__arm9__.bin');slot=ownership['current_owned_name_span'];at=slot['offset']
    assert target[at:at+12].hex()==slot['target_hex'] and len(original)==len(target)
    restored=bytearray(target);restored[at:at+12]=bytes.fromhex(slot['current_hex']);assert bytes(restored)==original
    assert target[at+12:at+20]==original[at+12:at+20]==b'Blades\0\0'
    fresh,parent_census=census(image),census(parent)
    assert fresh['branches']==parent_census['branches'] and fresh['literal_aliases']==parent_census['literal_aliases']==[]
    assert [{k:v for k,v in u.items() if k!='sha256'} for u in fresh['units']]==[{k:v for k,v in u.items() if k!='sha256'} for u in parent_census['units']]
    different=[dict(parent=a,research=b) for a,b in zip(parent_census['units'],fresh['units'],strict=True) if a!=b]
    assert len(different)==1
    assert image.read_file('/data/EV2.DK4')==parent.read_file('/data/EV2.DK4')==NdsImage.open('work/clean.nds').read_file('/data/EV2.DK4')
    bank=IlnkContainer.parse(image.read_file(mapping['file_path'])).blocks
    loads=read(loader['load_proof']);route=next(r for r in loads['routes'] if r['route']==2)
    groups=[]
    for cg,tg in zip(current['groups'],mapping['groups'],strict=True):
        number=cg['block'];assert number==tg['block'] and number in [27,74]
        block=bank[number];assert sha(block)==tg['target_block_sha256'] and block[:8].hex()==tg['target_header_hex']
        rows=[]
        for source,before,after,m in zip(cg['all_source_commands'],cg['all_current_commands'],tg['all_target_commands'],tg['command_map'],strict=True):
            assert source['word']==before['word']==after['word']==m['word']
            assert before['offset']==m['old_offset'] and after['offset']==m['new_offset']
            assert before['native_extent']==m['old_extent'] and after['native_extent']==m['new_extent']
            assert before['ancestor_0100_offsets']==m['source_0100_ancestors'] and after['ancestor_0100_offsets']==m['target_0100_ancestors']
            offset=after['offset'];assert block[offset:offset+after['native_extent']].hex()==after['whole_command_hex']
            if source['word']==0x4000:assert source['whole_command_hex'][:12]==before['whole_command_hex'][:12]==after['whole_command_hex'][:12]
            elif source['word'] not in [0x100,0x200,0x300,0x400]:assert before['whole_command_hex']==after['whole_command_hex']
            rows.append(deepcopy(m))
        assert rows[-1]['word']==0 and rows[-1]['new_offset']+4==tg['target_logical_end']
        selected=[a for a in route['actions'] if a['kind']==2 and a['native_selected_block']==number]
        assert len(selected)==1 and selected[0]['payload_sha256']==sha(block)
        groups.append(dict(block=number,all_command_maps=rows,relative_operand_maps=deepcopy(tg['relative_fixups']),
            clean_native_skip_cases=deepcopy(tg['clean_native_skip_cases']),current_native_skip_cases=deepcopy(tg['current_native_skip_cases']),
            relocated_native_skip_cases=deepcopy(tg['relocated_native_skip_cases']),corrected_text_records=deepcopy(tg['text_records']),
            original_selected_action=selected[0],original_entry_payload_offset=8,no_interior_entry_offset=True))
    assert sum(len(g['all_command_maps']) for g in groups)==225 and sum(len(g['relative_operand_maps']) for g in groups)==44
    assert sum(len(c['cases']) for g in groups for c in g['relocated_native_skip_cases'])==220
    assert len(controls['final_dispatches'])==5 and controls['raw_native_evaluations']==30 and controls['normal_seeded_end_cases']==150
    ROOT.mkdir(parents=True);save(ROOT/'all225_commands44_relative_sites_five_revisions_EV2_entries_shipped_callers.json',dict(
        parent=str(parentpath),parent_sha256=reference['parent_sha256'],research_ROM=str(rom),research_ROM_sha256=reference['research_ROM_sha256'],
        groups=groups,native_call_census=dict(research=fresh,parent=parent_census),fresh_caller_censuses=2,
        decoded_unit_hash_differences=different,only_owned12byte_name_data_differs_in_ARM9_every_other_byte_inverse_exact=True,
        all_shipped_decoded_native_units_bound=True,only_original24070_interpreter_call_no_literal_alias=True,
        all_original_EV2_block_indices336_load_cache_paths672_parent_modes_verified=True,
        all225_source_current_target_commands44_relative_sites_bound_to_research_ROM=True,all130_preambles_andfive_corrected_bodies_exact=True,
        prior_translated_Hamburg_choice_preserved_not_retranslated_here=True,original_entry_payload_offset=8,
        no_interior_entry_offsets_orunmapped_nested_relative_targets=True,
        caller_entry_checks_not_actual_event_selection_orarbitrary_dynamic_reference_proof=True,
        no_repeated_native_walk_orrelative_cases_when_exact_hashes_andmaps_already_bound=True,
        representative_actual_surname_headers_bodies_transitions_policy_atomic_registered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,CURRENT,MAP,LOADER,CONTROLS,OWNERSHIP,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Fullreference:225 commands/44relative sites/5revised bodies,336load-cachepaths/672parentmodes and2freshcallercensuses bound.No natural activation claim.')
