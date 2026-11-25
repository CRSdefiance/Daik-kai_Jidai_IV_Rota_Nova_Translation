"""Reversibly rebuild B207's13 source-owned speeches;derive every target bound."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_B207_profile_v1 import profile_for
from dk4tool.dialogue.lil_B207_layout_v2 import encode_relocatable_dialogue
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_relocation_v6365')
DOC=Path('translations/lil_B207_editorial_manuscript_v5.json')
PLAN=ROOT/'nested_source_relocation_research.json'
PARENT=Path('out/all_routes_combined_v6327_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);approval=read(doc['native_approval']);assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['all13_five_gates_approved'] and sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    image=NdsImage.open(PARENT);arm=image.read_file('/__arm9__.bin');source_file=image.read_file('/data/SC2.DK4');bank=IlnkContainer.parse(source_file).blocks;block=bank[207];context=read(doc['source_context']);spec=context['blocks'][0];font=read(doc['native_font_proof']);fonts={r['id']:r for r in font['cases']};inventory,walker,invsource=scoped_inventory()
    assert sha(block)==spec['current_block_sha256'] and (len(block),8+struct.unpack_from('<H',block,4)[0])==(656,654) and block[654:]==bytes(2)
    old_commands,old_speeches=inventory(arm,block);assert len(old_commands)==15 and len(old_speeches)==13 and old_commands==spec['all_current_native_commands']
    assert [c['word'] for c in old_commands]==[0x4000]*13+[0xA000,0] and all(not c['ancestor_0100_offsets'] for c in old_commands)
    patches=[];texts=[];profile=profile_for(arm,block)
    for row in doc['records']:
        assert row['block']==207 and row['source_selector'] in [2,14] and all(row['review'].values());at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);assert block[at:at+len(old)+1]==old+b'\0' and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        value=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile).encoded;assert value.hex()==row['compiled_hex']==fonts[row['id']]['encoded_hex'];pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        assert b'\0' not in value and value[0]==old[0] and len(value)%2==len(old)%2
        patches.append(dict(start=at,end=at+len(old),old=old,value=value));texts.append(dict(id=row['id'],record_index=row['current_record_index'],old_offset=at,old_length=len(old),new_length=len(value),parity_space_added=pad,target_hex=value.hex()))
    patches.sort(key=lambda r:r['start']);assert len(patches)==13 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            assert not p['start']<offset<p['end'],'Interior reference into changed speech body'
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    pieces=[];last=0
    for p in patches:pieces.extend([block[last:p['start']],p['value']]);last=p['end']
    pieces.append(block[last:654]);logical=bytearray(b''.join(pieces));assert len(logical)==mapped(654) and len(logical)<0x2400;struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    commands,speeches=inventory(arm,target);assert len(commands)==15 and len(speeches)==13;by={c['offset']:c for c in commands};command_map=[]
    for old in old_commands:
        new=by[mapped(old['offset'])];assert old['word']==new['word'] and not new['ancestor_0100_offsets'];assert mapped(old['offset']+old['native_extent'])==new['offset']+new['native_extent']
        if old['word']==0x4000:assert block[old['offset']:old['offset']+6]==target[new['offset']:new['offset']+6]
        else:assert old['whole_command_hex']==new['whole_command_hex']
        command_map.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],old_extent=old['native_extent'],new_extent=new['native_extent']))
    assert target[mapped(650):mapped(650)+4]==bytes(4) and mapped(650)+4==len(logical)
    for r in texts:r.update(new_offset=mapped(r['old_offset']),new_record_index=target[:mapped(r['old_offset'])].count(b'\0'))
    inverse=bytearray(logical);struct.pack_into('<H',inverse,4,646)
    for p in reversed(patches):at=mapped(p['start']);inverse[at:at+len(p['value'])]=p['old']
    assert bytes(inverse)+block[654:]==block
    ROOT.mkdir(parents=True);bp=ROOT/'SC2_block207_RESEARCH_ONLY.bin';bp.write_bytes(target);newbank=list(bank);newbank[207]=target;data=IlnkContainer(newbank).to_bytes();path=ROOT/'SC2_RESEARCH_ONLY.DK4';path.write_bytes(data);assert [i for i,(a,b) in enumerate(zip(bank,IlnkContainer.parse(data).blocks,strict=True)) if a!=b]==[207]
    result=dict(block=207,source_block_sha256=sha(block),research_block_sha256=sha(target),source_bytes=len(block),research_bytes=len(target),source_logical_end=654,research_logical_end=len(logical),unowned_appended_copy=None,original2000_pause_and_resume_maps=[],original_declared_end_word_maps=[dict(source_offset=650,target_offset=mapped(650),extent=4,source_four_zero_bytes_exact=True)],text_records=texts,actor_style_commands=[],choice_commands=[],relative_skip_fixups=[],target_native_skip_cases=[],command_map=command_map,all_original_command_types_preambles_and_opaque_bytes_preserved=True,inverse_restoration_recovers_every_original_logical_byte=True,inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte=True,research_block=str(bp),external_entry_and_actual_revised_paths_approval_pending=True)
    save(PLAN,dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=doc['source_context'],target_SC2=str(path),target_SC2_sha256=sha(data),source_SC2_sha256=sha(source_file),blocks=[result],all13speech15commands_and_original_A000_complete_end_preserved=True,all335_other_SC2_blocks_exact=True,no_source_typed_menus_relative_operands_actor_style_FE_or_macros=True,explicit_unmatched_native_walk=walker,unchanged_inventory_function=invsource,external_references_complete=False,not_a_release_relocation_map=True,no_ROM_registry_or_completion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_stored=656,source_logical=654,target_stored=len(target),target_logical=len(logical),target_tail=len(target)-len(logical),target_A000=mapped(642),target_end=mapped(650),parity_tails=sum(r['parity_space_added'] for r in texts),target_SC2_sha256=sha(data),inverse656_exact=True))
