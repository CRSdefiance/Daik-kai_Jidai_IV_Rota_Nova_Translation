"""Rebuild sixteen speech C strings with all command boundaries and a complete1112-byte inverse."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B222_profile_v1 import profile_for
from dk4tool.dialogue.lil_B222_layout_v1 import encode_relocatable_dialogue
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_relocation_v7052');DOC=Path('translations/lil_B222_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);SOURCE=Path(doc['source_context']);packet=read(SOURCE);spec=packet['blocks'][0];image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');container=IlnkContainer.parse(image.read_file('/data/SC2.DK4'));source=container.blocks[222];assert len(source)==1112 and 8+struct.unpack_from('<H',source,4)[0]==1112 and source[1112:]==bytes(0) and sha(source)==spec['current_block_sha256'];patches=[];texts=[]
    for row in doc['records']:
        at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);assert source[at:at+len(old)+1]==old+b'\0';encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,source,row['id']));value=encoded.encoded;pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        assert b'\0' not in value and value[0]==old[0]==row['source_selector'] and len(value)%2==len(old)%2;patches.append(dict(start=at,end=at+len(old),value=value,old=old,id=row['id']));texts.append(dict(id=row['id'],kind='progressive',source_selector=row['source_selector'],source_voice_class=row['source_voice_class'],old_offset=at,old_length=len(old),new_length=len(value),compiled_hex=encoded.encoded.hex(),target_hex=value.hex(),parity_space_added=pad,source_reference=row['source_reference'],current_reference=row['current_reference'],source_preamble_hex=row['source_complete_preamble_hex']))
    patches.sort(key=lambda p:p['start']);assert len(patches)==16 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            assert not p['start']<at<p['end']
            if at==p['start']:return at+delta
            delta+=len(p['value'])-len(p['old'])
        return at+delta
    parts=[];last=0
    for p in patches:parts.extend([source[last:p['start']],p['value']]);last=p['end']
    parts.append(source[last:1112]);logical=bytearray(b''.join(parts));assert len(logical)==mapped(1112)<0x2400;struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4);inventory,_,_=scoped_inventory();commands,speeches=inventory(arm,target);assert len(commands)==18 and len(speeches)==16;byoffset={c['offset']:c for c in commands};maps=[]
    for old in spec['all_current_native_commands']:
        new=byoffset[mapped(old['offset'])];assert new['word']==old['word'] and not old['ancestor_0100_offsets'] and not new['ancestor_0100_offsets'] and new['native_extent']==mapped(old['offset']+old['native_extent'])-new['offset']
        if old['word']==0x4000:assert source[old['offset']:old['offset']+6]==target[new['offset']:new['offset']+6]
        else:assert old['whole_command_hex']==new['whole_command_hex']
        maps.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],old_extent=old['native_extent'],new_extent=new['native_extent'],source_0100_ancestors=[],target_0100_ancestors=[]))
    for r in texts:
        at=mapped(r['old_offset']);r.update(new_offset=at,new_record_index=target[:at].count(b'\0'));assert target[at-5:at+1].hex()==r['source_preamble_hex'] and target[at:at+r['new_length']].hex()==r['target_hex'] and target[at+r['new_length']]==0
    effects=[dict(source_offset=1100,target_offset=mapped(1100),extent=8,source_hex='00a0ffff44000110')];uis=[];ends=[dict(source_offset=1108,target_offset=mapped(1108),extent=4,source_hex='00000000')];assert mapped(1108)+4==len(logical)
    restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,1104)
    for p in reversed(patches):at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
    assert bytes(restored)+source[1112:]==source;ROOT.mkdir(parents=True);bp=ROOT/'SC2_block222_RESEARCH_ONLY.bin';bp.write_bytes(target);blocks=list(container.blocks);blocks[222]=target;archive=IlnkContainer(blocks).to_bytes();ap=ROOT/'SC2_RESEARCH_ONLY.DK4';ap.write_bytes(archive);assert [i for i,(a,b) in enumerate(zip(container.blocks,IlnkContainer.parse(archive).blocks,strict=True)) if a!=b]==[222]
    group=dict(block=222,source_block_sha256=sha(source),research_block_sha256=sha(target),source_bytes=1112,source_logical_end=1112,source_tail_bytes=0,research_bytes=len(target),research_logical_end=len(logical),research_tail_bytes=len(target)-len(logical),research_block=str(bp),text_records=texts,all_object_references=texts,choice_commands=[],actor_style_commands=[],relative_skip_fixups=[],target_native_skip_cases=[],command_map=maps,original_A000_map=effects,original_C200_map=uis,complete_end_map=ends,inverse_recovers_every_original1112_byte=True,all18_original_commands_and_complete_preambles_preserved=True,external_references_complete=False)
    save(ROOT/'all16_objects18_commands_full1112_inverse_RESEARCH.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),target_SC2=str(ap),target_SC2_sha256=sha(archive),blocks=[group],all335_other_SC2_blocks_exact=True,all16_exact_source_current_compiled_and_research_references_bound=True,source_tail_and_header_full_inverse=True,final_stored_fonts_loaders_external_references_actual_and_release_pending=True,external_references_complete=False,not_release_map_or_candidate=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,SOURCE,Path('translations/lil_B222_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B222_profile_v1.py'),Path('dk4tool/dialogue/lil_B222_layout_v1.py'),Path(__file__)]},full_goal_complete=False));print(dict(source=1112,target=len(target),logical=len(logical),tail=len(target)-len(logical),parity_tails=sum(r['parity_space_added'] for r in texts),A000=effects,ends=ends,credit=0))
