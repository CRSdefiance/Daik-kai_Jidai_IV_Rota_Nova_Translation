"""Register the reviewed 186-speech Rafael append, including the exact staged FE evidence."""
from dk4tool.patch import rafael_story_b161_b165_release_v2 as previous
from dk4tool.patch import rafael_story_b141_b160_release_v1 as common
from scripts.source_locked_derivation_v5118 import checked_text

qualification=checked_text(previous.qualification,{
    "conf['scoped_name_count']==8":"conf['scoped_name_count']==24",
    "conf['native_pages']==68":"conf['native_pages']==187",
    "conf['relative_cases']==100":"conf['relative_cases']==740",
    "conf['speech_count']==67":"conf['speech_count']==186",
    "conf['FE_count']==1":"conf['FE_count']==29",
    "len(lookup['records'])==67":"len(lookup['records'])==186",
    '(343,10,676)':'(343,4,682)',
    "==56":"==102",
    "    renderer=NdsImage.open(conf['final_dependency_ROM'])":
        """    alias=load(conf['actor8_alias'])
    require(actual['all_29_modal_pages_observed'] and actual['source_actor8_alias_proof']==conf['actor8_alias']
        and alias['retain_Arcadius_as_source_progressive_header_Eirene_as_scene_voice_and_FE_heading'],'complete staged and alias observations')
    require({r['id'] for r in alias['actors']}=={f'DK4_MES_B166_R{i:04d}' for i in (584,658,770,779)},'all four original actor-8 headers')
    require(sum(r.get('source_staged_FE',False) for r in compiled.values())==22
        and all(r['complete_native_English_display']['planned_native_row_comparison']['complete_visible_row_origins_exact']
            for r in compiled.values() if r.get('source_staged_FE')),'all 22 native staged origins')
    renderer=NdsImage.open(conf['final_dependency_ROM'])""",
})
env=dict(common.env)
exec(compile(qualification,__file__+'::exact-staged-and-alias-evidence','exec'),common.qualify_evidence.__globals__,env)
exec(compile(common.source,__file__+'::same-source-bound-transaction','exec'),env)
plan_release=env['plan_release']
