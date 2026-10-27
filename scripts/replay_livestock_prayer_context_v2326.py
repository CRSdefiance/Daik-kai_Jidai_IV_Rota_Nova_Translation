"""Fifty current native role helpers bind Livestock17 and Chapel18 voices."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_livestock_prayer_context_v852 import select
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/livestock_prayer_context_v2326');ROM=Path('out/all_routes_combined_v2284_candidate.nds');BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists();arm=NdsImage.open(ROM).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C),(0x7E988,0x7E9A0),(0x7F244,0x7F268));assert all(arm[a:b]==clean[a:b]for a,b in spans)
 namespath=Path('work/analysis/personal_context_v2297/native_context.json');np=read(namespath);assert np['ARM9_sha256']==sha(arm);names={r['actor_ID']:r['current_native_name']for r in np['all25_current_actor_names']};receipt=np['genuine_current_preinteraction_snapshot'];raw=Path(receipt['path']).read_bytes();assert sha(raw)==receipt['sha256'];cpu,get=get_machine(arm,raw);actors=get(0xCB184);npc_table=struct.unpack_from('<I',arm,0x12834)[0];hero_table=struct.unpack_from('<I',arm,0x1291C)[0];groups={};voices=[];heroes=[]
 for role,first,name in((17,1423,'Livestock'),(18,1435,'Chapel')):
  npc=struct.unpack_from('<I',arm,npc_table-BASE+role*4)[0];hero=struct.unpack_from('<I',arm,hero_table-BASE+role*4)[0];assert struct.unpack_from('<8I',arm,npc-BASE)==tuple(range(first,first+8))and struct.unpack_from('<4I',arm,hero-BASE)==tuple(range(first+8,first+12));assert arm[npc-BASE:npc-BASE+32]==clean[npc-BASE:npc-BASE+32]and arm[hero-BASE:hero-BASE+16]==clean[hero-BASE:hero-BASE+16];groups[role]=dict(role_ID=role,role_name=name,NPC_group=npc,NPC_IDs=list(range(first,first+8)),protagonist_group=hero,protagonist_IDs=list(range(first+8,first+12)))
  for actor in range(4,25):
   voice=get(0x7E988,actors+4+actor*32);assert 0<=voice<8;case=select(arm,raw,actor,role,first+voice);case.update(native_name=names[actor],voice_class=voice,role_ID=role);voices.append(case)
 old=read('work/analysis/work_context_v2307b/native_context.json');receipts={r['native_captain_ID']:r['source_actual_RAM']for r in old['all8_real_protagonist_helper_selections']}
 for actor,hrec in receipts.items():
  hraw=Path(hrec['path']).read_bytes();assert sha(hraw)==hrec['sha256']and hrec['read_only_export'];assert hraw[0x53C6C:0x53CB0]==arm[0x53C6C:0x53CB0]and hraw[0x7F244:0x7F268]==arm[0x7F244:0x7F268];u,hget=get_machine(arm,hraw);assert hget(0x7F244)==actor
  for role,first in((17,1423),(18,1435)):
   case=select(arm,hraw,actor,role,first+8+actor);case.update(actual_protagonist=names[actor],native_captain_ID=actor,role_ID=role,source_actual_RAM=hrec,no_captain_ID_or_record_substitution=True,historical_snapshot_not_new_current_hero_visit=True);heroes.append(case)
 assert len(voices)==42 and len(heroes)==8 and {r['selected_message_ID']for r in voices+heroes}==set(range(1423,1447))
 assert all(r['selected_message_ID']==groups[r['role_ID']]['NPC_IDs'][r['voice_class']]for r in voices if r['actor_ID']==24)
 ROOT.mkdir(parents=True);save(ROOT/'native_context.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),source_code_spans_clean_exact=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],source_role_groups=groups,all42_NPC_voice_selections=voices,all8_real_protagonist_helper_selections=heroes,current_NPC_source_snapshot=receipt,names_proof=str(namespath),names_proof_sha256=sha(namespath.read_bytes()),actor_records_and_captain_IDs_not_replaced=True,source_role_assignments_only_isolated_CPU_not_live_or_earned_eligibility=True,Sera_uses_ordinary_voice_no_special_override_for_roles17_or18=True,all24_independent_alternatives_not_sequential_conversation=True,no_new_current_four_hero_or_Sera_visits_claim=True,no_ROM_live_RAM_save_or_gameplay_fixture_changes=True,native_font_and_actual_family_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(NPC_helper_calls=42,real_hero_helper_calls=8,all24_IDs_selected=True,no_captain_substitution=True))
