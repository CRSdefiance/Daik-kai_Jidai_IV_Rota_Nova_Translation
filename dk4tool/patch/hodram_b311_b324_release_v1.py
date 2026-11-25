"""Qualify the complete400-record append with preserved runtime, source keys and bounded returns."""
from dk4tool.patch import hodram_b301_b310_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

load = previous.load
sha = previous.sha
require = previous.require
evidence_source = checked_text(previous.evidence_source, {
    '(234,127,107)': '(400,175,225)',
    "conf['scoped_name_count']==8": "conf['scoped_name_count']==11",
    "conf['native_pages']==228": "conf['native_pages']==389",
    "conf['relative_cases']==190": "conf['relative_cases']==495",
    'all225_ordinary_and_style_bodies_checked': 'all387_ordinary_and_style_bodies_checked',
    '(325,20,630)': '(325,28,622)',
    "(73,152,conf['speech_count'])": "(151,236,conf['speech_count'])",
    'len(planes)==225': 'len(planes)==387',
    "conf['FE_count']==8": "conf['FE_count']==14",
    'all 8 FE bodies': 'all 14 FE bodies',
    "len(styles['objects'])==23 and styles['native_target_slot_cases']==184 and styles['physical_alternatives']==152":
        "len(styles['objects'])==38 and styles['native_target_slot_cases']==304 and styles['physical_alternatives']==236",
    "for r in styles['compiler_negatives'])==207": "for r in styles['compiler_negatives'])==342",
    "len(menu['menus'])==4": "len(menu['menus'])==6",
    "conf['typed_choice_count']==9": "conf['typed_choice_count']==13",
    "stored['typed_labels_checked']==9 and len(stored['typed_objects'])==4":
        "stored['typed_labels_checked']==13 and len(stored['typed_objects'])==6",
    '(34162,2,96,97,129)': '(57202,2,189,191,198)',
    'all8_FE_FI_23_voice_objects_Mihwa_pagination_andcorrected_departure_rows_observed':
        'all14_FE_FI_38_voice_objects_Rafael0_two_page_passages_andreturns_observed',
    "{(302,1226,(0,)),(302,2272,(0,)),(304,576,(0,)),(309,738,(0,))},'four source-bound two/three-choice menu behaviors'":
        "{(311,1086,(0,)),(311,1306,(0,)),(313,782,(0,)),(316,674,(0,)),(316,934,(0,)),(317,764,(0,))},'six source-bound two/three-choice menu behaviors'",
    "visual['actual_sheets_directly_viewed']==10": "visual['actual_sheets_directly_viewed']==17",
    "exitproof['qualified_frames']==34162": "exitproof['qualified_frames']==57202",
    'all97_display_pages_qualified': 'all191_display_pages_qualified',
})
evidence_source += '''
    require(exitproof['all14_production_blocks_inside_conservative_bound']
        and exitproof['current_production_max_target_block_bytes']<=capacity['safe_QA_block_limit'],'current production allocation bounds')
    resolutionpath='work\\\\Hodram_B311_B324_clean_20261107\\\\source_occurrence_resolution_v2.json'
    require(ready['evidence'].get(resolutionpath)==sha(Path(resolutionpath).read_bytes())
        and exitproof['evidence'].get(resolutionpath)==sha(Path(resolutionpath).read_bytes()),'sealed duplicate-command source occurrence proof')
    resolution=load(resolutionpath)
    require(resolution['duplicate_command_source_key_regression_pass']
        and resolution['all195_copied_commands_and189_selected_records_bound_to_exact_source_keys']
        and resolution['original_fixtures_ROMs_terminals_captures_andpixel_receipts_unchanged']
        and resolution['pre_run_source_selection_andfixture_ordinal_define_occurrence'],'unambiguous declared source occurrences')
    for p,h in resolution['evidence'].items():require(sha(Path(p).read_bytes())==h,'source occurrence dependency: '+p)
'''
evidence_env = {**previous.qualify_evidence.__globals__, **globals(), '__file__':__file__}
exec(compile(evidence_source,__file__+'::same-complete-evidence-guards-new-scope-and-source-occurrence-proof','exec'),evidence_env)
qualify_evidence = evidence_env['qualify_evidence']
source = checked_text(previous.source, {
    "'dk4-reviewed-hodram-b301-b310-release-v1'": "'dk4-reviewed-hodram-b311-b324-release-v1'",
    "len(styles['objects']) == 23": "len(styles['objects']) == 38",
})
env = {**previous.env, 'qualify_evidence':qualify_evidence, '__file__':__file__}
exec(compile(source,__file__+'::same-SC1-source-transaction-and-complete-inverse-guards-new-scope','exec'),env)
plan_release = env['plan_release']
