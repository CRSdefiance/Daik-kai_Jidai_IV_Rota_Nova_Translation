"""Preserve existing numeric details at nativey60 before the caption at72."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_refit_spritsail_actual_v2290.py')
if __name__=='__main__':
 source=OLD.read_text().replace("refit_spritsail_actual_verification_v2290'","refit_spritsail_actual_verification_v2290b'");old='not any(initial[60*168:])';new='not any(initial[72*168:84*168])';assert source.count(old)==1;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_spritsail_actual_verification_v2290b/successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='The source UI has already drawn numeric details at nativey60-71 before drawing the heading at72. Requiring the entire60-107 region to be blank was incorrect. The caption destination72-83 is blank;all preexisting details are preserved in the full before/after plane oracle.',all_existing_detail_pixels_preserved=True,caption_native_return_and_full_plane_verified=True,no_ROM_or_geometry_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
