"""Relocate the complete Maria exchange; preserve CS0101 and reconstruct predecessor andclean source exactly."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.maria_B207_profile_v1 import profile_for
from dk4tool.dialogue.maria_B207_layout_v1 import encode_relocatable_dialogue
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.draft_Maria_B207_prose_v7687 import MANUSCRIPT,CURRENT,CLEAN
MANUSCRIPTS={3:MANUSCRIPT}
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_relocation_v7696')
POLICY=Path('work/analysis/maria_B207_policy_validation_v7695/18_positives89_expected_actual_changing_rejections_before_mutation.json')
if __name__=='__main__':
    assert not ROOT.exists();current,policy=map(read,[CURRENT,POLICY]);assert policy['positive_count']==18 and policy['negative_count']==89
    image=NdsImage.open(current['current_ROM']);arm=image.read_file('/__arm9__.bin')
    assert sha(Path(current['current_ROM']).read_bytes())==current['current_ROM_sha256'];groups=[];ROOT.mkdir(parents=True)
    inventory,_,_=scoped_inventory()
    for route,mp in MANUSCRIPTS.items():
        doc=read(mp);spec=current;file,n=spec['file_path'],spec['block'];original_archive=image.read_file(file);container=IlnkContainer.parse(original_archive);source=container.blocks[n]
        assert sha(source)==spec['current_block_sha256'] and len(source)==8+struct.unpack_from('<H',source,4)[0]==1468 and source[1468:]==b''
        patches=[];texts=[]
        for row in doc['records']:
            at=row['current_reference']['offset'];old=bytes.fromhex(row['current_hex']);assert source[at:at+len(old)+1]==old+b'\0'
            encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,source,row['id'],file))
            value=encoded.encoded;pad=len(value)%2!=len(old)%2
            if pad:value+=b' '
            assert b'\0' not in value and value[0]==old[0]==row['source_selector'] and len(value)%2==len(old)%2
            patches.append(dict(start=at,end=at+len(old),value=value,old=old,id=row['id']))
            texts.append(dict(id=row['id'],file_path=file,kind='progressive',source_selector=row['source_selector'],source_voice_class=row['source_voice_class'],old_offset=at,old_length=len(old),old_hex=old.hex(),new_length=len(value),compiled_hex=encoded.encoded.hex(),target_hex=value.hex(),parity_space_added=pad,source_reference=row['source_reference'],current_reference=row['current_reference'],source_preamble_hex=row['source_complete_preamble_hex']))
        patches.sort(key=lambda p:p['start']);assert len(patches)==18 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
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
        parts.append(source[last:1468]);logical=bytearray(b''.join(parts));assert len(logical)==mapped(1468)<0x2400
        struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
        commands,speeches=inventory(arm,target);assert len(commands)==20 and len(speeches)==18;byoffset={c['offset']:c for c in commands};maps=[]
        for old in spec['all_current_native_commands']:
            new=byoffset[mapped(old['offset'])]
            assert new['word']==old['word'] and not old['ancestor_0100_offsets'] and not new['ancestor_0100_offsets']
            assert new['native_extent']==mapped(old['offset']+old['native_extent'])-new['offset']
            if old['word']==0x4000:assert source[old['offset']:old['offset']+6]==target[new['offset']:new['offset']+6]
            else:assert old['whole_command_hex']==new['whole_command_hex']
            maps.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],old_extent=old['native_extent'],new_extent=new['native_extent'],source_0100_ancestors=[],target_0100_ancestors=[]))
        for r in texts:
            at=mapped(r['old_offset']);r.update(new_offset=at,new_record_index=target[:at].count(b'\0'))
            assert target[at-5:at+1].hex()==r['source_preamble_hex'] and target[at:at+r['new_length']].hex()==r['target_hex'] and target[at+r['new_length']]==0
        effects=[dict(source_offset=1456,target_offset=mapped(1456),extent=8,source_hex='00a0ffff6a000110')]
        ends=[dict(source_offset=1464,target_offset=mapped(1464),extent=4,source_hex='00000000')];assert mapped(1464)+4==len(logical)
        restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,1460)
        for p in reversed(patches):
            at=mapped(p['start']);restored[at:at+len(p['value'])]=p['old']
        assert bytes(restored)==source
        assert source[:8].hex()=='43530101b4050000' and target[:4]==source[:4]
        cleanpacket=read(CLEAN);cleanblock=bytes.fromhex(cleanpacket['clean_block_hex']);cleanrestored=bytearray(target[:len(logical)]);struct.pack_into('<H',cleanrestored,4,len(cleanblock)-8)
        byid={r['id']:r for r in doc['records']}
        for p in reversed(patches):
            at=mapped(p['start']);cleanrestored[at:at+len(p['value'])]=bytes.fromhex(byid[p['id']]['source_hex'])
        assert bytes(cleanrestored)==cleanblock
        bp=ROOT/f'SC{route}_block{n}_RESEARCH_ONLY.bin';bp.write_bytes(target);blocks=list(container.blocks);blocks[n]=target
        archive=IlnkContainer(blocks).to_bytes();ap=ROOT/f'SC{route}_RESEARCH_ONLY.DK4';ap.write_bytes(archive);parsed=IlnkContainer.parse(archive)
        assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==[n]
        reverse=list(parsed.blocks);reverse[n]=bytes(restored);assert IlnkContainer(reverse).to_bytes()==original_archive
        groups.append(dict(route=route,route_identity=doc['route_identity'],file_path=file,block=n,manuscript=str(mp),manuscript_sha256=sha(mp.read_bytes()),source_archive_sha256=sha(original_archive),target_archive=str(ap),target_archive_sha256=sha(archive),source_block_sha256=sha(source),research_block_sha256=sha(target),source_bytes=1468,source_logical_end=1468,source_tail_bytes=0,research_bytes=len(target),research_logical_end=len(logical),research_tail_bytes=len(target)-len(logical),research_block=str(bp),text_records=texts,choice_commands=[],actor_style_commands=[],relative_skip_fixups=[],target_native_skip_cases=[],command_map=maps,original_A000_map=effects,original_630B_map=[],original_C200_map=[],complete_end_map=ends,all20_original_commands_andcomplete_preambles_preserved=True,inverse_recovers_every_original1468_byte=True,inverse_recovers_every_original_archive_byte=True,unchanged_other_block_count=len(container.blocks)-1,clean_source_block_inverse_exact=True,complete_CS0101_header_preserved=True,external_references_complete=False))
        print(dict(route=route,source=1468,target=len(target),logical=len(logical),tail=len(target)-len(logical),parity_tails=sum(r['parity_space_added'] for r in texts),unchanged_other_blocks=len(container.blocks)-1,A000=effects,ends=ends))
    assert len(groups)==1 and groups[0]['route']==3 and groups[0]['clean_source_block_inverse_exact']
    save(ROOT/'Maria18_speeches20_commands_exact_clean_andpredecessor_inverse_RESEARCH.json',dict(candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],source_context=str(CURRENT),source_context_sha256=sha(CURRENT.read_bytes()),policy_validation=str(POLICY),policy_validation_sha256=sha(POLICY.read_bytes()),groups=groups,distinct_CS0101_header_preserved=True,all18_source_current_compiled_stored_references_bound=True,all20_commands_complete_preambles_opaque_operands_andfour_byte_end_preserved=True,complete_clean_source_block_andfull_predecessor_archive_reconstruct_exactly=True,source_zero_storage_tails_distinct_from_complete_four_byte_normal_ends=True,external_references_complete=False,stored_fonts_loaders_callers_actual_andrelease_pending=True,research_archives_only_no_ROM_registry_ledger_mutation=True,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,POLICY,*MANUSCRIPTS.values(),Path('translations/maria_B207_native_contract_v1.json'),Path('dk4tool/dialogue/maria_B207_profile_v1.py'),Path('dk4tool/dialogue/maria_B207_layout_v1.py'),Path(__file__)]},new_credit=0,full_goal_complete=False))
