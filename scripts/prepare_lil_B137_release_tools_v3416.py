"""Preserve rejected V3409 and prepare the separately registered v2 hook build."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/lil_B137_release_tools_v3416');assert not root.exists()
    registry=read('translations/release_stack.json')
    assert len(registry['accepted_layers'])==114
    assert registry['profiles']['all-routes-unified-v3416']['lil_B137_editorial_v2']
    pairs=[]
    for old,new in [('scripts/build_lil_B137_v3409.py','scripts/build_lil_B137_v3416.py'),('scripts/verify_lil_B137_release_v3410.py','scripts/verify_lil_B137_release_v3417.py'),('scripts/run_lil_B137_startup_v3411.py','scripts/run_lil_B137_startup_v3418.py'),('scripts/verify_lil_B137_startup_v3412.py','scripts/verify_lil_B137_startup_v3419.py')]:
        a,b=Path(old),Path(new);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in [('v3409','v3416'),('V3409','V3416'),('Current3409','Current3416'),('version=3409','version=3416'),('registration_v3408b','registration_v3415'),('release_v3410','release_v3417'),('runs_v3411','runs_v3418'),('lil_B137_v3411_','lil_B137_v3418_'),('startup_v3412','startup_v3419')]:t=t.replace(x,y)
        if 'verify_lil_B137_release_' in new:
            assert t.count("'lil_B137_editorial'")==3
            t=t.replace("'lil_B137_editorial'","'lil_B137_editorial_v2'")
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8')
        pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    root.mkdir(parents=True);save(root/'provenance.json',dict(producers=pairs,registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),profile='all-routes-unified-v3416',stage_key='lil_B137_editorial_v2',validated_compiler='dk4tool/patch/lil_B137_editorial_v2.py',failed_V3409_profile_hook_and_all_prior_artifacts_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
