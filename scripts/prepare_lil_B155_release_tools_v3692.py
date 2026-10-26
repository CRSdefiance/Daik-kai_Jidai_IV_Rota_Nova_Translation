"""Derive registered cumulative build,exact clean patch andfresh startup/town checks."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B155_release_tools_v3692')
if __name__=='__main__':
    assert not ROOT.exists();pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x in changes:assert x in t,x
        t=re.sub('|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],t);compile(t,str(b),'exec');b.write_text(t,encoding='utf-8',newline='\n');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('scripts/build_lil_B152_B154_v3650.py','scripts/build_lil_B155_v3692.py',{'lil_B152_B154_build_v3650':'lil_B155_build_v3692','all_routes_combined_v3650':'all_routes_combined_v3692','lil_B152_B154_registration_v3649':'lil_B155_registration_v3691','all-routes-unified-v3650':'all-routes-unified-v3692'})
    make('scripts/verify_lil_B152_B154_release_v3651.py','scripts/verify_lil_B155_release_v3693.py',{'lil_B152_B154_editorial_v1':'lil_B155_editorial_v1','lil_B152_B154_release_v3651':'lil_B155_release_v3693','all_routes_combined_v3650':'all_routes_combined_v3692','all_routes_combined_v3607':'all_routes_combined_v3650','lil_B152_B154_registration_v3649':'lil_B155_registration_v3691','all-routes-unified-v3650':'all-routes-unified-v3692','all-routes-unified-v3607':'all-routes-unified-v3650','lil_B152_B154_editorial':'lil_B155_editorial',"len(manifest['batches'])==529":"len(manifest['batches'])==530",'all529_manifest':'all530_manifest','exact_to_V3607':'exact_to_V3650','manifest_batches=529':'manifest_batches=530','lil_coin_al = profile_config':'lil_angelo = profile_config'})
    make('scripts/run_lil_B152_B154_startup_v3652.py','scripts/run_lil_B155_startup_v3694.py',{'lil_B152_B154_runs_v3652':'lil_B155_runs_v3694','version=3650':'version=3692','lil_B152_B154_v3652_':'lil_B155_v3694_','not_a_selected_B152_B154_activation':'not_a_selected_B155_activation','no selected B152-B154 activation':'no selected B155 activation'})
    make('scripts/verify_lil_B152_B154_startup_v3653.py','scripts/verify_lil_B155_startup_v3695.py',{'lil_B152_B154_startup_v3653':'lil_B155_startup_v3695','lil_B152_B154_runs_v3652':'lil_B155_runs_v3694','all_routes_combined_v3650':'all_routes_combined_v3692','all_routes_combined_v3607':'all_routes_combined_v3650','lil_B142_B145_runs_v3609':'lil_B152_B154_runs_v3652','equal_V3607':'equal_V3650','matchV3607':'matchV3650','V3607':'V3650','Current3650':'Current3692','actual_selected_B152_B154_IDs':'actual_selected_B155_IDs'})
    make('scripts/record_lil_B152_B154_startup_view_v3653.py','scripts/record_lil_B155_startup_view_v3695.py',{'lil_B152_B154_startup_v3653':'lil_B155_startup_v3695','equal_V3607':'equal_V3650','source_B152_B154_not_selected':'source_B155_not_selected'})
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(tools=pairs,all_predecessor_ROMs_translations_and_producers_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
