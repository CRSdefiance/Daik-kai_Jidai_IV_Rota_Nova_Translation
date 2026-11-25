"""Read-only checks for the guide's layout, index and saved data coverage."""
import json
import re
import unicodedata
from pathlib import Path

root = Path(__file__).resolve().parents[1]
text = (root / 'uncharted-waters-iv-rota-nova-ds-guide.txt').read_text(encoding='utf-8')
long_lines = [i for i, line in enumerate(text.splitlines(), 1) if len(line) > 80]
assert not long_lines, f'Lines wider than 80 columns: {long_lines}'
codes = ('ABOUT', 'VERSION', 'START', 'RAF01', 'CREW01', 'MISS01', 'SYSTEMS',
         'ROUTES', 'SHIPS', 'TRADE', 'PORTS', 'ITEMS', 'SECRETS', 'NAMES', 'SOURCES', 'HISTORY')
for code in codes:
    assert len(re.findall(r'\[' + code + r'\]', text)) == 2, f'Index mismatch: {code}'
steps = [int(n) for n in re.findall(r'^R(\d+)  ', text, re.M)]
assert steps == list(range(1, max(steps) + 1)), 'Route step gap or duplicate'
hodram_steps = [int(n) for n in re.findall(r'^H(\d+)  ', text, re.M)]
assert hodram_steps == list(range(1, max(hodram_steps) + 1)), 'Hodram step gap or duplicate'
lil_steps = [int(n) for n in re.findall(r'^L(\d+)  ', text, re.M)]
assert lil_steps == list(range(1, max(lil_steps) + 1)), 'Lil step gap or duplicate'
maria_steps = [int(n) for n in re.findall(r'^M(\d+)  ', text, re.M)]
assert maria_steps == list(range(1, max(maria_steps) + 1)), 'Maria step gap or duplicate'
items = json.loads((root / 'research/ds-static-item-reference.json').read_text(encoding='utf-8-sig'))
assert len(items) == 188 and {r['index'] for r in items} == set(range(188))
for item in items:
    assert item['name'] in text, f"Missing item: {item['name']}"
assert next(r for r in items if r['index'] == 148)['category'] == 'Proof'
settlements = json.loads((root / 'research/ds-settlement-reference.json').read_text(encoding='utf-8'))
assert len(settlements) == len({r['answer_record'] for r in settlements}) == 24
for village in settlements:
    assert village['english_password'] in text, f"Missing answer: {village['name']}"
    assert re.search(re.escape(village['name']) + r'\s+' + re.escape(village['japanese_password']), text), f"Missing Japanese answer: {village['name']}"
    assert re.fullmatch(r'[NS]\d+', village['latitude'])
    assert re.fullmatch(r'[EW]\d+', village['longitude'])
purchases = json.loads((root / 'research/ds-purchase-reference.json').read_text(encoding='utf-8'))
ports = json.loads((root / 'research/ds-port-facility-reference.json').read_text(encoding='utf-8'))
assert len(ports) == len({r['name'] for r in ports}) == 87
assert sum('G' in r['services'] for r in ports) == 22
for port in ports:
    assert port['name'] in text
    assert re.fullmatch(r'[G-][S-][T-][R-]', port['services'])
assert len(purchases) == 48 and len({r['index'] for r in purchases}) == len(purchases)
items_by_index = {r['index']: r for r in items}
for purchase in purchases:
    assert purchase['name'] in text
    assert purchase['price'] == items_by_index[purchase['index']]['base_value']
discoveries = json.loads((root / 'research/ds-discovery-reference.json').read_text(encoding='utf-8'))
assert len(discoveries) == len({r['index'] for r in discoveries}) == 76
section = text[text.index('12.3  DISCOVERY'):text.index('12.4  PURCHASES')]
for discovery in discoveries:
    assert discovery['name'] == items_by_index[discovery['index']]['name']
    pattern = (re.escape(discovery['name']) + r'\s+' +
               re.escape(discovery['latitude']) + r'\s+' +
               re.escape(discovery['longitude']) + r'\s+')
    assert re.search(pattern, section), discovery['name']
gifts = json.loads((root / 'research/ds-tavern-gift-reference.json').read_text(encoding='utf-8'))
assert len(gifts) == len({r['port'] for r in gifts}) == 21
section = text[text.index('11.4  TAVERN GIFTS'):text.index('12. ITEMS')]
for gift in gifts:
    assert gift['gift'] == items_by_index[gift['index']]['name']
    assert re.search(re.escape(gift['port']) + r'\s+' + re.escape(gift['person']) +
                     r'\s+' + re.escape(gift['gift']), section), gift['port']
source_pattern = r'(?:SP\d+|[SG]\d+)[A-Z]*'
source_section = text[text.index('15. SOURCES'):text.index('16. REVISION HISTORY')]
definitions = re.findall(r'^\[(' + source_pattern + r')\]', source_section, re.M)
assert len(definitions) == len(set(definitions)), 'Duplicate source definition'
for citation in re.findall(r'\[((?:SP\d+|[SG]\d+)[^\]]*)\]', text):
    for source in re.findall(source_pattern, citation):
        assert source in definitions, f'Missing reference: {source}'
print(f'PASS: 80-column layout, {len(codes)} section links, R01-R{max(steps):02}, '
      '188 regular items, 24 settlement answers, and source definitions.')
print('These checks cover document consistency, not gameplay verification or full-guide completion.')
print(f'Hodram steps H01-H{max(hodram_steps):02} are continuous.')
print(f'Lil steps L01-L{max(lil_steps):02} are continuous.')
print(f'Maria steps M01-M{max(maria_steps):02} are continuous.')
print(f'{len(purchases)} purchase entries match native base values.')
print(f'{len(ports)} source-listed ordinary ports, including 22 guild towns, are present.')
print(f'{len(discoveries)} discovery rows match saved names and coordinates.')
print(f'{len(gifts)} tavern gift pairings match the item catalog.')

# Resolve numerical prose links against real subsection headings.
headings = set(re.findall(r'^(\d{2}(?:\.\d+)?)(?=\s|\. )', text, re.M))
for reference in re.findall(r'\bsection (\d{2}(?:\.\d+)?)', text):
    assert reference in headings, f'Missing section target: {reference}'
terms = json.loads((root / 'research/player-terminology-reference.json').read_text(encoding='utf-8'))
glossary = text[text.index('14. NAMES'):text.index('15. SOURCES')]
for term in terms:
    assert term['english'] + ' / ' + term['japanese'] in glossary
print(f'{len(terms)} bilingual terms and numerical section links are present.')
goods = json.loads((root / 'research/ds-trade-goods-reference.json').read_text(encoding='utf-8'))
assert len(goods) == len({r['port'] for r in goods}) == 87
assert {r['port'] for r in goods} == {r['name'] for r in ports}
section = text[text.index('10.6  PORT GOODS'):text.index('11. PORTS')]
for row in goods:
    assert row['port'] + ':' in section
    for good in row['goods']:
        assert good in section, good
print('87 port-goods entries cover the facility directory; 326 product listings.')
display_wide = [n for n, line in enumerate(text.splitlines(), 1)
                if sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1
                       for c in line) > 80]
assert not display_wide, f'Overwide display-cell lines: {display_wide}'
assert '\ufffd' not in text, 'Unicode replacement character in guide'
print('UTF-8 text and 80-cell Japanese/English display widths pass.')
navigation = json.loads((root / 'research/task-navigation-reference.json').read_text(encoding='utf-8'))
assert len(navigation) == 36
real_headings = set(re.findall(r'^(\d{2}(?:\.\d+)?)(?:  |\. [A-Z])', text, re.M))
for target in navigation:
    assert target['section'] in real_headings, target['section']
    assert re.search(re.escape(target['task']) + r'\s+' + re.escape(target['section']), text)
print(f'{len(navigation)} task-index destinations resolve to real section headings.')
subsections = re.findall(r'^(\d{2}\.\d+)  [A-Z]', text, re.M)
assert len(subsections) == len(set(subsections)), 'Duplicate subsection heading'
print('All numbered subsection headings are unique.')
bilingual = json.loads((root / 'research/ds-item-bilingual-reference.json').read_text(encoding='utf-8'))['records']
assert len(bilingual) == 188 and {r['index'] for r in bilingual} == set(range(188))
section = text[text.index('14.5  JAPANESE ITEM'):text.index('15. SOURCES')]
for row in bilingual:
    assert row['english'] == items_by_index[row['index']]['name']
    assert row['english'] + ' / ' + row['japanese'] in section
print('188 original Japanese item names match the English lookup.')

# Acquisition references must target an existing section, not merely a name.
acquisition = json.loads((root / 'research/regular-item-acquisition-index.json').read_text(encoding='utf-8'))
assert len(acquisition) == 188 and {r['index'] for r in acquisition} == set(range(188))
for row in acquisition:
    assert row['name'] == items_by_index[row['index']]['name']
    assert row['section'] in real_headings, row['section']
    assert re.search(r'^' + f"{row['index']:03}" + r'  ' + re.escape(row['name']) + r'$', text, re.M)
print('188 acquisition-index entries have valid section targets.')

# Check actual item identity in each target subsection.
section_markers = list(re.finditer(r'^(\d{2}\.\d+)  [A-Z].*$', text, re.M))
section_bodies = {}
for n, marker in enumerate(section_markers):
    end = section_markers[n + 1].start() if n + 1 < len(section_markers) else len(text)
    section_bodies[marker.group(1)] = text[marker.start():end]
for row in acquisition:
    assert row['name'].casefold() in section_bodies[row['section']].casefold(), f"Acquisition target lacks item: {row['name']} -> {row['section']}"
print('188 acquisition targets contain their actual item names.')

# Check the values in the player tables, not just presence of names.
characters = json.loads((root / 'research/ds-character-attribute-reference.json').read_text(encoding='utf-8'))['records']
assert len(characters) == 28
for row in characters:
    values = [row['attributes'][key] for key in
              ('Stamina', 'Agility', 'Charm', 'Wits', 'Spirit', 'Luck')]
    pattern = r'^  ' + re.escape(row['name']) + ''.join(r'\s+' + str(value) for value in values) + r'\s*$'
    assert re.search(pattern, section_bodies['05.1'], re.M), row['name']
ships = json.loads((root / 'research/ds-ship-catalog-reference.json').read_text(encoding='utf-8'))['records']
assert len(ships) == 34
for row in ships:
    pattern = (r'^  ' + re.escape(row['name']) + r'\s+' + row['size'] +
               r'\s+' + str(row['hull']) + r'\s+' + f"{row['base_value']:,}" + r'\s*$')
    assert re.search(pattern, section_bodies['09.19'], re.M), row['name']
coordinates = json.loads((root / 'research/port-coordinate-reference.json').read_text(encoding='utf-8'))
assert len(coordinates) == len({row['name'] for row in coordinates}) == 90
for row in coordinates:
    pattern = re.escape(row['name']) + r'\s+' + row['latitude'] + r'\s+' + row['longitude']
    assert re.search(pattern, section_bodies['11.7']), row['name']
print('28 character attribute rows, 34 hull/base-price rows and 90 port coordinates match saved references.')

# Regional map identities must appear in their actual route chapters.
# The seven English identities follow original Japanese item records;
# source-qualified handoff visits remain in proof-map-handoff-reference.json.
map_chapters = {
    'Thales Paper Map': ('08.3', '08.15', '08.34'),
    'Cleobulus Cloth Map': ('08.11', '08.20', '08.33'),
    'Periander Stone Map': ('08.5', '08.16', '08.30'),
    'Solon Leaf Map': ('08.6', '08.18', '08.32'),
    'Bias Coin Map': ('08.9', '08.22', '08.28'),
    'Chiron Bamboo Map': ('08.9', '08.23', '08.27'),
    'Pittacus Blade Map': ('08.10', '08.17', '08.31'),
}
for map_name, chapters in map_chapters.items():
    assert map_name in {row['english'] for row in bilingual}
    for chapter in chapters:
        assert map_name in ' '.join(section_bodies[chapter].split()), f'{chapter} lacks {map_name}'
assert "King's Tomb Map" not in text, 'Use translated Royal Tomb Map label'
assert re.search(r'Royal Tomb Map.*2,500', section_bodies['12.4'])
assert 'Royal Tomb Map at Hangzhou' in section_bodies['08.25']
print('21 captain/region proof-map chapter identities and Royal Tomb Map naming/price pass.')
