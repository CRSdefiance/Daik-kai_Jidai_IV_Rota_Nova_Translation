"""Source-locked Deck/crew Help30 planner using the validated native width and phrase wrapper."""
from dk4tool.dialogue import reviewed_help_pages_v7 as previous
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(previous.SOURCE,{
    "topics!=set(range(81,103)) or len(original)!=202 or len(parent)!=217":
        "topics!=set(range(103,133)) or len(original)!=202 or len(parent)!=217",
    'Exact22 sea-battle-password articles andcurrent217-topic/sentinel contract required':
        'Exact30 Deck-crew articles andcurrent217-topic/sentinel contract required',
})
env={**previous.plan_articles.__globals__,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-full-source-links-bounds-and-unowned-inverse-for30-Deck-articles','exec'),env)
plan_articles=env['plan_articles']
