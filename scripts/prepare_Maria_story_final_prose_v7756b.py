"""Preserve the failed weak-of candidate; use the immediately established company pronoun."""
from copy import deepcopy
from pathlib import Path
from scripts import refine_Maria_story_final_prose_v7756 as previous
from scripts import plan_Maria_story_layout_v7733 as layout
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_story_final_prose_tools_v7756b')
ENGLISH="I hear their young leader has a strong sense of justice. They say she was furious and would never forgive FO."
if __name__=='__main__':
    assert not ROOT.exists() and not previous.OUTPUT.exists()
    doc=read(previous.PREVIOUS);row=deepcopy(next(r for r in doc['records'] if r['id']=='DK4_MES_B108_R0111'))
    antecedent=next(r for r in doc['records'] if r['id']=='DK4_MES_B108_R0107')
    assert antecedent['english']=="He fed the Argot Company false information, claiming FO was involved in dishonest trade."
    assert 'アーゴット商会' in antecedent['source_Japanese'] and 'アーゴット商会の総帥' in row['source_Japanese']
    env=dict(layout.ENV);adapter=checked_text(layout.ADAPTER,{'cost[0]+tiny,cost[1]+1,cost[2]+weak':'cost[0]+tiny+weak,cost[1]+1,cost[2]+weak'})
    exec(compile(adapter,__file__+'::unchanged-scoped-planner','exec'),env);row['english']='{SPEAKER:9B}'+ENGLISH.replace('FO','{MACRO:FO}')
    plan=env['plan'](row);qa=layout.base_qa(row,plan)
    assert plan['expected_native_pages']==1 and not any(i['severity'] in ['warning','error'] for i in qa['issues'])
    result=derive('scripts/refine_Maria_story_final_prose_v7756.py','scripts/refine_Maria_story_final_prose_v7756b.py',{
        'maria_story_final_prose_v7756':'maria_story_final_prose_v7756b',
        previous.CHANGES['DK4_MES_B108_R0111'][0]:ENGLISH,
        'The report frame They say scopes both the anger and categorical would never forgive.':
        "In this complete exchange, Their refers to the Argot Company explicitly named in R107, while FO is the listener's own company. The report frame They say scopes the anger and categorical would never forgive.",
        "Remove the redundant said she'd construction, whose verified v2 layout unnecessarily continued on a short second page.":
        "Use that clear pronoun and direct reported refusal to avoid repeating the company name and the redundant said she'd construction, whose verified v2 layout unnecessarily continued on a short second page.",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_whole_exchange_pronoun_final_prose.json',dict(
        derivation=result,source_antecedent_record=antecedent,reported_leader_source_record=row['id'],
        final_English=ENGLISH,automatic_plan=plan,base_QA=qa,
        no_weak_boundary_waiver_manual_break_orfact_omission=True,
        previous_failed_producer=str(Path(previous.__file__)),previous_failed_producer_sha256=sha(Path(previous.__file__).read_bytes()),
        previous_shortened_candidate_still_ended_line2_with_weak_of=True,
        failed_diagnostic_shell_quoting_attempt_changed_no_files=True,
        no_ROM_capture_orcredit_change=True,full_goal_complete=False))
    print('Frozen7756b:Their has explicit preceding ArgotCompany antecedent;whole reported meaning intact.One automatic page,no weak warnings.No waiver ormanual break.')
