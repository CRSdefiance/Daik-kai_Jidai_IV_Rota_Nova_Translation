"""Allow one exact reviewed ordinary preposition wrap that removes a needless page."""
import linecache
from scripts import plan_hodram_B211_B230_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "{'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}":
        "{'DK4_MES_B142_R0159','DK4_MES_B201_R0074','DK4_MES_B229_R0036'}",
})
env={**previous.main.__globals__,'__file__':__file__}
filename=__file__+'::same-planner-one-exact-reviewed-ordinary-wrap'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']

if __name__=='__main__':main()
