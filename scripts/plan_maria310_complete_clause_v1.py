"""Use the proven exact-clause page start for this batch's byte-bound closing clauses."""
from scripts import plan_maria310_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous.source,{
    'source=checked_text(inspect.getsource(planner.main),{':
        """source=checked_text(inspect.getsource(planner.main),{
    'if not final and (line+1)%4==0 and page_start is not None and page_start<stop<page_start+len(target):continue':
        'if not final and (line+1)%4==0 and page_start is not None and stop!=page_start:continue',""",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-geometry-guards-source-bound-exact-closing-clause-starts','exec'),globals())
