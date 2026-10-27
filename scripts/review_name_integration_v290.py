"""Hodram source review using its actual player state, with one held preamble."""

import json
from pathlib import Path

from scripts.review_name_integration_v286 import main

if __name__ == '__main__':
    source = Path('translations/confirmed_name_editorial_v290_source.json')
    fixes = json.loads(source.read_text(encoding='utf-8'))['records']
    main(start=226, end=241, root=Path('work/analysis/name_source_review_v290'),
         fixes=fixes, editorial_path=Path('translations/confirmed_name_editorial_v290.json'),
         previous_reviewed=224, review_version=290, held_indices=(240,))
