"""Next six flee/victory alternatives: exact source/current and original branches."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.research_battle_aftermath_context_v1248 import source_prefix
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/aftermath_fled_context_v2538');IDS=list(range(2046,2052));TABLE=0x02117900;BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists()
 ledger=read('translations/editorial_review_current_v1.json');candidate=ledger['current_integrated_candidate'];rom=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds')
 arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin')
 current=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
 assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']
 configpath=Path('translations/battle_aftermath_editorial_release_v1.json');config=read(configpath);manuscriptpath=Path(config['manuscript']);prior={r['message_id']:r for r in read(manuscriptpath)['records']}
 manifest=read(Path(candidate['path']).with_suffix('.manifest.json'));stage=manifest['relocations']['/COMMON/MESFILE.DK4']['battle_aftermath_editorial']
 assert sha(configpath.read_bytes())==stage['release_config_sha256']and sha(manuscriptpath.read_bytes())==config['dependencies'][str(manuscriptpath)]and set(IDS)<=set(stage['proof']['native_IDs'])
 historical={r['message_id']:dict(family=f['id'],record=r)for f in ledger['completed_editorial_families']for r in f['records']if r.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4'and r.get('message_id')in IDS}
 fresh={(r['file_path'],r['id'])for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
 assert len(historical)==6 and not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')in fresh for n in IDS)
 def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
 def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),current_reference=ref(current[n]),source_hex=jp[n].text.hex(),current_hex=current[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_stored_English=current[n].text.decode('cp932'),historical_review=historical.get(n),selected=n in IDS)
 records=[record(n)for n in IDS];neighbors=[record(n)for n in(2045,2052)]
 assert all(r['source_hex']==prior[r['message_ID']]['source_hex']and bytes.fromhex(r['current_hex'])==compiled(prior[r['message_ID']])for r in records)
 snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224/frame_005770_arm9_ram.bin');raw=snapshot.read_bytes()
 old=read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json');assert sha(raw)==old['snapshot_sha256']
 # Only original functions used here; current runtime formatter is checked later
 # through its registered consumer, never assumed equal to the clean renderer.
 spans=((0x72368,0x723C4),(0x53D44,0x53DB8),(0x53F4C,0x53F9C),(0x7E988,0x7E99C),(0x7EE08,0x7EE14),(0x117900,0x117920))
 for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
 cpu,get=get_machine(arm,raw);root=get(0xCB184);fleet=get(0xCB1A8);objects=[root+4+i*32 for i in range(207)]+[root+0x19E4]
 values=list(struct.unpack_from('<8i',arm,TABLE-BASE));assert values==[2046,2047,-1,-1,2048,2049,2050,2051]
 choices=[]
 for slot,obj in enumerate(objects):
  n=get(0x53F4C,obj,TABLE);voice=get(0x7E988,obj);expected=values[voice]if values[voice]!=-1 else next(v for v in values if v!=-1)
  assert n==expected
  choices.append(dict(actor_slot=slot,actor_object=obj,actor_ID=get(0x7EE08,obj),voice_class=voice,message_ID=n,original_negative_member_fallback=values[voice]==-1))
 assert {r['message_ID']for r in choices}==set(IDS)and get(0x53F4C,0,TABLE)==2046
 role_actor_ID=get(0x82478,fleet+0x2090,1);role_actor=root+0x19E4 if role_actor_ID==get(0x7F244)else root+4+role_actor_ID*32
 assert role_actor_ID==18 and get(0x53F4C,role_actor,TABLE)==2046
 prefixes=[]
 for mode,table in enumerate((0x02117740,0x021176A0,TABLE)):
  calls,_,_=source_prefix(arm,raw,0x72368,(0,mode),BASE+0x723C4)
  assert len(calls)==1 and calls[0]['entry']==BASE+0x53D44 and calls[0]['arguments'][:2]==[1,table]
  prefixes.append(dict(source_mode=mode,original_entry=BASE+0x72368,calls=calls,stopped_before_event_outcomes_CPU_only=True))
 ROOT.mkdir(parents=True);catalogpath=ROOT/'all6_clean_current_context_catalog.json'
 save(catalogpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
  selected_IDs=IDS,records=records,neighbors=neighbors,catalog_order_not_assumed_dialogue_chronology=True,source_prose_or_fresh_pass_credit_added=0,
  native_caller_graph_bound_editorial_current_font_historical_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 contextpath=ROOT/'source_context_packet.json'
 save(contextpath,dict(current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
  actual_snapshot=str(snapshot),actual_snapshot_sha256=sha(raw),snapshot_is_historical_V1224_not_current_gameplay=True,
  original_table=TABLE,original_signed_eight_members=values,all208_original_voice_selections=choices,null_actor_original_fallback_ID=2046,
  original_three_outcome_prefixes=prefixes,original_role_selector=1,source_role_actor_ID_in_snapshot=role_actor_ID,source_role_actor_object=role_actor,
  source_role1_unassigned_original_fallback_is_Charles18=True,unmodified_actor_IDs_and_no_CPU_roster_assignment=True,
  original_source_code=[dict(start=a,end=b,sha256=sha(arm[a:b]),current_clean_snapshot_exact=True)for a,b in spans],
  read_context='Complete independent alternative reports selected by original role1 and eight-class voice lookup. Source72368 mode2 calls53D44(1,02117900);mode0 selects flagship capture and mode1 flagship defeat instead. No argument or name macro belongs to2046..2051. Storage neighbor2045 is a city-defense challenge,not an earlier reply;2052 is separate subsequent storage. Only original table slots4,5,7 explicitly address the admiral. Voice slots2/3 are -1 and use the first valid member2046,not nonexistent alternative lines. The original prefix stops before event outcomes. Historical actual2046 confirms the result family;fresh gameplay is not claimed.',
  no_new_prose_or_fresh_or_completion_credit=True,full_goal_complete=False))
 historypath=Path('work/analysis/aftermath_victory_verified_v1271/actual_fled_victory_verification.json')
 save(ROOT/'next6_preflight.json',dict(packet=str(catalogpath),packet_sha256=sha(catalogpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),
  registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(manuscriptpath),registered_manuscript_sha256=sha(manuscriptpath.read_bytes()),
  all6_clean_current_registered_compilations_match=True,all208_current_original_voice_selections_and3_branch_prefixes_pass=True,
  historical_family_proof=str(historypath),historical_family_proof_sha256=sha(historypath.read_bytes()),historical_individual_IDs=[2046],
  pending_distinct_228x64_portrait_body_not_duel_208x36=True,fresh_credit=0,full_goal_complete=False))
 print('Six aftermath reports;208 original voice selections,three outcome prefixes,and registered compiler equality pass. Zero editorial credit.')
 for r in records:print(r['message_ID'],r['clean_Japanese'].replace('\n',' / '),' || ',r['current_stored_English'])
 for r in neighbors:print('NEIGHBOR',r['message_ID'],r['clean_Japanese'].replace('\n',' / '),' || ',r['current_stored_English'])
