"""Resolve observed one-word tails without changing any Deck tutorial prose."""
import inspect
from dk4tool.dialogue import reviewed_help_pages_v9 as previous
from scripts.source_locked_derivation_v5118 import checked_text

matcher=checked_text(inspect.getsource(previous.matches),{
    "a.rstrip('.,;:')in[b,b+'s']":"a.rstrip('.,;:')in[b.rstrip('.,;:'),b.rstrip('.,;:')+'s']",
})
env={**previous.protected_wrap.__globals__}
exec(compile(matcher,__file__+'::same-whole-phrase-match-with-terminal-punctuation','exec'),env)
env['PHRASES']=[*previous.PHRASES,['useful','for','exploring'],['useful','for','trade'],['repair','costs','at','shipyards'],
    ['improve','their','mood'],['at','twice','the','price'],['the',"city's",'surrender'],['a','mast'],['high','Aim']]
wrapper=checked_text(inspect.getsource(previous.protected_wrap),{
    "        groups.append(tokens[at:at+size]);at+=size":
        "        if at+3<len(tokens)and tokens[at:at+3]==['takes','part','in']and isinstance(tokens[at+3],dict)and tokens[at+3]['label']=='duels.':size=4\n        groups.append(tokens[at:at+size]);at+=size",
})
exec(compile(wrapper,__file__+'::same-prose-preserving-group-wrapper-with-complete-duel-clause','exec'),env)
SOURCE=previous.SOURCE
env.update(previous.plan_articles.__globals__)
env.update(wrap=env['protected_wrap'],__file__=__file__)
exec(compile(SOURCE,__file__+'::same-source-links-native-bounds-and-inverse-with-reviewed-tail-fixes','exec'),env)
plan_articles=env['plan_articles']
