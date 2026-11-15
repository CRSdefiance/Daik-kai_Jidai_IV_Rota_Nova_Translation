"""Pack body and caption sheets with normalized preview paths."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent = Path(__file__).with_name('pack_rafael_B201_B220_review_sheets_v1.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    "pic = read_image(page['preview'],page['preview_sha256'])":
        "pic = read_image(Path(page['preview']),page['preview_sha256'])",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-complete-review-sheets-path-normalization','exec'),globals())

