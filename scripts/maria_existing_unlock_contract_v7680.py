"""Require the exact existing system-only fixture; never grant earned-unlock credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
HISTORICAL=Path('work/analysis/maria_intro_v684/unlock_manifest.json')
FIXTURE_SHA='295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949'
def validate_fixture(manifest):
    historical=read(HISTORICAL);fixture=read(manifest)
    for key,value in historical.items():
        if key not in ['production_ROM','production_ROM_sha256','current_test_scope']:
            assert fixture[key]==value,(key,'changed historical fixture')
    donor=Path(fixture['original_donor']).read_bytes();test=Path(fixture['fixture_save']).read_bytes()
    assert sha(donor)==fixture['original_donor_sha256'] and sha(test)==fixture['fixture_save_sha256']==FIXTURE_SHA
    changes=[dict(offset=i,before=a,after=b) for i,(a,b) in enumerate(zip(donor,test)) if a!=b]
    assert len(donor)==len(test) and changes==historical['changes']
    assert fixture['only_system_low_four_bits_and_original_checksum_changed'] and fixture['all_six_route_save_slots_and_footer_unchanged'] and not fixture['earned_unlock_verified']
    assert sha(Path(fixture['production_ROM']).read_bytes())==fixture['production_ROM_sha256']
    return fixture
def validate_capture(report):
    fixtures=report['synthetic_gallery_fixtures'];assert len(fixtures)==1
    one=fixtures[0];path=Path(one['preloaded_save_manifest'])
    assert sha(path.read_bytes())==one['manifest_sha256'] and one['synthetic_gallery_fixture'] and not one['earned_unlock_verified']
    fixture=validate_fixture(path);battery=report['battery_save_preloaded']
    assert Path(battery['source'])==Path(fixture['fixture_save']) and battery['source_sha256']==FIXTURE_SHA
    assert battery['copied_byte_exact_before_cold_boot'] and not battery['savestate_loaded']
    assert report['ROM_sha256']==fixture['production_ROM_sha256'] and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_gallery_fixtures')
    return fixture
