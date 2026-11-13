"""Use the already qualified complete-object label reader for every two-choice caption."""
from scripts.check_rafael_two_choice_batch import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts/check_rafael_two_choice_display.py':'scripts/check_rafael_two_choice_display_v2.py'})
exec(compile(source,__file__+'::same-menu-checks-complete-caption-reader','exec'),globals())
