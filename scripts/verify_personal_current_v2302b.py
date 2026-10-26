"""Recognize the real two-slot Cabin preview assignment, restored by cancel."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_personal_current_v2302.py')
if __name__=='__main__':
 source=OLD.read_text().replace("personal_current_verification_v2302'","personal_current_verification_v2302b'")
 old="assert all(s['state']==states[0]['state']for s in states)"
 new="""assert states[0]['state']==states[-1]['state']
 before=bytes.fromhex(states[0]['state']['all31_original_occupant_bytes']);assert before[9]==18 and before[12]==0xD0
 for state in states[1:3]:
  assert all(state['state'][k]==states[0]['state'][k]for k in states[0]['state']if k!='all31_original_occupant_bytes')
  occupants=bytes.fromhex(state['state']['all31_original_occupant_bytes']);assert occupants[9]==0xD0 and occupants[12]==18 and all(a==b for i,(a,b)in enumerate(zip(before,occupants,strict=True))if i not in(9,12))"""
 assert source.count(old)==1;source=source.replace(old,new)
 old='all_funds_calendar31_roles_owned_companion_records_flagship_and_full_ship_models_equal=True'
 new='all_funds_calendar_owned_companion_records_flagship_and_full_ship_models_equal_across4=True,all31_roles_restored_after_cancel=True,ordinary_UI_preview_moves_Charles_from_slot9_to_Cabin12_then_restores=True'
 assert source.count(old)==1;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/personal_current_verification_v2302b/successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='The original ordinary UI temporarily assigns Charles fromslot9 toCabin12 while previewing the comment. Requiring all31 occupant bytes unchanged during that real interaction was incorrect.',actual_preview_actor18_moves_between_exact_slots9and12_only=True,all_other_scoped_state_fields_unchanged_during_preview=True,all31_role_bytes_and_other_scoped_state_restored_after_cancel=True,no_RAM_fixture_or_ROM_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
