"""Keep scoped phrases on a page without forcing them to start the next page."""
import inspect
import linecache
from scripts import plan_editorial_scene_prose_v19 as previous
from scripts.plan_hodram_B211_B230_v1 import qualify_source
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    'if line==3 and not final and page_start is not None and stop!=page_start:continue':
        'if not final and (line+1)%4==0 and page_start is not None and page_start<stop<page_start+len(target):continue',
    "    env={**previous.ENV,'PAGE_PHRASES'":
        """    required_pairs={k:{tuple(p) for p in v.get('required_pairs',[])} for k,v in scoped.items()}
    adapter=checked_text(adapter,{'            tail=solve(stop,line+1)':
        '            if not final and (norm(words[stop-1]),norm(words[stop])) in REQUIRED_PAIRS.get(row["id"],set()):continue\\n            tail=solve(stop,line+1)'})
    env={**previous.ENV,'REQUIRED_PAIRS':required_pairs,'PAGE_PHRASES'""",
})
env={**previous.main.__globals__,'qualify_source':qualify_source,'__file__':__file__}
filename=__file__+'::same-native-guards-scoped-phrase-boundaries'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']

if __name__=='__main__':main()
