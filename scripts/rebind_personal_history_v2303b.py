"""Include the historical read-only pause exports used by the timed holds."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/rebind_personal_history_v2303.py')
if __name__=='__main__':
 source=OLD.read_text().replace("personal_history_v2303'","personal_history_v2303b'");old="for r in report['read_only_capture_RAM_snapshots']if r['frame']==frame";new="for r in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[])if r['frame']==frame";assert source.count(old)==1;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/personal_history_v2303b/successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='The timed Julio holds use read-only pause RAM exports,which the first historical lookup omitted. No historical pixel approval was recorded before rejection.',both_original_capture_and_pause_exports_included=True,all_original_export_hashes_and_readonly_flags_checked=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
