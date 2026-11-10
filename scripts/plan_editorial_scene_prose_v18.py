"""Keep reviewed closing clauses at page starts and record one grammatical QA retention."""
import inspect
import linecache
from copy import deepcopy

from scripts import plan_editorial_scene_prose_v17 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    "    env={**previous.ENV,'ORDINARY':ordinary,":
    """    adapter=checked_text(adapter,{
        '    @cache':
        "    clause=PAGE_PHRASES.get(row['id']);target=clause.split() if clause else []\\n    starts=[i for i in range(len(words)-len(target)+1) if words[i:i+len(target)]==target] if target else []\\n    assert not target or len(starts)==1\\n    page_start=starts[0] if starts else None\\n    @cache",
        '            tail=solve(stop,line+1)':
        '            if line==3 and not final and page_start is not None and stop!=page_start:continue\\n            tail=solve(stop,line+1)',
    })
    env={**previous.ENV,'PAGE_PHRASES':page_phrases,'ORDINARY':ordinary,""",
    "            rows.append(result)":
    """            retention=preferences['records'].get(row['id'],{}).get('QA_line_ending_retention')
            if retention:
                assert row['id']=='DK4_MES_B142_R0159'
                assert result['lines'][3]==retention['exact_line']
                warnings=[i for i in result['base_QA']['issues'] if i['severity']=='warning']
                assert len(warnings)==1 and warnings[0]['code']=='weak-line-ending'
                result['unmodified_base_QA']=deepcopy(result['base_QA'])
                for issue in result['base_QA']['issues']:
                    if issue['severity']=='warning':issue.update(severity='info',reviewed_retention_reason=retention['reason'])
            rows.append(result)""",
})

env = {**previous.main.__globals__, '__file__': __file__, 'deepcopy': deepcopy}
filename = __file__ + '::complete-clause-page-starts-and-grammatical-retention'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
exec(compile(source, filename, 'exec'), env)
main = env['main']

if __name__ == '__main__':
    main()
