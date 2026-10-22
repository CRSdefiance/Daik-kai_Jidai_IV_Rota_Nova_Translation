"""Inventory current manuscript citations; does not verify gameplay facts."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
text = (root / 'uncharted-waters-iv-rota-nova-ds-guide.txt').read_text(encoding='utf-8')
start = text.index('15. SOURCES')
end = text.index('16. REVISION HISTORY')
source_text = text[start:end]
pattern = r'(?:SP\d+|[SG]\d+)[A-Z]*'
markers = list(re.finditer(r'^\[(' + pattern + r')\](.*)$', source_text, re.M))
records = []
citations = re.findall(r'\[((?:SP\d+|[SG]\d+)[^\]]*)\]', text[:start])
for n, marker in enumerate(markers):
    stop = markers[n + 1].start() if n + 1 < len(markers) else len(source_text)
    definition = source_text[marker.end():stop].strip()
    definition = (marker.group(2).strip() + '\n' + definition).strip()
    code = marker.group(1)
    count = sum(code in re.findall(pattern, citation) for citation in citations)
    records.append({'code': code, 'references_in_player_text': count,
                    'definition': definition})
assert len(records) == len({row['code'] for row in records})
referenced = {code for citation in citations for code in re.findall(pattern, citation)}
assert referenced <= {row['code'] for row in records}
(root / 'research/source-coverage-audit.json').write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
lines = ['# Current source citation inventory', '',
         'Generated from the current TXT. Counts measure citation use, not independent corroboration or gameplay verification.', '',
         '| Code | Citation groups in player chapters |', '|---|---|']
lines += [f"| {row['code']} | {row['references_in_player_text']} |" for row in records]
(root / 'research/source-coverage-audit.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'{len(records)} unique definitions; {len(referenced)} source codes used in player chapters; all resolve.')
