"""Exact clean/current context packet for remaining Square, Market, Yard and Port exchanges."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.square_contextual_reference_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_trade_port_source_v2149');IDS=sorted(set(range(765,820))|{267,653,654,655,1245,1246})
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);l=read('translations/editorial_review_current_v1.json');c=l['current_integrated_candidate'];rom=NdsImage.open(c['path']);clean=NdsImage.open('work/clean.nds');arm=rom.read_file('/__arm9__.bin');source_arm=clean.read_file('/__arm9__.bin');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source_arm);current=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);assert sha(Path(c['path']).read_bytes())==c['sha256'];old={}
 for f in l['completed_editorial_families']:
  for r in f.get('records',[]):
   if r.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4'and r.get('message_id')in IDS:old[r['message_id']]=dict(family=f['id'],record=r)
 def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
 def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),current_reference=ref(current[n]),source_hex=jp[n].text.hex(),current_hex=current[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_stored_English=current[n].text.decode('cp932'),historical_review=old.get(n),selected=n in IDS)
 records=[record(n)for n in IDS];neighbors=[record(n)for n in sorted({n+d for n in IDS for d in(-1,1)if 0<=n+d<3668}-set(IDS))];assert len(records)==61 and len(old)==61
 save(ROOT/'all61_clean_current_context_catalog.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),source_ARM9_sha256=sha(source_arm),source_COMMON_sha256=sha(clean.read_file('/COMMON/MESFILE.DK4')),selected_IDs=IDS,records=records,neighbors=neighbors,catalog_order_not_assumed_dialogue_chronology=True,source_prose_or_fresh_pass_credit_added=0,native_caller_graph_and_contextual_editorial_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(records=len(records),neighbors=len(neighbors),historically_complete=len(old),fresh_credit=0))
 for r in records:print(r['message_ID'],r['clean_Japanese'].replace('\n',' / '),' || ',r['current_stored_English'].replace('\n',' / '))
 print('NEIGHBORS')
 for r in neighbors:print(r['message_ID'],r['clean_Japanese'].replace('\n',' / '),' || ',r['current_stored_English'].replace('\n',' / '))
