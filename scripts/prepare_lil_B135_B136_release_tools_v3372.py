"""Prepare registered522-batch build,exactclean patch andfresh cold boots."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B135_B136_release_tools_v3372');assert not root.exists();pairs=[]
    specs=[('scripts/build_lil_B131_B133_v3338.py','scripts/build_lil_B135_B136_v3372.py'),('scripts/verify_lil_B131_B133_release_v3339.py','scripts/verify_lil_B135_B136_release_v3373.py'),('scripts/run_lil_B131_B133_startup_v3340.py','scripts/run_lil_B135_B136_startup_v3374.py'),('scripts/verify_lil_B131_B133_startup_v3341.py','scripts/verify_lil_B135_B136_startup_v3375.py')]
    for a,b in specs:
        old,new=Path(a),Path(b);assert not new.exists();t=old.read_text(encoding='utf-8')
        t=t.replace('v3338','__NEW__').replace('V3338','__NEWUP__').replace('Current3338','Current3372').replace('v3300','v3338').replace('V3300','V3338').replace('__NEW__','v3372').replace('__NEWUP__','V3372')
        # Prior gameplay controls are the actually completed V3338 runs.
        t=t.replace('work/analysis/lil_B122_B127_runs_v3302','work/analysis/__PRIOR_RUNS__')
        t=t.replace('lil_B131_B133','lil_B135_B136').replace('B131/B133','B135/B136').replace('B122_B127','B135_B136').replace('B122-B127','B135/B136')
        t=t.replace('work/analysis/__PRIOR_RUNS__','work/analysis/lil_B131_B133_runs_v3340')
        t=t.replace('registration_v3337b','registration_v3371b').replace('release_v3339','release_v3373').replace('runs_v3340','runs_v3374').replace('lil_B135_B136_v3340_','lil_B135_B136_v3374_').replace('startup_v3341','startup_v3375').replace('version=3338','version=3372')
        # Restore the prior-run path after updating this run's folder name.
        t=t.replace('work/analysis/lil_B131_B133_runs_v3374','work/analysis/lil_B131_B133_runs_v3340')
        t=t.replace('==521','==522').replace('521manifest','522manifest').replace('all521_','all522_').replace('manifest_batches=521','manifest_batches=522')
        if 'verify_lil_B131_B133_release' in a:
            x="[normal(conf['manuscript']),normal(conf['choices'])]";assert x in t;t=t.replace(x,"[normal(conf['manuscript'])]")
        compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    root.mkdir(parents=True);save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],previous_ROMs_producers_and_gameplay_controls_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
