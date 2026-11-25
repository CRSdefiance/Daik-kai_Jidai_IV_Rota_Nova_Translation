"""Preserve Help67 prose with complete menu/range phrases and a continuous share prerequisite."""
from types import FunctionType
from dk4tool.dialogue import reviewed_help_pages_v13 as previous
from scripts.source_locked_derivation_v5118 import checked_text

original_wrap=previous.plan_articles.__globals__['wrap']
wrap_env={**original_wrap.__globals__}
wrap_env['PHRASES']=[*wrap_env['PHRASES'],['Trade','House'],['available','commands'],['auxiliary','masts'],
    ['Shared','Commands','menu'],['1','percent'],['100','percent'],['500','percent'],['1','to','5'],['Left','or','Right']]
active_wrap=FunctionType(original_wrap.__code__,wrap_env,original_wrap.__name__,original_wrap.__defaults__,original_wrap.__closure__)
SOURCE=checked_text(previous.SOURCE,{
    "{133:16,139:2,150:3,151:2,168:2}":"{133:16,139:2,150:2,151:2,168:2}",
})
env={**previous.plan_articles.__globals__,'wrap':active_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-seven-gates-source-links-ownership-andbounds-with-reviewed-phrase-groups','exec'),env)
plan_articles=env['plan_articles']
