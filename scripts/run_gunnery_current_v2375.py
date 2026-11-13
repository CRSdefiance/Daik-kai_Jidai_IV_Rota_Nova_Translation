"""Ordinary Gunnery8 selection at source-bound physical slot9;no RAM fixtures."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/run_cooking_current_v2319.py')
if __name__=='__main__':
 geometry=Path('work/analysis/cooking_button_geometry_v2320/source_bound_Galley_touch.json');button=read(geometry)['all31_native_buttons'][9];assert button['native_role_type']==8 and button['rectangle']==[172,46,212,86]
 source=OLD.read_text();changes={'cooking_current_run_v2319':'gunnery_current_run_v2375','cooking_current_v2319_V2284':'gunnery_current_v2375_V2284','[224,150]':'[192,66]','existing Galley room21,native Cook role15':'existing Gunnery room9,native role8','intended_ID1411':'intended_ID1548'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/gunnery_current_run_v2375/source_geometry_binding.json',dict(geometry=str(geometry),geometry_sha256=sha(geometry.read_bytes()),native_button=button,touch=[192,66],actual_actor_eligibility_and_comment_not_assumed_until_verified=True,no_new_RAM_code_or_gameplay_fixture=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
