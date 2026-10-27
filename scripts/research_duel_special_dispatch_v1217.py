"""Prove cache-tail ownership and exact dispatch before a ROM is registered."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.common_single_cache_v861 import SINGLE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts.duel_special_dispatch_v1217 import helper,front,HELPER,HELPER_END,FRONT,FRONT_END,TABLES,IDS
from scripts.duel_bark_front_v1201 import assemble as old_front
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_escape_direct_runtime_v1184b import literal_accesses
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_dispatch_v1217')
ROM=Path('out/all_routes_combined_v1206_candidate.nds')
BASE=0x02000000


def main():
    assert not ROOT.exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(arm)=='13478d94d189bf0fa89b4af2e29147ca8fc7a0567651fb1238e75265071d479d'
    assert arm[0x535E0:0x535E8]==SINGLE and arm[HELPER-BASE:HELPER_END-BASE]==clean[HELPER-BASE:HELPER_END-BASE]
    assert arm[FRONT-BASE:FRONT_END-BASE]==old_front(1480)[0]
    span=[(HELPER,HELPER_END)];private=[(0x020535E0,HELPER_END),(0x0200DA28,FRONT_END)]
    before_refs=census(rom,span,private);before_literals=literal_accesses(rom,span)
    assert before_refs==[] and before_literals==[]
    h,ha,hn=helper();f,fa,fn=front(1480)
    target=bytearray(arm);target[HELPER-BASE:HELPER_END-BASE]=h;target[FRONT-BASE:FRONT_END-BASE]=f;target=bytes(target)
    assert target[0x535E0:0x535E8]==arm[0x535E0:0x535E8]==SINGLE
    restored=bytearray(target)
    for lo,hi in ((HELPER,HELPER_END),(FRONT,FRONT_END)):restored[lo-BASE:hi-BASE]=arm[lo-BASE:hi-BASE]
    assert bytes(restored)==arm
    old,new=map(lambda v:MainCodeFile(v,BASE),(arm,target))
    shape=lambda o:[(s.ramAddress,len(s.data),s.bssSize) for s in o.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(target)
    assert all(old.sections[i].data==new.sections[i].data for i in (1,2,3,4)) and len(new.sections[3].data)-48==123040
    after=NdsImage.open(ROM);after.rom.arm9=target
    after_refs=census(after,span,private);after_literals=literal_accesses(after,span)
    assert len(after_refs)==1 and after_refs[0][0]=='Thumb_BL_BLX' and after_refs[0][3]==HELPER and after_refs[0][-1]
    assert all(any(lo<=r[2]<hi for lo,hi in private) for r in after_literals)
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_bark_v1207_1206/frame_006113_arm9_ram.bin').read_bytes()
    cpu,get=get_machine(target,raw)
    for lo,hi in ((HELPER,HELPER_END),(FRONT,FRONT_END)):cpu.mem_write(lo,target[lo-BASE:hi-BASE])
    context,pointer=0x02460000,0x02461000
    for pc in (0x0205528C,0x020D5404):cpu.hook_add(UC_HOOK_CODE,lambda c,p,s,d:c.emu_stop(),begin=pc,end=pc)
    count=0;selected=0
    def check(parent,key):
        nonlocal count,selected
        cpu.mem_write(context+108,struct.pack('<I',parent));cpu.mem_write(context+148,struct.pack('<I',key))
        cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP);cpu.reg_write(UC_ARM_REG_R0,context);cpu.reg_write(UC_ARM_REG_R1,pointer)
        cpu.emu_start(FRONT|1,STOP,count=300)
        wanted=(parent==0x0200D4BC and key in TABLES) or (parent==0x0200D528 and key in IDS)
        assert cpu.reg_read(UC_ARM_REG_PC)==(0x0205528C if wanted else 0x020D5404),(hex(parent),hex(key))
        assert cpu.reg_read(UC_ARM_REG_SP)==STACK-16
        if wanted:assert cpu.reg_read(UC_ARM_REG_R0)==1931
        else:assert (cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1))==(context,pointer)
        count+=1;selected+=wanted
    for low in range(65536):check(0x0200D4BC,0x02110000|low)
    assert selected==5
    for low in range(65536):check(0x0200D528,low)
    assert selected==20
    controls=(*TABLES,*IDS,0,0xFFFFFFFF,0x02117500,0x02117620)
    for parent in (0,0xFFFFFFFF,0x0200D4B8,0x0200D52C,0x1200D4BC,0x1200D528):
        for key in controls:check(parent,key)
    for parent in (0x0200D4BC,0x0200D528):
        for key in controls:check(parent,key)
        for high in (1,0x0210,0x0212,0x1211,0xFFFF):
            for low in (1980,1993,2146,0x7340,0x7560,0x75C0):check(parent,(high<<16)|low)
    # The public ARM slot entry remains the same two instructions for every
    # source message ID; full native copies are a separate next gate.
    for n in range(3668):assert get(0x535E0,0x0228E6DC,n)==0
    ROOT.mkdir(parents=True);out=ROOT/'ARM9_DISPATCH_RESEARCH_ONLY.bin';out.write_bytes(target)
    save(ROOT/'owned_dispatch_proof.json',{'source_ROM_sha256':sha(ROM.read_bytes()),'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),
        'research_ARM9':str(out),'source_owned_ARM_cache_slot_function':[0x020535E0,HELPER_END],
        'exact_live_single_slot_return0_BX_prefix_preserved':True,
        'unreachable_original_tail_reused_only_after_complete_no_incoming_reference_census':True,
        'source_tail_hex':arm[HELPER-BASE:HELPER_END-BASE].hex(),'helper_hex':h.hex(),'helper_assembly':ha,'helper_code_and_owned_bytes':[hn,64],
        'source_front_hex':arm[FRONT-BASE:FRONT_END-BASE].hex(),'target_front_hex':f.hex(),'front_assembly':fa,'front_code_and_owned_bytes':[fn,108],
        'source_incoming_refs':before_refs,'target_incoming_refs':after_refs,'source_PC_literal_refs':before_literals,'target_PC_literal_refs':after_literals,
        'all_other_bytes_restore_exact_sections_BSS_cache_arena_ITCM_and123040_staged_unchanged':True,
        'exact_front_dispatch_cases':count,'all65536_voice_and65536_numeric_keys_and_negative_controls_pass':True,
        'exact_qualified_parent_tables':[0x0200D4BC,list(TABLES)],'exact_qualified_parent_IDs':[0x0200D528,list(IDS)],
        'all3668_original_ARM_slot_calls_still_return0':True,'native_full_fonts_copies_actual_and_registered_integration_pending':True,
        'no_ROM_or_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Owned dispatch:',hn,'/64 helper,',fn,'/108 front;',count,'exact cases;3668 live slot entries unchanged.',flush=True)


if __name__=='__main__':main()
