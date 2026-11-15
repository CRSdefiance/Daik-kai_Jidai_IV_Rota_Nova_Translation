"""Fresh formatting after two contextual wording fixes and observed phrase-continuity findings."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/plan_HELP_T103_T132_v1.py').read_text(encoding='utf-8'),{
    'dk4tool.dialogue.reviewed_help_pages_v8':'dk4tool.dialogue.reviewed_help_pages_v9',
    'dk4tool/dialogue/reviewed_help_pages_v8.py':'dk4tool/dialogue/reviewed_help_pages_v9.py',
    "ROOT=Path('work/analysis/Shared_HELP_T103_T132_formatting_20261104')":"ROOT=Path('work/analysis/Shared_HELP_T103_T132_formatting_20261104/refined_v2')",
    'whole_article_comparisons_v3.json':'whole_article_comparisons_v4.json',
    'proposed_revisions=12,justified_retentions=18':'proposed_revisions=13,justified_retentions=17',
    'all18_retained_bodies_word_exact=True':'all17_retained_bodies_word_exact=True',
})
exec(compile(source,__file__+'::same-source-lock-and-prose-preserving-normalization-with-final-prose-and-reviewed-phrase-flow','exec'),globals())
