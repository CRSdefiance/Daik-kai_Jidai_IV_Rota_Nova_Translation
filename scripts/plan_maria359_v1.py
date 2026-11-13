"""Permit one exact ordinary article wrap to keep the complete cure paragraph on one page."""
import inspect
import linecache
from scripts import plan_hodram_B211_B230_v2 as planner
from scripts import plan_scoped_clean_editorial_v1 as scoped
from scripts.source_locked_derivation_v5118 import checked_text

def main():
    source=checked_text(inspect.getsource(planner.main),{
        "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}":
        "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'} or (row['id']=='DK4_MES_B254_R0012' and row['english']==\"They say there's a wondrous medicine hidden somewhere around Africa that cures scurvy in an instant. Know anything about it?\" and retention.get('line_index')==2 and retention['exact_line']=='Africa that cures scurvy in an')",
    })
    name=__file__+'::one-source-current-English-bound-ordinary-article-retention'
    linecache.cache[name]=(len(source),None,source.splitlines(keepends=True),name)
    env={**planner.main.__globals__,'__file__':__file__}
    exec(compile(source,name,'exec'),env);planner.main=env['main'];scoped.main()

if __name__=='__main__':main()
