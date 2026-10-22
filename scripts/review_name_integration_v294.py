"""Maria naming-source review with her own macro state and one held preamble."""

import json
from pathlib import Path

from scripts.review_name_integration_v286 import main

if __name__ == '__main__':
    source = Path('translations/confirmed_name_editorial_v294_source.json')
    fixes = json.loads(source.read_text(encoding='utf-8'))['records']
    main(start=393, end=444, root=Path('work/analysis/name_source_review_v294'),
         fixes=fixes, editorial_path=Path('translations/confirmed_name_editorial_v294.json'),
         previous_reviewed=390, review_version=294, held_indices=(406,))
