"""Prove new source 0400 third-result skips using original clean/current code."""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_next_0400_control_v3153')
ROM=Path('out/all_routes_combined_v3144_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists();proof=read('work/analysis/lil_after_Crew_Items_clean_scope_v3152/complete_clean_next_exchange_inventory.json');source,current=[NdsImage.open(p)for p in ['work/clean.nds',ROM]];arms=[i.read_file('/__arm9__.bin')for i in [source,current]];blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [source,current]]
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256'];assert arms[0][0x2A414:0x2A5BC]==arms[1][0x2A414:0x2A5BC]
    inventory,_,_=scoped_inventory();cases=[];sites=[]
    OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100
    for b in proof['blocks']:
        if b['block']==120:continue
        n=b['block'];commands,speeches=inventory(arms[1],blocks[1][n]);clean_boundaries={c['offset']for c in b['commands']}|{8+int.from_bytes(blocks[0][n][4:6],'little')};current_boundaries={c['offset']for c in commands}|{8+int.from_bytes(blocks[1][n][4:6],'little')}
        for row in b['commands']:
            if row['word']!=0x400:continue
            at=row['offset'];data=blocks[0][n][at:at+4];assert blocks[1][n][at:at+4]==data
            target=at+4+int.from_bytes(data[2:4],'little');assert target in clean_boundaries and target in current_boundaries and at+4 in clean_boundaries and at+4 in current_boundaries
            sites.append(dict(block=n,offset=at,source_command_hex=data.hex(),matched_target=target,unmatched_target=at+4))
            for version,arm,bb in zip(['clean','current'],arms,blocks,strict=True):
                cpu=machine(arm);block=bb[n];cpu.mem_write(STREAM-16,b'\xA5'*(len(block)+32));cpu.mem_write(STREAM,block);before=bytes(cpu.mem_read(0x02000000,0x400000))
                for last in [0,1,2,3,0xFFFFFFFF]:
                    cpu.mem_write(OWNER-16,b'\xA5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+at,0,0));owner=bytes(cpu.mem_read(OWNER-16,64))
                    cpu.mem_write(RESULT-16,b'\xA5'*80);cpu.mem_write(RESULT,bytes(24));cpu.mem_write(LENGTH-16,b'\xA5'*36);cpu.mem_write(LENGTH,bytes(4))
                    call(cpu,0x2A510,(RESULT,OWNER,LENGTH,last));extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
                    assert at+extent==(target if last==2 else at+4) and struct.unpack('<6I',cpu.mem_read(RESULT,24))==(3,0,0,0,0,0)
                    assert bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(STREAM,len(block)))==block and bytes(cpu.mem_read(OWNER-16,64))==owner
                    for p in [STREAM-16,STREAM+len(block),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4]:assert bytes(cpu.mem_read(p,16))==b'\xA5'*16
                    cases.append(dict(block=n,offset=at,version=version,last_result=last,native_extent=extent,target=at+extent,only_result2_skips=True,all4MiB_owner_stream_ABI_and_boundary_guards_exact=True))
    assert sites and len(cases)==len(sites)*10
    ROOT.mkdir(parents=True);md=Cs(CS_ARCH_ARM,CS_MODE_ARM);asm='\n'.join(f'{i.address:08x}: {i.mnemonic} {i.op_str}'for i in md.disasm(arms[0][0x2A414:0x2A510],0x0202A414));(ROOT/'clean_current_exact_relative_handler.asm.txt').write_text(asm+'\n',encoding='utf8')
    save(ROOT/'original_clean_current_0400_result2_skip_proof.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_inventory='work/analysis/lil_after_Crew_Items_clean_scope_v3152/complete_clean_next_exchange_inventory.json',sites=sites,cases=cases,only_last_result2_takes_source_0400_span=True,explicit_FFFFFFFF_inventory_walk_exposes_fallthrough_without_changing_gameplay_state=True,original_handler_source_range=[0x2A414,0x2A5BC],original_clean_current_handler_sha256=sha(arms[0][0x2A414:0x2A5BC]),source_and_current_target_commands_are_native_boundaries=True,global_helpers_runtime_ROM_registry_and_ledger_unchanged=True,source_4100_text_objects_still_require_decoder_label_count_consumer_and_native_display_proofs=True,new_emulator_runs=0,editorial_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Source0400sites',len(sites),'clean/current native cases',len(cases),'Only result2 skips;allguards pass;no gameplay/credit claim.')
