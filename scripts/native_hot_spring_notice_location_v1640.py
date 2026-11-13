"""Same48-byte own-fleet location fixture,retargeted to V1637 hashes."""
import inspect
from pathlib import Path
from scripts import native_fatigue_region2_fixture_v1605 as previous
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import save
ROM=Path('out/all_routes_combined_v1637_candidate.nds')
ROOT=Path('work/analysis/hot_spring_notice_location_v1640')
REQUEST=previous.REQUEST
def apply_fixture(arm,raw,request):
    source=inspect.getsource(previous.apply_fixture)
    old="read('work/analysis/fatigue_status_release_v1593/registered_release_verification.json')['ARM9_sha256']"
    new="read('translations/hot_spring_notice_editorial_release_v1.json')['target_arm9_sha256']"
    assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'ROOT':ROOT};exec(compile(source,__file__,'exec'),env)
    return env['apply_fixture'](arm,raw,request)
if __name__=='__main__':
    assert not ROOT.exists()
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_search_pilot_v1587b_1578/frame_005000_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(arm,raw,REQUEST);ROOT.mkdir(parents=True);save(ROOT/'preflight.json',proof)
    print('V1637 fixture preflight:48 coordinate bytes only;all other4MiB,actors,stats,RNG and outcomes exact.')
