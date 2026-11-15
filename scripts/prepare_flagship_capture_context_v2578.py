"""Five capture reports;two registered prose owners and original logical-role fallback."""
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_aftermath_native_plan_v1255 import compiled as original_compiled
from scripts.flagship_precision_native_plan_v1356 import compiled as precision_compiled
from scripts.research_battle_aftermath_context_v1248 import source_prefix
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/flagship_capture_context_v2578');IDS=list(range(2011,2016));BASE=0x02000000;TABLE=0x02117740
if __name__=='__main__':
 assert not ROOT.exists()
 ledger=read('translations/editorial_review_current_v1.json');c=ledger['current_integrated_candidate'];rom=NdsImage.open(c['path']);clean=NdsImage.open('work/clean.nds');arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin');en=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
 assert sha(Path(c['path']).read_bytes())==c['sha256']
 manifest=read(Path(c['path']).with_suffix('.manifest.json'));stages=manifest['relocations']['/COMMON/MESFILE.DK4'];bindings=[];prior={};owners={}
 for stage_name,selected,compiler in(('battle_aftermath_editorial',list(range(2011,2015)),original_compiled),('flagship_capture_precision',[2015],precision_compiled)):
  stage=stages[stage_name];cfgpath=Path(stage['release_config']);cfg=read(cfgpath);docpath=Path(cfg['manuscript']);doc=read(docpath)
  assert sha(cfgpath.read_bytes())==stage['release_config_sha256'] and sha(docpath.read_bytes())==cfg['dependencies'][str(docpath)] and set(selected)<=set(stage['proof']['native_IDs'])
  selectedrows={r['message_id']:r for r in doc['records'] if r['message_id'] in selected};assert set(selectedrows)==set(selected)
  for n,r in selectedrows.items():
   assert r['source_hex']==jp[n].text.hex() and compiler(r)==en[n].text;prior[n]=r;owners[n]=stage_name
  bindings.append(dict(stage=stage_name,selected_IDs=selected,registered_config=str(cfgpath),registered_config_sha256=sha(cfgpath.read_bytes()),registered_manuscript=str(docpath),registered_manuscript_sha256=sha(docpath.read_bytes()),registered_stage_native_IDs=stage['proof']['native_IDs'],compiler=compiler.__module__+'.compiled'))
 assert set(prior)==set(IDS) and prior[2015]['english']=="We've captured the enemy flagship after defeating its entire crew!"
 historical={r['message_id']:dict(family=f['id'],record=r) for f in ledger['completed_editorial_families'] for r in f['records'] if r.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4' and r.get('message_id') in IDS};fresh={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};assert len(historical)==5 and not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') in fresh for n in IDS)
 def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
 def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),current_reference=ref(en[n]),source_hex=jp[n].text.hex(),current_hex=en[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_stored_English=en[n].text.decode('cp932'),historical_review=historical.get(n),registered_prose_owner=owners.get(n),registered_English=prior[n]['english'] if n in prior else None,selected=n in IDS)
 records=[record(n) for n in IDS];neighbors=[record(n) for n in(2010,2016)]
 historypath=Path('work/analysis/flagship_capture_verified_v1370/actual_flagship_capture_verification.json');h=read(historypath);reportpath=Path(h['report']);report=read(reportpath);assert sha(reportpath.read_bytes())==h['report_sha256'] and report['ROM_sha256']==h['candidate_sha256']
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};item=snapshots[10800];snapshot=Path(item['path']);raw=snapshot.read_bytes();assert sha(raw)==item['sha256']
 spans=((0x72368,0x72484),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x82428,0x82570),(0x7E988,0x7E99C),(0x117740,0x117760))
 for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
 values=list(struct.unpack_from('<8i',arm,TABLE-BASE));assert values==[2011,-1,2012,-1,-1,2013,2014,2015]
 cpu,get=get_machine(arm,raw);root=get(0xCB184);fleets=get(0xCB1A8);objects=[root+4+i*32 for i in range(207)]+[root+0x19E4];choices=[]
 for slot,obj in enumerate(objects):
  voice=get(0x7E988,obj);n=get(0x53F4C,obj,TABLE);assert n==(values[voice] if values[voice]!=-1 else 2011)
  choices.append(dict(actor_slot=slot,actor_object=obj,actor_ID=get(0x7EE08,obj),voice_class=voice,message_ID=n,original_negative_member_fallback=values[voice]==-1))
 assert {r['message_ID'] for r in choices}==set(IDS) and get(0x53F4C,0,TABLE)==2011
 duty=fleets+0x2090;logical=get(0x82478,duty,1);physical=get(0x82428,duty,1);actor=root+4+logical*32
 assert logical==16 and physical==0 and get(0x7EE08,actor)==16 and get(0x7E988,actor)==1 and get(0x53F4C,actor,TABLE)==2011
 rolecalls=[dict(address=i.address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(arm[0x53D44:0x53DCC],BASE+0x53D44) if i.mnemonic=='bl' and i.op_str=='#0x2082478'];assert len(rolecalls)==1
 prefixes=[]
 for mode,table in enumerate((TABLE,0x021176A0,0x02117900)):
  calls,_,_=source_prefix(arm,raw,0x72368,(0,mode),BASE+0x723C4)
  assert len(calls)==1 and calls[0]['entry']==BASE+0x53D44 and calls[0]['arguments'][:2]==[1,table]
  prefixes.append(dict(original_mode=mode,original_calls=calls,CPU_prefix_stops_before_outcomes=True))
 ROOT.mkdir(parents=True);packetpath=ROOT/'all5_clean_current_context_catalog.json';contextpath=ROOT/'source_context_packet.json'
 save(packetpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),selected_IDs=IDS,records=records,neighbors=neighbors,registered_prose_owner_bindings=bindings,catalog_order_not_assumed_dialogue_chronology=True,source_prose_or_fresh_pass_credit_added=0,editorial_current_native_historical_and_two_owner_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 save(contextpath,dict(current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),actual_snapshot=str(snapshot),actual_snapshot_sha256=sha(raw),snapshot_historical_V1364_not_current_gameplay=True,original_signed_eight_members=values,all208_original_voice_selections=choices,null_actor_original_fallback_ID=2011,three_current_original72368_outcome_prefixes=prefixes,
  original_role_selector=1,original_entry=0x02053D44,original_parent=0x02053DB8,original_table_stack_offset=0x27C,original_table=TABLE,original53D44_call_to82478=rolecalls[0],actual_logical_member_ID=logical,actual_physical_FirstMate_object=physical,actual_actor_object=actor,actual_voice1_negative_member_falls_back_to2011=True,no_actor_ID_roster_or_result_changes=True,
  registered_prose_owner_bindings=bindings,current2015_precision_confines_entire_crew_to_captured_flagship=True,original_source_code=[dict(start=a,end=b,sha256=sha(arm[a:b]),current_clean_historical_snapshot_exact=True) for a,b in spans],
  context='Complete independent capture report after original72368 mode0 selects53D44(role1,02117740). Mode1 is enemy flagship defeat and mode2 flight/victory,not subsequent replies. Role1 uses logical82478 member selection;it must not be confused with physical-room82428. In the actual historical sample,physical First Mate is empty,logical member16 Gerhard is selected,and voice1 -1 correctly falls back to2011. Three fallback voices1/3/4 use2011. Four alternatives2011-2014 belong to the original battle_aftermath layer;2015 belongs to the later registered precision layer and keeps the captured flagship\'s crew scope. Do not compile2015 from its superseded manuscript wording or add fresh credit for that old correction. Read all five clean reports with defeated sailors and taking the ship;do not invent death of every sailor or defeat of the whole enemy fleet. Historical later victory/rewards/cargo-transfer/ordinary-sailing flow provides transition context only;do not turn discarded untransferred spoil cargo or tested approach positions into earned inventory or travel.',no_new_prose_or_fresh_or_completion_credit=True,full_goal_complete=False))
 save(ROOT/'next5_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),registered_prose_owner_bindings=bindings,all5_clean_current_own_registered_compilers_match=True,all208_voice_choices_and3_outcome_prefixes_and_logical16_physical0_selection_pass=True,historical_family_proof=str(historypath),historical_family_proof_sha256=sha(historypath.read_bytes()),historical_individual_IDs=[2011],two_registered_prose_owners_must_both_be_reconciled=True,fresh_credit=0,full_goal_complete=False))
 print('Next5 flagship capture:two registered prose owners,208 voices,three original outcomes,and logical16/physical0 selection pass;zero fresh credit.')
