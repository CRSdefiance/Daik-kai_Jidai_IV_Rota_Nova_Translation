"""Admit only the exact reviewed ordinary soft wrap; preserve all source and native guards."""
import inspect
import linecache
from scripts import plan_hodram_B211_B230_v2 as planner
from scripts import plan_scoped_clean_editorial_v1 as scoped
from scripts.source_locked_derivation_v5118 import checked_text

def main():
    source=checked_text(inspect.getsource(planner.main),{
        "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}":
        "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'} or (row['id']=='SC3_B280_STYLE_8_90' and row['english']==\"Admiral, we should visit the clan guarding the map to the Proof as soon as possible. Their village is far northeast of China, I was told.\" and retention.get('line_index')==1 and retention['exact_line']=='guarding the map to the Proof as')",
    })
    name=__file__+'::one-exact-source-current-English-bound-complete-word-soft-wrap'
    linecache.cache[name]=(len(source),None,source.splitlines(keepends=True),name)
    env={**planner.main.__globals__,'__file__':__file__}
    exec(compile(source,name,'exec'),env);planner.main=env['main'];scoped.main()

if __name__=='__main__':main()
