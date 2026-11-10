"""Read-only comparison of a subject/verb phrase boundary; no changed prose/geometry/QA."""
from scripts import plan_Hodram_B47_B48_v8323 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read
ORIGINAL='''if not final and (norm(words[stop-1]),norm(words[stop]))==("governor's",'office'):continue'''
REPLACEMENT='''if not final and (norm(words[stop-1]),norm(words[stop])) in REQUIRED_COHERENT_PAIRS:continue'''
ADAPTER=checked_text(prior.ADAPTER,{ORIGINAL:REPLACEMENT})
REQUIRED_COHERENT_PAIRS={("governor's",'office'),('you','have')}
if __name__=='__main__':
    env={**prior.ENV,'REQUIRED_COHERENT_PAIRS':REQUIRED_COHERENT_PAIRS};exec(compile(ADAPTER,__file__+'::source-scoped-subject-verb','exec'),env)
    row=dict(read(prior.DOC)['records'][2]);row['english']='{SPEAKER:02}'+row['english'];plan=env['plan'](row)
    print(plan['lines']);print(plan['planning_cost']);print(prior.base_qa(row,plan)['issues'])
