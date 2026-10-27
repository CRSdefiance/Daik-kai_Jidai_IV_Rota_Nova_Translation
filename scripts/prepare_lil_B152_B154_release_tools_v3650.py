"""Derive full cumulative build,clean patch andfresh cold-boot tools with exact provenance."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B152_B154_release_tools_v3650')
if __name__=='__main__':
    assert not ROOT.exists();pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x in changes:assert x in t,x
        pattern='|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True));t=re.sub(pattern,lambda m:changes[m.group(0)],t);compile(t,str(b),'exec');b.write_text(t,encoding='utf-8',newline='\n');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('scripts/build_lil_B142_B145_v3607.py','scripts/build_lil_B152_B154_v3650.py',{'lil_B142_B145_build_v3607':'lil_B152_B154_build_v3650','all_routes_combined_v3607':'all_routes_combined_v3650','lil_B142_B145_registration_v3606':'lil_B152_B154_registration_v3649','all-routes-unified-v3607':'all-routes-unified-v3650'})
    make('scripts/verify_lil_B142_B145_release_v3608.py','scripts/verify_lil_B152_B154_release_v3651.py',{'lil_B142_B145_editorial_v1':'lil_B152_B154_editorial_v1','lil_B142_B145_release_v3608':'lil_B152_B154_release_v3651','all_routes_combined_v3607':'all_routes_combined_v3650','all_routes_combined_v3561':'all_routes_combined_v3607','lil_B142_B145_registration_v3606':'lil_B152_B154_registration_v3649','all-routes-unified-v3607':'all-routes-unified-v3650','all-routes-unified-v3561':'all-routes-unified-v3607','lil_B142_B145_editorial':'lil_B152_B154_editorial',"len(manifest['batches'])==528":"len(manifest['batches'])==529",'all528_manifest':'all529_manifest','exact_to_V3561':'exact_to_V3607','manifest_batches=528':'manifest_batches=529','lil_polder_armor_map = profile_config':'lil_coin_al = profile_config'})
    make('scripts/run_lil_B142_B145_startup_v3609.py','scripts/run_lil_B152_B154_startup_v3652.py',{'lil_B142_B145_runs_v3609':'lil_B152_B154_runs_v3652','version=3607':'version=3650','lil_B142_B145_v3609_':'lil_B152_B154_v3652_','not_a_selected_B142_B145_activation':'not_a_selected_B152_B154_activation','no selected B142-B145 activation':'no selected B152-B154 activation'})
    make('scripts/verify_lil_B142_B145_startup_v3610.py','scripts/verify_lil_B152_B154_startup_v3653.py',{'lil_B142_B145_startup_v3610':'lil_B152_B154_startup_v3653','lil_B142_B145_runs_v3609':'lil_B152_B154_runs_v3652','all_routes_combined_v3607':'all_routes_combined_v3650','all_routes_combined_v3561':'all_routes_combined_v3607','lil_B141_runs_v3563':'lil_B142_B145_runs_v3609','equal_V3561':'equal_V3607','matchV3561':'matchV3607','V3561':'V3607','Current3607':'Current3650','actual_selected_B142_B145_IDs':'actual_selected_B152_B154_IDs'})
    make('scripts/record_lil_B142_B145_startup_view_v3610.py','scripts/record_lil_B152_B154_startup_view_v3653.py',{'lil_B142_B145_startup_v3610':'lil_B152_B154_startup_v3653','equal_V3561':'equal_V3607','source_B142_B145_not_selected':'source_B152_B154_not_selected'})
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(tools=pairs,all_predecessor_ROMs_translations_and_producers_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
