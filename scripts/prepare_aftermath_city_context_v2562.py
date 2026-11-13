"""Next eight city-defense challenges; original defending fleet captain/direct frame."""
from pathlib import Path
import struct
from unicorn.arm_const import UC_ARM_REG_R4
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.research_battle_aftermath_bindings_v1249 import prefix
from scripts.verify_personal_gameplay_v841 import get_machine,rtti
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/aftermath_city_context_v2562');IDS=list(range(2038,2046));BASE=0x02000000;TABLE=0x021178C0
if __name__=='__main__':
 assert not ROOT.exists()
 ledger=read('translations/editorial_review_current_v1.json');c=ledger['current_integrated_candidate'];rom=NdsImage.open(c['path']);clean=NdsImage.open('work/clean.nds');arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin');en=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
 assert sha(Path(c['path']).read_bytes())==c['sha256']
 configpath=Path('translations/battle_aftermath_editorial_release_v1.json');config=read(configpath);manuscriptpath=Path(config['manuscript']);prior={r['message_id']:r for r in read(manuscriptpath)['records']};stage=read(Path(c['path']).with_suffix('.manifest.json'))['relocations']['/COMMON/MESFILE.DK4']['battle_aftermath_editorial']
 assert sha(configpath.read_bytes())==stage['release_config_sha256'] and sha(manuscriptpath.read_bytes())==config['dependencies'][str(manuscriptpath)] and set(IDS)<=set(stage['proof']['native_IDs'])
 historical={r['message_id']:dict(family=f['id'],record=r) for f in ledger['completed_editorial_families'] for r in f['records'] if r.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4' and r.get('message_id') in IDS}
 fresh={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};assert len(historical)==8 and not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') in fresh for n in IDS)
 def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
 def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),current_reference=ref(en[n]),source_hex=jp[n].text.hex(),current_hex=en[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_stored_English=en[n].text.decode('cp932'),historical_review=historical.get(n),selected=n in IDS)
 records=[record(n) for n in IDS];neighbors=[record(n) for n in(2037,2046)];assert all(r['source_hex']==prior[r['message_ID']]['source_hex'] and bytes.fromhex(r['current_hex'])==compiled(prior[r['message_ID']]) for r in records)
 snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224/frame_005770_arm9_ram.bin');raw=snapshot.read_bytes();older=read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json');assert sha(raw)==older['snapshot_sha256']
 spans=((0x6ED34,0x6EE90),(0x3697C,0x369AC),(0x53F0C,0x53F9C),(0x7E988,0x7E99C),(0x1178C0,0x1178E0))
 for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
 cpu,get=get_machine(arm,raw);root=get(0xCB184);fleets=get(0xCB1A8);objects=[root+4+i*32 for i in range(207)]+[root+0x19E4];values=list(struct.unpack_from('<8i',arm,TABLE-BASE));assert values==IDS
 choices=[]
 for slot,obj in enumerate(objects):
  voice=get(0x7E988,obj);n=get(0x53F4C,obj,TABLE);assert n==values[voice];choices.append(dict(actor_slot=slot,actor_object=obj,actor_ID=get(0x7EE08,obj),voice_class=voice,message_ID=n))
 assert {r['message_ID'] for r in choices}==set(IDS) and get(0x53F4C,0,TABLE)==2038
 bindings=[]
 for fleet_id in(1,8):
  fleet=fleets+4+fleet_id*132;vt=struct.unpack('<I',cpu.mem_read(fleet,4))[0];assert rtti(raw,vt)=='6CFleet';actor=get(0x3697C,fleet)
  call=prefix(arm,raw,0x6EE20,BASE+0x6EE30,{UC_ARM_REG_R4:fleet});assert call['entry']==BASE+0x53F0C and call['arguments'][:2]==[actor,TABLE] and call['original_return']==BASE+0x6EE30
  bindings.append(dict(source_fleet_ID=fleet_id,source_fleet=fleet,source_captain_actor_ID=get(0x7EE08,actor),source_captain_object=actor,original_call=call,CPU_post_eligibility_prefix_only_not_actual_attack=True))
 historypath=Path('work/analysis/aftermath_city_verified_v1287/actual_city_defense_verification.json');h=read(historypath);reportpath=Path(h['report']);report=read(reportpath);assert sha(reportpath.read_bytes())==h['report_sha256'] and report['ROM_sha256']==h['candidate_sha256']
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};item=snapshots[6720];actualraw=Path(item['path']).read_bytes();assert sha(actualraw)==item['sha256']
 for a,b in spans:assert actualraw[a:b]==arm[a:b]
 actualcpu,actualget=get_machine(arm,actualraw);fleet=actualget(0xCB1A8)+4+22*132;captain=actualget(0x3697C,fleet)
 assert actualget(0x35320,fleet)==6 and actualget(0x7EE08,captain)==46 and actualget(0x53F4C,captain,TABLE)==2043
 actualcall=prefix(arm,actualraw,0x6EE20,BASE+0x6EE30,{UC_ARM_REG_R4:fleet});assert actualcall['arguments'][:2]==[captain,TABLE]
 bindings.append(dict(source_fleet_ID=22,source_fleet=fleet,source_captain_actor_ID=46,source_captain_object=captain,original_call=actualcall,historical_actual_frame=6720,historical_snapshot=item['path'],historical_snapshot_sha256=sha(actualraw),CPU_post_eligibility_prefix_only_not_new_attack=True))
 ROOT.mkdir(parents=True);packetpath=ROOT/'all8_clean_current_context_catalog.json';contextpath=ROOT/'source_context_packet.json'
 save(packetpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),selected_IDs=IDS,records=records,neighbors=neighbors,catalog_order_not_assumed_dialogue_chronology=True,source_prose_or_fresh_pass_credit_added=0,editorial_current_direct_fonts_and_historical_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 save(contextpath,dict(current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),actual_snapshot=str(snapshot),actual_snapshot_sha256=sha(raw),snapshot_historical_V1224_not_current_gameplay=True,original_signed_eight_members=values,all208_original_voice_selections=choices,null_actor_original_fallback_ID=2038,three_current_original_city_defender_captain_bindings=bindings,
  original_entry=0x02053F0C,original_parent=0x02053F40,original_table_stack_offset=0x274,original_table=TABLE,original_callsite=0x0206EE2C,no_actor_ID_roster_or_live_eligibility_changes=True,
  historical_actual_selected_ID=2043,historical_actual_captain_ID46_defender_fleet22_company6=True,original_source_code=[dict(start=a,end=b,sha256=sha(arm[a:b]),current_clean_historical_snapshots_exact=True) for a,b in spans],
  context='Complete independent city-defense challenge spoken by the defending fleet captain selected through original3697C,not the player First Mate or a newly invented town official. Original6EE20 post-eligibility prefix calls53F0C(captain,021178C0),saved parent53F40/table stack+274. It is a direct portrait consumer,distinct from prior role1 parent53DB8/+27C. Three CPU prefixes use unchanged original fleet/captain objects;they begin after eligibility and do not force a new city attack or RNG success. Historical actual Madeira defense selected captain46,fleet22/company6,message2043 after original presence/share checks and unforced one-in-three choice. Read all clean challenges with defender resolve,confidence,anger or accusation,not as sequential replies;claims of protection/revenge are speaker intent,not guaranteed outcomes or invented civic ranks. Storage neighbors2037 surrender reply and2046 flight/victory are separate event families.',no_new_prose_or_fresh_or_completion_credit=True,full_goal_complete=False))
 save(ROOT/'next8_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(manuscriptpath),registered_manuscript_sha256=sha(manuscriptpath.read_bytes()),all8_clean_current_registered_compilations_match=True,all208_voice_choices_and3_current_original_direct_defender_prefixes_pass=True,historical_family_proof=str(historypath),historical_family_proof_sha256=sha(historypath.read_bytes()),historical_individual_IDs=[2043],fresh_credit=0,full_goal_complete=False))
 print('Next8 city defense:208 original voices,three source captain/direct prefixes including actual captain46/fleet22;zero fresh credit.')
