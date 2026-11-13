"""Prepare the sole registered cumulative builder wrapper, preserving predecessors."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    old=Path('scripts/build_lil_shrines_v3204.py');new=Path('scripts/build_lil_B111_B119_v3251.py');assert not new.exists()
    reg=Path('work/analysis/lil_B111_B119_registration_v3250/registration_receipt.json');assert read(reg)['negative_cases']==54
    t=old.read_text(encoding='utf-8')
    for a,b in [('lil_Shrines_Temples_build_v3204','lil_B111_B119_build_v3251'),('all_routes_combined_v3204_candidate.nds','all_routes_combined_v3251_candidate.nds'),('lil_Shrines_Temples_registration_v3203b','lil_B111_B119_registration_v3250'),('all-routes-unified-v3204','all-routes-unified-v3251'),('==515','==517'),('RegisteredV3204','RegisteredV3251'),('515manifest','517manifest')]:assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    save(Path('work/analysis/lil_B111_B119_compiler_tools_v3249/registered_build_wrapper_provenance.json'),dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),registration=str(reg),registration_sha256=sha(reg.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
