"""Current-ROM full capture/reward control;no new24-event completion claims."""
from pathlib import Path

if __name__=='__main__':
    source = Path('scripts/verify_enemy_capture_replay_v1435.py').read_text(encoding='utf-8')
    for old,new in [
        ('dk4tool.patch.enemy_capture_editorial import current_entries','dk4tool.patch.ship_loss_surrender_editorial import current_entries'),
        ('scripts.native_enemy_capture_fixture_v1433 import apply_fixture,ROM','scripts.native_loss_surrender_fixture_v1460 import apply_fixture,ROM'),
        ("'work/analysis/enemy_capture_verified_v1435'","'work/analysis/loss_surrender_control_verified_v1465'"),
        ("'work/analysis/enemy_capture_replay_v1434'","'work/analysis/loss_surrender_control_v1461b'"),
        ('enemy_capture_v1434_1430','loss_surrender_control_v1461b_1456'),
        ('V1430 Enemy ship capture','V1456 Previous capture control'),
        ('work/analysis/enemy_capture_release_v1429/registered_release_verification.json','work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json'),
        ('scripts/run_enemy_capture_replay_v1434.py','scripts/run_loss_surrender_control_v1461b.py'),
        ('work/analysis/battle_victory_verified_v1410/actual_victory_and_return_verification.json','work/analysis/enemy_capture_verified_v1435b/actual_capture_and_return_verification.json'),
        ('whole_RGB_equal_to_V1404','whole_RGB_equal_to_V1430'),
        ('later10_whole_reward_cargo_and_sailing_screens_exact_to_V1404','later10_whole_reward_cargo_and_sailing_screens_exact_to_V1430')]:
        assert source.count(old)==1,(old,source.count(old))
        source = source.replace(old,new)
    old = "    assert fonts['ARM9_sha256']==sha(arm) and fonts['COMMON_sha256']==sha(common)"
    new = """    config = read('translations/ship_loss_surrender_editorial_release_v1.json')
    assert fonts['ARM9_sha256']==config['source_arm9_sha256'] and fonts['COMMON_sha256']==config['source_common_sha256']
    assert release['ARM9_sha256']==sha(arm) and release['COMMON_sha256']==sha(common)
    assert release['all24_loss_surrender_paragraphs_and3644_unselected_texts_preserved']"""
    assert source.count(old)==1
    source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
