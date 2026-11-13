"""Source caption is projected from nativey72 to UIy32; preserve detail pixels."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_refit_spritsail_actual_v2290.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 "refit_spritsail_actual_verification_v2290'":"refit_spritsail_actual_verification_v2290c'",
 'not any(initial[60*168:])':'not any(initial[72*168:84*168])',
 '(64+i*6+x,40+y)':'(64+i*6+x,32+y)',
 'range(40,52)':'range(32,44)',
 'heading_native_y72_projected_separately_to_UI_y40':'heading_native_y72_projected_separately_to_UI_y32',
 'heading_native_y72_UI_y40_distinct':'heading_native_y72_UI_y32_distinct'
 }
 for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_spritsail_actual_verification_v2290c/successor_provenance.json',dict(failed_producers=['scripts/verify_refit_spritsail_actual_v2290.py','scripts/verify_refit_spritsail_actual_v2290b.py'],first_failure='Source numeric details at nativey60-71 were already painted;the full plane oracle now preserves them.',second_failure='The source caption projection was incorrectly assumed to be UIy40. Complete unique Spritsail ink matches atx64,y32;native captiony72 remains unchanged.',pixel_anchor_search_x=list(range(56,81)),pixel_anchor_search_y=list(range(20,60)),only_complete_glyph_anchor=[64,32],all_blank_caption_cells_also_checked=True,no_ROM_font_metrics_or_geometry_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
