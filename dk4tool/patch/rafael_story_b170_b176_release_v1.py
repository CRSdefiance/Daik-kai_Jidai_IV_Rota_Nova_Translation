"""Register 190 reviewed speeches with exact proof for the six native modal panels."""
from dk4tool.patch import rafael_story_b141_b160_release_v1 as common
from dk4tool.patch import rafael_story_b168_b169_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


qualification = checked_text(previous.qualification, {
    "conf['scoped_name_count']==10": "conf['scoped_name_count']==13",
    "conf['native_pages']==117": "conf['native_pages']==190",
    "conf['relative_cases']==125": "conf['relative_cases']==100",
    "conf['speech_count']==115": "conf['speech_count']==190",
    "conf['FE_count']==0": "conf['FE_count']==6",
    "len(lookup['records'])==115": "len(lookup['records'])==190",
    '(343,4,682)': '(343,14,672)',
    '==60': '==72',
    "    renderer=NdsImage.open(conf['final_dependency_ROM'])":
        "    staged={r['id'] for r in compiled.values() if r.get('source_staged_FE')}\n"
        "    require(staged=={'DK4_MES_B171_R0044','DK4_MES_B171_R0047','DK4_MES_B171_R0061'}\n"
        "        and actual['all_six_FE_pages_observed'] and actual['three_source_staged_heading_panels_observed'], 'complete source-staged patron coverage')\n"
        "    require(all(compiled[k]['complete_native_English_display']['planned_native_row_comparison']['complete_visible_row_origins_exact']\n"
        "        for k in staged),'exact patron heading row origins')\n"
        "    renderer=NdsImage.open(conf['final_dependency_ROM'])",
})
env = dict(common.env)
exec(compile(qualification, __file__+'::seven-block-exact-evidence', 'exec'), common.qualify_evidence.__globals__, env)
exec(compile(common.source, __file__+'::same-source-bound-transaction', 'exec'), env)
plan_release = env['plan_release']
