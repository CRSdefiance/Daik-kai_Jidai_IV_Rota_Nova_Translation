"""Reproduce the final62 Lil naming-source reviews and natural corrections."""

import json
from pathlib import Path

from scripts.review_name_integration_v286 import main

if __name__ == '__main__':
    source = Path('translations/confirmed_name_editorial_v293_source.json')
    fixes = json.loads(source.read_text(encoding='utf-8'))['records']
    main(start=331, end=393, root=Path('work/analysis/name_source_review_v293'),
         fixes=fixes, editorial_path=Path('translations/confirmed_name_editorial_v293.json'),
         previous_reviewed=328, review_version=293, held_indices=())
