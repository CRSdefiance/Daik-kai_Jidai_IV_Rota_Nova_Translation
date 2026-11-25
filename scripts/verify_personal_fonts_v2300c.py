"""Bind25 complete native fonts to the genuine initialized current parent draw."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_personal_fonts_v2300.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 "personal_fonts_v2300'":"personal_fonts_v2300c'",
 'from scripts.verify_personal_gameplay_v841 import actual_view':'from scripts.verify_personal_gameplay_v841 import actual_view,projected',
 "results=[];panels=[]":"results=[];panels=[];current_projection=projected(rom,raw,view);assert current_projection[-1]['source_origin']==[0,60]and current_projection[-1]['destination']==[16,112]and current_projection[-1]['size']==[216,36]",
 "projection=composition(rom,raw,text,False,actor=row['actor_ID'],state=1);assert projection['selected_IDs']==[n]and projection['draws'][-1]['source_origin']==[0,60]and projection['draws'][-1]['destination']==[16,112]and projection['draws'][-1]['size']==[216,36]":"assert case['message_id']==n;projection=current_projection",
 'native_original_parent_projection=projection':'binding_to_current_actual_initialized_parent_draw=projection[-1]',
 'all25_complete_native_font_and_parent_cases=results':'all25_complete_native_font_and_parent_binding_cases=results,current_initialized_parent_draw_commands=current_projection,current_initialized_parent_complete_draw_controls=1',
 'parent_projections=25':'parent_projection_controls=1',
 'parent_SDK_GPU_blit_boundary_intercepted_not_actual25_UI_visits=True':'current_initialized_parent_SDK_GPU_blit_boundary_intercepted_not_actual25_UI_visits=True,all25_native_font_cases_share_verified_source_projection_not25_reinitializations=True'
 }
 for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/personal_fonts_v2300c/successor_provenance.json',dict(failed_producers=['scripts/verify_personal_fonts_v2300.py','scripts/verify_personal_fonts_v2300b.py'],first_failure='The cloned historical parent helper lost its keyword-only default.',second_failure='Historical15948 reinitialization from a different captured UI context hit an unmapped read. No parent approval was recorded.',successor_uses_current_genuine_initialized_view_and_original14BE8_draw_dispatch=True,current_parent_projection_control_count=1,all25_fonts_independently_execute_full_original_actor_selector_expander_clear_and_font=True,all25_bind_to_same_source_projection_metadata_not25_reinitialization_claims=True,no_frozen_helper_ROM_or_geometry_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
