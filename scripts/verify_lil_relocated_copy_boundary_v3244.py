"""Prove the moved original return still excludes the preserved appended copy."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.classify_lil_B115_tail_v3216 import graph,ACTIVE,BASE
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prepare_lil_B111_B119_research_v3240b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_relocated_copy_v3244')
if __name__=='__main__':
    assert not ROOT.exists();plan=read(PLAN);spec=next(b for b in plan['blocks'] if b['block']==115);copy=spec['unowned_appended_copy']
    image,parent=NdsImage.open(ROM),NdsImage.open(PARENT);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[115]
    old=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks[115]
    at=copy['new_offset'];logical=8+struct.unpack_from('<H',block,4)[0]
    assert logical-at==1886 and block[at:logical]==old[440:2326] and sha(block[at:logical])==copy['sha256']
    inventory,_,_=scoped_inventory();commands,_=inventory(arm,block);cfg=graph(commands,8,logical)
    assert cfg['reachable_return0_commands']==[at-4] and not any(p>=at for p in cfg['reachable_commands'])
    assert block[at-4:at]==bytes(4);cases=[]
    for mode in [0,1]:
        cpu=machine(arm);stream,owner=0x02660000,0x02662000
        cpu.mem_write(stream-16,b'\xa5'*(len(block)+32));cpu.mem_write(stream,block)
        cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,struct.pack('<2I',0,stream+at-4));owner_before=bytes(cpu.mem_read(owner-16,64))
        cpu.mem_write(ACTIVE,struct.pack('<I',1));before=bytes(cpu.mem_read(BASE,0x400000));executed=[];reads=[]
        def observe(u,pc,size,unused):
            executed.append(pc)
            if pc==BASE+0x2A524:reads.append(pc)
        hook=cpu.hook_add(UC_HOOK_CODE,observe)
        try:call(cpu,0x23FFC,(0,owner,0,mode),instruction_limit=20000)
        finally:cpu.hook_del(hook)
        assert reads==[BASE+0x2A524] and BASE+0x24098 in executed and BASE+0x240EC not in executed
        assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owner_before
        assert bytes(cpu.mem_read(stream,len(block)))==block
        assert bytes(cpu.mem_read(stream-16,16))==bytes(cpu.mem_read(stream+len(block),16))==b'\xa5'*16
        cases.append(dict(mode=mode,return_word_offset=at-4,sole_native_decoder_call_reads_return0=True,original_VM_returns_before_cursor_advance=True,ABI_all4MiB_owner_stream_and_boundary_guards_exact=True,source_owned_ACTIVE1_is_isolated_VM_input_not_a_gameplay_fixture=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'moved_return0_and_unowned_copy_proof.json',dict(research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),source_plan=str(PLAN),source_plan_sha256=sha(PLAN.read_bytes()),unowned_copy=copy,conservative_relocated_prefix_graph=cfg,original_VM_return_cases=cases,all32_unowned_copy_speeches_byte_exact_and_unreachable_from_ordinary_Lil_entry=True,canonical_Maria_SC3_B97_32_targets_pending_uncredited=True,no_new_entrypoint_route_macro_or_gameplay_fixture=True,new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Moved B115 return0:both native VM modes andfull prefix graph exclude the exact1886byte unowned copy. CanonicalMaria32 remains queued.')
