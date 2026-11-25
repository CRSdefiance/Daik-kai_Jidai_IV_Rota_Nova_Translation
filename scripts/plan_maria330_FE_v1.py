"""Retain all original source/current guards and exact source-owned FE child ownership."""
import inspect
import linecache
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/plan_maria328_FE_v1.py').read_text(encoding='utf-8'),{
    'plan_maria328_v1 as previous':'plan_maria330_v1 as previous',
    'work/Maria_B73_B95_clean_20261109':'work/Maria_B96_B124_clean_20261109',
    'DK4_MES_B87_R0139':'DK4_MES_B116_R0051',
    '== 313':'== 328','== 328':'== 330','== 314':'== 329','== 329':'== 331',
})
env={'__name__':'qualified_maria330_FE_planner','__file__':__file__}
exec(compile(source,__file__+'::same-source-current-FE-owner-andfull-paragraph-guards330','exec'),env)
prior=env['main']
body=checked_text(inspect.getsource(prior),{
    "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}":"assert row['id']=='DK4_MES_B115_R0035'",
})
filename=__file__+'::same-planner-one-exact-complete-question-row-retention'
linecache.cache[filename]=(len(body),None,body.splitlines(keepends=True),filename)
scope={**prior.__globals__,'__file__':__file__}
exec(compile(body,filename,'exec'),scope)
main=scope['main']
if __name__=='__main__':main()
