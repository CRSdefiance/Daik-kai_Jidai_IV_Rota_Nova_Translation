"""Use full-width natural rows and page-aware bottom space, rather than sparse forced rows."""
import inspect
import linecache
from copy import deepcopy
from scripts import replan_hodram_B151_B170_visual_findings as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "        '            tail=solve(stop,line+1)':\n            '            if line==3 and not final and page_start is not None and stop!=page_start:continue\\n            tail=solve(stop,line+1)',":
    """        '    def solve(start,line):':
            '    def solve(start,line):\\n        if page_start is not None and start==page_start and 0<line<4:\\n            tail=solve(start,4)\\n            if tail is None:return None\\n            cost,breaks=tail\\n            return cost,(start,)*(4-line)+breaks',
        '            tail=solve(stop,line+1)':
            '            if page_start is not None and ((line<4 and start<page_start<stop) or (line>=4 and start<page_start)):continue\\n            tail=solve(stop,line+1)',
        "assert ' '.join(lines)==body;markup=":
            "assert ' '.join(s for s in lines if s)==body;markup=",
        'for a,b in zip(lines,lines[1:])':
            'for a,b in zip(lines,lines[1:]) if a.strip() and b.strip()', """,
    "            assert ' '.join(result['lines'])==row['english']":
        "            assert ' '.join(s for s in result['lines'] if s)==row['english']",
    "            result['scoped_visual_preference']=scoped[row['id']]":
        """            result['scoped_visual_preference']=scoped[row['id']]
            result['automatic_bottom_blank_rows']=sum(not s for s in result['lines'])
            if result['automatic_bottom_blank_rows']:
                assert row['id'] in clauses and result['lines'][4] and len(result['lines'])>4
                result['automatic_page_space_reason']='Retain natural full-width rows; leave unused space below the completed first-page thought so the next complete sentence or conditional clause begins page two. No word was shortened and no break was authored in the prose.'
            if row['id']=='DK4_MES_B157_R0024':
                warnings=[i for i in result['base_QA']['issues'] if i['severity']=='warning']
                assert warnings==[dict(severity='warning',code='weak-line-ending',message=\"line 2 ends with weak wrap word 'for.'\")]
                assert result['lines'][1]==\"he's good for.\"
                result['unmodified_base_QA']=deepcopy(result['base_QA'])
                for issue in result['base_QA']['issues']:
                    if issue['severity']=='warning':issue.update(severity='info',reviewed_retention_reason='The preceding Fighting is all and he is good for. complete a sentence about his only skill; for is terminal within that construction. The period closes the thought before Would not do as he was told. Preserve the raw lexical QA warning and this exact grammatical retention.')""",
})
env={**previous.main.__globals__,'__file__':__file__,'deepcopy':deepcopy}
filename=__file__+'::natural-rows-with-source-bound-complete-thought-page-starts'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
