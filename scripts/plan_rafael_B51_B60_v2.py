"""Keep reviewed phrases intact andavoid treating sentence boundaries as phrase breaks."""
import linecache
from scripts import plan_rafael_B51_B60 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "    env={**previous.ENV,'PAGE_PHRASES':page_phrases,'ORDINARY':ordinary,":
        """    line_phrases={k:v.get('line_phrases',[]) for k,v in scoped.items()}
    adapter=checked_text(adapter,{
        'weak=int(not final and not ordinary and ((':'weak=int(not final and not ordinary and not terminal and ((',
        '    @cache':
            "    forbidden_stops=set()\\n    normalized=[norm(w) for w in words]\\n    for phrase in LINE_PHRASES.get(row['id'],[]):\\n        tokens=[norm(w) for w in phrase.split()]\\n        hits=[i for i in range(len(words)-len(tokens)+1) if normalized[i:i+len(tokens)]==tokens]\\n        assert len(tokens)>=2 and len(hits)==1\\n        forbidden_stops.update(range(hits[0]+1,hits[0]+len(tokens)))\\n    @cache",
        '            tail=solve(stop,line+1)':'            if stop in forbidden_stops:continue\\n            tail=solve(stop,line+1)',
    })
    env={**previous.ENV,'LINE_PHRASES':line_phrases,'PAGE_PHRASES':page_phrases,'ORDINARY':ordinary,""",
})
env={**previous.env,'qualify_source':previous.qualify_source,'__file__':__file__}
filename=__file__+'::same-native-geometry-record-bound-phrase-and-page-preferences'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
