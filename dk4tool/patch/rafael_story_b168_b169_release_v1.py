"""Register the 115 source-bound ordinary dialogue decisions and verified display."""
from dk4tool.patch import rafael_story_b141_b160_release_v1 as common
from dk4tool.patch import rafael_story_b161_b165_release_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text


qualification = checked_text(previous.qualification, {
    "conf['scoped_name_count']==8": "conf['scoped_name_count']==10",
    "conf['native_pages']==68": "conf['native_pages']==117",
    "conf['relative_cases']==100": "conf['relative_cases']==125",
    "conf['speech_count']==67": "conf['speech_count']==115",
    "conf['FE_count']==1": "conf['FE_count']==0",
    "len(lookup['records'])==67": "len(lookup['records'])==115",
    '(343,10,676)': '(343,4,682)',
    '==56': '==60',
})
env = dict(common.env)
exec(compile(qualification, __file__+'::exact-two-block-evidence', 'exec'), common.qualify_evidence.__globals__, env)
exec(compile(common.source, __file__+'::same-source-bound-transaction', 'exec'), env)
plan_release = env['plan_release']
