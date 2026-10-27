"""Next source/context catalog; no editorial completion or fresh-pass credit."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.primary_town_services_reference_v2 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/market_context_source_v2108')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 clean=NdsImage.open('work/clean.nds');rom=NdsImage.open('out/all_routes_combined_v2097_candidate.nds');arm=rom.read_file('/__arm9__.bin');source_arm=clean.read_file('/__arm9__.bin');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source_arm);current=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);ledger=read('translations/editorial_review_current_v1.json');completed={}
 for family in ledger['completed_editorial_families']:
  for row in family.get('records',[]):
   if isinstance(row.get('message_id'),int)and row.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4':completed[row['message_id']]=dict(family=family['id'],manuscript=row.get('manuscript'),context=row.get('context'),historical_not_automatically_fresh=True)
 def ref(row):return dict(block=row.block,offset=row.block_offset,copy_end=row.copy_end,bytes=len(row.text),record_index=row.record_index,table_offset=row.table_offset,start_in_record=row.start)
 records=[dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),current_reference=ref(current[n]),source_hex=jp[n].text.hex(),current_hex=current[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_stored_English=current[n].text.decode('cp932'),historical_review=completed.get(n),reviewed_but_incomplete=n in ledger['reviewed_but_incomplete_COMMON_IDs'])for n in range(656,765)]
 leads=[]
 for n in(750,751,752):
  needle=struct.pack('<I',n);pos=0
  while True:
   at=source_arm.find(needle,pos)
   if at<0:break
   pos=at+1;lo=max(0,at-24);hi=min(len(source_arm),at+28);leads.append(dict(message_ID=n,address=0x02000000+at,offset=at,word_aligned=at%4==0,source_window_start=0x02000000+lo,source_window_hex=source_arm[lo:hi].hex(),current_window_hex=arm[lo:hi].hex(),byte_pattern_lead_not_resolved_message_caller=True))
 save(ROOT/'market656_764_clean_current_context_catalog.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM='out/all_routes_combined_v2097_candidate.nds',current_ROM_sha256=sha(Path('out/all_routes_combined_v2097_candidate.nds').read_bytes()),source_COMMON_sha256=sha(clean.read_file('/COMMON/MESFILE.DK4')),current_COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),source_ARM9_sha256=sha(source_arm),current_ARM9_sha256=sha(arm),records=records,source_constant_leads=leads,initial_uncompleted_focus=[750,751,752],native_context_and_conversation_graph_still_required=True,catalog_order_does_not_mean_consecutive_speakers=True,remaining116_and1403_historical_fresh_reconciliations_stay_in_scope=True,source_prose_or_fresh_pass_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(catalog_records=len(records),historically_complete=sum(r['historical_review']is not None for r in records),incomplete_focus=[r['message_ID']for r in records if r['reviewed_but_incomplete']],constant_byte_leads=len(leads),new_coverage_credit=0))
