"""Registered build/reconstruction and fresh cold-boot successors."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B122_B127_release_tools_v3300')
if __name__=='__main__':
    assert not ROOT.exists();pairs=[]
    def generate(old,new,changes):
        old,new=Path(old),Path(new);assert not new.exists();text=old.read_text(encoding='utf-8')
        for key in changes:assert key in text,key
        text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
        text=text.replace('B111_B119','B122_B127').replace('B111-B119','B122-B127')
        compile(text,str(new),'exec');new.write_text(text,encoding='utf-8');pairs.append(dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes())))
    reg=Path('work/analysis/lil_B122_B127_registration_v3299b/registration_receipt.json');assert read(reg)['negative_cases']==50
    generate('scripts/build_lil_B111_B119_v3251.py','scripts/build_lil_B122_B127_v3300.py',{
      'lil_B111_B119_build_v3251':'lil_B122_B127_build_v3300','all_routes_combined_v3251_candidate.nds':'all_routes_combined_v3300_candidate.nds','lil_B111_B119_registration_v3250':'lil_B122_B127_registration_v3299b','all-routes-unified-v3251':'all-routes-unified-v3300','==517':'==519','RegisteredV3251':'RegisteredV3300','517manifest':'519manifest'})
    generate('scripts/verify_lil_B111_B119_release_v3252b.py','scripts/verify_lil_B122_B127_release_v3301.py',{
      'lil_B111_B119_editorial as owned':'lil_B122_B127_editorial_v2 as owned','lil_B111_B119_release_v3252b':'lil_B122_B127_release_v3301','all_routes_combined_v3251_candidate.nds':'all_routes_combined_v3300_candidate.nds','all_routes_combined_v3204_candidate.nds':'all_routes_combined_v3251_candidate.nds','lil_B111_B119_registration_v3250':'lil_B122_B127_registration_v3299b','all-routes-unified-v3251':'all-routes-unified-v3300','all-routes-unified-v3204':'all-routes-unified-v3251',"conf['actor_styles']":"conf['choices']",'==517':'==519','all517_':'all519_','manifest_batches=517':'manifest_batches=519','exact_to_V3204':'exact_to_V3251'})
    generate('scripts/run_lil_B111_B119_startup_v3253.py','scripts/run_lil_B122_B127_startup_v3302.py',{
      'lil_B111_B119_runs_v3253':'lil_B122_B127_runs_v3302','version=3251':'version=3300','lil_B111_B119_v3253_':'lil_B122_B127_v3302_'})
    generate('scripts/verify_lil_B111_B119_startup_v3254.py','scripts/verify_lil_B122_B127_startup_v3303.py',{
      'lil_B111_B119_startup_v3254':'lil_B122_B127_startup_v3303','lil_B111_B119_runs_v3253':'lil_B122_B127_runs_v3302','all_routes_combined_v3251_candidate.nds':'all_routes_combined_v3300_candidate.nds','all_routes_combined_v3204_candidate.nds':'all_routes_combined_v3251_candidate.nds','lil_Shrines_Temples_runs_v3206':'lil_B111_B119_runs_v3253','V3204':'V3251'})
    # The last substitution changes only the controls folder to the preserved prior
    # B111-B119 run,not to a nonexistent B122-B127 prior-run folder.
    p=Path('scripts/verify_lil_B122_B127_startup_v3303.py');text=p.read_text(encoding='utf-8');a='lil_B122_B127_runs_v3253';assert a in text;text=text.replace(a,'lil_B111_B119_runs_v3253');p.write_text(text,encoding='utf-8');pairs[-1]['successor_sha256']=sha(p.read_bytes())
    ROOT.mkdir(parents=True);save(ROOT/'release_and_startup_tools_provenance.json',dict(producers=pairs,registration=str(reg),registration_sha256=sha(reg.read_bytes()),preserve_all_earlier_executed_producers_and_ROMs=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
