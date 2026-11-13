"""Keep the mixed review's declared archive path on Help rows that inherit it."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

ORIGINAL = Path('scripts/complete_Help97_Rafael330_review_v1.py')
source = checked_text(ORIGINAL.read_text(encoding='utf-8'), {
    "        for row in doc['records']:\n            key = row['file_path'], row['id']":
        """        for original_row in doc['records']:
            row=deepcopy(original_row)
            assert row.get('file_path',doc['file_path'])==doc['file_path']
            row['file_path']=doc['file_path']
            key = row['file_path'], row['id']""",
    '[bp, cp, rp, sp, np, Path(__file__)]': '[bp, cp, rp, sp, np, ORIGINAL, Path(__file__)]',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-once-only-credit-explicit-Help-row-archive', 'exec'), globals())
