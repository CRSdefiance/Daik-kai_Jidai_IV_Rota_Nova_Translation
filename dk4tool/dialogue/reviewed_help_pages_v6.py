"""Source-locked sea/battle/password Help planner;preserve native button punctuation asone phrase."""
from dk4tool.dialogue import reviewed_help_pages_v5 as previous
from scripts.source_locked_derivation_v5118 import checked_text

wrapper=checked_text(previous.wrapper,{
 "tokens[index+1] in ['A','A.','B','B.','X','X.','Y','Y.']":
 "isinstance(tokens[index+1],str) and tokens[index+1].rstrip('.,;:') in ['A','B','X','Y','L','R']",
})
wrapenv={**previous.protected_wrap.__globals__}
exec(compile(wrapper,__file__+'::same-wrap-with-native-button-punctuation','exec'),wrapenv)
protected_wrap=wrapenv['protected_wrap']
SOURCE=checked_text(previous.SOURCE,{
 "topics!=set(range(44,81)) or len(original)!=202 or len(parent)!=216":
 "topics!=set(range(81,103)) or len(original)!=202 or len(parent)!=217",
 'Exact37 shipyard-to-ruins articles andcurrent216-topic/sentinel contract required':
 'Exact22 sea-battle-password articles andcurrent217-topic/sentinel contract required',
})
env={**previous.plan_articles.__globals__,'wrap':protected_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-complete-source-links-width-andunowned-inverse-for22-sea-help-articles','exec'),env)
plan_articles=env['plan_articles']
