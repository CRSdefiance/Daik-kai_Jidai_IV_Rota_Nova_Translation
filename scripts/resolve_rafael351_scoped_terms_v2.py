"""Keep all individual decisions; choice captions have no dialogue macro-count map."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

ORIGINAL = Path('scripts/resolve_rafael351_scoped_terms_v1.py')
source = checked_text(ORIGINAL.read_text(encoding='utf-8'), {
    "row['source_macros'].items()": "row.get('source_macros',{}).items()",
    '[PARENT,IDENTITY,TERMS,Path(__file__)]': '[PARENT,IDENTITY,TERMS,ORIGINAL,Path(__file__)]',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-prose-review-source-bound-choice-captions-have-no-dialogue-macros','exec'),globals())
