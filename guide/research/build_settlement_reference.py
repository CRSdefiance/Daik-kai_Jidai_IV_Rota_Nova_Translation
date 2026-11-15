"""Build the settlement lookup from DS-source coordinates and patch answers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
answers = json.loads((REPO / 'translations/village_promised_words_manuscript_v1.json').read_text(encoding='utf-8'))
answer_map = {r['japanese'].strip(): r for r in answers['records'] if r['kind'] == 'ANSWER'}
# Coordinates/password associations: Dekuno DS village list.
# R/H/C facilities: mixed-version wiki, not independent DS confirmation.
rows = [
    ('Azores','アソーレス','N38','W28','テルセイラ','---'),
    ('Inuvik','イヌビク','N69','W136','オーロラ','RHC'),
    ('Ezo','エゾ','N42','E141','カムイ','RH-'),
    ('Karibib','カリビブ','S22','E14','カラハリ','R--'),
    ('Callao','カリャオ','S8','W78','タワンティンスウユ','---'),
    ('Guam','グアム','N15','E145','ラッテ','-HC'),
    ('Cod','コッド','N41','W70','シャンプレーン','RH-'),
    ('Korfu','コルフ','N60','E165','アバチャ','-H-'),
    ('Santa Barbara','サンタバーバラ','N34','W120','ヨセミテ','-H-'),
    ('Tahiti','タヒチ','S14','W147','ボラボラ','---'),
    ('Tiksi','チクシ','N72','E129','ツンドラ','R--'),
    ('Churchill','チャーチル','N58','W93','ベルーガ','R--'),
    ('Dikson','ディクソン','N73','E80','バイカル','RH-'),
    ('Narvik','ナルビク','N69','E18','スバルトイス','R-C'),
    ('Nome','ノーム','N68','W165','アラスカ','--C'),
    ('Perth','パース','S31','E115','ピナクルス','---'),
    ('Valparaiso','バルバライソ','S38','W73','モアイ','-H-'),
    ('Hawaii','ハワイ','N22','W159','キラウェア','---'),
    ('Forel','フォレル','N65','W39','エイリーク','-HC'),
    ('Hekla','ヘクラ','N63','W18','ヘクラ','-H-'),
    ('Montevideo','モンテビデオ','S38','W60','マゼラン','---'),
    ('Rio de Janeiro','リオデジャネイロ','S22','W43','ポンジアスカール','-H-'),
    ('Leveque','レバキュー','S16','E122','パーヌルル','-H-'),
    ('Wanganui','ワンガヌイ','S39','E174','モア','---'),
]
records = []
for name, jp, latitude, longitude, password, facilities in rows:
    matched = answer_map[password]
    records.append(dict(name=name, japanese_name=jp, latitude=latitude, longitude=longitude,
                        japanese_password=password, english_password=matched['english'],
                        answer_record=matched['id'], facilities=facilities,
                        coordinate_status='DS-source-reported', facility_status='Cross-platform-unverified'))
assert len(records) == len({r['answer_record'] for r in records}) == 24
(ROOT / 'research/ds-settlement-reference.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
table = '''========================================================================
11. PORTS, SETTLEMENTS, AND PASSWORDS                             [PORTS]
========================================================================

11.1  HIDDEN SETTLEMENTS
------------------------------------------------------------------------
Use the coordinates below when planning an exploration trip. N/S is
latitude; E/W is longitude. Check both letters before setting out:
crossing the right latitude in the wrong hemisphere will not help.
Names and coordinates follow the DS settlement list [S1V].

When the village chief asks for the promised words, use the exact
English answer listed here for the English patch. Capitalization and
spaces matter. After a successful answer, the new facilities open
on your next visit, not immediately. Leave and return. [G2]

  Settlement          Latitude  Longitude  English password
  --------------------------------------------------------------------
'''
for row in records:
    table += f"  {row['name']:20}{row['latitude']:10}{row['longitude']:11}{row['english_password']}\n"
table += '''
For an unmodified Japanese game, use the original Japanese words.
The accompanying glossary preserves those strings; the English
answers are not a promise that the Japanese release accepts Latin
input. Some settlement name spellings still need screen matching.

11.2  FACILITIES FOR VOYAGE PLANNING
------------------------------------------------------------------------
The wiki lists resupply at all settlements. Its repair, rest, and
recruitment entries are reproduced below as a provisional planning
reference. They still need DS confirmation; the wiki explicitly says
PSP rest facilities differ. Do not sail into a remote region relying
on a PSP inn list or an unconfirmed repair stop. [S3V]

R = ship repairs; H = rest/lodging; C = sailor recruitment.
A dash means the source does not list that service.

'''
for i in range(0, len(records), 2):
    left, right = records[i:i+2]
    table += f"  {left['name']:20}{left['facilities']}     {right['name']:20}{right['facilities']}\n"
table += '''
Keep enough supplies for the return trip. Reaching a settlement and
opening trade are separate milestones, so note which villages you
have actually revisited after giving the password.

The ordinary-port directory, settlement goods, and DS service checks
are still being compiled. This table covers the 24 password villages;
it is not a complete directory of every port in the game.

'''
guide = ROOT / 'uncharted-waters-iv-rota-nova-ds-guide.txt'
text = guide.read_text(encoding='utf-8')
if '11.3  ORDINARY PORT' in text:
    facilities_start = text.index('11.3  ORDINARY PORT')
    facilities_end = text.index('=' * 72 + '\n12. ITEMS', facilities_start)
    table += text[facilities_start:facilities_end]
rule = '=' * 72
start = text.index(rule+'\n11. PORTS')
end = text.index(rule+'\n12. ITEMS', start)
text = text[:start]+table+text[end:]
assert all(len(line) <= 80 for line in text.splitlines())
guide.write_text(text, encoding='utf-8')
print('Added 24 settlement coordinates, exact English answers, and qualified service flags.')
