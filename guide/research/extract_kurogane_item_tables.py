"""Repair optional-end-tag table rows without guessing Japanese item aliases."""
import json
from html.parser import HTMLParser
from pathlib import Path

class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None
    def finish_cell(self):
        if self.cell is not None and self.row is not None:
            self.row.append(' '.join(''.join(self.cell).split()))
        self.cell = None
    def finish_row(self):
        self.finish_cell()
        if self.row:
            self.rows.append(self.row)
        self.row = None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.finish_row()
            self.row = []
        elif tag in ('td', 'th'):
            self.finish_cell()
            self.cell = []
        elif tag == 'br' and self.cell is not None:
            self.cell.append(' ')
    def handle_endtag(self, tag):
        if tag in ('td', 'th'):
            self.finish_cell()
        elif tag == 'tr':
            self.finish_row()
    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

root = Path(__file__).resolve().parent
names = json.loads((root/'ds-item-bilingual-reference.json').read_text(encoding='utf-8'))['records']
by_japanese = {r['japanese']: r for r in names}
results, unmatched = [], []
for path in sorted(root.glob('kurogane-item-*.html')):
    if 'index' in path.name:
        continue
    parser = Rows()
    parser.feed(path.read_bytes().decode('euc_jp'))
    parser.finish_row()
    current = None
    for cells in parser.rows:
        if len(cells) >= 4 and cells[0] in by_japanese:
            item = by_japanese[cells[0]]
            current = dict(index=item['index'], english=item['english'],
                           japanese=cells[0], cells=cells, event_rows=[],
                           source='http://www.kurogane.biz/dk4/item/'+path.name[len('kurogane-item-'):-5]+'.php')
            results.append(current)
        elif len(cells) >= 4:
            unmatched.append(dict(file=path.name, cells=cells))
            current = None
        elif len(cells) == 1 and current is not None:
            current['event_rows'].append(cells[0])
    print(path.name, 'parsed', len(parser.rows), 'rows')
(root/'kurogane-item-matched-reference.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(root/'kurogane-item-unmatched-reference.json').write_text(json.dumps(unmatched, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Matched', len({r['index'] for r in results}), 'regular item identities; unmatched numerical rows:', len(unmatched))
