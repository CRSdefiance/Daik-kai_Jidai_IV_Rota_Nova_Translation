"""Ordinary Boarding7 selection at source-bound physical slot10;no RAM fixtures."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/run_cooking_current_v2319.py')
if __name__=='__main__':
 geometry=Path('work/analysis/cooking_button_geometry_v2320/source_bound_Galley_touch.json');button=read(geometry)['all31_native_buttons'][10];assert button['native_role_type']==7 and button['rectangle']==[214,46,254,86]
 source=OLD.read_text();changes={'cooking_current_run_v2319':'boarding_current_run_v2364','cooking_current_v2319_V2284':'boarding_current_v2364_V2284','[224,150]':'[234,66]','existing Galley room21,native Cook role15':'existing Boarding room10,native role7','intended_ID1411':'intended_ID1536'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/boarding_current_run_v2364/source_geometry_binding.json',dict(geometry=str(geometry),geometry_sha256=sha(geometry.read_bytes()),native_button=button,touch=[234,66],actual_actor_eligibility_and_comment_not_assumed_until_verified=True,no_new_RAM_code_or_gameplay_fixture=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
