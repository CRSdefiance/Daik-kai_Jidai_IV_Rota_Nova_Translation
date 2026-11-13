"""Pure37-article release with38 native pages,17 observed pages andsource-bound Refit controls."""
from dk4tool.patch import town_help23_release_v1 as previous
from dk4tool.dialogue.reviewed_help_pages_v5 import plan_articles
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(previous.SOURCE,{
 'dk4-town-help23-release-v1':'dk4-shipyard-help37-release-v1',
 "conf['record_count']==23":"conf['record_count']==37",
 'list(range(21,44))':'list(range(44,81))',
 '==(19,4)':'==(27,10)',
 "native['native_pages']==28 and native['complete_articles']==23":"native['native_pages']==38 and native['complete_articles']==37",
 "visual['all28_complete_pages_approved'] and visual['all_seven_refined_sheets_directly_viewed']":"visual['all38_complete_pages_approved'] and visual['all_ten_sheets_directly_viewed']",
 "actual['actual_pages']==15 and actual['actual_articles']==10 and actual['offline_only_pages']==13 and len(actual['offline_only_article_IDs'])==13":
 "actual['actual_pages']==17 and actual['actual_articles']==16 and actual['offline_only_pages']==21 and len(actual['offline_only_article_IDs'])==21",
 "len(actual['original_forward_back_andL_R_history_returns'])==6":"len(actual['original_forward_back_andL_R_history_returns'])==7",
 "actual_visual['all15_observed_pages_approved'] and actual_visual['all_four_actual_sheets_directly_viewed']":"actual_visual['all17_observed_pages_approved'] and actual_visual['all_five_actual_sheets_directly_viewed']",
 'len(actual_cases)==15':'len(actual_cases)==17',
 'len(native_cases)==28':'len(native_cases)==38',
 "sum(r['offline_only'] for r in doc['records'])==13":"sum(r['offline_only'] for r in doc['records'])==21",
 "    changed=[]":
 """    control_row=next(r for r in doc['records'] if r['topic_id']==51)
    control_path=Path(control_row['native_control_binding']);control=load(control_path)
    require(sha(control_path.read_bytes())==control_row['native_control_binding_sha256'],'Refit51 control proof identity')
    require(control['current_ARM9_sha256']==conf['final_runtime_ARM9_sha256'],'Refit51 same native control runtime')
    require(control['source51_symbol_mapping']==dict(circle='A',triangle='X'),'Refit51 original controls mapping')
    require('Press A' in control_row['english'] and 'press X' in control_row['english'],'Refit51 reviewed physical instructions')
    changed=[]""",
 "[dict(article=22,page_ids=[22,212]),dict(article=25,page_ids=[25,213]),dict(article=37,page_ids=[37,204]),dict(article=38,page_ids=[38,214]),dict(article=39,page_ids=[39,215])]":
 "[dict(article=66,page_ids=[66,216])]",
 'articles=23,pages=28,revisions=19,retentions=4,actual_pages=15,offline_only_pages=13':
 'articles=37,pages=38,revisions=27,retentions=10,actual_pages=17,offline_only_pages=21',
 'HELP212_to216_with_unused205_andall_unowned_data_preserved=True':'HELP216_to217_with_all_unowned_data_preserved=True',
})
env={**previous.plan_release.__globals__,'plan_articles':plan_articles,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-complete-source-individual-native-actual-inverse-andatomic-commit-with-bound-Refit-controls','exec'),env)
plan_release=env['plan_release']
