"""Derive isolated registered-build/patch/current-startup workflows without replaying source tests."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_release_tools_v7229b')
if __name__=='__main__':
    assert not ROOT.exists();reports=[]
    common={'B224':'B225','lil_B224_editorial_v3':'lil_B225_editorial_v1','7168':'7230','7118':'7168','7167':'7229','7169':'7231','7170':'7232','7171':'7233','7172':'7234','7173':'7235','lil_B223_runs_v7121':'lil_B224_runs_v7171'}
    for old,new,extra in [
      ('build_lil_B224_v7168.py','build_lil_B225_v7230.py',{}),
      ('run_lil_B224_regressions_v7168.py','run_lil_B225_regressions_v7230.py',{}),
      ('verify_lil_B224_release_v7169.py','verify_lil_B225_release_v7231.py',{'lil_B223_editorial':'lil_B224_editorial','617':'618','lil_B224_reference_v7150_RESEARCH_ONLY.nds':'lil_B225_reference_v7215_RESEARCH_ONLY.nds'}),
      ('pin_lil_B224_v7170.py','pin_lil_B225_v7232.py',{}),
      ('run_lil_B224_startup_v7171.py','run_lil_B225_startup_v7233.py',{}),
      ('verify_lil_B224_startup_v7172.py','verify_lil_B225_startup_v7234.py',{}),
      ('record_lil_B224_startup_view_v7172.py','record_lil_B225_startup_view_v7234.py',{}),
      ('bind_current_V7168_native_v7173.py','bind_current_V7230_native_v7235.py',{})]:
        src=Path('scripts')/old;changes={k:v for k,v in {**common,**extra}.items() if k in src.read_text(encoding='utf-8')};reports.append(derive(src,Path('scripts')/new,changes))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_release_tools.json',reports);print('B225 release tools prepared;registration must await all production challenges.')
