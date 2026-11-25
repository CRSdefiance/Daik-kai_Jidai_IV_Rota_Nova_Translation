"""Bind all26 mapped commands and the shipped caller census without repeating immutable inputs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.create_lil_B212_reference_v6624 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_reference_census_v6626');LOADER=Path('work/analysis/lil_B212_loader_v6625/whole_SC2_and_B212_initial_entry_proof.json');PRIOR=Path('work/analysis/lil_B211_reference_census_v6571/all14_commands_no_relative_sites_and_shipped_entry_census.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,loader,prior=map(read,[PLAN,LOADER,PRIOR]);packet=read(plan['source_context']);assert loader['all336_whole_blocks_and672_modes_each_pass'] and loader['original_parent_both_modes_start_at_loaded_payload_plus8'] and loader['original_EV2_actions_select_by_block_index_without_interior_byte_offset']
    for v in loader['versions']:
        for k in ['load','parent']:assert sha(Path(v[k+'_proof']).read_bytes())==v[k+'_sha256']
    assert sha(PARENT.read_bytes())==plan['candidate_sha256']==prior['research_ROM_sha256'];current,target=NdsImage.open(PARENT),NdsImage.open(ROM);assert current.read_file('/__arm9__.bin')==target.read_file('/__arm9__.bin') and all(current.read_file(p)==target.read_file(p) for _,p,v in current.iter_files() if p!='/data/SC2.DK4');clean=NdsImage.open('work/clean.nds');assert sha(Path('work/clean.nds').read_bytes())==packet['source_ROM_sha256']==read('work/analysis/lil_B211_source_v6550c/twelve_clean_current_complete_exchange_source_references.json')['source_ROM_sha256'];fresh=census(target);assert fresh==prior['native_call_census']['research'];code=dict(clean=deepcopy(prior['native_call_census']['clean']),current=deepcopy(prior['native_call_census']['research']),research=fresh);banks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [clean,current,target]];assert all(len(b)==336 for b in banks) and [i for i,(a,b) in enumerate(zip(banks[1],banks[2],strict=True)) if a!=b]==[212];spec=plan['blocks'][0];source=packet['blocks'][0];assert sha(banks[0][212])==source['clean_block_sha256'] and sha(banks[1][212])==spec['source_block_sha256']==source['current_block_sha256'] and sha(banks[2][212])==spec['research_block_sha256'];inventory,_,_=scoped_inventory();walk=inventory(target.read_file('/__arm9__.bin'),banks[2][212])[0];walks=[source['all_clean_native_commands'],source['all_current_native_commands'],walk];assert all(len(w)==26 for w in walks)
    patches=sorted([dict(start=r['old_offset'],end=r['old_offset']+r['old_length'],delta=r['new_length']-r['old_length']) for r in spec['text_records']+spec['choice_commands']],key=lambda r:r['start'])
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            assert not p['start']<at<p['end']
            if at==p['start']:return at+delta
            delta+=p['delta']
        return at+delta
    commands=[]
    for jp,old,new in zip(*walks,strict=True):
        assert jp['word']==old['word']==new['word'] and jp['offset']==old['offset'] and jp['native_extent']==old['native_extent'];assert new['offset']==mapped(old['offset']) and new['native_extent']==mapped(old['offset']+old['native_extent'])-new['offset'] and new['ancestor_0100_offsets']==[mapped(a) for a in old['ancestor_0100_offsets']]
        if old['word']==0x4000:assert banks[1][212][old['offset']:old['offset']+6]==banks[2][212][new['offset']:new['offset']+6]
        elif old['word'] not in [0x100,0x200,0x300,0x400,0x2100,0x2200]:assert old['whole_command_hex']==new['whole_command_hex']
        commands.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],old_native_extent=old['native_extent'],new_native_extent=new['native_extent'],source_0100_ancestors=old['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
    assert len(spec['relative_skip_fixups'])==10 and len(spec['target_native_skip_cases'])==50 and len(spec['choice_commands'])==2 and len(spec['text_records'])==9;ROOT.mkdir(parents=True);save(ROOT/'all26_commands10_relative_sites_two_typed_menus_and_shipped_census.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(current.read_file('/__arm9__.bin')),native_call_census=code,fresh_caller_censuses=1,exact_reused_caller_censuses=2,current_control_global_census_reused_by_byte_identical_ROM_and_all_native_units=True,source_current_structural_walks_reused_by_exact_block_and_runtime_hashes=True,fresh_target_structural_walks=1,blocks=[dict(block=212,native_walks=dict(zip(['clean','current','research'],walks,strict=True)),mapped_commands=commands,complete_preambles_ancestors_and_all_opaque_commands_preserved=True,typed_choice_count=2,typed_actor_style_count=0,typed_relative_span_count=10,target_native_skip_cases=50,entry_point_offset=8)],only_original24070_interpreter_call_no_literal_alias=True,all335_other_SC2_blocks_preserved=True,all26_clean_current_target_commands_bound=True,original_block_index_loader_two_parent_modes_verified=True,source_flagged_00000080_and_two_normal_end_forms_exact=True,structural_walk_bridges_opaque_effects_not_gameplay=True,actual_English_controls_pixels_and_final_reference_approval_pending=True,registered_release_or_credit_not_created=True,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,LOADER,PRIOR,Path(plan['source_context']),Path(__file__)]},new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('All26 commands/10 relative sites/two menus/three exact ends and shipped caller census pass. One fresh census/walk; immutable clean/current evidence reused by hashes.')
