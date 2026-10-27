"""Bound clean native-unit leads for three unresolved market records; no unused claim."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_shipyard_storage_v760 import units
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/market_unresolved_context_v2113')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 rom=NdsImage.open('work/clean.nds');results=[]
 for label,base,data in units(rom):
  records=[]
  for n in (750,751,752):
   half=[dict(address=base+i,context_hex=data[max(0,i-8):i+10].hex())for i in range(0,len(data)-1,2)if struct.unpack_from('<H',data,i)[0]==n]
   raw=[dict(address=base+i,aligned=i%4==0,context_hex=data[max(0,i-8):i+12].hex())for i in range(len(data)-3)if struct.unpack_from('<I',data,i)[0]==n]
   mov=[]
   for i in range(0,len(data)-3,4):
    w=struct.unpack_from('<I',data,i)[0]
    if (w>>25)&7!=1 or (w>>21)&15!=13:continue
    imm=w&255;rotation=((w>>8)&15)*2;value=((imm>>rotation)|(imm<<(32-rotation)))&0xffffffff if rotation else imm
    if value==n:mov.append(dict(address=base+i,condition=w>>28,register=(w>>12)&15,word_hex=data[i:i+4].hex()))
   records.append(dict(message_ID=n,raw_word_leads=raw,aligned_halfword_leads=half,ARM_MOV_immediate_leads=mov))
  results.append(dict(unit=label,base=base,bytes=len(data),sha256=sha(data),records=records))
 save(ROOT/'clean_native_constant_census.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),units=results,interpretation='No verified dialogue caller for750/751/752 established. The aligned750 word at02120EAC is among town-name/stat data, not a proved consumer. Halfword coincidences include instructions, addresses and numeric tables. This finite census cannot rule out indirect construction or a script consumer.',no_unused_or_unreachable_claim=True,no_new_editorial_completion_credit=True,unresolved_IDs=[750,751,752],next_required='Find a verified caller/choice or table path before treating these three as one exchange or authoring final dialogue.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(units=len(results),unresolved=[750,751,752],completion_credit=0))
