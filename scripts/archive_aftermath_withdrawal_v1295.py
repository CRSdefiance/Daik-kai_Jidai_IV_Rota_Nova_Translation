"""Archive withdrawal source/gameplay evidence using the audited copy-only helper."""
import inspect
from pathlib import Path
from scripts import archive_aftermath_city_v1289 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    replacements = [
        ('== 1288','== 1296'),
        ('translations/battle_aftermath_city_defense_final_review_v1.json',
         'translations/battle_aftermath_withdrawal_final_review_v1.json'),
        ('docs/aftermath_city_v1288_completion.md','docs/aftermath_withdrawal_v1294_completion.md'),
        ("r'_v128[0-9]", "r'_v129[0-9]"),
        ("r'_v128[0-8]", "r'_v129[0-4]"),
        ("['aftermath_navigation_v1281_1266', 'aftermath_city_v1283b_1266', 'aftermath_city_v1286_1266']",
         "['aftermath_town_v1291_1266']"),
        ('Guide screenshots/V1266 City defense','Guide screenshots/V1266 Town withdrawal'),
        ("'complete':1288", "'complete':1296"),
        ("'aftermath_complete':28", "'aftermath_complete':36"),
        ("'aftermath_pending':47", "'aftermath_pending':39"),
        ('all3 terminal capture/RAM sets','the terminal capture/RAM set'),
    ]
    for old,new in replacements:
        assert source.count(old) == 1,(old,source.count(old))
        source = source.replace(old,new)
    env = {**previous.__dict__, '__file__':__file__,
        'DEST':Path('E:/Rota Nova translations/Editorial review/V1295 Town withdrawal verification'),
        'ROOT':Path('work/analysis/aftermath_withdrawal_archive_v1295')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
