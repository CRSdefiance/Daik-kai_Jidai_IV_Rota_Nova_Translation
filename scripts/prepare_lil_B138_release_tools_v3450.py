"""Prepare one524-batch build,exact clean patch and two fresh current cold boots."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_release_tools_v3450');assert not root.exists();pairs=[]
    for old,new in [('scripts/build_lil_B137_v3416.py','scripts/build_lil_B138_v3450.py'),('scripts/verify_lil_B137_release_v3417.py','scripts/verify_lil_B138_release_v3451.py'),('scripts/run_lil_B137_startup_v3418.py','scripts/run_lil_B138_startup_v3452.py'),('scripts/verify_lil_B137_startup_v3419.py','scripts/verify_lil_B138_startup_v3453.py')]:
        a,b=Path(old),Path(new);assert not b.exists();t=a.read_text(encoding='utf-8')
        t=t.replace('from dk4tool.patch import lil_B137_editorial_v2','from dk4tool.patch import lil_B138_editorial_v1')
        t=t.replace('B137','B138')
        t=t.replace('v3416','__NEW__').replace('V3416','__NEWUP__').replace('Current3416','Current3450').replace('version=3416','version=3450').replace('v3372','v3416').replace('V3372','V3416').replace('__NEW__','v3450').replace('__NEWUP__','V3450')
        for x,y in [('registration_v3415','registration_v3449'),('release_v3417','release_v3451'),('runs_v3418','runs_v3452'),('lil_B138_v3418_','lil_B138_v3452_'),('startup_v3419','startup_v3453'),('work/analysis/lil_B135_B136_runs_v3374','work/analysis/lil_B137_runs_v3418'),('==523','==524'),('all523_','all524_'),('manifest_batches=523','manifest_batches=524'),('523manifest','524manifest')]:t=t.replace(x,y)
        t=t.replace("'lil_B138_editorial_v2'","'lil_B138_editorial'")
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append((a,b))
    root.mkdir(parents=True);save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],parent_profile='all-routes-unified-v3416',profile='all-routes-unified-v3450',expected_manifest_batches=524,stage_key='lil_B138_editorial',producer_sha256=sha(Path(__file__).read_bytes()),all_previous_ROMs_producers_and_translations_preserved=True,full_goal_complete=False))
