"""Refine observed phrase tails without changing Help prose,source guards or continuation ownership."""
from types import FunctionType
from dk4tool.dialogue import reviewed_help_pages_v15 as previous

original_wrap=previous.plan_articles.__globals__['wrap']
wrap_env={**original_wrap.__globals__}
wrap_env['PHRASES']=[*wrap_env['PHRASES'],['change','their','job'],['Press','Left','or','Right'],
    ['when','attacked'],['in','a','crisis'],['such','as','sailing'],['It','is'],['It','suits'],['this','faction'],['better','relations']]
refined_wrap=FunctionType(original_wrap.__code__,wrap_env,original_wrap.__name__,original_wrap.__defaults__,original_wrap.__closure__)
SOURCE=previous.SOURCE
env={**previous.plan_articles.__globals__,'wrap':refined_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-complete-prose-guards-with-directly-observed-tail-refinements','exec'),env)
plan_articles=env['plan_articles']
