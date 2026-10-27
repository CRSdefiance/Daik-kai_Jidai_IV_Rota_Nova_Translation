"""All24 current native fonts and48 copies;reuse the current shared body control."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/verify_work_fonts_v2309.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'work_fonts_v2309':'livestock_prayer_fonts_v2328',
 'translations/work_contextual_editorial_manuscript_v1.json':'translations/livestock_prayer_contextual_editorial_manuscript_v1.json',
 'work_current_v2310_V2284':'cooking_current_v2320_V2284',
 'scripts.work_comments_layout_v843 import compiled,layout':'scripts.livestock_prayer_layout_v854 import compiled,layout',
 'range(1386,1410)':'range(1423,1447)',
 'scripts/work_comments_layout_v843.py':'scripts/livestock_prayer_layout_v854.py',
 'full36_cell1405_trailing_period_consumed_and_inside_visible_crop':'complete_three_row1435_invocation_including_Holy_Spirit_inside_visible_crop',
 'assert len(cases)==24 and len(copies)==48;save(':'assert len(next(c for c in cases if c["message_ID"]==1435)["generated_lines"])==3;assert len(cases)==24 and len(copies)==48;save('
 }
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 geometry=Path('work/analysis/cooking_button_geometry_v2320/source_bound_Galley_touch.json');g=read(geometry);assert not any(b['native_role_type']in(17,18)for b in g['all31_native_buttons'])
 save('work/analysis/livestock_prayer_fonts_v2328/shared_current_control_scope.json',dict(current_shared_consumer_control='work/analysis/cooking_current_verification_v2321/ordinary_current_Cook_actual.json',shared_control_has_only_current_1411_holds_not24_family_visits=True,source_bound_current_flagship31_button_geometry=str(geometry),geometry_sha256=sha(geometry.read_bytes()),current_flagship_has_no_Livestock17_or_Chapel18_room=True,other_ship_room_availability_not_claimed=True,existing_current_initialized_parent_projection_reused_no_new_emulator_run=True,all24_native_role_selector_expander_clear_font_checks_are_current_offline_CPU_proofs=True,historical_actual_Livestock_and_Chapel_captures_are_separately_bound=True,original_formatter=str(Path('scripts/livestock_prayer_layout_v854.py')),producer_sha256=sha(Path(__file__).read_bytes()),effective_source_sha256=sha(source.encode()),full_goal_complete=False))
