"""Fresh shipped entry census and104-command/8-span three-block mapping."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
inventory,_,_=scoped_inventory()
from scripts.prepare_lil_B152_B154_research_v3640 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B152_B154_reference_census_v3642')
LOADER = Path('work/analysis/lil_B152_B154_loader_v3641/whole_SC2_and_B152_B154_initial_entry_proof.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    plan,loader = map(read,(PLAN,LOADER))
    assert loader['all336_whole_blocks_and672_modes_each_pass']
    assert loader['original_parent_both_modes_start_at_loaded_payload_plus8']
    assert loader['original_EV2_actions_select_by_block_index_without_interior_byte_offset']
    for row in loader['versions']:
        for k in ('load','parent'):assert sha(Path(row[k+'_proof']).read_bytes())==row[k+'_sha256']
    images = [NdsImage.open(p) for p in('work/clean.nds',PARENT,ROM)]
    clean,current,target = images
    assert sha(PARENT.read_bytes()) == plan['candidate_sha256']
    assert current.read_file('/__arm9__.bin') == target.read_file('/__arm9__.bin')
    arm = current.read_file('/__arm9__.bin')
    code = {label:census(image)for label,image in zip(('clean','current','research'),images,strict=True)}
    blocks = [IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks for image in images]
    assert all(len(bs)==336 for bs in blocks)
    assert all(a==b for n,(a,b) in enumerate(zip(blocks[1],blocks[2],strict=True))if n not in [152,153,154])
    result = []
    for spec in plan['blocks']:
        number = spec['block']
        assert sha(blocks[1][number]) == spec['source_block_sha256']
        assert sha(blocks[2][number]) == spec['research_block_sha256']
        walks = [inventory(im.read_file('/__arm9__.bin'),bs[number])[0] for im,bs in zip(images,blocks,strict=True)]
        expected = len(spec['command_map'])
        assert all(len(w)==expected for w in walks)
        patches = sorted([dict(start=r['old_offset'],end=r['old_offset']+r['old_length'],
            delta=r['new_length']-r['old_length'])for r in spec['text_records']+spec['actor_style_commands']+spec['choice_commands']],key=lambda r:r['start'])
        def mapped(at):
            delta = 0
            for p in patches:
                if at<p['start']:break
                assert not p['start']<at<p['end']
                if at==p['start']:return at+delta
                delta += p['delta']
            return at+delta
        commands = []
        for jp,old,new in zip(*walks,strict=True):
            assert jp['word']==old['word']==new['word'] and jp['offset']==old['offset']
            assert jp['native_extent']==old['native_extent']
            assert new['offset']==mapped(old['offset'])
            assert new['native_extent']==mapped(old['offset']+old['native_extent'])-new['offset']
            assert new['ancestor_0100_offsets']==[mapped(a)for a in old['ancestor_0100_offsets']]
            if old['word']==0x4000:
                assert blocks[1][number][old['offset']:old['offset']+6]==blocks[2][number][new['offset']:new['offset']+6]
            elif old['word'] not in (0x100,0x200,0x300,0x400,0x4100,0x2100):
                assert old['whole_command_hex']==new['whole_command_hex']
            commands.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],
                old_native_extent=old['native_extent'],new_native_extent=new['native_extent'],
                source_0100_ancestors=old['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
        assert len(spec['relative_skip_fixups']) == sum(c['word'] in [0x100,0x200,0x300,0x400] for c in spec['command_map'])
        result.append(dict(block=number,native_walks=dict(zip(('clean','current','research'),walks,strict=True)),
            mapped_commands=commands,complete_speech_preambles_and_all_opaque_commands_preserved=True,
            typed_choice_count=len(spec['choice_commands']),typed_actor_style_count=len(spec['actor_style_commands']),typed_relative_span_count=len(spec['relative_skip_fixups']),
            target_native_skip_cases=len(spec['target_native_skip_cases']),entry_point_offset=8))
    assert sum(len(r['mapped_commands'])for r in result)==104
    assert sum(r['typed_relative_span_count']for r in result)==8
    assert sum(r['target_native_skip_cases']for r in result)==40
    ROOT.mkdir(parents=True)
    save(ROOT/'all104_commands8_relative_sites_and_shipped_entry_census.json',dict(parent=str(PARENT),
        parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(arm),native_call_census=code,blocks=result,
        only_original24070_interpreter_call_no_literal_alias=True,all333_other_SC2_blocks_preserved=True,
        all104_clean_current_target_commands_and8_relative_sites_reexecuted=True,
        original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes=True,
        structural_walk_bridges_opaque_effects_not_a_gameplay_claim=True,
        original_scene_controls_actual_revised_paths_and_final_reference_approval_pending=True,
        registered_ROM_patch_orcompletion_credit_not_created=True,
        evidence={str(p):sha(p.read_bytes())for p in(PLAN,LOADER)},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(entry_censuses=3,native_commands_each=104,relative_sites=8,target_native_skip_cases=40,representative_and_release_pending=True))
