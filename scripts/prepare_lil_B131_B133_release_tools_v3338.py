"""Preserve earlier producers while preparing the registered cumulative release."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B131_B133_release_tools_v3338');assert not root.exists();pairs=[]
    specs=[
      ('scripts/build_lil_B122_B127_v3300.py','scripts/build_lil_B131_B133_v3338.py'),
      ('scripts/verify_lil_B122_B127_release_v3301.py','scripts/verify_lil_B131_B133_release_v3339.py'),
      ('scripts/run_lil_B122_B127_startup_v3302.py','scripts/run_lil_B131_B133_startup_v3340.py'),
      ('scripts/verify_lil_B122_B127_startup_v3303b.py','scripts/verify_lil_B131_B133_startup_v3341.py'),
    ]
    for a,b in specs:
        old,new=Path(a),Path(b);assert not new.exists();t=old.read_text(encoding='utf-8')
        # Protect current version first,then advance predecessor references.
        t=t.replace('v3300','__NEW__').replace('V3300','__NEWUP__').replace('Current3300','Current3338')
        t=t.replace('v3251','v3300').replace('V3251','V3300').replace('__NEW__','v3338').replace('__NEWUP__','V3338')
        t=t.replace('lil_B122_B127','lil_B131_B133').replace('B122-B127','B131/B133')
        t=t.replace('editorial_v2','editorial_v1').replace('registration_v3299b','registration_v3337b')
        t=t.replace('build_v3338','build_v3338').replace('release_v3301','release_v3339')
        t=t.replace('runs_v3302','runs_v3340').replace('lil_B131_B133_v3302_','lil_B131_B133_v3340_').replace('version=3300','version=3338')
        t=t.replace('startup_v3303','startup_v3341').replace('==519','==521').replace('519manifest','521manifest').replace('all519_','all521_').replace('manifest_batches=519','manifest_batches=521')
        # Actual comparison inputs remain prior V3300 proofs,not renamed copies.
        t=t.replace('work/analysis/lil_B111_B119_runs_v3253','work/analysis/lil_B122_B127_runs_v3302')
        compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    root.mkdir(parents=True);save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],no_previous_ROM_orproducer_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
