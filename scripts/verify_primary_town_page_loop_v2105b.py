"""Bind native page returns to the unchanged inter-page continuation control."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC,UC_ARM_REG_LR
from scripts.probe_primary_town_glyph_pitch_v2062b import REGS
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_page_loop_v2105b')
BASE=0x02000000
INPUT=0x02660000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 rom=NdsImage.open('out/all_routes_combined_v2097_candidate.nds');arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert arm[0x54928:0x54984]==clean[0x54928:0x54984]
 obs=read('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_font_actual_v2098_V2097/common_observer/requests.json');seed=obs['rows'][0];raw=Path(seed['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==seed['snapshots']['WRAM']['sha256']
 fontproof=read('work/analysis/town_services_actual_pitch_v2103b/all155_correct_pitch_native_pages.json');multi=next(r for r in fontproof['cases']if r['page_count']>1);text=bytes.fromhex(multi['formatted_hex']);offset=multi['pages'][0]['consumed_bytes'];assert offset==86 and text[offset:]==b'  in tribute.'
 source_regs=seed['registers'];assert source_regs[4]==0 and source_regs[6]==source_regs[9]+0x30
 receipts=[]
 for label,returned,mode in [('continue_mode0',offset,0),('continue_mode4',offset,4),('cancel_mode5',offset,5),('continue_fullword_control',offset,0xFFFFFFFF),('end_of_text',len(text),0),('no_progress',0,0)]:
  cpu,get=get_machine(arm,raw);cpu.reg_write(UC_ARM_REG_CPSR,0x1F)
  for reg,value in zip(REGS,source_regs[:len(REGS)],strict=True):cpu.reg_write(reg,value)
  cpu.reg_write(REGS[8],INPUT);cpu.reg_write(REGS[0],INPUT+returned);cpu.mem_write(INPUT,text+b'\0');cpu.mem_write(source_regs[10]+0x54,struct.pack('<I',mode));before=bytes(cpu.mem_read(BASE,len(raw)));sp=source_regs[13]
  stops=(BASE+0x54E44,BASE+0xD3718,BASE+0x54910,BASE+0x54974)
  for pc in stops:cpu.hook_add(UC_HOOK_CODE,lambda u,p,s,d:u.emu_stop(),begin=pc,end=pc)
  cpu.emu_start(BASE+0x54928,BASE+0x54984,count=1000);pc=cpu.reg_read(UC_ARM_REG_PC);trace=[pc]
  if label in('end_of_text','no_progress'):
   assert pc==BASE+0x54974
  else:
   assert pc==BASE+0x54E44 and cpu.reg_read(UC_ARM_REG_LR)==BASE+0x5494C and cpu.reg_read(REGS[5])==INPUT+returned
   # These are explicit normal-return ABI boundaries. The original window
   # helper and bitmap commit execute in gameplay,not in this CPU control test.
   cpu.emu_start(BASE+0x5494C,BASE+0x54984,count=1000);pc=cpu.reg_read(UC_ARM_REG_PC);trace.append(pc)
   assert pc==BASE+0xD3718 and cpu.reg_read(UC_ARM_REG_LR)==BASE+0x54964
   assert [cpu.reg_read(r)for r in REGS[:4]]==[source_regs[9],0,0,0]and struct.unpack('<I',cpu.mem_read(sp,4))[0]==source_regs[6]
   cpu.emu_start(BASE+0x54964,BASE+0x54984,count=1000);pc=cpu.reg_read(UC_ARM_REG_PC);trace.append(pc)
   assert pc==(BASE+0x54974 if mode==5 else BASE+0x54910)and cpu.reg_read(REGS[8])==INPUT+returned
  assert cpu.reg_read(REGS[13])==sp and bytes(cpu.mem_read(INPUT,len(text)+1))==text+b'\0'
  after=bytearray(cpu.mem_read(BASE,len(raw)));after[sp-BASE:sp-BASE+4]=before[sp-BASE:sp-BASE+4];assert bytes(after)==before
  for index in(4,6,7,9,10,11):assert cpu.reg_read(REGS[index])==source_regs[index]
  receipts.append(dict(case=label,returned_offset=returned,mode=mode,native_stop_trace=trace,next_text_pointer=cpu.reg_read(REGS[8]),SP_and_callee_registers_and_whole4MiB_except_original_stack_store_exact=True))
 save(ROOT/'original_native_interpage_request_and_continuation_contract.json',dict(ARM9_sha256=sha(arm),source_font_snapshot=seed['snapshots']['WRAM'],native_font_page_proof='work/analysis/town_services_actual_pitch_v2103b/all155_correct_pitch_native_pages.json',original_clean_exact_control_span=[BASE+0x54928,BASE+0x54984],source_span_hex=arm[0x54928:0x54984].hex(),cases=receipts,original_next_page_pointer_and_terminal_no_progress_and_cancel_routes_pass=True,window_helper_54E44_and_bitmap_commit_D3718_are_explicit_unexecuted_normal_return_ABI_boundaries=True,font_painters_are_unstubbed_in_separate_page_proof=True,no_actual_income_visit_or_press_A_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(native_continuation_cases=len(receipts),original_source_control_exact=True,UI_and_bitmap_boundaries_explicit=True))
