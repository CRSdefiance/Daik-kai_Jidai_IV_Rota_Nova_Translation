"""Bind current trade/port prose to clean decisions and actual installed typed-number calls."""
from pathlib import Path
import struct
from itertools import product
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R6,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_SP,UC_ARM_REG_PC,UC_ARM_REG_LR
from scripts.probe_primary_town_glyph_pitch_v2062b import REGS
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import review_market_stock_v755 as stock,review_port_services_v761 as port,review_shipyard_editorial_v759 as yard,verify_town_event_context_v750 as trend
from dk4tool.patch.shipyard_editorial import PRICE_RETURNS,DAY_RETURN
ROOT=Path('work/analysis/town_trade_port_context_v2150');REPORT=Path('E:/Rota Nova translations/Generated/work/emulation_v193/promoter_context_live_v2144_V2143/capture_report.json')
def number(n):return str(n).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);rom=NdsImage.open('out/all_routes_combined_v2143_candidate.nds');arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');report=read(REPORT);snapshot=next(r for r in report['read_only_pause_RAM_snapshots']if r['frame']==3200);raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
 spans=[]
 for a,b in stock.SPANS:assert arm[a:b]==clean[a:b];spans.append(dict(start=a,end=b,sha256=sha(clean[a:b])))
 stock_cases=stock.fragments(arm);assert stock_cases==stock.fragments(clean)and len(stock_cases)==36
 trend_source=read('work/analysis/town_events_v750/native_context.json')
 for r in trend_source['original_code_spans']:assert clean[r['start']:r['end']]==arm[r['start']:r['end']]
 trend_cases=trend.trend(arm);assert trend_cases==trend.trend(clean)and len(trend_cases)==288
 port.RAM_REPORT=REPORT;port_proof=port.context(arm,clean);assert len(port_proof['all416_original_companion_actor_flag_cases'])==416
 yard_source=read('work/analysis/shipyard_editorial_v759/native_context.json');bindings=[]
 for r in yard_source['original_call_bindings']:
  a,b=r['load']-BASE,r['call']-BASE+4;assert arm[a:b]==clean[a:b];bindings.append(dict(**r,clean_current_source_instructions_exact=True,span_sha256=sha(clean[a:b])))
 for a,b in((0x63038,0x63044),(0x62B8C,0x62D40),(0xBBC24,0xBBC38),(0x5FB54,0x5FD20)):assert arm[a:b]==clean[a:b]
 voices=yard.voice_cases(arm);assert voices==yard.voice_cases(clean);preparation=yard.preparation_cases(arm);assert preparation==yard.preparation_cases(clean)
 pronouns=yard.pronoun_and_literal_cases(clean,arm);assert len(pronouns)==16
 amounts=(0,1,9,99,1000,50000,1000000,2147483647);typed=[];cs=Cs(CS_ARCH_ARM,CS_MODE_ARM)
 for ret,n in product((*PRICE_RETURNS,DAY_RETURN),amounts):
  u,_=get_machine(arm,raw);u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R0,n);before=[u.reg_read(REGS[i])for i in range(4,12)];word=bytes(u.mem_read(ret-4,4));instruction=next(cs.disasm(word,ret-4));assert instruction.mnemonic=='bl';u.emu_start(ret-4,ret,count=100000)
  ptr=u.reg_read(UC_ARM_REG_R0);text=bytes(u.mem_read(ptr,100)).split(b'\0')[0];suffix=(b' day'if n==1 else b' days')if ret==DAY_RETURN else(b' gold coin'if n==1 else b' gold coins');assert text==number(n)+suffix,(ret,n,text)
  assert u.reg_read(UC_ARM_REG_PC)==ret and u.reg_read(UC_ARM_REG_SP)==STACK and[u.reg_read(REGS[i])for i in range(4,12)]==before
  typed.append(dict(return_PC=ret,original_call_word_hex=word.hex(),installed_target=instruction.op_str,value=n,returned_pointer=ptr,complete_typed_argument_hex=text.hex(),native_number_and_installed_adapter_unstubbed=True,stack_and_callee_registers_preserved=True))
 print(dict(stock_fragments=36,trend_cases=288,companion_cases=416,typed_number_original_calls=len(typed)),flush=True)
 copies=[]
 for days,amount,name_text in product((0,1,2,16),(1,50000),('Vestaros','FALCON','ICARUS')):
  u,_=get_machine(arm,raw);model,vt,getter,name=0x02450000,0x02451000,0x02452000,0x02453000;u.mem_write(model,struct.pack('<I',vt));u.mem_write(vt+4,struct.pack('<I',getter));u.mem_write(name,name_text.encode()+b'\0');u.reg_write(UC_ARM_REG_SP,STACK);u.emu_start(BASE+0x63038,BASE+0x63044,count=10);assert struct.unpack('<I',u.mem_read(STACK+0x18,4))[0]==804
  for reg,v in((UC_ARM_REG_R6,model),(UC_ARM_REG_R8,amount),(UC_ARM_REG_R9,0x02454000),(UC_ARM_REG_R10,0x02455000)):u.reg_write(reg,v)
  events=[]
  def watch(cpu,at,size,unused):
   if at in(BASE+0x62B8C,getter):cpu.reg_write(UC_ARM_REG_R0,days if at==BASE+0x62B8C else name);cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
   elif at==BASE+0x53F9C:
    selected=cpu.reg_read(UC_ARM_REG_R1);pointers=[cpu.reg_read(UC_ARM_REG_R2),cpu.reg_read(UC_ARM_REG_R3)]
    if selected==803:pointers.append(struct.unpack('<I',cpu.mem_read(STACK,4))[0])
    events.append((selected,[bytes(cpu.mem_read(p,100)).split(b'\0')[0].hex()for p in pointers]));cpu.emu_stop()
  h=u.hook_add(UC_HOOK_CODE,watch)
  try:u.emu_start(BASE+0x63114,0x027E0000,count=100000)
  finally:u.hook_del(h)
  values=[name_text.encode(),number(amount)+(b' gold coin'if amount==1 else b' gold coins')]+([number(days)+(b' day'if days==1 else b' days')]if days else[]);assert events==[(803 if days else804,[v.hex()for v in values])],events
  copies.append(dict(supplied_days=days,amount=amount,literal_name=name_text,native_selected_ID=events[0][0],argument_hex=events[0][1],original_numeric_calls_not_rewritten_or_intercepted=True))
 save(ROOT/'clean_graphs_current_typed_arguments_and_companion_roles.json',dict(ARM9_sha256=sha(arm),clean_ARM9_sha256=sha(clean),source_spans=spans,all36_stock_letter_fragments=stock_cases,all288_trend_selections=trend_cases,port=port_proof,yard_speech_bindings=bindings,yard_eight_voice_selections=voices,all160_supplied_preparation_cases=preparation,IC_first_person_not_a_character_name_cases=pronouns,all56_original_numeric_calls=typed,all24_original_copy_purchase_arguments=copies,source_snapshot=snapshot,explicit_supplied_getter_and_UI_boundaries_not_full_eligibility_or_earned_progress=True,no_ROM_or_registry_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(contexts='pass',typed_calls=len(typed),copy_arguments=len(copies)),flush=True)
