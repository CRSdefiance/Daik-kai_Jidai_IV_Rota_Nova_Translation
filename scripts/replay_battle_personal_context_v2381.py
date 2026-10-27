"""Current battle-personal paths and discriminating ordinary controls for all25 actors."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_battle_personal_context_v890 import choose
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_personal_context_v2381');ROM=Path('out/all_routes_combined_v2284_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists();arm=NdsImage.open(ROM).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');spans=((0x12104,0x12920),(0x3F0F8,0x3F100),(0x7F244,0x7F268));assert all(arm[a:b]==clean[a:b]for a,b in spans)and struct.unpack_from('<I',arm,0x1271C)[0]==1571 and struct.unpack_from('<I',arm,0x128B0)[0]==1361
 namespath=Path('work/analysis/personal_context_v2297/native_context.json');namesproof=read(namespath);assert namesproof['ARM9_sha256']==sha(arm);names={r['actor_ID']:r['current_native_name']for r in namesproof['all25_current_actor_names']};npc_receipt=namesproof['genuine_current_preinteraction_snapshot'];npc=Path(npc_receipt['path']).read_bytes();assert sha(npc)==npc_receipt['sha256'];old=read('work/analysis/work_context_v2307b/native_context.json');heroes={r['native_captain_ID']:r['source_actual_RAM']for r in old['all8_real_protagonist_helper_selections']};cases=[]
 for actor in range(25):
  receipt=heroes[actor]if actor<4 else npc_receipt;raw=Path(receipt['path']).read_bytes();assert sha(raw)==receipt['sha256']
  specs=(('direct_battle_personal',0x126A8,None,None,False,1571+actor),('battle_activity1',0x12104,1,(0,1),False,1571+actor),('ordinary_activity1_control',0x12104,1,(0,0),False,1361+actor),('nonzero_field8_blocks_battle_control',0x12104,1,(1,1),False,1361+actor),('battle_working_Cabin12',0x12104,0,(0,1),True,1571+actor))
  for label,entry,state,mode,cabin,expected in specs:
   case=choose(arm,raw,actor,entry,state,mode,cabin);assert case['selected_message_ID']==expected;case.update(case=label,source_RAM=receipt,current_native_name=names[actor],historical_captain_snapshot_not_new_current_hero_visit=actor<4);cases.append(case)
 assert len(cases)==125 and {r['selected_message_ID']for r in cases if r['case']=='direct_battle_personal'}==set(range(1571,1596))
 ROOT.mkdir(parents=True);save(ROOT/'native_context.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),source_code_spans_clean_exact=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],all125_original_selector_and_discriminating_control_cases=cases,current_NPC_source_snapshot=npc_receipt,four_actual_captain_source_snapshots=heroes,names_proof=str(namespath),names_proof_sha256=sha(namespath.read_bytes()),source_battle_predicate=dict(object_field8_must_equal=0,object_field12_must_equal=1),battle_working_Cabin12_and_activity1_paths_select_battle_personal=True,ordinary_and_nonzero_field8_controls_select_ordinary1361_base=True,actor_captain_health_mood_records_not_replaced=True,mode_role_and_occupants_are_declared_isolated_CPU_controls=True,actual_battle_initialization_and_current_battle_gameplay_not_claimed=True,special_actors25_26_27_outside_family_no_new_credit_or_repeat_required=True,no_ROM_live_RAM_save_or_gameplay_fixture_change=True,native_fonts_and_historical_battle_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(current_selector_and_discriminating_controls=125,all25_battle_and_ordinary_paths_pass=True,no_captain_substitution=True))
