"""Reproduce the next60 Lil source reviews and complete natural corrections."""

import json
from pathlib import Path

from scripts.review_name_integration_v286 import main

if __name__ == '__main__':
    source = Path('translations/confirmed_name_editorial_v292_source.json')
    fixes = json.loads(source.read_text(encoding='utf-8'))['records']
    main(start=271, end=331, root=Path('work/analysis/name_source_review_v292'),
         fixes=fixes, editorial_path=Path('translations/confirmed_name_editorial_v292.json'),
         previous_reviewed=268, review_version=292, held_indices=())
