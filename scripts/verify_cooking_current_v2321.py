"""Current ordinary Cook1411 follows the verified two-slot preview/cancel model."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_work_current_v2311.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'work_current_verification_v2311':'cooking_current_verification_v2321',
 'work_current_v2310_V2284':'cooking_current_v2320_V2284',
 'work_current_run_v2310':'cooking_current_run_v2320',
 'translations/work_contextual_editorial_manuscript_v1.json':'translations/cooking_contextual_editorial_manuscript_v1.json',
 '1387':'1411',
 'hold(rom,ram[frame],shots[frame],row,13)':'hold(rom,ram[frame],shots[frame],row,21)',
 "case['source_role_type']==13":"case['source_role_type']==15",
 'before[13]':'before[21]',
 'occupants[13]':'occupants[21]',
 'i not in(7,13)':'i not in(7,21)',
 'ordinary_Gerhard_Shipwright_and_return':'ordinary_Gerhard_Cook_and_return',
 'ordinary_current_Shipwright_actual':'ordinary_current_Cook_actual',
 'ordinary Shipwright':'ordinary Cook',
 'actual_source_role13_slot13_and_original_whole12104_selector_verified':'actual_source_role15_slot21_and_original_whole12104_selector_verified',
 'ordinary_input_selection_moves_Gerhard_from_slot7_to13_only':'ordinary_input_selection_moves_Gerhard_from_slot7_to21_only',
 'other23_new_current_visits_not_claimed':'other12_new_current_visits_not_claimed',
 'native_role13=True':'native_role15=True'
 }
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/cooking_current_verification_v2321/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),all_original_whole_selector_bitmap_RGB_bounds_and_scoped_state_assertions_preserved=True,source_bound_touch_geometry='work/analysis/cooking_button_geometry_v2320/source_bound_Galley_touch.json',initial_wrong_cell_run_has_no_Cook_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
