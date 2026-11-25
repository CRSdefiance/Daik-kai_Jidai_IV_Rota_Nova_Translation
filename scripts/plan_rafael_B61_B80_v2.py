"""One exact article-boundary retention uses full width without changing prose or geometry."""
import linecache
from scripts import plan_rafael_B61_B80 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077']":
        "assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077','DK4_MES_B69_R0143']",
    "result['lines'][0 if row['id']=='DK4_MES_B56_R0077' else 3]":
        "result['lines'][retention.get('line_index',0 if row['id']=='DK4_MES_B56_R0077' else 3)]",
})
env={**previous.env,'__file__':__file__}
filename=__file__+'::same-native-planner-one-exact-grammatical-soft-boundary'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']

if __name__=='__main__':main()
