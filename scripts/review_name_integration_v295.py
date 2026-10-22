"""Reproduce the four formerly held source/presentation/name corrections."""

import json
from pathlib import Path

from scripts.review_name_integration_v286 import main

if __name__ == '__main__':
    source = Path('translations/confirmed_name_editorial_v295_source.json')
    fixes = json.loads(source.read_text(encoding='utf-8'))['records']
    mapping = json.loads(Path('translations/held_presentation_state_v295.json').read_text(encoding='utf-8'))
    scoped = {(row['file_path'], row['id']): row for row in mapping['records']}
    main(root=Path('work/analysis/name_source_review_v295'), fixes=fixes,
         editorial_path=Path('translations/confirmed_name_editorial_v295.json'),
         previous_reviewed=440, review_version=295, held_indices=(),
         indices=[14, 216, 240, 406], presentation_map=scoped)
