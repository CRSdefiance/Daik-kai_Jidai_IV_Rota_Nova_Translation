"""Preserve previous release tools; produce explicitly mapped cumulative successors."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_B109_release_tools_v3526');assert not root.exists();pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x in changes:assert x in t,x
        pattern='|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True));t=re.sub(pattern,lambda m:changes[m.group(0)],t)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('scripts/build_lil_B139_B140_v3487.py','scripts/build_maria_B109_v3526.py',{
        'lil_B139_B140_build_v3487':'maria_B109_build_v3526','all_routes_combined_v3487':'all_routes_combined_v3526',
        'lil_B139_B140_registration_v3486':'maria_B109_registration_v3525','all-routes-unified-v3487':'all-routes-unified-v3526',
        "registration['release_stack_sha256']":"registration['registry_after_sha256']","registration['builder_sha256']":"registration['builder_after_sha256']",
        "len(manifest['batches'])==525":"len(manifest['batches'])==526",'RegisteredV3487':'RegisteredV3526','525manifest':'526manifest'})
    make('scripts/verify_lil_B139_B140_release_v3488.py','scripts/verify_maria_B109_release_v3527.py',{
        'lil_B139_B140_editorial_v2':'maria_B109_editorial_v1','lil_B139_B140_release_v3488':'maria_B109_release_v3527',
        'all_routes_combined_v3487':'all_routes_combined_v3526','all_routes_combined_v3450':'all_routes_combined_v3487',
        'lil_B139_B140_registration_v3486':'maria_B109_registration_v3525','all-routes-unified-v3487':'all-routes-unified-v3526',
        'all-routes-unified-v3450':'all-routes-unified-v3487','lil_B139_B140_editorial':'maria_B109_editorial',
        "len(manifest['batches'])==525":"len(manifest['batches'])==526",'target_SC2_sha256':'target_SC3_sha256',
        'all525_manifest':'all526_manifest','exact_to_V3450':'exact_to_V3487','manifest_batches=525':'manifest_batches=526'})
    make('scripts/run_lil_B139_B140_startup_v3489.py','scripts/run_maria_B109_startup_v3528.py',{
        'lil_B139_B140_runs_v3489':'maria_B109_runs_v3528','version=3487':'version=3526',
        'lil_B139_B140_v3489_':'maria_B109_v3528_',
        'not_a_selected_B139_B140_activation':'not_a_selected_source_B109_activation',
        'no selectedB139/B140 activation':'no selected sourceB109 activation'})
    make('scripts/verify_lil_B139_B140_startup_v3490b.py','scripts/verify_maria_B109_startup_v3529.py',{
        'lil_B139_B140_startup_v3490':'maria_B109_startup_v3529','lil_B139_B140_runs_v3489':'maria_B109_runs_v3528',
        'all_routes_combined_v3487':'all_routes_combined_v3526','all_routes_combined_v3450':'all_routes_combined_v3487',
        'lil_B138_runs_v3452':'lil_B139_B140_runs_v3489','equal_V3450':'equal_V3487','matchV3450':'matchV3487',
        'V3450':'V3487','Current3487':'Current3526','actual_selected_B139_B140_IDs':'actual_selected_source_B109_IDs'})
    root.mkdir(parents=True);save(root/'provenance.json',dict(tools=pairs,all_predecessors_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
