"""Preserve both earlier plans; fix observed tails before running fresh native checks."""
from scripts import plan_refined_HELP_T103_T132_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'dk4tool.dialogue.reviewed_help_pages_v9':'dk4tool.dialogue.reviewed_help_pages_v10',
    'dk4tool/dialogue/reviewed_help_pages_v9.py':'dk4tool/dialogue/reviewed_help_pages_v10.py',
    'Shared_HELP_T103_T132_formatting_20261104/refined_v2':'Shared_HELP_T103_T132_formatting_20261104/refined_v3',
})
exec(compile(source,__file__+'::same-exact-prose-source-locks-with-punctuation-aware-tail-flow','exec'),globals())
