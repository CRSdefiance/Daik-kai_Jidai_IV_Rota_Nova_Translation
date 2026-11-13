"""Reproduce the second source-review batch and complete correction previews."""

import json
from pathlib import Path

from scripts.review_name_integration_v286 import main

if __name__ == '__main__':
    source = Path('translations/confirmed_name_editorial_v287_source.json')
    fixes = json.loads(source.read_text(encoding='utf-8'))['records']
    main(start=100, end=160, root=Path('work/analysis/name_source_review_v287'),
         fixes=fixes, editorial_path=Path('translations/confirmed_name_editorial_v287.json'),
         previous_reviewed=99, review_version=287)
