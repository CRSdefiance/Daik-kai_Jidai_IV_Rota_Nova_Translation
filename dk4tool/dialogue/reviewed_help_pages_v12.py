"""Preserve v11 formatting and fail closed on the six confirmed active-skill instructions."""
from dk4tool.dialogue import reviewed_help_pages_v11 as previous
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(previous.SOURCE,{
    "        title,english=row['heading'],row['english']":
        """        title,english=row['heading'],row['english']
        expected_active={33:['Speech score','at least 200'],116:['Vigor 130'],117:['Speech 160'],118:['Guile 120'],121:['Speech 100'],126:['Vigor 30']}
        if topic in expected_active and any(term not in english for term in expected_active[topic]):
            raise ValueError('Confirmed active skill label or unchanged threshold differs')""",
})
env={**previous.plan_articles.__globals__,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-pages-with-explicit-current-active-skill-prose-contract','exec'),env)
plan_articles=env['plan_articles']
