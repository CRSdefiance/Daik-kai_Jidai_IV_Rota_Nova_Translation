"""Successor accounts for the current run's extra terminal frame20601."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_refit_current_actual_v2281.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 "refit_current_actual_verification_v2281'":"refit_current_actual_verification_v2281b'",
 'and len(shots)==62 and shots.keys()==oldshots.keys()':'and len(shots)==63 and shots.keys()==oldshots.keys()|{20601}',
 'for f in shots],six_paired':'for f in oldshots],unpaired_extra_terminal_frame=20601,six_paired'
 }
 for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_current_actual_verification_v2281b/successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='Preflight expected62 images; current20601frame run has the62 identical scheduled capture frames plus one extra final frame20601. No native or pixel checks ran before that assertion.',extra_terminal_frame_retained_and_reported_without_historical_pair=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
