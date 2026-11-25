"""Pure town Help23 release;all28 pages checked with15 observed/13 offline-only explicit."""
import inspect
from dk4tool.patch import early_help23_release_v1 as previous
from dk4tool.dialogue.reviewed_help_pages_v3 import plan_articles as town_plan
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(inspect.getsource(previous.plan_release),{
    'dk4-early-help23-release-v1':'dk4-town-help23-release-v1',
    "list(range(21))+[181,184]":"list(range(21,44))",
    "==(16,7)":"==(19,4)",
    "native['native_pages']==25":"native['native_pages']==28",
    "visual['all25_complete_pages_approved'] and visual['all_seven_readable_sheets_directly_viewed']":
        "visual['all28_complete_pages_approved'] and visual['all_seven_refined_sheets_directly_viewed']",
    "actual['all25_complete_actual_pages_andnative_child_targets_pass'] and actual['actual_pages']==25 and actual['actual_articles']==23":
        "actual['all_selected_complete_actual_pages_andnative_child_targets_pass'] and actual['actual_pages']==15 and actual['actual_articles']==10 and actual['offline_only_pages']==13 and len(actual['offline_only_article_IDs'])==13",
    "len(actual['original_forward_back_andL_R_history_returns'])==3":"len(actual['original_forward_back_andL_R_history_returns'])==6",
    "actual_visual['all25_complete_pages_approved'] and actual_visual['all_seven_readable_actual_sheets_directly_viewed']":
        "actual_visual['all15_observed_pages_approved'] and actual_visual['all_four_actual_sheets_directly_viewed']",
    "    changed=[]":
        """    expected_actual={p['block'] for r in doc['records'] for p in r['planned_stored_pages'] if 'actual_frame' in p}
    require(set(actual_cases)==expected_actual and len(actual_cases)==15,'individual actual membership')
    require(set(native_cases)=={p['topic_id'] for p in compiled['pages']} and len(native_cases)==28,'individual complete native membership')
    require(sum(r['offline_only'] for r in doc['records'])==13,'explicit offline-only articles')
    changed=[]""",
    "            require(ref['target_archive_sha256']==sha(encoded) and ref['actual_frame']==actual_cases[t]['frame'],'individual actual reference')\n            require(actual_cases[t]['all_first_internal_final_glyphs_andblank_gaps_exact'],'all complete actual characters')":
        """            require(ref['target_archive_sha256']==sha(encoded),'individual target archive')
            if t in actual_cases:
                require(ref['actual_frame']==actual_cases[t]['frame'] and actual_cases[t]['all_first_internal_final_glyphs_andblank_gaps_exact'],'individual complete actual reference')
            else:
                require('actual_frame' not in ref and row['offline_only'],'offline page has no fabricated actual reference')""",
    "[dict(article=7,page_ids=[7,202]),dict(article=9,page_ids=[9,211])]":
        "[dict(article=22,page_ids=[22,212]),dict(article=25,page_ids=[25,213]),dict(article=37,page_ids=[37,204]),dict(article=38,page_ids=[38,214]),dict(article=39,page_ids=[39,215])]",
    'articles=23,pages=25,revisions=16,retentions=7':'articles=23,pages=28,revisions=19,retentions=4,actual_pages=15,offline_only_pages=13',
    'HELP211_to212_with_existing202_preserved=True':'HELP212_to216_with_unused205_andall_unowned_data_preserved=True',
})
env={**previous.plan_release.__globals__,'plan_articles':town_plan,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-source-gates-inverses-andwhole-NDS-commit-with-honest-partial-actual-coverage','exec'),env)
plan_release=env['plan_release']
