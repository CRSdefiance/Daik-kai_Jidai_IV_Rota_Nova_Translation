"""Materialize the audited RNG-to-availability successor, including its explicit counter guard."""
import ast
from collections import Counter
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers

if __name__ == '__main__':
    source = Path('scripts/prepare_lil_B194_actual_audit_v5517.py')
    correction = Path('scripts/prepare_lil_B194_actual_audit_v5517b.py')
    tree = ast.parse(correction.read_text(encoding='utf-8'))
    changes = next(ast.literal_eval(n) for n in ast.walk(tree) if isinstance(n, ast.Dict))
    before = source.read_text(encoding='utf-8')
    after = before.replace(*next(iter(changes.items())))
    assert native_numbers(after) - native_numbers(before) == Counter({4294967295: 1, 1103515245: 1})
    assert not native_numbers(before) - native_numbers(after)
    print(derive(str(source), 'scripts/prepare_lil_B194_actual_audit_v5517c.py', changes))
