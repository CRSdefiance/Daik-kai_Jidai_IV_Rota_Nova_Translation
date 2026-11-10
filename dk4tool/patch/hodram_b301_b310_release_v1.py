"""Qualify the complete234-record append, including the proven native QA capacity repair."""
from dk4tool.patch import hodram_b281_b300_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

load=previous.load;sha=previous.sha;require=previous.require
evidence_source=checked_text(previous.evidence_source,{
    '(384,181,203)':'(234,127,107)',
    "conf['scoped_name_count']==18":"conf['scoped_name_count']==8",
    "conf['native_pages']==374":"conf['native_pages']==228",
    "conf['relative_cases']==1415":"conf['relative_cases']==190",
    'all373_ordinary_and_style_bodies_checked':'all225_ordinary_and_style_bodies_checked',
    '(325,40,610)':'(325,20,630)',
    "(242,131,conf['speech_count'])":"(73,152,conf['speech_count'])",
    'len(planes)==373':'len(planes)==225',
    "conf['FE_count']==16":"conf['FE_count']==8",'all 16 FE bodies':'all 8 FE bodies',
    "len(styles['objects'])==18 and styles['native_target_slot_cases']==144 and styles['physical_alternatives']==131":
        "len(styles['objects'])==23 and styles['native_target_slot_cases']==184 and styles['physical_alternatives']==152",
    "for r in styles['compiler_negatives'])==162":"for r in styles['compiler_negatives'])==207",
    "len(menu['menus'])==5":"len(menu['menus'])==4",
    "conf['typed_choice_count']==11":"conf['typed_choice_count']==9",
    "stored['typed_labels_checked']==11 and len(stored['typed_objects'])==5":
        "stored['typed_labels_checked']==9 and len(stored['typed_objects'])==4",
    '(38561,1,134,135,239)':'(34162,2,96,97,129)',
    'twelve_of16_FE_panels_FI_FA_seven_voice_objects_royal_pagination_andcorrected_injury_rows_observed':
        'all8_FE_FI_23_voice_objects_Mihwa_pagination_andcorrected_departure_rows_observed',
    "{(290,876,(0,)),(290,1876,(0,)),(291,1114,(0,)),(294,820,(0,)),(300,560,(0,))},'five source-bound two/three-choice menu behaviors'":
        "{(302,1226,(0,)),(302,2272,(0,)),(304,576,(0,)),(309,738,(0,))},'four source-bound two/three-choice menu behaviors'",
    "visual['actual_sheets_directly_viewed']==13":"visual['actual_sheets_directly_viewed']==10",
})
evidence_source+='''
    exitpath=conf['bounded_QA_return_proof']
    require(ready['evidence'].get(exitpath)==sha(Path(exitpath).read_bytes()),'sealed QA return proof')
    exitproof=load(exitpath)
    require(exitproof['qualified_runs']==2 and exitproof['qualified_frames']==34162
        and exitproof['all_copied_commands_andbindings_exact'] and exitproof['all97_display_pages_qualified']
        and exitproof['following_native_dialogue_observed'] and exitproof['native_stack_buffer_overflow_proven_andguarded']
        and exitproof['no_production_scene_controls_changed'] and exitproof['prior_failed_runs_preserved'],'capacity-safe representative gameplay')
    capacitypath=exitproof['capacity_proof']
    require(exitproof['evidence'].get(capacitypath)==sha(Path(capacitypath).read_bytes()),'exact native QA capacity proof')
    capacity=load(capacitypath)
    require(capacity['registered_ARM9_sha256']==native['runtime']['ARM9_sha256']
        and capacity['safe_QA_block_limit']==9216 and capacity['source_current_consumer_code_exact']
        and capacity['native_saved_LR_overwritten_by_fixture_text']
        and capacity['all_ten_production_blocks_inside_conservative_bound'],'source-bound native host allocation')
'''
evidence_env={**previous.qualify_evidence.__globals__,**globals(),'__file__':__file__}
exec(compile(evidence_source,__file__+'::same-complete-evidence-contract-new-scope-and-QA-capacity','exec'),evidence_env)
qualify_evidence=evidence_env['qualify_evidence']
source=checked_text(previous.source,{
    "'dk4-reviewed-hodram-b281-b300-release-v1'":"'dk4-reviewed-hodram-b301-b310-release-v1'",
    "len(styles['objects']) == 18":"len(styles['objects']) == 23",
})
env={**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::same-SC1-transaction-all-source-and-inverse-guards','exec'),env)
plan_release=env['plan_release']
