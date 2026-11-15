"""Execute original0100/0200/0300 relative skip operands at every nested site."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_post_Seville_branches_v2733')
PACKET=Path('work/analysis/lil_post_Seville_source_v2732/complete34_clean_current_native_context.json')
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100


if __name__=='__main__':
    assert not ROOT.exists()
    original=read(PACKET)
    packet={**original,'blocks':[dict(block=b['block'],all_nested_native_commands=b['all_clean_native_commands']) for b in original['blocks']]}
    cases=[];edges=[]
    for label,path in [('clean','work/clean.nds'),('current',packet['current_ROM'])]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');cpu=machine(arm)
        clean_arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
        assert all(arm[a:b]==clean_arm[a:b]for a,b in [(0x2A414,0x2A530),(0x24048,0x24118)])
        blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
        for spec in packet['blocks']:
            block=blocks[spec['block']];logical=8+struct.unpack_from('<H',block,4)[0]
            boundaries={r['offset'] for r in spec['all_nested_native_commands']}|{logical}
            cpu.mem_write(STREAM-16,b'\xA5'*(len(block)+32));cpu.mem_write(STREAM,block)
            for row in spec['all_nested_native_commands']:
                if row['word'] not in (0x100,0x200,0x300):continue
                at=row['offset'];word=row['word'];span=struct.unpack_from('<H',block,at+2)[0]
                assert at+4 in boundaries and at+4+span in boundaries
                if label=='clean':edges.append({'block':spec['block'],'offset':at,'word':word,
                    'span_field_offset':at+2,'unmatched_next_offset':at+4,'matched_skip_target':at+4+span,
                    'condition':'always' if word==0x100 else ('last_result_equals0' if word==0x200 else 'last_result_equals1')})
                for last in (0,1,2,3,0xFFFFFFFF):
                    cpu.mem_write(OWNER-16,b'\xA5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+at,0,0))
                    source_owner=bytes(cpu.mem_read(OWNER-16,64))
                    cpu.mem_write(RESULT-16,b'\xA5'*80);cpu.mem_write(LENGTH-16,b'\xA5'*36)
                    cpu.mem_write(RESULT,bytes(24));cpu.mem_write(LENGTH,bytes(4))
                    call(cpu,0x2A510,(RESULT,OWNER,LENGTH,last))
                    actual=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
                    taken=word==0x100 or (word==0x200 and last==0) or (word==0x300 and last==1)
                    expected=4+(span if taken else 0)
                    assert actual==expected
                    result=struct.unpack('<6I',cpu.mem_read(RESULT,24));assert result==(3,0,0,0,0,0)
                    assert bytes(cpu.mem_read(STREAM,len(block)))==block
                    assert bytes(cpu.mem_read(OWNER-16,64))==source_owner
                    for address in (STREAM-16,STREAM+len(block),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4):
                        assert bytes(cpu.mem_read(address,16))==b'\xA5'*16
                    cases.append({'version':label,'block':spec['block'],'offset':at,'word':word,
                        'last_choice_or_result':last,'skip_taken':taken,'native_decoded_extent':actual,
                        'original_next_command_offset':at+actual,'target_is_independently_mapped_native_boundary':True,
                        'source_block_owner_input_result_guards_and_ABI_exact':True})
    assert len(cases)==10*len(edges)
    ROOT.mkdir(parents=True)
    save(ROOT/'original_relative_skip_operand_proof.json',{'source_context':str(PACKET),'source_context_sha256':sha(PACKET.read_bytes()),
        'source_bound_native_parser':0x0202A510,'skip_handler_span':[0x0202A414,0x0202A510],
        'branch_span_is_relative_to_command_plus4':True,'choice_result0_1_is_preserved_by_type3_VM_commands':True,
        'VM_original_source_span':[0x02024048,0x02024118],
        'operands_requiring_adjustment_when_resizing':edges,'cases':cases,
        'all_scoped_destinations_equal_mapped_instruction_boundaries':True,
        'no_registered_relocation_map_or_branch_gameplay_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'relative_skip_sites':len(edges),'native_clean_current_cases':len(cases),'all_targets_mapped':True},flush=True)
