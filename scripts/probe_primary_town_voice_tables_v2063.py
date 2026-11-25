"""Nine original voice tables, native catalog selections and exact fallback.

Offline selector coverage; not conditional event activation or actor placement.
"""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_voice_tables_v2063')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_actual_v2053_V2047/common_observer/requests.json')
TABLES={0x02117460:('unassigned sailors',[71,-1,72,-1,-1,73,74,75]),0x021174A0:('repair warning',[29,30,31,-1,32,33,34,35]),0x021189C0:('monthly tribute',[76,77,78,79,80,81,-1,82]),0x02118A00:('docking',[65,-1,66,-1,67,68,69,70]),0x02118A20:('food warning',[42,-1,43,44,45,46,47,48]),0x02118A40:('supplies warning',[36,-1,37,-1,38,39,40,41]),0x02118A60:('crowd alert',list(range(8))),0x02118A80:('barter',list(range(19,27))),0x02118AA0:('terms confirmation',[11,-1,12,13,14,15,16,17])}
if __name__=='__main__':
 assert not ROOT.exists()
 arm=NdsImage.open('out/all_routes_combined_v2047_candidate.nds').read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
 assert arm[0x53F4C:0x53F9C]==clean[0x53F4C:0x53F9C]
 seed=read(OBS)['rows'][0]['complete_readonly_snapshots']['WRAM'];raw=Path(seed['path']).read_bytes();assert sha(raw)==seed['sha256']
 cpu,get=get_machine(arm,raw);root=get(0xCB184);captain=get(0x7F244);assert captain==3
 rows=[];all_numbers=set();source_words=[struct.unpack_from('<I',clean,at)[0]for at in range(0,len(clean)-3,4)]
 for table,(name,expected)in TABLES.items():
  at=table-0x02000000;assert arm[at:at+32]==clean[at:at+32];members=list(struct.unpack_from('<8i',arm,at));assert members==expected
  cases=[]
  for actor_id in range(207):
   actor=root+0x19E4 if actor_id==captain else root+4+32*actor_id
   voice=get(0x7E988,actor);assert 0<=voice<8
   n=get(0x53F4C,actor,table);assert n==(members[voice]if members[voice]>=0 else members[0])
   cases.append(dict(catalog_actor_ID=actor_id,actor_address=actor,source_voice=voice,message_ID=n,minus1_fallback_to_first=members[voice]<0))
  assert {r['source_voice']for r in cases}==set(range(8))
  assert {r['message_ID']for r in cases}==set(members)-{-1}
  all_numbers|=set(members)-{-1}
  rows.append(dict(table=table,family=name,source_members=members,table_hex=arm[at:at+32].hex(),clean_current_table_exact=True,
   clean_ARM9_pointer_literal_references=[i*4 for i,v in enumerate(source_words)if v==table],native_selector_cases=cases))
 assert len(all_numbers)==61 and 64 not in all_numbers and bytes(cpu.mem_read(0x02000000,len(raw)))==raw
 ROOT.mkdir(parents=True)
 save(ROOT/'nine_clean_exact_voice_tables_and_all_native_catalog_selections.json',dict(ARM9_sha256=sha(arm),clean_ARM9_sha256=sha(clean),source_snapshot=seed,
  tables=rows,all61_table_selected_native_message_IDs=sorted(all_numbers),remaining23_direct_IDs=sorted(set(range(85))-{64}-all_numbers),
  native_selector_calls=9*207,native_voice_calls=9*207,all8_voices_and_original_minus1_fallback_per_table_verified=True,
  all4MiB_RAM_and_native_call_ABI_unchanged=True,actor_catalog_queries_not_proof_of_scene_participation_or_actual_conditional_visits=True,
  no_ROM_save_registry_or_emulator_mutation=True,formatting_repacking_revised_gameplay_and_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(source_tables=9,selected_IDs=61,direct_IDs=23,native_selector_calls=1863,native_voice_calls=1863,all4MiB_exact=True))
