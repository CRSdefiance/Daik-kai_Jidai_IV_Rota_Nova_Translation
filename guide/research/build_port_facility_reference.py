"""Build DS-source guild/shipyard port coverage, without guessing coordinates."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
groups = [
    ('Mediterranean', [('Lisbon','GST-'),('Seville','GSTR'),('Genoa','GSTR'),
     ('Athens','GSTR'),('Istanbul','GSTR'),('Alexandria','GSTR')],
     ['Syracuse','Venice','Tunis','Algiers']),
    ('North Sea', [('London','GSTR'),('Amsterdam','GST-'),('Hamburg','GSTR'),
     ('Stockholm','GSTR')], ['Bristol','Copenhagen','Lubeck']),
    ('Africa', [('Sao Jorge','GSTR'),('Sofala','GSTR')], ['Mozambique']),
    ('Indian Ocean', [('Basra','GSTR'),('Calicut','GSTR')], ['Aden','Muscat','Goa','Ceylon']),
    ('Southeast Asia', [('Malacca','GSTR'),('Batavia','GSTR')], ['Ternate']),
    ('East Asia', [('Hangzhou','GSTR'),('Seoul','GSTR'),('Osaka','GSTR')],
     ['Macao','Naha','Nagasaki']),
    ('New World', [('Veracruz','GSTR'),('Havana','GSTR'),('Pensacola','GS--')],
     ['Pernambuco','San Juan','Santo Domingo','Portobelo']),
]
other_towns = {
    'Mediterranean': ['Ceuta','Madeira','Las Palmas','Valencia','Marseille',
                     'Ragusa','Crete','Cyprus','Beirut','Tripoli'],
    'North Sea': ['Nantes','Bruges','Oslo','Riga'],
    'Africa': ['Cape Verde','Sierra Leone','Sao Tome','Luanda','Cape Town',
               'Madagascar','Mombasa','Mogadishu'],
    'Indian Ocean': ['Socotra','Hormuz','Diu','Madras','Masulipatam','Calcutta','Ava'],
    'Southeast Asia': ['Aceh','Palembang','Banjarmasin','Surabaya','Makassar',
                      'Amboina','Brunei','Gia Dinh','Manila'],
    'East Asia': ['Quanzhou','Yizhou'],
    'New World': ['Cayenne','Maracaibo','Jamaica','Trujillo','Merida'],
}
records = []
for region, full, yards in groups:
    records.extend(dict(region=region, name=name, services=services) for name,services in full)
    records.extend(dict(region=region, name=name, services='-S--') for name in yards)
    records.extend(dict(region=region, name=name, services='----')
                   for name in other_towns[region])
assert len(records) == len({r['name'] for r in records}) == 87
assert sum('G' in r['services'] for r in records) == 22
(root / 'research/ds-port-facility-reference.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')
section = '''11.3  ORDINARY PORT DIRECTORY
------------------------------------------------------------------------
These services follow the DS facility list [S1F]. G = Guild;
S = Shipyard; T = named tavern gift character; R = ruin/church site.
T does not mean that every other town lacks a tavern. R identifies
a listed site, not permission to enter it without its story lead.

  Region            Port                G S T R
  --------------------------------------------------------------------
'''
for row in records:
    section += f"  {row['region']:18}{row['name']:20}" + ' '.join(row['services'])+'\n'
section += '''
Use this table when planning repairs, refits, guild reports, and gift
visits. A nearby supply port is not necessarily a shipyard. Check the
services before loading a voyage with the assumption that you can
repair or buy a map at every destination.

Pensacola's services depend on town development. Other ruin access
and shop availability can depend on story progress too. The flags
are source-listed coverage, not a claim that every service has been
visited in a tested save.

This table covers all 87 ordinary ports in the DS facility list.
A ---- entry has none of these four services marked in that source;
it can still be a useful trading or supply stop. Story-built towns
outside this list, trade goods, and DS port coordinates need separate
coverage. Do not read these flags as a list of every available command.

'''
guide = root / 'uncharted-waters-iv-rota-nova-ds-guide.txt'
text = guide.read_text(encoding='utf-8')
end = text.index('11.4  TAVERN GIFTS') if '11.4  TAVERN GIFTS' in text else text.index('=' * 72 + '\n12. ITEMS')
start = text.index('11.3  ORDINARY PORTS') if '11.3  ORDINARY PORTS' in text else end
text = text[:start]+section+text[end:]
assert all(len(line) <= 80 for line in text.splitlines())
guide.write_text(text, encoding='utf-8')
print('Added 87 ordinary-port rows, including 22 guild towns.')
