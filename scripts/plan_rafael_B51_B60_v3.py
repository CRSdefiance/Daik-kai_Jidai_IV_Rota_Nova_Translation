"""Avoid sparse middle rows andqualify one exact complete phrasal-verb line ending."""
import linecache
from scripts import plan_rafael_B51_B60_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "    line_phrases={k:v.get('line_phrases',[]) for k,v in scoped.items()}":
        """    line_phrases={k:v.get('line_phrases',[]) for k,v in scoped.items()}
    adapter=checked_text(adapter,{
        '(line==0 and not final and length<=12 and not terminal)':'(not final and length<=12 and not terminal)',
    })""",
    "                assert row['id']=='DK4_MES_B142_R0159'":
        "                assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077']",
    "                assert result['lines'][3]==retention['exact_line']":
        "                assert result['lines'][0 if row['id']=='DK4_MES_B56_R0077' else 3]==retention['exact_line']",
})
env={**previous.env,'__file__':__file__}
filename=__file__+'::same-native-bounds-sparse-middle-penalty-and-exact-grammatical-retention'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
