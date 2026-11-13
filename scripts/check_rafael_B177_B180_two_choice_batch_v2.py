"""Run all four original menu providers with the exact B177 legacy slot allowance."""
from scripts import check_rafael_B177_B180_two_choice_batch_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    'scripts/check_rafael_B177_B180_two_choice_display_v1.py': 'scripts/check_rafael_B177_B180_two_choice_display_v2.py',
})
exec(compile(source, __file__+'::same-four-two-choice-batch-exact-B177-current-padding', 'exec'), globals())
