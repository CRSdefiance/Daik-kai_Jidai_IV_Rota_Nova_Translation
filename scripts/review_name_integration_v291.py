"""First Lil naming-source batch using its actual three-character player name."""

import json
from pathlib import Path

from scripts.review_name_integration_v286 import main

if __name__ == '__main__':
    source = Path('translations/confirmed_name_editorial_v291_source.json')
    fixes = json.loads(source.read_text(encoding='utf-8'))['records']
    main(start=241, end=271, root=Path('work/analysis/name_source_review_v291'),
         fixes=fixes, editorial_path=Path('translations/confirmed_name_editorial_v291.json'),
         previous_reviewed=238, review_version=291, held_indices=())
