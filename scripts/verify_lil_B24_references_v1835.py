"""Fresh shipped-source call census and all17 mapped native B24 commands."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.prepare_lil_B24_research_v1829 import ROM,PARENT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_reference_census_v1835')
RELOCATION=Path('work/analysis/lil_B24_relocation_v1828/parity_and17_native_command_research.json')
LOADER=Path('work/analysis/lil_B24_loader_v1830/whole_SC2_and_B24_initial_entry_proof.json')
CONTEXT=Path('work/analysis/lil_B24_event_context_v1832b/original_full_event24_and_packed_set_prefix.json')

if __name__=='__main__':
    assert not ROOT.exists()
    research=read(RELOCATION);loader=read(LOADER);context=read(CONTEXT)
    assert research['inverse_reconstruction_of_every_original_logical_byte_exact']
    assert research['all4_nonspeech_commands_exact_at_mapped_positions']
    assert loader['all336_whole_blocks_and672_modes_each_pass']
    assert loader['original_EV2_actions_select_by_block_index_without_interior_byte_offset']
    assert loader['original_parent_both_modes_start_at_loaded_payload_plus8']
    assert context['source_flag27_requires_empty_intersection_with_original_owner_set']
    assert sha(PARENT.read_bytes())==research['candidate_sha256']==context['ROM_sha256']
    for v in loader['versions']:
        for k in ('load','parent'):assert sha(Path(v[k+'_proof']).read_bytes())==v[k+'_sha256']
    clean=NdsImage.open('work/clean.nds');current=NdsImage.open(PARENT);target=NdsImage.open(ROM)
    arm=current.read_file('/__arm9__.bin');assert arm==target.read_file('/__arm9__.bin')
    call_census={name:census(image)for name,image in [('clean',clean),('current',current),('research',target)]}
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in (clean,current,target)]
    assert len(blocks[0])==len(blocks[1])==len(blocks[2])==336
    assert all(a==b for i,(a,b)in enumerate(zip(blocks[1],blocks[2],strict=True))if i!=24)
    assert sha(blocks[1][24])==research['old_block_sha256']
    assert sha(blocks[2][24])==research['target_block_sha256']
    walks=[inventory(im.read_file('/__arm9__.bin'),bs[24])[0]for im,bs in zip((clean,current,target),blocks,strict=True)]
    assert all(len(w)==17 for w in walks)
    mapping=research['all17_commands'];assert len(mapping)==17
    for japanese,old,new,spec in zip(*walks,mapping,strict=True):
        assert japanese['word']==old['word']==new['word']==spec['word']
        assert japanese['offset']==old['offset']==spec['old_offset']
        assert japanese['native_extent']==old['native_extent']==spec['old_extent']
        assert new['offset']==spec['new_offset']and new['native_extent']==spec['new_extent']
        assert japanese['ancestor_0100_offsets']==old['ancestor_0100_offsets']==new['ancestor_0100_offsets']==[]
        if old['word']!=0x4000:
            assert japanese['whole_command_hex']==old['whole_command_hex']==new['whole_command_hex']
    assert [r['word']for r in mapping if r['word']!=0x4000]==[0x61FF,0xA000,0xC200,0]
    ROOT.mkdir(parents=True)
    save(ROOT/'complete_shipped_entry_and17_mapped_command_census.json',{
        'parent':str(PARENT),'parent_sha256':sha(PARENT.read_bytes()),'research_ROM':str(ROM),
        'research_ROM_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),
        'block':24,'original_interpreter_entry_census':call_census,
        'native_walks':dict(zip(('clean','current','research'),walks,strict=True)),
        'mapped_commands':mapping,'all17_native_commands_reexecuted_clean_current_and_research':True,
        'all4_nonspeech_commands_preserved_including_complete_terminal':True,
        'no_relative_span_or_choice_operands_in_exact_block':True,
        'all336_loads_and672_parent_modes_each_ROM_bound_to_proof':True,
        'all335_other_blocks_exact':True,
        'entry_point_offset':8,'only_original24070_interpreter_caller_no_literal_alias':True,
        'opaque_effects_bridged_only_in_structural_walk_not_claimed_actual_gameplay':True,
        'actual_research_B24_activation_displays_and_return_required_before_reference_approval':True,
        'registered_layer_and_completion_credit_not_yet_authorized':True,
        'evidence':{str(p):sha(p.read_bytes())for p in (RELOCATION,LOADER,CONTEXT)},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'entry_censuses':3,'native_B24_walks':3,'commands_each':17,'actual_gate_still_open':True},flush=True)
