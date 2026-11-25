"""Keep the fleet definition and operating-fund rules in source-bound logical paragraphs."""
from dk4tool.dialogue import reviewed_help_pages_v4 as previous
from scripts.source_locked_derivation_v5118 import checked_text

wrapper=checked_text(previous.wrapper,{
 "        if index+1<len(tokens) and isinstance(tokens[index],str) and tokens[index].lower()=='press' and tokens[index+1] in ['A','A.','B','B.','X','X.','Y','Y.']:":
 "        if tokens[index:index+3]==['at','least','150.']:\n            merged.append('at least 150.');index+=3\n        elif index+1<len(tokens) and isinstance(tokens[index],str) and tokens[index].lower()=='press' and tokens[index+1] in ['A','A.','B','B.','X','X.','Y','Y.']:",
})
wrapenv={**previous.protected_wrap.__globals__}
exec(compile(wrapper,__file__+'::same-wrap-with-complete-reviewed-threshold-phrase','exec'),wrapenv)
protected_wrap=wrapenv['protected_wrap']
SOURCE=checked_text(previous.SOURCE,{
 "if topic not in [22,25,37,38,39] or len(sections)!=2 or not row.get('semantic_section_reason'):":
 "if topic!=66 or len(sections)!=2 or not row.get('semantic_section_reason'):",
 'Only reviewed source-tip,letter-instruction,investment andcontract-condition paragraphs aresectioned':
 'Only the source-bound regional-fleet definition andoperating-funds paragraphs aresectioned',
 "markers={22:['【！】','主計長'],25:['紹介状','総督府'],37:['１口につき','投資すると武装度が上がります'],38:['100％','ただし'],39:['100％','ただし']}":
 "markers={66:['委任方針','運用資金','金貨10万枚']}",
 "protected_plain_English_phrases=['press A','press B','press X','press Y']":
 "protected_plain_English_phrases=['press A','press B','press X','press Y','at least 150.']",
})
env={**previous.plan_articles.__globals__,'wrap':protected_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-source-ownership-width-andinverse-with-source66-paragraphs','exec'),env)
plan_articles=env['plan_articles']
