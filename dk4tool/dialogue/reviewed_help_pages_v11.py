"""Deck30 plus one previously credited Coerce amendment, using confirmed active skill names."""
from types import FunctionType
from dk4tool.dialogue import reviewed_help_pages_v10 as previous
from scripts.source_locked_derivation_v5118 import checked_text

original_wrap=previous.plan_articles.__globals__['wrap']
wrap_env={**original_wrap.__globals__}
wrap_env['STATS']={'Aim','Speech','Guile','Observe','Command','Swords','Vigor','Sailing','Survey','Finance'}
wrap_env['PHRASES']=[*wrap_env['PHRASES'],['at','least','200']]
active_wrap=FunctionType(original_wrap.__code__,wrap_env,original_wrap.__name__,original_wrap.__defaults__,original_wrap.__closure__)
SOURCE=checked_text(previous.SOURCE,{
    "topics!=set(range(103,133)) or len(original)!=202 or len(parent)!=217":
        "topics!=({33}|set(range(103,133))) or len(original)!=202 or len(parent)!=217",
    'Exact30 Deck-crew articles andcurrent217-topic/sentinel contract required':
        'Exact Deck30 plus Coerce33 amendment andcurrent217-topic/sentinel contract required',
})
env={**previous.plan_articles.__globals__,'wrap':active_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-source-links-bounds-and-inverse-with-active-stat-word-groups-and-one-explicit-amendment','exec'),env)
plan_articles=env['plan_articles']
