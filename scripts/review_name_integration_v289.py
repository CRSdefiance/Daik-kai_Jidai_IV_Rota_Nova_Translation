"""Reproduce the final Rafael source-review batch, excluding held actor97."""

import json
from pathlib import Path

from scripts.review_name_integration_v286 import main

if __name__ == '__main__':
    source = Path('translations/confirmed_name_editorial_v289_source.json')
    fixes = json.loads(source.read_text(encoding='utf-8'))['records']
    main(start=160, end=226, root=Path('work/analysis/name_source_review_v289'),
         fixes=fixes, editorial_path=Path('translations/confirmed_name_editorial_v289.json'),
         previous_reviewed=159, review_version=289, held_indices=(216,))
