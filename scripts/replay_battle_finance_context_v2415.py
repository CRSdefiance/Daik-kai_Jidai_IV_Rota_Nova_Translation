"""75 current direct/main battle helpers and ordinary controls for role20."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_battle_repair_medical_context_v899 import select
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_finance_context_v2415');ROM=Path('out/all_routes_combined_v2284_candidate.nds');BASE=0x02000000
GROUPS=((20,1669,1459,'Finance'),)
if __name__=='__main__':
 assert not ROOT.exists();arm=NdsImage.open(ROM).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');spans=((0x12104,0x12920),(0x3F0F8,0x3F100),(0x7E988,0x7E9A0),(0x7F244,0x7F268));assert all(arm[a:b]==clean[a:b]for a,b in spans)
 np=Path('work/analysis/personal_context_v2297/native_context.json');namesproof=read(np);assert namesproof['ARM9_sha256']==sha(arm);names={r['actor_ID']:r['current_native_name']for r in namesproof['all25_current_actor_names']};npc_receipt=namesproof['genuine_current_preinteraction_snapshot'];npc=Path(npc_receipt['path']).read_bytes();assert sha(npc)==npc_receipt['sha256'];u,get=get_machine(arm,npc);actors=get(0xCB184);nt=struct.unpack_from('<I',arm,0x126A4)[0];ht=struct.unpack_from('<I',arm,0x12788)[0];groups=[]
 for role,first,ordinary,label in GROUPS:
  n=struct.unpack_from('<I',arm,nt-BASE+role*4)[0];h=struct.unpack_from('<I',arm,ht-BASE+role*4)[0];assert struct.unpack_from('<8I',arm,n-BASE)==tuple(range(first,first+8))and struct.unpack_from('<4I',arm,h-BASE)==tuple(range(first+8,first+12));assert arm[n-BASE:n-BASE+32]==clean[n-BASE:n-BASE+32]and arm[h-BASE:h-BASE+16]==clean[h-BASE:h-BASE+16];groups.append(dict(role_ID=role,label=label,NPC_pointer=n,NPC_IDs=list(range(first,first+8)),protagonist_pointer=h,protagonist_IDs=list(range(first+8,first+12)),ordinary_control_base=ordinary))
 old=read('work/analysis/work_context_v2307b/native_context.json');heroes={r['native_captain_ID']:r['source_actual_RAM']for r in old['all8_real_protagonist_helper_selections']};cases=[]
 for actor in range(25):
  receipt=heroes[actor]if actor<4 else npc_receipt;raw=Path(receipt['path']).read_bytes();assert sha(raw)==receipt['sha256'];voice=None if actor<4 else get(0x7E988,actors+4+actor*32)
  for role,first,ordinary,label in GROUPS:
   suffix=8+actor if actor<4 else voice;helper=0x12720 if actor<4 else 0x12600
   for label,entry,mode,expected in(('direct_battle_working',helper,(0,1),first+suffix),('main_battle_working',0x12104,(0,1),first+suffix),('ordinary_working_control',0x12104,(0,0),ordinary+suffix)):
    case=select(arm,raw,actor,role,mode,entry,expected);case.update(case=label,role_ID=role,native_voice_class=voice,current_native_name=names[actor],source_RAM=receipt,historical_captain_snapshot_not_new_current_hero_visit=actor<4);cases.append(case)
 assert len(cases)==75 and {r['selected_message_ID']for r in cases if r['case']!='ordinary_working_control'}==set(range(1669,1681))
 ROOT.mkdir(parents=True);save(ROOT/'native_context.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),source_code_spans_clean_exact=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],source_role_groups=groups,all75_battle_direct_main_and_ordinary_control_cases=cases,current_NPC_source_snapshot=npc_receipt,four_actual_captain_source_snapshots=heroes,names_proof=str(np),names_proof_sha256=sha(np.read_bytes()),source_battle_predicate_fields8_12=[0,1],actor_captain_health_mood_records_not_replaced=True,mode_role_and_occupants_are_declared_isolated_CPU_controls=True,no_new_current_battle_initializer_or_family_gameplay_claim=True,no_ROM_live_RAM_save_or_gameplay_fixture_change=True,native_fonts_and_historical_battle_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(current_context_and_discriminating_controls=75,all12_battle_IDs_and_ordinary_controls_pass=True,no_captain_substitution=True))
