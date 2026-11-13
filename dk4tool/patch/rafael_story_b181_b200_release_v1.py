"""Register the complete 384-record Rafael story and town transaction."""
from dk4tool.patch import rafael_story_b141_b160_release_v1 as common
from dk4tool.patch import rafael_story_b168_b169_release_v1 as earlier
from scripts.source_locked_derivation_v5118 import checked_text

qualification = checked_text(earlier.qualification, {
    "conf['scoped_name_count']==10": "conf['scoped_name_count']==29",
    "conf['native_pages']==117": "conf['native_pages']==384",
    "conf['relative_cases']==125": "conf['relative_cases']==210",
    "conf['speech_count']==115": "conf['speech_count']==384",
    "conf['FE_count']==0": "conf['FE_count']==27",
    "len(lookup['records'])==115": "len(lookup['records'])==384",
    '(343,4,682)': '(343,40,646)',
    '==60': '==148',
    "    renderer=NdsImage.open(conf['final_dependency_ROM'])":
        "    fe={r['id'] for r in speech if r['kind']=='system-FE'}\n"
        "    require(fe==set(actual['observed_FE_source_IDs'])<=observed and actual['all27_FE_bodies_observed']\n"
        "        and actual['all13_town_forecasts_observed'], 'all FE bodies and town forecasts observed')\n"
        "    renderer=NdsImage.open(conf['final_dependency_ROM'])",
})
env = dict(common.env)
exec(compile(qualification, __file__+'::complete-story-town-evidence', 'exec'), common.qualify_evidence.__globals__, env)
exec(compile(common.source, __file__+'::same-source-bound-transaction', 'exec'), env)
plan_release = env['plan_release']
