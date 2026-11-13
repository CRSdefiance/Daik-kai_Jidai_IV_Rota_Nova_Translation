"""Extract the DS port-goods table and use existing commodity labels."""
import html
import json
import re
import textwrap
from pathlib import Path

root = Path(__file__).resolve().parents[2]
guide = root/'guide'
source = 'https://dekunobou-rotanova.seesaa.net/category/2333225-1.html'
page = (guide/'research/ds-trade-goods-source.html').read_bytes().decode('cp932')
tables = re.findall(r'<table\b.*?</table>', page, re.S)[1:8]
catalog = json.loads((root/'translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8-sig'))['records']
names = {row['Japanese']: row['English'] for row in catalog}
# Source typo: sapis lazuli. Preserve the source term and qualify the correction.
names['\u30b5\u30d4\u30b9\u30e9\u30ba\u30ea'] = names['\u30e9\u30d4\u30b9\u30e9\u30ba\u30ea']
ports = [
 ('Mediterranean','Lisbon|Seville|Ceuta|Madeira|Las Palmas|Valencia|Marseille|Genoa|Syracuse|Ragusa|Venice|Crete|Athens|Istanbul|Cyprus|Beirut|Alexandria|Tripoli|Tunis|Algiers'),
 ('North Sea','Nantes|Bristol|London|Bruges|Amsterdam|Hamburg|Oslo|Copenhagen|Lubeck|Stockholm|Riga'),
 ('Africa','Cape Verde|Sierra Leone|Sao Jorge|Sao Tome|Luanda|Cape Town|Sofala|Madagascar|Mozambique|Mombasa|Mogadishu'),
 ('Indian Ocean','Socotra|Aden|Muscat|Hormuz|Basra|Diu|Goa|Calicut|Ceylon|Madras|Masulipatam|Calcutta|Ava'),
 ('Southeast Asia','Aceh|Malacca|Palembang|Batavia|Banjarmasin|Surabaya|Makassar|Amboina|Ternate|Brunei|Gia Dinh|Manila'),
 ('East Asia','Macao|Quanzhou|Naha|Hangzhou|Yizhou|Seoul|Nagasaki|Osaka'),
 ('New World','Pernambuco|Cayenne|Maracaibo|San Juan|Santo Domingo|Jamaica|Portobelo|Trujillo|Merida|Veracruz|Havana|Pensacola'),
]
records = []
for table, (region, order) in zip(tables, ports):
    regional = []
    for row in re.findall(r'<tr>.*?</tr>', table, re.S)[1:]:
        cells = [html.unescape(re.sub('<[^>]+>', '', c)).strip()
                 for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)]
        if len(cells)==2:
            regional.append(dict(region=region, japanese_port=cells[0],
                                 japanese_goods=[], goods=[], source=source))
        assert cells[-1] in names, cells[-1]
        regional[-1]['japanese_goods'].append(cells[-1])
        regional[-1]['goods'].append(names[cells[-1]])
    order = order.split('|')
    assert len(order)==len(regional), region
    for port, record in zip(order, regional):
        record['port'] = port
    records.extend(regional)
assert len(records)==len({r['port'] for r in records})==87
(guide/'research/ds-trade-goods-reference.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

section = '''10.6  PORT GOODS DIRECTORY
------------------------------------------------------------------------
Use this directory to choose buying stops, then compare actual prices
in your save. These are the DS blog's listed products [S1G], with the
existing English commodity labels. Stock, quality, town development,
and your share can affect what you can actually buy. A listed product
does not promise a profit at the next port.

'''
for region, _ in ports:
    section += region.upper()+'\n\n'
    for row in (r for r in records if r['region']==region):
        section += textwrap.fill('; '.join(row['goods']), width=76,
                                 initial_indent=f"  {row['port']}: ",
                                 subsequent_indent='    ')+'\n'
    section+='\n'
section+='''Goa's last product is printed with a spelling error in the Japanese
source; Lapis Lazuli is the provisional reading used here. Check the
actual cargo label before making a delivery plan around it.

Do not substitute a seed or plant item for the corresponding cargo.
For example, a Pepper Plant in special inventory is different from
Pepper loaded into the holds. Quest quantities refer to the actual
goods named by the request. Pensacola is a developed story town;
its listed products are not starting stock in an undeveloped site.

'''
path = guide/'uncharted-waters-iv-rota-nova-ds-guide.txt'
text = path.read_text(encoding='utf-8')
end = text.index('='*72+'\n11. PORTS')
start = text.index('10.6  PORT GOODS') if '10.6  PORT GOODS' in text else end
text = text[:start]+section+text[end:]
assert all(len(line)<=80 for line in text.splitlines())
path.write_text(text, encoding='utf-8')
print(f'Added {len(records)} port entries and {sum(len(r["goods"]) for r in records)} product listings.')
