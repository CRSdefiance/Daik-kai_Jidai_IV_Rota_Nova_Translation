"""Use the registered stage's18 historical revisions;25 fresh retentions stay distinct."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/complete_personal_context_v2304.py')
if __name__=='__main__':
 source=OLD.read_text().replace('V2304','V2304b').replace('v2304','v2304b')
 for old,new in [('historical19 revised','historical18 revised'),('len(historically_changed)==19','len(historically_changed)==18')]:assert source.count(old)==1,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/personal_completion_v2304b/successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='Preflight expected19 historical changed records,but the registered stage has18 revisions and25 reviewed IDs. It rejected before creating completion files or changing the ledger.',actual_historical_changed_IDs=[1361,1365,1366,1367,1368,1369,1370,1373,1374,1375,1376,1378,1379,1380,1381,1382,1384,1385],fresh_retained_records=25,no_new_revisions_or_double_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
