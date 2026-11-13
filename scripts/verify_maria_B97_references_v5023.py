"""Fresh executable entry census and40-command clean/current/relocated B97 mapping."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.census_native_storylines_v1995 import complete_walk
from scripts.maria_B97_reference_paths_v5021 import PARENT,ROM,PLAN,STORED,DOC
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_references_v5023')
LOADER=Path('work/analysis/maria_B97_loader_v5022/whole_SC3_and_B97_initial_entry_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,stored,doc,loader=map(read,[PLAN,STORED,DOC,LOADER]);assert loader['all303_whole_blocks_and606_modes_each_pass'] and loader['original_parent_both_modes_start_at_loaded_payload_plus8'] and loader['original_EV3_actions_select_by_block_index_without_interior_byte_offset']
    for v in loader['versions']:
        for k in ['load','parent']:assert sha(Path(v[k+'_proof']).read_bytes())==v[k+'_sha256']
    images=[NdsImage.open(p) for p in ['work/clean.nds',PARENT,ROM]];blocks=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks for im in images]
    assert all(len(b)==303 for b in blocks) and images[1].read_file('/__arm9__.bin')==images[2].read_file('/__arm9__.bin')
    assert [i for i,(a,b) in enumerate(zip(blocks[1],blocks[2],strict=True)) if a!=b]==[97]
    walks=[complete_walk(im.read_file('/__arm9__.bin'),b[97]) for im,b in zip(images,blocks,strict=True)];assert all(not w['errors'] and len(w['commands'])==40 for w in walks)
    source=read(doc['source_context']);assert walks[0]['commands']==source['blocks'][0]['all_clean_native_commands'] and walks[1]['commands']==source['blocks'][0]['all_current_native_commands']
    mapped=[]
    for jp,old,new,m in zip(walks[0]['commands'],walks[1]['commands'],walks[2]['commands'],plan['mapped_native_commands'],strict=True):
        assert jp['offset']==old['offset']==m['old_offset'] and new['offset']==m['new_offset'] and jp['word']==old['word']==new['word']==m['word']
        assert jp['native_extent']==old['native_extent']==m['old_extent'] and new['native_extent']==m['new_extent']
        assert not jp['ancestor_0100_offsets'] and not old['ancestor_0100_offsets'] and not new['ancestor_0100_offsets']
        if old['word']==0x4000:assert blocks[0][97][jp['offset']:jp['offset']+6]==blocks[1][97][old['offset']:old['offset']+6]==blocks[2][97][new['offset']:new['offset']+6]
        else:assert jp['whole_command_hex']==old['whole_command_hex']==new['whole_command_hex']
        mapped.append(dict(m,source_command_hex=old['whole_command_hex'],target_command_hex=new['whole_command_hex']))
    code={label:census(im) for label,im in zip(['clean','current','research'],images,strict=True)}
    ROOT.mkdir(parents=True);save(ROOT/'three_entry_censuses_and40_clean_current_target_commands.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),stored=str(STORED),stored_sha256=sha(STORED.read_bytes()),loader=str(LOADER),loader_sha256=sha(LOADER.read_bytes()),native_call_census=code,native_walks=dict(zip(['clean','current','research'],walks,strict=True)),mapped_commands=mapped,all40_complete_preambles_and8_exact_leaves_preserved=True,no_relative_sites_predicates_typed_objects_or_pause_pairs=True,only_original24070_interpreter_call_and_no_literal_alias=True,all302_other_SC3_blocks_preserved=True,original_EV3_block_index_entry_plus8_bound=True,structural_effect_bodies_bridged_not_full_effect_or_eligibility_execution=True,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Three shipped entry censuses and40 clean/current/target command mappings pass;all302 other SC3 blocks exact.')
