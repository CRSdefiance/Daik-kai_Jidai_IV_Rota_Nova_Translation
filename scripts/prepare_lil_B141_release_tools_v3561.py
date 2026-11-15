"""Produce cumulative build,exact-patch and cold-boot successors without overwrites."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B141_release_tools_v3561');assert not root.exists();pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x in changes:assert x in t,x
        pattern='|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True));t=re.sub(pattern,lambda m:changes[m.group(0)],t);compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('scripts/build_maria_B109_v3526.py','scripts/build_lil_B141_v3561.py',{
        'maria_B109_build_v3526':'lil_B141_build_v3561','all_routes_combined_v3526':'all_routes_combined_v3561','maria_B109_registration_v3525':'lil_B141_registration_v3560','all-routes-unified-v3526':'all-routes-unified-v3561',"len(manifest['batches'])==526":"len(manifest['batches'])==527",'RegisteredV3526':'RegisteredV3561','526manifest':'527manifest'})
    make('scripts/verify_maria_B109_release_v3527.py','scripts/verify_lil_B141_release_v3562.py',{
        'maria_B109_editorial_v1':'lil_B141_editorial_v1','maria_B109_release_v3527':'lil_B141_release_v3562','all_routes_combined_v3526':'all_routes_combined_v3561','all_routes_combined_v3487':'all_routes_combined_v3526','maria_B109_registration_v3525':'lil_B141_registration_v3560','all-routes-unified-v3526':'all-routes-unified-v3561','all-routes-unified-v3487':'all-routes-unified-v3526','maria_B109_editorial':'lil_B141_editorial',"len(manifest['batches'])==526":"len(manifest['batches'])==527",'target_SC3_sha256':'target_SC2_sha256','all526_manifest':'all527_manifest','exact_to_V3487':'exact_to_V3526','manifest_batches=526':'manifest_batches=527'})
    make('scripts/run_maria_B109_startup_v3528.py','scripts/run_lil_B141_startup_v3563.py',{
        'maria_B109_runs_v3528':'lil_B141_runs_v3563','version=3526':'version=3561','maria_B109_v3528_':'lil_B141_v3563_','not_a_selected_source_B109_activation':'not_a_selected_B141_activation','no selected sourceB109 activation':'no selected B141 activation'})
    make('scripts/verify_maria_B109_startup_v3529.py','scripts/verify_lil_B141_startup_v3564.py',{
        'maria_B109_startup_v3529':'lil_B141_startup_v3564','maria_B109_runs_v3528':'lil_B141_runs_v3563','all_routes_combined_v3526':'all_routes_combined_v3561','all_routes_combined_v3487':'all_routes_combined_v3526','lil_B139_B140_runs_v3489':'maria_B109_runs_v3528','equal_V3487':'equal_V3526','matchV3487':'matchV3526','V3487':'V3526','Current3526':'Current3561','actual_selected_source_B109_IDs':'actual_selected_B141_IDs'})
    make('scripts/record_maria_B109_startup_view_v3529.py','scripts/record_lil_B141_startup_view_v3564.py',{
        'maria_B109_startup_v3529':'lil_B141_startup_v3564','equal_V3487':'equal_V3526','source_event109_not_selected':'source_B141_not_selected'})
    root.mkdir(parents=True);save(root/'provenance.json',dict(tools=pairs,all_predecessor_ROMS_translations_and_producers_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
