"""Current clean-source role tables,42 NPC voices and8 real-hero helper calls."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/work_context_v2307');ROM=Path('out/all_routes_combined_v2284_candidate.nds');BASE=0x02000000
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);arm=NdsImage.open(ROM).read_file('/__arm9__.bin');source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C),(0x7E988,0x7E9A0),(0x7F244,0x7F268));assert all(arm[a:b]==source[a:b]for a,b in spans)
 namesproof=read('work/analysis/personal_context_v2297/native_context.json');assert namesproof['ARM9_sha256']==sha(arm);names={r['actor_ID']:r['current_native_name']for r in namesproof['all25_current_actor_names']};snapshot=namesproof['genuine_current_preinteraction_snapshot'];raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256'];cpu,get=get_machine(arm,raw);actors=get(0xCB184);npc_table=struct.unpack_from('<I',arm,0x12834)[0];hero_table=struct.unpack_from('<I',arm,0x1291C)[0];groups={}
 for role,first in((13,1386),(14,1398)):
  npc=struct.unpack_from('<I',arm,npc_table-BASE+role*4)[0];hero=struct.unpack_from('<I',arm,hero_table-BASE+role*4)[0];assert struct.unpack_from('<8I',arm,npc-BASE)==tuple(range(first,first+8))and struct.unpack_from('<4I',arm,hero-BASE)==tuple(range(first+8,first+12));assert arm[npc-BASE:npc-BASE+32]==source[npc-BASE:npc-BASE+32]and arm[hero-BASE:hero-BASE+16]==source[hero-BASE:hero-BASE+16];groups[role]=dict(role_ID=role,role_name='Shipwright'if role==13 else'Doctor',NPC_group=npc,NPC_IDs=list(range(first,first+8)),protagonist_group=hero,protagonist_IDs=list(range(first+8,first+12)))
 voices=[]
 for actor in range(4,25):
  obj=actors+4+actor*32;voice=get(0x7E988,obj);assert 0<=voice<8
  for role,first in((13,1386),(14,1398)):
   selected=get(0x53F4C,obj,groups[role]['NPC_group']);assert selected==first+voice;voices.append(dict(actor_ID=actor,native_name=names[actor],voice_class=voice,role_ID=role,selected_message_ID=selected,complete_native_helper_ABI=True))
 assert len(voices)==42 and {r['voice_class']for r in voices}==set(range(8));assert names[10]=='Xien';old=read('work/analysis/work_comments_v842/native_context.json');heroes=[];seen=set()
 for row in old['all8_real_protagonist_group_selections']:
  hero,name,role=row['native_captain_ID'],row['actual_protagonist'],row['role_ID'];hrec=row['read_only_RAM'];hraw=Path(hrec['path']).read_bytes();assert sha(hraw)==hrec['sha256']and hrec['read_only_export'];assert hraw[0x53C6C:0x53CB0]==arm[0x53C6C:0x53CB0]and hraw[0x7F244:0x7F268]==arm[0x7F244:0x7F268]
  address=groups[role]['protagonist_group'];assert hraw[address-BASE:address-BASE+16]==arm[address-BASE:address-BASE+16];u,hget=get_machine(arm,hraw);assert hget(0x7F244)==hero;selected=hget(0x53C6C,address);first=1386 if role==13 else1398;assert selected==first+8+hero;heroes.append(dict(actual_protagonist=name,native_captain_ID=hero,role_ID=role,selected_message_ID=selected,source_actual_RAM=hrec,complete_current_clean_exact_helper_ABI=True,no_captain_ID_or_record_substitution=True));seen.add((hero,role))
 assert len(heroes)==len(seen)==8
 save(ROOT/'native_context.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),source_code_spans_clean_exact=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],source_role_groups=groups,all42_NPC_voice_selections=voices,all8_real_protagonist_helper_selections=heroes,current_NPC_source_snapshot=snapshot,names_proof='work/analysis/personal_context_v2297/native_context.json',names_proof_sha256=sha(Path('work/analysis/personal_context_v2297/native_context.json').read_bytes()),native_Xien_name=names[10],actor_names_inherited_under_same_exact_current_ARM9=True,original_consumer_chain='12104 working branch ->1278C/128B4 role helpers ->53F4C NPC voice or53C6C actual captain ->5528C',body_consumer='CDeckCabinInfoView;15334/154CC;registered216x36crop',role_ID_not_room_slot=True,historical_real_hero_snapshots_not_new_current_hero_visits=True,all24_are_independent_voice_alternatives_not_adjacent_speeches=True,no_live_RAM_code_ROM_save_or_gameplay_fixture_changes=True,native_full_font_and_actual_family_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(NPC_voice_calls=42,real_hero_calls=8,roles=[13,14],classes=8,no_captain_substitution=True))
