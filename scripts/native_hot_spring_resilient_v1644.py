"""Preserve naturally changed crew counts in location/resource-only test fixtures."""
import inspect
from pathlib import Path
from scripts import native_fatigue_region2_fixture_v1605 as original_location
from scripts import native_hot_spring_provisions_v1642 as original_supply
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROM=original_supply.ROM
ROOT=Path('work/analysis/hot_spring_resilient_fixture_v1644')
REQUEST=original_supply.REQUEST

def preserve_natural_health(source):
    old='assert health==([60,49] if slot==0 else [25,19])'
    new='assert 0<health[0]<=([60,49] if slot==0 else [25,19])[0] and 0<=health[1]<=([60,49] if slot==0 else [25,19])[1]'
    assert source.count(old)==1
    return source.replace(old,new)

def apply_fixture(arm,raw,request):
    if request==REQUEST:
        source=preserve_natural_health(inspect.getsource(original_supply.apply_fixture))
        source=source.replace('if request!=REQUEST:return location.apply_fixture(arm,raw,request)','assert request==REQUEST')
        env={**original_supply.__dict__,'__file__':__file__,'ROM':ROM,'ROOT':ROOT}
    else:
        assert request==original_location.REQUEST
        source=preserve_natural_health(inspect.getsource(original_location.apply_fixture))
        old="read('work/analysis/fatigue_status_release_v1593/registered_release_verification.json')['ARM9_sha256']"
        assert source.count(old)==1;source=source.replace(old,"read('translations/hot_spring_notice_editorial_release_v1.json')['target_arm9_sha256']")
        env={**original_location.__dict__,'__file__':__file__,'ROM':ROM,'ROOT':ROOT}
    exec(compile(source,__file__,'exec'),env);after,proof=env['apply_fixture'](arm,raw,request)
    proof['naturally_changed_Hull_Crew_preserved_no_recruitment_or_healing']=True
    proof['guard_change_only_accepts_live_counts_within_original_initial_maxima']=True
    return after,proof

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_supplied_v1643_1637/frame_021700_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,original_location.REQUEST)
    assert sum(s['Hull_Crew_preserved'][1] for s in proof['ships'])==113
    ROOT.mkdir(parents=True);save(ROOT/'location_after_natural_crew_loss_preflight.json',{**proof,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Location preflight after original12-sailor loss:113 crew preserved,48 coordinates owned,all otherRAM exact. No healing,recruitment,skill/RNG or outcome edit.')
