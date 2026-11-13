"""Use captured production compact-font state; no metric, view, or glyph stubs."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_SP,UC_ARM_REG_CPSR
from scripts.probe_primary_town_glyph_pitch_v2062b import REGS
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import glyph_codes
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/production_compact_capacity_v2138')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/promoter_context_live_v2136_V2097/common_observer/requests.json')
BASE=0x02000000;INPUT=0x0228E5A8;STOP=0x02FFFFFC
RECEIPTS=[('square','work/analysis/square_context_pages_v2130b/all_square_native_pages.json'),('town','work/analysis/town_services_actual_pitch_v2103b/all155_correct_pitch_native_pages.json'),('market','work/analysis/market_context_pages_v2115/all18_market_native_pages.json')]
def captured_machine(arm,row):
 raw=Path(row['snapshots']['WRAM']['path']).read_bytes();assert sha(raw)==row['snapshots']['WRAM']['sha256'];cpu,_=get_machine(arm,raw)
 for label,addresses in [('DTCM',[row['DTCM_base']]),('ITCM',[0,0x01FF8000])]:
  data=Path(row['snapshots'][label]['path']).read_bytes();assert sha(data)==row['snapshots'][label]['sha256']
  for address in addresses:
   try:cpu.mem_write(address,data)
   except Exception:cpu.mem_map(address,len(data));cpu.mem_write(address,data)
 cpu.mem_map(0x06000000,0x100000);cpu.mem_write(0x06000000,bytes(0x100000));cpu.reg_write(UC_ARM_REG_CPSR,0x1F)
 for reg,value in zip(REGS,row['registers'][:len(REGS)],strict=True):cpu.reg_write(reg,value)
 return cpu

def probe(arm,row,text):
 cpu=captured_machine(arm,row);ctx=row['registers'][0];assert list(struct.unpack('<12I',cpu.mem_read(ctx,48)))[1:11]==[0,0,228,48,1,0,0,0,0,0]
 assert struct.unpack('<2I',cpu.mem_read(0x02312098+4,8))==(6,12)
 guard=bytes.fromhex('a7b35c91')*8;cpu.mem_write(INPUT-32,guard);cpu.mem_write(INPUT,text+b'\0'+guard)
 cpu.reg_write(UC_ARM_REG_R0,ctx);cpu.reg_write(UC_ARM_REG_R1,INPUT);cpu.reg_write(UC_ARM_REG_LR,STOP)
 before_sp=cpu.reg_read(UC_ARM_REG_SP);before_regs=[cpu.reg_read(REGS[i])for i in range(4,12)];glyphs=[];faults=[]
 def observe(u,pc,size,data):
  code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8));glyphs.append(dict(PC=pc,code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
 for pc in(0x020D16B4,0x01FF83AC):cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
 def invalid(u,access,address,size,value,data):faults.append(dict(access=access,address=address,size=size,PC=u.reg_read(UC_ARM_REG_PC)));return False
 cpu.hook_add(UC_HOOK_MEM_INVALID,invalid);cpu.emu_start(0x01FFCE40,STOP,count=2000000)
 consumed=cpu.reg_read(UC_ARM_REG_R0)-INPUT;assert 0<consumed<=len(text) and cpu.reg_read(UC_ARM_REG_PC)==STOP and not faults
 assert before_sp==cpu.reg_read(UC_ARM_REG_SP) and before_regs==[cpu.reg_read(REGS[i])for i in range(4,12)]
 assert bytes(cpu.mem_read(INPUT-32,32))==guard and bytes(cpu.mem_read(INPUT,len(text)+1+32))==text+b'\0'+guard
 codes=[e['code']for e in glyphs if e['code']!=32];assert codes==glyph_codes(text[:consumed]),(consumed,text,glyphs)
 assert all(0<=e['x'] and e['x']+(12 if e['code']>255 else 6)<=228 and 0<=e['y'] and e['y']+11<=48 for e in glyphs)
 vram=bytes(cpu.mem_read(0x06000000,0x100000));assert not any(vram[:0x1A000])and not any(vram[0x1A000+144*48:])
 for y in range(48):assert not any(vram[0x1A000+y*144+114:0x1A000+(y+1)*144])
 return dict(consumed_bytes=consumed,input_bytes=len(text),complete=consumed==len(text),logical_row_origins=sorted({e['y']for e in glyphs}),ordered_glyphs=glyphs,VRAM_sha256=sha(vram),input_and_canaries_exact=True,ABI_preserved=True,full_native_execution_without_glyph_or_UI_stubs=True)

if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);obs=read(OBS);row=obs['rows'][0];assert row['source_request']['ID']==675 and row['font_input_offset']==0
 arm=NdsImage.open('out/all_routes_combined_v2097_candidate.nds').read_file('/__arm9__.bin');cases=[];sources=[]
 plan=read('work/analysis/square_context_payload_v2124/native_payload_plan.json');assert plan['all_executable_font_other_runtime_and123040_staged_bytes_exact']
 for kind,path in RECEIPTS:
  receipt=read(path);sources.append(dict(kind=kind,path=path,sha256=sha(Path(path).read_bytes())))
  for index,r in enumerate(receipt['cases']):
   text=bytes.fromhex(r['formatted_hex']);position=0;pages=[]
   while position<len(text):
    page=probe(arm,row,text[position:]);pages.append(dict(input_offset=position,**page));position+=page['consumed_bytes'];assert len(pages)<=3
   cases.append(dict(kind=kind,index=index,message_ID=r.get('message_ID'),formatted_hex=text.hex(),pages=pages,page_count=len(pages)))
  print(dict(kind=kind,cases=sum(r['kind']==kind for r in cases),pages=sum(r['page_count']for r in cases if r['kind']==kind)),flush=True)
 five=b'  First row.\n  Second row.\n  Third row.\n  Fourth row.\n  Fifth row.';capacity=probe(arm,row,five);assert not capacity['complete']and capacity['logical_row_origins']==[0,12,24,36]and five[capacity['consumed_bytes']:].strip()==b'Fifth row.'
 save(ROOT/'all307_production_native_font_cases.json',dict(source_observer=str(OBS),source_observer_sha256=sha(OBS.read_bytes()),ARM9_sha256=sha(arm),source_receipts=sources,cases=cases,case_count=len(cases),page_count=sum(r['page_count']for r in cases),multi_page_cases=[dict(kind=r['kind'],index=r['index'],message_ID=r['message_ID'])for r in cases if r['page_count']>1],five_row_capacity_control=capacity,production_metrics=[6,12],production_logical_view=[228,48],physical_framebuffer_row_pitch_16_is_not_logical_capacity=True,VRAM_zero_initialized_explicit_not_live_GPU_state=True,no_geometry_or_runtime_change=True,Square_text_payload_execution_inherited_only_under_verified_executable_font_identity=True,earlier_16_metric_48_plane_pagination_claims_superseded=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(cases=len(cases),pages=sum(r['page_count']for r in cases),multi=sum(r['page_count']>1 for r in cases)),flush=True)
