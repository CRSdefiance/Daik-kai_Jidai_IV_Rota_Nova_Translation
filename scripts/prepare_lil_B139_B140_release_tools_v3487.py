"""Prepare cumulative build,reconstruction and scoped actual startup successors."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B139_B140_release_tools_v3487');assert not root.exists();reg=read('work/analysis/lil_B139_B140_registration_v3486/registration_receipt.json');assert reg['negative_cases']==43 and reg['stage_import_module']=='dk4tool.patch.lil_B139_B140_editorial_v2';pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('scripts/build_lil_B138_v3450.py','scripts/build_lil_B139_B140_v3487.py',[
      ('lil_B138_build_v3450','lil_B139_B140_build_v3487'),('all_routes_combined_v3450_candidate','all_routes_combined_v3487_candidate'),('lil_B138_registration_v3449','lil_B139_B140_registration_v3486'),('all-routes-unified-v3450','all-routes-unified-v3487'),("len(manifest['batches'])==524","len(manifest['batches'])==525"),('RegisteredV3450 cumulative build passes:524manifest','RegisteredV3487 cumulative build passes:525manifest')])
    make('scripts/verify_lil_B138_release_v3451.py','scripts/verify_lil_B139_B140_release_v3488.py',[
      ('from dk4tool.patch import lil_B138_editorial_v1','from dk4tool.patch import lil_B139_B140_editorial_v2'),('lil_B138_release_v3451','lil_B139_B140_release_v3488'),('all_routes_combined_v3450_candidate','all_routes_combined_v3487_candidate'),('all_routes_combined_v3416_candidate','all_routes_combined_v3450_candidate'),('lil_B138_registration_v3449','lil_B139_B140_registration_v3486'),('all-routes-unified-v3450','all-routes-unified-v3487'),('all-routes-unified-v3416','all-routes-unified-v3450'),('lil_B138_editorial','lil_B139_B140_editorial'),("len(manifest['batches'])==524","len(manifest['batches'])==525"),('all524_manifest_batches','all525_manifest_batches'),('exact_to_V3416','exact_to_V3450'),('manifest_batches=524','manifest_batches=525')])
    make('scripts/run_lil_B138_startup_v3452.py','scripts/run_lil_B139_B140_startup_v3489.py',[
      ('lil_B138_runs_v3452','lil_B139_B140_runs_v3489'),('version=3450','version=3487'),('lil_B138_v3452','lil_B139_B140_v3489'),('not_a_selected_B138_activation','not_a_selected_B139_B140_activation'),('selectedB138','selectedB139/B140')])
    make('scripts/verify_lil_B138_startup_v3453.py','scripts/verify_lil_B139_B140_startup_v3490.py',[
      ('V3416','V3450'),('lil_B138_startup_v3453','lil_B139_B140_startup_v3490'),('lil_B138_runs_v3452','lil_B139_B140_runs_v3489'),('all_routes_combined_v3450_candidate','all_routes_combined_v3487_candidate'),('all_routes_combined_v3416_candidate','all_routes_combined_v3450_candidate'),('lil_B137_runs_v3418','lil_B138_runs_v3452'),('Current3450','Current3487'),('actual_selected_B138_IDs','actual_selected_B139_B140_IDs')])
    make('scripts/record_lil_B138_startup_view_v3453.py','scripts/record_lil_B139_B140_startup_view_v3490.py',[
      ('lil_B138_startup_v3453','lil_B139_B140_startup_v3490'),('V3416','V3450'),('actual_selected_B138_IDs','actual_selected_B139_B140_IDs'),('targeted_headless_actual_framebuffers_not_B138_scene','targeted_headless_actual_framebuffers_not_B139_B140_scene')])
    root.mkdir(parents=True);save(root/'provenance.json',dict(tools=pairs,registration=reg['profile'],producer_sha256=sha(Path(__file__).read_bytes()),all_prior_artifacts_preserved=True,full_goal_complete=False))
