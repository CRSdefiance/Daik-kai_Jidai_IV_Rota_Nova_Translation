"""Run each complete two-choice object using the current Rafael native context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_editorial_two_choice_batch.py').read_text(encoding='utf-8'),{
    'scripts/check_editorial_two_choice_display.py':'scripts/check_rafael_two_choice_display.py',
})
exec(compile(source,__file__+'::same-two-choice-batch-explicit-Rafael','exec'),globals())
