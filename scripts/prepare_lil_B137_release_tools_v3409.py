"""Prepare registered523-batch build,exactclean patch andfresh cold boots."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B137_release_tools_v3409');assert not root.exists();pairs=[]
    for a,b in [('scripts/build_lil_B135_B136_v3372.py','scripts/build_lil_B137_v3409.py'),('scripts/verify_lil_B135_B136_release_v3373.py','scripts/verify_lil_B137_release_v3410.py'),('scripts/run_lil_B135_B136_startup_v3374.py','scripts/run_lil_B137_startup_v3411.py'),('scripts/verify_lil_B135_B136_startup_v3375.py','scripts/verify_lil_B137_startup_v3412.py')]:
        old,new=Path(a),Path(b);assert not new.exists();t=old.read_text(encoding='utf-8')
        t=t.replace('work/analysis/lil_B131_B133_runs_v3340','__PRIORRUNS__').replace('lil_B135_B136_editorial_v1','lil_B137_editorial_v2')
        t=t.replace('v3372','__NEW__').replace('V3372','__NEWUP__').replace('Current3372','Current3409').replace('v3338','v3372').replace('V3338','V3372').replace('__NEW__','v3409').replace('__NEWUP__','V3409')
        t=t.replace('B135_B136','B137').replace('B135/B136','B137').replace('registration_v3371b','registration_v3408b').replace('release_v3373','release_v3410').replace('runs_v3374','runs_v3411').replace('lil_B137_v3374_','lil_B137_v3411_').replace('startup_v3375','startup_v3412').replace('version=3372','version=3409')
        t=t.replace('__PRIORRUNS__','work/analysis/lil_B135_B136_runs_v3374').replace('==522','==523').replace('522manifest','523manifest').replace('all522_','all523_').replace('manifest_batches=522','manifest_batches=523')
        compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    root.mkdir(parents=True);save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],previous_ROMs_profiles_and_actual_gameplay_controls_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
