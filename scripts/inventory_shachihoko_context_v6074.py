"""Census clean cultural-term/item116 candidates before any broader English comparison."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import TABLE as ACTORS
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_context_inventory_v6074')
SOURCE=Path('work/analysis/lil_B204_source_v6062/all20_clean_current_complete_context.json')
ITEM=Path('work/analysis/lil_B204_item_fields_v6073/clean_item116_current_name_and_original_picture_descriptor.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,item=map(read,[SOURCE,ITEM]);clean,current=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    arm=clean.read_file('/__arm9__.bin');target_arm=current.read_file('/__arm9__.bin');inventory,walker,invsource=scoped_inventory()
    needles=['シャチホコ','鯱'];encoded=[s.encode('cp932') for s in needles];blocks=[];prefilters=[];total=0
    for route in range(4):
        file=f'/data/SC{route}.DK4';data=clean.read_file(file);bank=IlnkContainer.parse(data).blocks;total+=len(bank)
        for number,blob in enumerate(bank):
            if not any(n in blob for n in encoded+[struct.pack('<H',0xA874),struct.pack('<H',0x3074)]):continue
            commands,speeches=inventory(arm,blob);records=[]
            for speech in speeches:
                at=speech['offset']+5;end=blob.index(0,at+1);raw=blob[at:end]
                records.append(dict(source_record_index=blob[:at].count(b'\0'),source_selector=raw[0],source_hex=raw.hex(),complete_preamble_hex=blob[at-5:at+1].hex(),Japanese=raw[1:].decode('cp932'),source_reference=dict(file_path=file,block=number,offset=at,bytes=len(raw),header_offset=at-5)))
            text=[r for r in records if any(t in r['Japanese'] for t in needles)];pictures=[];packed=[]
            for c in commands:
                raw=bytes.fromhex(c['whole_command_hex'])
                if c['word']&0xFF00==0x4800 and len(raw)==4:
                    operand=struct.unpack_from('<H',raw,2)[0]
                    if operand&255==116:pictures.append(c)
                if c['word']==0xA000 and len(raw)==8 and struct.unpack_from('<H',raw,6)[0]==0x3074:packed.append(c)
            prefilters.append(dict(file_path=file,block=number,typed_literal_hits=len(text),typed_picture116_candidates=len(pictures),packed3074_A000_candidates=len(packed)))
            if text or pictures or packed:blocks.append(dict(file_path=file,block=number,source_file_sha256=sha(data),source_block_sha256=sha(blob),source_block_hex=blob.hex(),all_native_commands=commands,all_speech_records=records,direct_cultural_term_records=text,picture116_commands=pictures,packed3074_A000_candidates=packed,packed_semantics_not_inferred_from_number_alone=True))
    assert total==1307
    pointer=item['current_pointer'];old=bytes.fromhex(item['current_terminated_hex']);aliases=[]
    for ident in range(218):
        f=0x11E210+ident*24;p=struct.unpack_from('<I',target_arm,f)[0]
        if pointer<=p<pointer+len(old):aliases.append(dict(item_ID=ident,pointer_field=f,pointer=p,interior_delta=p-pointer))
    actors=[]
    for ident in range(207):
        for delta in [0,4,8]:
            f=ACTORS+ident*32+delta;p=struct.unpack_from('<I',target_arm,f)[0]
            if pointer<=p<pointer+len(old):actors.append(dict(actor_ID=ident,column=delta,pointer_field=f,pointer=p,interior_delta=p-pointer))
    literal=[at for at in range(len(target_arm)-3) if target_arm[at:at+4]==struct.pack('<I',pointer)]
    ROOT.mkdir(parents=True);save(ROOT/'all_route_clean_term_and_item116_candidates_and_current_pointer_aliases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_item_proof=str(ITEM),source_item_proof_sha256=sha(ITEM.read_bytes()),clean_ARM9_sha256=sha(arm),current_ARM9_sha256=sha(target_arm),source_blocks_scanned=total,raw_prefilter_native_validations=prefilters,selected_native_blocks=blocks,
        current_owned_title_reference=item,current218_item_table_aliases=aliases,current207_actor_field_aliases=actors,current_literal_ARM9_pointer_occurrences=literal,
        finding='The clean item name 鯱の像 uses the shachi character,while the complete B204 castle dialogue explicitly says シャチホコ and the source image is the upturned Japanese ornament. Current Orca Figurehead needs contextual terminology review. Preserve the intentionally mistaken/self-serving figurehead explanation as character dialogue. A shared-name correction must bind owned storage,all aliases,native item/widget/list/acquisition consumers and registered runtime ancestry;do not perform a global text substitution.',
        proposed_replacement_not_yet_selected=True,current_story_English_not_read_by_this_clean_census=True,literal_census_not_exhaustive_dynamic_item_or_UI_consumer_proof=True,
        clean_inventory_walker=walker,clean_inventory_function=invsource,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,ITEM,Path(__file__)]},new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('Selected source contexts',[(b['file_path'],b['block'],len(b['all_speech_records']),len(b['direct_cultural_term_records']),len(b['picture116_commands']),len(b['packed3074_A000_candidates'])) for b in blocks])
    print('Item aliases',aliases,'actor aliases',actors,'literal pointer fields',literal,'no replacement or credit')
