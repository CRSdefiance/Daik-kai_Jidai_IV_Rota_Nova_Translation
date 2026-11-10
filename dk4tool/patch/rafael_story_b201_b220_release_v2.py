"""Bind the original natural-dialogue validator in the mixed transaction qualification."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent=Path(__file__).with_name('rafael_story_b201_b220_release_v1.py')
source=checked_text(parent.read_text(encoding='utf-8'),{
    "env={**common.env,'__file__':__file__}":"env={**common.env,'validate':common.validate,'__file__':__file__}",
})
exec(compile(source,__file__+'::same-source-qualified-mixed-transaction-with-validator','exec'),globals())

