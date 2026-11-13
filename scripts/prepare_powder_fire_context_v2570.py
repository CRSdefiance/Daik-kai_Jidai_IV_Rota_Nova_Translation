"""Six fire alerts;original per-battery gunner/direct caller and follow-up context."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R8,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.powder_fire_native_plan_v1309 import compiled
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/powder_fire_context_v2570');IDS=list(range(2052,2058));BASE=0x02000000;TABLE=0x02117980
if __name__=='__main__':
 assert not ROOT.exists()
 ledger=read('translations/editorial_review_current_v1.json');c=ledger['current_integrated_candidate'];rom=NdsImage.open(c['path']);clean=NdsImage.open('work/clean.nds');arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin');en=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
 assert sha(Path(c['path']).read_bytes())==c['sha256']
 configpath=Path('translations/powder_fire_editorial_release_v1.json');config=read(configpath);manuscriptpath=Path(config['manuscript']);prior={r['message_id']:r for r in read(manuscriptpath)['records']};stage=read(Path(c['path']).with_suffix('.manifest.json'))['relocations']['/COMMON/MESFILE.DK4']['powder_fire_editorial']
 assert sha(configpath.read_bytes())==stage['release_config_sha256'] and sha(manuscriptpath.read_bytes())==config['dependencies'][str(manuscriptpath)] and stage['proof']['native_IDs']==IDS
 historical={r['message_id']:dict(family=f['id'],record=r) for f in ledger['completed_editorial_families'] for r in f['records'] if r.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4' and r.get('message_id') in IDS};fresh={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};assert len(historical)==6 and not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') in fresh for n in IDS)
 def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
 def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),current_reference=ref(en[n]),source_hex=jp[n].text.hex(),current_hex=en[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_stored_English=en[n].text.decode('cp932'),historical_review=historical.get(n),selected=n in IDS)
 records=[record(n) for n in IDS];neighbors=[record(n) for n in(2051,2058)];followups=[record(n) for n in(585,586)]
 assert all(r['source_hex']==prior[r['message_ID']]['source_hex'] and bytes.fromhex(r['current_hex'])==compiled(prior[r['message_ID']]) for r in records)
 historypath=Path('work/analysis/powder_fire_verified_v1322b/actual_powder_fire_verification.json');h=read(historypath);reportpath=Path(h['report']);report=read(reportpath);assert sha(reportpath.read_bytes())==h['report_sha256'] and report['ROM_sha256']==h['candidate_sha256']
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};item=snapshots[7210];snapshot=Path(item['path']);raw=snapshot.read_bytes();assert sha(raw)==item['sha256']
 spans=((0x755CC,0x7564C),(0x55DC4,0x55E6C),(0x53F0C,0x53F9C),(0x7E988,0x7E99C),(0x117980,0x1179A0))
 for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
 cpu,get=get_machine(arm,raw);root=get(0xCB184);fleets=get(0xCB1A8);objects=[root+4+i*32 for i in range(207)]+[root+0x19E4]
 values=list(struct.unpack_from('<8i',arm,TABLE-BASE));assert values==[2052,2053,-1,-1,2054,2055,2056,2057];choices=[]
 for slot,obj in enumerate(objects):
  voice=get(0x7E988,obj);n=get(0x53F4C,obj,TABLE);assert n==(values[voice] if values[voice]!=-1 else 2052)
  choices.append(dict(actor_slot=slot,actor_object=obj,actor_ID=get(0x7EE08,obj),voice_class=voice,message_ID=n,original_negative_member_fallback=values[voice]==-1))
 assert {r['message_ID'] for r in choices}==set(IDS) and get(0x53F4C,0,TABLE)==2052
 mobile=get(0x36C70,fleets+4+132+12);gunner=get(0x82428,fleets+0x2090,9);assert get(0x7EE08,gunner)==16 and get(0x53F4C,gunner,TABLE)==2053
 sections=MainCodeFile(arm,BASE).sections;battery_calls=[]
 for slot in range(4):
  u,g=get_machine(arm,raw);expected_actor=g(0x55DC4,mobile,slot);seen=[];executed=set();before=bytes(u.mem_read(root,0x1A04))
  def exact(v,pc,size,unused):
   for section in sections:
    start=section.ramAddress
    if start<=pc and pc+size<=start+len(section.data):
     assert bytes(v.mem_read(pc,size))==bytes(section.data[pc-start:pc-start+size]);executed.add(pc);break
  def observe(v,pc,size,unused):
   if pc==BASE+0x75614:v.emu_stop();return
   seen.append(dict(entry=pc,original_return=v.reg_read(UC_ARM_REG_LR),arguments=[v.reg_read(r) for r in(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]))
   v.reg_write(UC_ARM_REG_PC,v.reg_read(UC_ARM_REG_LR))
  u.hook_add(UC_HOOK_CODE,exact)
  for pc in(BASE+0x53F0C,BASE+0x75614):u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
  u.mem_write(STACK+0x28,struct.pack('<I',slot));u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP);u.reg_write(UC_ARM_REG_R8,mobile)
  u.emu_start(BASE+0x75600,STOP,count=100000)
  assert u.reg_read(UC_ARM_REG_PC)==BASE+0x75614 and len(seen)==1 and seen[0]['entry']==BASE+0x53F0C and seen[0]['arguments'][:2]==[expected_actor,TABLE] and seen[0]['original_return']==BASE+0x75614
  assert bytes(u.mem_read(root,0x1A04))==before
  battery_calls.append(dict(original_battery_slot=slot,original_mobile_ship=mobile,original_gunner_object=expected_actor,original_gunner_actor_ID=g(0x7EE08,expected_actor) if expected_actor else None,selected_message_ID=g(0x53F4C,expected_actor,TABLE),original_call=seen[0],executed_current_instruction_addresses=len(executed),all_executed_section_code_current_exact=True,actor_model_bytes_unchanged=True,CPU_stack_slot_argument_only_no_new_fire_or_eligibility_claim=True))
 assert gunner in[get(0x55DC4,mobile,slot) for slot in range(4)]
 ROOT.mkdir(parents=True);packetpath=ROOT/'all6_clean_current_context_catalog.json';contextpath=ROOT/'source_context_packet.json'
 save(packetpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),selected_IDs=IDS,records=records,neighbors=neighbors,extinguished_followup_candidates_context_only=followups,followup585_586_identical_current_payload=en[585].text==en[586].text,catalog_order_not_assumed_dialogue_chronology=True,source_prose_or_fresh_pass_credit_added=0,editorial_current_native_historical_and_registered_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 save(contextpath,dict(current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),actual_snapshot=str(snapshot),actual_snapshot_sha256=sha(raw),snapshot_historical_V1316_not_current_gameplay=True,original_signed_eight_members=values,all208_original_voice_selections=choices,null_actor_original_fallback_ID=2052,four_current_original_gun_position_speaker_prefixes=battery_calls,
  actual_ship_Gunnery_role9_actor16_is_one_original_battery_gunner=True,actual_source_selected_ID=2053,original_entry=0x02053F0C,original_parent=0x02053F40,original_table_stack_offset=0x274,original_table=TABLE,original_callsite=0x02075610,no_actor_ID_roster_RNG_or_fire_flag_changes=True,
  original_source_code=[dict(start=a,end=b,sha256=sha(arm[a:b]),current_clean_historical_snapshot_exact=True) for a,b in spans],
  complete_exchange_context='Original powder-fire alert from the damaged ship\'s per-battery gunner selected by55DC4(mobile,original stack+28 battery slot),then53F0C(gunner,02117980). This is direct parent53F40/table+274,not role1 or a role9 speech call;Gerhard16 happens to occupy Gunnery9 and is an original gun-position speaker in the preserved own-ship sample. Table slots2/3 are -1 and fall back to2052,not2054. Four current CPU post-eligibility prefixes vary only the original battery-slot stack argument,not actor IDs,crew assignments,RNG,fire state or actual gameplay. Read the complete alert,then original Fire extinguished response and battle return. Historical follow-up cached bytes match both585/586;do not claim one individually selected ID without a getter trace. Cleanup of original fire bit is deferred until that follow-up is dismissed,not while it is still displayed. The corrected1322b proof is authoritative;1322\'s premature cleanup expectation is preserved. No new ignition source,explosion,casualty,ship loss or earned assignment is inferred.',no_new_prose_or_fresh_or_completion_credit=True,full_goal_complete=False))
 save(ROOT/'next6_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(manuscriptpath),registered_manuscript_sha256=sha(manuscriptpath.read_bytes()),all6_clean_current_registered_compilations_match=True,all208_voice_choices_and4_current_original_gun_position_prefixes_pass=True,historical_family_proof=str(historypath),historical_family_proof_sha256=sha(historypath.read_bytes()),historical_individual_IDs=[2053],current_followup_candidates_context_only_no_extra_credit=True,fresh_credit=0,full_goal_complete=False))
 print('Next6 powder-fire alerts:208 original voices,four current per-battery direct speaker prefixes,follow-up context;zero fresh credit.')
