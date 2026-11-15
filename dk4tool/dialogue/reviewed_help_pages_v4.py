"""Source-locked Shipyard-to-Ruins Help planner,with atomic native button phrases."""
import inspect
from dk4tool.dialogue import reviewed_help_pages_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

wrapper=checked_text(inspect.getsource(previous.protected_wrap),{
 "if tokens[index:index+2]==['press','B.']:":
 "if index+1<len(tokens) and isinstance(tokens[index],str) and tokens[index].lower()=='press' and tokens[index+1] in ['A','A.','B','B.','X','X.','Y','Y.']:",
 "merged.append('press B.');index+=2":"merged.append(tokens[index]+' '+tokens[index+1]);index+=2",
})
wrapenv={**previous.protected_wrap.__globals__}
exec(compile(wrapper,__file__+'::same-wrap-with-whole-native-button-phrases','exec'),wrapenv)
protected_wrap=wrapenv['protected_wrap']
SOURCE=checked_text(previous.SOURCE,{
 "topics!=set(range(21,44)) or len(original)!=202 or len(parent)!=212":
 "topics!=set(range(44,81)) or len(original)!=202 or len(parent)!=216",
 'Exact23 town articles andcurrent212-topic/sentinel contract required':
 'Exact37 shipyard-to-ruins articles andcurrent216-topic/sentinel contract required',
 "protected_plain_English_phrases=['press B.']":
 "protected_plain_English_phrases=['press A','press B','press X','press Y']",
})
env={**previous.plan_articles.__globals__,'wrap':protected_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-source-links-native-bounds-all-unowned-pages-and-inverse-for37-help-articles','exec'),env)
plan_articles=env['plan_articles']
