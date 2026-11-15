"""Archive the completed capture family,exact patch references and terminal evidence."""
from pathlib import Path

if __name__=='__main__':
    source = Path('scripts/archive_battle_victory_v1412.py').read_text(encoding='utf-8')
    replacements = [
        ('battle_victory_archive_v1412','enemy_capture_archive_v1438'),
        ('V1412 Victory reports completed','V1438 Enemy ship capture completed'),
        ('20261022T0445599603149Z','20261022T0543468687909Z'),
        ('battle_victory_completion_v1411','enemy_capture_completion_v1437'),
        ('battle_victory_release_v1403','enemy_capture_release_v1429'),
        ('battle_victory_final_review_v1','enemy_capture_final_review_v1'),
        ('battle_victory_editorial_release_v1','enemy_capture_editorial_release_v1'),
        ('battle_victory_v1411_completion','enemy_capture_v1437_completion'),
        ('verify_battle_victory_release_v1405','verify_enemy_capture_release_v1431'),
        ('run_battle_victory_startup_v1406','run_enemy_capture_startup_v1432'),
        ('recheck_shop_formatting_v1407','recheck_shop_formatting_v1436'),
        ('native_battle_victory_fixture_v1408','native_enemy_capture_fixture_v1433'),
        ('run_battle_victory_replay_v1409','run_enemy_capture_replay_v1434'),
        ('verify_battle_victory_replay_v1410','verify_enemy_capture_replay_v1435b'),
        ('complete_battle_victory_v1411','complete_enemy_capture_v1437'),
        ('battle_victory_payload_v1396','enemy_capture_payload_v1423'),
        ('battle_victory_fonts_v1397b','enemy_capture_fonts_v1424'),
        ('battle_victory_copies_v1399','enemy_capture_copies_v1425'),
        ('battle_victory_escape_v1400','enemy_capture_escape_v1426'),
        ('battle_victory_native_review_v1401','enemy_capture_native_review_v1427'),
        ('battle_victory_replay_v1409','enemy_capture_replay_v1434'),
        ('battle_victory_verified_v1410','enemy_capture_verified_v1435b'),
        ('battle_victory_v1404_newgame','enemy_capture_v1430_newgame'),
        ('battle_victory_v1404_title','enemy_capture_v1430_title'),
        ('battle_victory_v1409_1404','enemy_capture_v1434_1430'),
        ('V1404 Victory reports','V1430 Enemy ship capture'),
        ('[1105,1266,1316,1344,1364,1404]','[1105,1266,1316,1344,1364,1404,1430]'),
        ('(1315,1403,8)','(1323,1411,8)'),('==1315','==1323'),('==1403','==1411'),
        ("'completed':1315,'source_prose':1403","'completed':1323,'source_prose':1411"),
        ('==241','==243'),('all241','all243'),('Victory8 completion archived','Capture8 completion archived')]
    for old,new in replacements:
        assert old in source,old
        source = source.replace(old,new)
    marker = "    for folder in ['work/analysis/enemy_capture_payload_v1423'"
    assert source.count(marker)==1
    source = source.replace(marker,"    paths.add(Path('scripts/verify_enemy_capture_replay_v1435.py'))\n"+marker)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
