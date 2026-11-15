"""Pure reviewed sailing Help integration; all22 pages have explicit native and actual proofs."""
from dk4tool.patch import town_help23_release_v1 as previous
from dk4tool.dialogue.reviewed_help_pages_v7 import plan_articles
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(previous.SOURCE,{
    'dk4-town-help23-release-v1':'dk4-sea-help22-release-v1',
    "conf['record_count']==23":"conf['record_count']==22",
    'list(range(21,44))':'list(range(81,103))',
    '==(19,4)':'==(17,5)',
    "native['native_pages']==28 and native['complete_articles']==23":"native['native_pages']==22 and native['complete_articles']==22",
    "visual['all28_complete_pages_approved'] and visual['all_seven_refined_sheets_directly_viewed']":"visual['all22_complete_pages_approved'] and visual['all_six_sheets_directly_viewed']",
    "actual['actual_pages']==15 and actual['actual_articles']==10 and actual['offline_only_pages']==13 and len(actual['offline_only_article_IDs'])==13":
        "actual['actual_pages']==22 and actual['actual_articles']==22 and actual['offline_only_pages']==0 and len(actual['offline_only_article_IDs'])==0",
    "len(actual['original_forward_back_andL_R_history_returns'])==6":"len(actual['original_forward_back_andL_R_history_returns'])==17",
    "actual_visual['all15_observed_pages_approved'] and actual_visual['all_four_actual_sheets_directly_viewed']":"actual_visual['all22_observed_pages_approved'] and actual_visual['all_six_actual_sheets_directly_viewed']",
    'len(actual_cases)==15':'len(actual_cases)==22',
    'len(native_cases)==28':'len(native_cases)==22',
    "sum(r['offline_only'] for r in doc['records'])==13":"sum(r['offline_only'] for r in doc['records'])==0",
    "[dict(article=22,page_ids=[22,212]),dict(article=25,page_ids=[25,213]),dict(article=37,page_ids=[37,204]),dict(article=38,page_ids=[38,214]),dict(article=39,page_ids=[39,215])]":"[]",
    'articles=23,pages=28,revisions=19,retentions=4,actual_pages=15,offline_only_pages=13':'articles=22,pages=22,revisions=17,retentions=5,actual_pages=22,offline_only_pages=0',
    'HELP212_to216_with_unused205_andall_unowned_data_preserved=True':'HELP217_topics_andall_unowned_data_preserved=True',
})
env={**previous.plan_release.__globals__,'plan_articles':plan_articles,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-source-individual-gates-native-actual-and-complete-inverse-for22','exec'),env)
plan_release=env['plan_release']
