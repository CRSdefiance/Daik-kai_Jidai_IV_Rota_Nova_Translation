"""Keep the exact-row reviewed infinitive boundary while preserving every base QA result."""
import linecache
from scripts import plan_rafael_B141_B160_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077']":
        "assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077','DK4_MES_B142_R0005']",
    "result['lines'][0 if row['id']=='DK4_MES_B56_R0077' else 3]":
        "result['lines'][0 if row['id'] in ['DK4_MES_B56_R0077','DK4_MES_B142_R0005'] else 3]",
})
env={**previous.env,'__file__':__file__}
filename=__file__+'::same-native-plan-and-one-exact-source-bound-reviewed-infinitive-wrap'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
