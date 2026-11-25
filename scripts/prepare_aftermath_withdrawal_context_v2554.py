"""Next eight withdrawal voices and source-bound historical distance predicate."""
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.research_battle_aftermath_context_v1248 import source_prefix
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/aftermath_withdrawal_context_v2554');IDS=list(range(2114,2122));BASE=0x02000000;TABLE=0x02117D00
if __name__=='__main__':
 assert not ROOT.exists()
 ledger=read('translations/editorial_review_current_v1.json');c=ledger['current_integrated_candidate'];rom=NdsImage.open(c['path']);clean=NdsImage.open('work/clean.nds');arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin');en=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
 assert sha(Path(c['path']).read_bytes())==c['sha256']
 configpath=Path('translations/battle_aftermath_editorial_release_v1.json');config=read(configpath);manuscriptpath=Path(config['manuscript']);prior={r['message_id']:r for r in read(manuscriptpath)['records']};stage=read(Path(c['path']).with_suffix('.manifest.json'))['relocations']['/COMMON/MESFILE.DK4']['battle_aftermath_editorial']
 assert sha(configpath.read_bytes())==stage['release_config_sha256']and sha(manuscriptpath.read_bytes())==config['dependencies'][str(manuscriptpath)]and set(IDS)<=set(stage['proof']['native_IDs'])
 historical={r['message_id']:dict(family=f['id'],record=r)for f in ledger['completed_editorial_families']for r in f['records']if r.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4'and r.get('message_id')in IDS};fresh={(r['file_path'],r['id'])for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
 assert len(historical)==8 and not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')in fresh for n in IDS)
 def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
 def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),current_reference=ref(en[n]),source_hex=jp[n].text.hex(),current_hex=en[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_stored_English=en[n].text.decode('cp932'),historical_review=historical.get(n),selected=n in IDS)
 records=[record(n)for n in IDS];neighbors=[record(n)for n in(2113,2122)]
 assert all(r['source_hex']==prior[r['message_ID']]['source_hex']and bytes.fromhex(r['current_hex'])==compiled(prior[r['message_ID']])for r in records)
 snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224/frame_005770_arm9_ram.bin');raw=snapshot.read_bytes();old=read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json');assert sha(raw)==old['snapshot_sha256']
 spans=((0x717F8,0x718D4),(0x53D44,0x53DB8),(0x53F4C,0x53F9C),(0x7E988,0x7E99C),(0x117D00,0x117D20),(0x7251C,0x72BDC),(0x513D0,0x514C0))
 for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
 cpu,get=get_machine(arm,raw);root=get(0xCB184);fleet=get(0xCB1A8);objects=[root+4+i*32 for i in range(207)]+[root+0x19E4];values=list(struct.unpack_from('<8i',arm,TABLE-BASE));assert values==IDS
 choices=[]
 for slot,obj in enumerate(objects):
  n=get(0x53F4C,obj,TABLE);voice=get(0x7E988,obj);assert n==values[voice];choices.append(dict(actor_slot=slot,actor_object=obj,actor_ID=get(0x7EE08,obj),voice_class=voice,message_ID=n))
 assert {r['message_ID']for r in choices}==set(IDS)and get(0x53F4C,0,TABLE)==2114
 duty=fleet+0x2090;assert get(0x82428,duty,1)==0 and get(0x82478,duty,1)==18 and get(0x53F4C,root+4+18*32,TABLE)==2114
 calls,_,_=source_prefix(arm,raw,0x717F8,(0,2),BASE+0x718D4)
 assert len(calls)==1 and calls[0]['entry']==BASE+0x53D44 and calls[0]['arguments'][:2]==[1,TABLE]
 ins=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(arm[0x7251C:0x72BDC],BASE+0x7251C));byaddr={r.address:r for r in ins}
 mode2=[]
 for addr in(0x02072A5C,0x02072A88,0x02072AB4):
  assert byaddr[addr].mnemonic=='bl'and byaddr[addr].op_str=='#0x20717f8'and byaddr[addr-4].mnemonic=='mov'and byaddr[addr-4].op_str=='r1, #2'
  mode2.append(dict(callsite=addr,source_mode=2,instructions=[dict(address=byaddr[a].address,bytes=byaddr[a].bytes.hex(),mnemonic=byaddr[a].mnemonic,operands=byaddr[a].op_str)for a in range(addr-8,addr+12,4)]))
 assert byaddr[0x020729DC].mnemonic=='bl'and byaddr[0x020729DC].op_str=='#0x20513d0'and byaddr[0x020729E0].op_str=='r0, #2'
 historypath=Path('work/analysis/aftermath_withdrawal_verified_v1293/actual_withdrawal_verification.json');h=read(historypath);reportpath=Path(h['report']);report=read(reportpath);assert sha(reportpath.read_bytes())==h['report_sha256']and report['ROM_sha256']==h['candidate_sha256']
 snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']};distances=[]
 for s in h['original_town_battle_movement_withdrawal_and_return_states']:
  item=snapshots[s['frame']];data=Path(item['path']).read_bytes();assert sha(data)==item['sha256']==s['RAM_sha256']and data[0x513D0:0x514C0]==arm[0x513D0:0x514C0]
  u,g=get_machine(arm,data);u.mem_write(0x02470000,struct.pack('<2i',*s['native_town_center']));u.mem_write(0x02470010,struct.pack('<2i',*s['own_live_map_point']));value=g(0x513D0,0x02470000,0x02470010,0);assert value==s['original513D0_distance_result']
  distances.append(dict(frame=s['frame'],historical_RAM=item['path'],historical_RAM_sha256=sha(data),original_town_center=s['native_town_center'],original_ship_point=s['own_live_map_point'],current_original513D0_result=value,original_result=s['original513D0_distance_result'],CPU_scratch_point_copies_only_no_emulator_position_change=True))
 assert len(distances)==9 and {r['current_original513D0_result']for r in distances}>={0,1,2}
 ROOT.mkdir(parents=True);packetpath=ROOT/'all8_clean_current_context_catalog.json';contextpath=ROOT/'source_context_packet.json'
 save(packetpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),selected_IDs=IDS,records=records,neighbors=neighbors,catalog_order_not_assumed_dialogue_chronology=True,source_prose_or_fresh_pass_credit_added=0,editorial_current_fonts_historical_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 save(contextpath,dict(current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),actual_snapshot=str(snapshot),actual_snapshot_sha256=sha(raw),snapshot_historical_V1224_not_current_gameplay=True,original_signed_eight_members=values,all208_original_voice_selections=choices,null_actor_original_fallback_ID=2114,original_mode2_withdrawal_prefix=calls,three_original7251C_mode2_callsites=mode2,current_original513D0_on9_historical_town_ship_positions=distances,
  source_role1_unassigned_original_Charles18_fallback2114=True,no_actor_ID_or_roster_changes=True,original_source_code=[dict(start=a,end=b,sha256=sha(arm[a:b]),current_clean_snapshot_exact=True)for a,b in spans],
  context='Independent withdrawal alternative selected by original role1/table02117D00. Original717F8 mode2 issues one withdrawal report,without the mode0/1 flagship-loss follow-up. Original7251C has three mode2 callsites;one source path tests original513D0 distance result2. Nine preserved town/ship positions reproduce the original distance classes0/1/2 through current clean-exact code using CPU scratch arguments only. Historical actual2114 follows town attack,Sao Tome73,assigned Charles18 and original movement to withdrawal,then normal A clears mode and town ID. No other seven individual visits or current gameplay are implied. This family states withdrawal;do not infer defeat,victory,surrender,flagship destruction or actual safe escape from the character speech alone.',no_new_prose_or_fresh_or_completion_credit=True,full_goal_complete=False))
 save(ROOT/'next8_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(manuscriptpath),registered_manuscript_sha256=sha(manuscriptpath.read_bytes()),all8_clean_current_registered_compilations_match=True,all208_voice_choices_original_mode2_prefix_3_callsites_and9_distance_samples_pass=True,historical_family_proof=str(historypath),historical_family_proof_sha256=sha(historypath.read_bytes()),historical_individual_IDs=[2114],fresh_credit=0,full_goal_complete=False))
 print('Next8 withdrawal:208 voice choices,one original report prefix,three mode2 callsites,nine historical-position distance tests pass;zero fresh credit.')
