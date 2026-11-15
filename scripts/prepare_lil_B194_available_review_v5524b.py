"""Audit the two explicitly added original getters and full-RAM readonly guards."""
import ast
import re
from collections import Counter
from pathlib import Path
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__ == '__main__':
    producer = Path('scripts/prepare_lil_B194_available_review_v5524.py')
    tree = ast.parse(producer.read_text(encoding='utf-8'))
    changes = next(ast.literal_eval(n) for n in ast.walk(tree) if isinstance(n, ast.Dict))
    path = Path('scripts/review_lil_B194_default_actual_v5522.py')
    source = path.read_text(encoding='utf-8')
    assert all(k in source for k in changes)
    target = re.sub('|'.join(re.escape(k) for k in sorted(changes, key=len, reverse=True)), lambda m: changes[m.group(0)], source)
    assert native_numbers(target) - native_numbers(source) == Counter({0x7E958: 1, 0x7DB14: 1, 0x400000: 2, 0x02000000: 2})
    assert not native_numbers(source) - native_numbers(target)
    print(derive(str(path), 'scripts/review_lil_B194_available_actual_v5524.py', changes))
