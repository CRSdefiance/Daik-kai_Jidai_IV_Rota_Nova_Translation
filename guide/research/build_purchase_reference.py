"""Add source-listed purchases matched against the native DS item catalog."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
items = json.loads((root / 'research/ds-static-item-reference.json').read_text(encoding='utf-8-sig'))
by_name = {r['name']: r for r in items}
entries = [
    ('Lisbon', 'Travels of Marco Polo', 10000), ('Lisbon', 'Sextant', 2500),
    ('Seville', "Hannibal's Campaigns", 10000), ('Seville', 'Compass', 5500),
    ('Genoa', 'Da Vinci Anatomy', 20000), ('Genoa', 'Stained-Glass Flower', 2000),
    ('Athens', "Horace's Poems", 1500), ('Athens', "Sappho's Poems", 5000),
    ('Athens', 'Cave Village Map', 1500), ('Istanbul', 'Golden Cutlass', 30000),
    ('Istanbul', 'Arabian Nights', 2000), ('London', 'Loom', 11000),
    ('London', 'Gallic Wars', 8000), ('Amsterdam', 'Rainbow Marbles', 1500),
    ('Amsterdam', 'Stone Circle Map', 500), ('Hamburg', 'Pocket Watch', 5000),
    ('Hamburg', 'Arena Map', 700), ('Stockholm', 'Snow-Silk Robe', 5000),
    ('Stockholm', 'Supreme Loupe', 10000), ('Sofala', 'Royal Mosque Map', 2000),
    ('Calicut', 'Golden Temple Map', 3000), ('Hangzhou', "Hua Tuo's Tonic", 12000),
    ('Seoul', 'Black Glass Bowl', 7000), ('Veracruz', 'Ancient City Map', 1000),
]
entries.extend([
    ('Alexandria', "Alexander's Campaigns", 12000),
    ('Alexandria', 'Bread Millstone', 1000),
    ('Sao Jorge', 'Gauze Mask', 2500), ('Sao Jorge', 'Sahara Map', 1500),
    ('Sofala', 'Beehive', 1200), ('Sofala', 'Illustrated Bible', 20000),
    ('Basra', 'Embroidered Carpet', 7500), ('Basra', 'Mughal Empire Map', 1000),
    ('Calicut', 'Pepper Plant', 8500), ('Malacca', 'Pearl Oyster', 9000),
    ('Malacca', 'Mangosteen Seeds', 3000), ('Batavia', 'Banana Tree', 2400),
    ('Batavia', 'Clove Plant', 8600), ('Batavia', 'Ancient Temple Map', 1000),
    ('Hangzhou', 'Gunpowder Manual', 50000), ('Hangzhou', 'Royal Tomb Map', 2500),
    ('Seoul', 'Silkworms', 7700), ('Seoul', 'Beijing Map', 1000),
    ('Osaka', 'War Drum', 2500), ('Osaka', 'Kinokuniya Abacus', 20000),
    ('Veracruz', 'Cacao Seeds', 6800), ('Havana', 'Pimento Plant', 6500),
    ('Havana', 'Tobacco Plant', 7200), ('Havana', 'Aztec Pictorial Map', 2000),
])
port_order = list(dict.fromkeys(port for port, _, _ in entries))
entries.sort(key=lambda row: port_order.index(row[0]))
assert len(entries) == 48
records = []
for port, name, price in entries:
    item = by_name[name]
    assert item['base_value'] == price, f'Native/source price mismatch: {name}'
    records.append(dict(port=port, name=name, price=price, index=item['index'],
                        source='https://dekunobou-rotanova.seesaa.net/article/29158147.html',
                        status='DS-source-reported; native base value matches'))
(root / 'research/ds-purchase-reference.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')
section = '''12.4  PURCHASES TO PLAN AROUND
------------------------------------------------------------------------
The town and listed price come from the DS purchase table [S1P].
Names match the regular English item catalog, and these prices also
match its base values [G1]. Live stock and transaction prices have
not been checked for every entry. Keep funds for the voyage too.

  Town          Item                           Listed gold
  --------------------------------------------------------------------
'''
for row in records:
    section += f"  {row['port']:14}{row['name']:34}{row['price']:>8,}\n"
section += '''
A gift belongs to a particular tavern character; buying it does not
automatically open every ruin in the region. Follow the relevant
protagonist's event before giving away an object. A map is also a
separate inventory item, not ordinary cargo space.

These 48 purchases cover the complete DS-source shop table. Treat
local products such as seeds and plants as special inventory items;
they are different from barrels of trade goods requested by a quest.
Event-dependent stock and unlock conditions need separate checks.

'''
guide = root / 'uncharted-waters-iv-rota-nova-ds-guide.txt'
text = guide.read_text(encoding='utf-8')
boundary = '=' * 72 + '\n13. SECRETS'
end = text.index('12.5  ') if '12.5  ' in text else text.index(boundary)
start = text.index('12.4  PURCHASES TO PLAN AROUND') if '12.4  PURCHASES TO PLAN AROUND' in text else end
text = text[:start] + section + text[end:]
assert all(len(line) <= 80 for line in text.splitlines())
guide.write_text(text, encoding='utf-8')
print('Added 48 purchases; all source-listed prices match native item base values.')
