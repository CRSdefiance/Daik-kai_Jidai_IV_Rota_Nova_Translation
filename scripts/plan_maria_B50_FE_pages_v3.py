"""Add the exact grammatical noun-phrase ending to the existing scoped retention guard."""
import linecache
from scripts import plan_maria_B50_FE_pages_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous.source,{
    "{'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}":
        "{'DK4_MES_B142_R0159','DK4_MES_B201_R0074','DK4_MES_B50_R0057'}",
})
env={**previous.env,'__file__':__file__}
filename=__file__+'::same-native-width-guards-exact-source-bound-grammatical-ending'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
