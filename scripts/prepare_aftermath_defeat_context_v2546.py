"""Fourteen abandonment/loss alternatives with complete original paired reports."""
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
ROOT=Path('work/analysis/aftermath_defeat_context_v2546');IDS=[*range(2016,2022),*range(2138,2146)];BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists()
 ledger=read('translations/editorial_review_current_v1.json');candidate=ledger['current_integrated_candidate'];rom=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds')
 arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin');current=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
 assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']
 configpath=Path('translations/battle_aftermath_editorial_release_v1.json');config=read(configpath);manuscriptpath=Path(config['manuscript']);prior={r['message_id']:r for r in read(manuscriptpath)['records']}
 stage=read(Path(candidate['path']).with_suffix('.manifest.json'))['relocations']['/COMMON/MESFILE.DK4']['battle_aftermath_editorial']
 assert sha(configpath.read_bytes())==stage['release_config_sha256']and sha(manuscriptpath.read_bytes())==config['dependencies'][str(manuscriptpath)]and set(IDS)<=set(stage['proof']['native_IDs'])
 historical={r['message_id']:dict(family=f['id'],record=r)for f in ledger['completed_editorial_families']for r in f['records']if r.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4'and r.get('message_id')in IDS}
 fresh={(r['file_path'],r['id'])for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
 assert len(historical)==14 and not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')in fresh for n in IDS)
 def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
 def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),current_reference=ref(current[n]),source_hex=jp[n].text.hex(),current_hex=current[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_stored_English=current[n].text.decode('cp932'),historical_review=historical.get(n),selected=n in IDS)
 records=[record(n)for n in IDS];neighbors=[record(n)for n in(2015,2022,2137,2146)];flood=[record(n)for n in range(2006,2011)]
 assert all(r['source_hex']==prior[r['message_ID']]['source_hex']and bytes.fromhex(r['current_hex'])==compiled(prior[r['message_ID']])for r in records+flood)
 snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224/frame_005770_arm9_ram.bin');raw=snapshot.read_bytes();old=read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json');assert sha(raw)==old['snapshot_sha256']
 spans=((0x717F8,0x718D4),(0x53D44,0x53DB8),(0x53F4C,0x53F9C),(0x7E988,0x7E99C),(0x7EE08,0x7EE14),(0x117760,0x117780),(0x117F00,0x117F20),(0x1176E0,0x117700),(0x117D00,0x117D20))
 for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
 cpu,get=get_machine(arm,raw);root=get(0xCB184);fleet=get(0xCB1A8);objects=[root+4+i*32 for i in range(207)]+[root+0x19E4]
 tables=[];allchoices=[]
 for family,table,selected in(('crew_abandonment',0x02117760,list(range(2016,2022))),('own_flagship_loss',0x02117F00,list(range(2138,2146)))):
  values=list(struct.unpack_from('<8i',arm,table-BASE));choices=[]
  assert {v for v in values if v!=-1}==set(selected)
  for slot,obj in enumerate(objects):
   n=get(0x53F4C,obj,table);voice=get(0x7E988,obj);assert n==(values[voice]if values[voice]!=-1 else next(v for v in values if v!=-1))
   choices.append(dict(actor_slot=slot,actor_object=obj,actor_ID=get(0x7EE08,obj),voice_class=voice,message_ID=n,table=table,original_negative_member_fallback=values[voice]==-1))
  assert {r['message_ID']for r in choices}==set(selected)
  tables.append(dict(family=family,table=table,signed_eight_members=values,all208_original_voice_selections=choices,null_actor_original_fallback=get(0x53F4C,0,table)));allchoices+=choices
 prefixes=[]
 for mode,table in enumerate((0x02117760,0x021176E0,0x02117D00)):
  calls,_,_=source_prefix(arm,raw,0x717F8,(0,mode),BASE+0x718D4)
  assert [(r['entry'],r['arguments'][:2])for r in calls]==[(BASE+0x53D44,[1,table])]+([(BASE+0x53D44,[1,0x02117F00])]if mode in(0,1)else[])
  prefixes.append(dict(source_mode=mode,original_entry=BASE+0x717F8,calls=calls,stopped_before_event_outcomes_CPU_only=True))
 paired=[]
 for slot,obj in enumerate(objects):
  voice=get(0x7E988,obj);paired.append(dict(actor_slot=slot,actor_object=obj,actor_ID=get(0x7EE08,obj),voice_class=voice,
   source_mode0_messages=[get(0x53F4C,obj,t)for t in(0x02117760,0x02117F00)],source_mode1_messages=[get(0x53F4C,obj,t)for t in(0x021176E0,0x02117F00)]))
 assert len({tuple(r['source_mode0_messages'])for r in paired})==8
 duty=fleet+0x2090;assert get(0x82428,duty,1)==0 and get(0x82478,duty,1)==18
 fallbackactor=root+4+18*32;assert get(0x7EE08,fallbackactor)==18 and [get(0x53F4C,fallbackactor,t)for t in(0x02117760,0x02117F00)]==[2016,2138]
 ROOT.mkdir(parents=True);catalogpath=ROOT/'all14_clean_current_context_catalog.json'
 save(catalogpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
  selected_IDs=IDS,records=records,neighbors=neighbors,other_complete_flood_reports_context_only=flood,catalog_order_not_assumed_dialogue_chronology=True,source_prose_or_fresh_pass_credit_added=0,native_context_bound_editorial_current_font_and_historical_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 contextpath=ROOT/'source_context_packet.json'
 save(contextpath,dict(current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),actual_snapshot=str(snapshot),actual_snapshot_sha256=sha(raw),snapshot_is_historical_V1224_not_current_gameplay=True,
  original_voice_tables=tables,all416_original_selected_voice_choices=allchoices,all208_complete_original_voice_report_pairs=paired,original_three_outcome_prefixes=prefixes,original_role_selector=1,unassigned_role1_original_fallback_actor18_pairs2016_2138=True,no_actor_ID_or_roster_changes=True,
  original_source_code=[dict(start=a,end=b,sha256=sha(arm[a:b]),current_clean_snapshot_exact=True)for a,b in spans],
  complete_exchange_context='Original717F8 mode0 issues crew-abandonment report then flagship-loss report through the same role1 selection. Mode1 issues flooding report2006..2010 then flagship-loss report;all five complete flood reports are provided as context only. Mode2 issues withdrawal alone,with no appended flagship-loss report. Pairing follows original voice class and first-valid fallback,not numeric storage order. Only report2016 and loss2138 have individual historical activations in the selected family sample. Speakers/captain survival must be read with the game\'s sailors/crew term and role context;do not invent that every officer died. Death,progressive losses,down/incapacitated wording,abandoning to another ship,immediacy,explicit Admiral addresses,uncertainty2143 and emotional voice differences require fresh individual review. Loss statements alone do not prove a ship sank or all people aboard died.',
  no_new_prose_or_fresh_or_completion_credit=True,full_goal_complete=False))
 historypath=Path('work/analysis/aftermath_defeat_verified_v1276/actual_abandonment_and_flagship_defeat.json')
 save(ROOT/'next14_preflight.json',dict(packet=str(catalogpath),packet_sha256=sha(catalogpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(manuscriptpath),registered_manuscript_sha256=sha(manuscriptpath.read_bytes()),
  all14_clean_current_registered_compilations_match=True,all416_voice_choices_208_paired_exchanges_and3_branch_prefixes_pass=True,five_complete_flood_reports_context_only_no_extra_credit=True,
  historical_family_proof=str(historypath),historical_family_proof_sha256=sha(historypath.read_bytes()),historical_individual_IDs=[2016,2138],pending_current_role1_228x64_fonts_and_historical_loss_GameOver_title_binding=True,fresh_credit=0,full_goal_complete=False))
 print('Next14:416 source voice selections,208 complete report pairs,three outcome prefixes;five complete flood reports as context. Zero fresh credit.')
