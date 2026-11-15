"""Audit actual font contexts/RGB parity and explicit font-control capacity.

Glyph-paint returns in CPU capacity cases are boundaries,not pixel approval.
"""
from pathlib import Path
import struct
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_ARM_REG_LR
from scripts.probe_primary_town_glyph_pitch_v2062b import REGS
from scripts.verify_personal_gameplay_v841 import get_machine
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_consumer_audit_v2064')
RUN=Path('work/analysis/town_services_font_actual_v2060')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_font_actual_v2060_V2047')
if __name__=='__main__':
 assert not ROOT.exists();plan=read(RUN/'run_plan.json');terminal=read(RUN/'terminal.json');report=read(CAP/'capture_report.json');obs=read(CAP/'common_observer/requests.json')
 assert terminal['terminal']and terminal['all_observer_host_slots_restored']and report['frames']==38500
 assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
 assert report['ROM_sha256']==plan['candidate_sha256']==sha(Path(plan['candidate']).read_bytes())
 assert report['scripted_input_schedule']==read(plan['inputs'])and len(report['synthetic_gallery_fixtures'])==1
 assert not report['synthetic_gallery_fixtures'][0]['earned_unlock_verified']
 assert all(k=='synthetic_gallery_fixtures'or not v for k,v in report.items()if k.startswith('synthetic_'))
 assert sha(Path(plan['existing_isolated_system_unlock']).read_bytes())==plan['donor_sha256']
 assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']and len(obs['rows'])==8
 prior=read(plan['prior_report']);old={r['frame']:r for r in prior['frames_captured']};pairs=[]
 for p in report['frames_captured']:
  if p['frame']<31000:continue
  previous=old[p['frame']];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
  assert Image.open(p['path']).convert('RGB').tobytes()==Image.open(previous['path']).convert('RGB').tobytes()
  pairs.append(dict(frame=p['frame'],capture=p['path'],sha256=p['PNG_sha256'],prior=previous['path'],whole256x384_RGB_exact=True))
 assert len(pairs)==20
 arm=NdsImage.open(plan['candidate']).read_file('/__arm9__.bin');rows=[]
 for r in obs['rows']:
  assert r['CPU_WRAM_DTCM_ITCM_configuration_exact']and r['bounds']==[0,0,228,48]
  for snap in r['snapshots'].values():assert sha(Path(snap['path']).read_bytes())==snap['sha256']
  raw=Path(r['snapshots']['WRAM']['path']).read_bytes();context=bytes.fromhex(r['context128_hex'])
  assert struct.unpack_from('<2I',raw,0x31209C)==(6,12)and struct.unpack_from('<2I',context,56)==(6,12)
  rows.append(dict(native_ID=r['source_request']['ID'],font_frame=r['frame'],source_request=r['source_request'],bounds=r['bounds'],font6x12=True,source_font_observation=r))
 pitch=read('work/analysis/town_services_glyph_pitch_v2062b/eight_original_native_font_continuations.json')
 assert all(r['original_return_completed']and r['nonblank_glyph_order_complete']and not r['error']and r['SP_preserved']and r['input_bytes_unchanged']for r in pitch['rows'])
 assert next(r for r in pitch['rows']if r['message_ID']==49)['native_row_origins']==[0,12]
 seed=obs['rows'][0];raw=Path(seed['snapshots']['WRAM']['path']).read_bytes();capacity=[]
 for phase in range(4):
  for first in('A','Ab'):
   for lines in(4,5):
    text=(first+'\n  B\n  C\n  D'+('\n  E'if lines==5 else '')).encode('ascii');pointer=0x02670000+phase
    cpu,get=get_machine(arm,raw);cpu.reg_write(UC_ARM_REG_CPSR,0x1f)
    for reg,value in zip(REGS,seed['registers']):cpu.reg_write(reg,value)
    for label,at in(('DTCM',seed['DTCM_base']),('ITCM',0)):
     blob=Path(seed['snapshots'][label]['path']).read_bytes()
     try:cpu.mem_write(at,blob)
     except Exception:cpu.mem_map(at,len(blob));cpu.mem_write(at,blob)
    cpu.mem_write(pointer-16,b'\xa5'*(len(text)+33));cpu.mem_write(pointer,text+b'\0');cpu.reg_write(UC_ARM_REG_R1,pointer);events=[]
    def glyph(u,pc,size,data):
     code,style=struct.unpack('<2I',u.mem_read(u.reg_read(REGS[13]),8));events.append(dict(code=code,x=u.reg_read(REGS[2]),y=u.reg_read(REGS[3])))
     u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    for pc in(0x020D16B4,0x01FF83AC):cpu.hook_add(UC_HOOK_CODE,glyph,begin=pc,end=pc)
    cpu.emu_start(seed['PC'],seed['LR'],count=2000000)
    assert cpu.reg_read(UC_ARM_REG_PC)==seed['LR']and cpu.reg_read(REGS[13])==seed['registers'][13]
    assert sorted({e['y']for e in events})==[0,12,24,36]
    assert ''.join(chr(e['code'])for e in events if e['code']!=32)==first+'BCD'
    consumed=cpu.reg_read(UC_ARM_REG_R0)-pointer
    assert 0<consumed<=len(text)and(consumed==len(text))==(lines==4)
    assert bytes(cpu.mem_read(pointer-16,len(text)+33))==b'\xa5'*16+text+b'\0'+b'\xa5'*16
    capacity.append(dict(alignment=phase,first_row=first,input_lines=lines,native_row_origins=[0,12,24,36],consumed_bytes=consumed,input_bytes=len(text),fifth_line_not_drawn=lines==5,original_control_complete=True,glyph_paint_return_boundary=True))
 ROOT.mkdir(parents=True)
 save(ROOT/'actual_eight_consumers_four12pixel_rows_and_numeric_scope.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],ARM9_sha256=sha(arm),
  actual_font_observer=str(CAP/'common_observer/requests.json'),actual_font_observer_sha256=sha((CAP/'common_observer/requests.json').read_bytes()),actual_font_rows=rows,
  whole_town_RGB_pairs=pairs,body_paper=[228,48],font_dimensions=[6,12],native_row_step=12,font_control_capacity_cases=capacity,
  current_38500frame_readonly_replay_complete=True,existing_system_unlock_not_earned=True,no_savestate_story_location_RNG_funds_outcome_fixture=True,
  four_rows_fit_fifth_returns_unconsumed=True,capacity_cases_use_glyph_paint_return_boundary_not_full_pixel_proof=True,
  unsupported_full_native_clones_preserved=['work/analysis/town_services_consumers_v2059','work/analysis/town_services_consumers_v2059b','work/analysis/town_services_glyph_pitch_v2062'],
  no_revised_batch_native_font_repack_pagination_gameplay_or_release_approval=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(actual_body_contexts=8,whole_RGB_pairs=20,native_capacity_cases=len(capacity),body=[228,48],font=[6,12],rows=4,no_formatting_approval=True))
