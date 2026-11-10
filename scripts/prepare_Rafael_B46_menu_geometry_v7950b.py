"""Correct copied three-option screen Y using the original measured two-option native rectangle."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_menu_geometry_tools_v7950b');assert not root.exists()
    row=derive('scripts/audit_Rafael_B46_menu_v7950.py','scripts/audit_Rafael_B46_menu_v7950b.py',{
        'Rafael_B46_menu_actual_v7950':'Rafael_B46_menu_actual_v7950b',
        "labels=g['fixture']['original_menu_records'];width=84 if version=='clean_Japanese' else 66":"labels=g['fixture']['original_menu_records'];width=84 if version=='clean_Japanese' else 66\n        flow=read('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')\n        native_rect=(flow['source_menu_versions'][0]['native_VM'] if version=='clean_Japanese' else choices['native_target_VM'])['native_menu_rectangle']\n        assert native_rect[1:4:2]==[64,128] and native_rect[2]-native_rect[0]==width+32",
        'x=(256-width)//2':"x=native_rect[0]+16;assert x==(256-width)//2",
        'y=262+20*index':'y=192+native_rect[1]+16+20*index',
        'im.crop((56,244,200,310))':'im.crop((56,254,200,320))',
        'actual_physical_backing=[256,36],actual_caption_view=[width,12]':'actual_physical_backing=[256,36],actual_caption_view=[width,12],original_native_menu_rectangle=native_rect',
    })
    root.mkdir(parents=True);save(root/'source_locked_geometry_correction.json',dict(derivation=row,
        failed_producer='scripts/audit_Rafael_B46_menu_v7950.py',
        diagnostic='The copied B212 three-choice first-caption Y262 mismatched the two-choice B46 image. Original two-choice provider rectangle top64 plus DS bottom192 plus16 gives Y272. All pixel/backing/highlight assertions remain intact.',
        first_owned_backing_check_passed_but_visible_origin_check_failed_before_any_approval=True,
        no_failed_check_counted_aspassing_negative=True,no_ROM_snapshot_image_orinput_mutation=True,new_credit=0,full_goal_complete=False))
