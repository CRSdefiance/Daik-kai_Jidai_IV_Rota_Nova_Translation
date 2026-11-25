"""Qualify the complete reviewed SC1 successor, preserving credited B237 and every prior layer."""
import inspect
from pathlib import Path
from dk4tool.patch import hodram_b211_b230_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

load=previous.load;sha=previous.sha;require=previous.require
evidence_source=inspect.getsource(previous.qualify_evidence)
qa_start=evidence_source.index('    # One grammatical soft-wrap preference')
qa_end=evidence_source.index("    renderer=",qa_start)
assert evidence_source[qa_start:qa_end].count('DK4_MES_B229_R0036')==1
evidence_source=checked_text(evidence_source,{
    '(277,170,107)':'(225,115,110)',
    "conf['scoped_name_count']==23":"conf['scoped_name_count']==19",
    "conf['native_pages']==284":"conf['native_pages']==228",
    "conf['relative_cases']==150":"conf['relative_cases']==170",
    'all270_ordinary_and_style_bodies_checked':'all223_ordinary_and_style_bodies_checked',
    '(325,38,612)':'(325,36,614)',
    "(241,29,conf['speech_count'])":"(209,14,conf['speech_count'])",
    "len(planes)==270":"len(planes)==223",
    "len(styles['objects'])==4 and styles['native_target_slot_cases']==32 and styles['physical_alternatives']==29":
        "len(styles['objects'])==2 and styles['native_target_slot_cases']==16 and styles['physical_alternatives']==14",
    "for r in styles['compiler_negatives'])==36":"for r in styles['compiler_negatives'])==18",
    "len(menu['menus'])==3":"len(menu['menus'])==1",
    "conf['typed_choice_count']==7":"conf['typed_choice_count']==2",
    "stored['typed_labels_checked']==7 and len(stored['typed_objects'])==3":"stored['typed_labels_checked']==2 and len(stored['typed_objects'])==1",
    '(23441,1,65,74,205)':'(21521,1,63,68,160)',
    'all_four_FE_panels_FI_expansion_four_voice_objects_andrepresentative_pagination_observed':
        'all_four_FE_panels_FI_expansions_two_voice_objects_andrepresentative_pagination_observed',
    "=={(216,64,(0,)),(216,230,(0,))},'two distinct source-bound menu behaviors')":
        "=={(243,674,(0,))},'source-bound two-choice menu behavior')",
    "    require(not actual['repeated_B224_yes_no_menu']['complete_occurrence_highlight_background_credit']\n        and actual['repeated_B224_yes_no_menu']['stored_source_bytes_andnative_providers_exact'],'no duplicate-pixel occurrence overclaim')":
        """    model=load(actual['cursor_model_qualification'])
    require(model['all6_pixel_andcursor_mutations_rejected'] and model['no_ROM_orcapture_mutation'],'complete menu glyph/background negative cases')""",
    "visual['actual_sheets_directly_viewed']==14":"visual['actual_sheets_directly_viewed']==13",
    evidence_source[qa_start:qa_end]:"""    layout=load(conf['plan'])
    require(all(not r.get('qa_waivers') for r in doc['records']),'no heuristic waivers')
    require(all('unmodified_base_QA' not in r and not any(i['severity'] in ('warning','error') for i in r['base_QA']['issues']) for r in layout['records']),'all original QA diagnostics pass')
""",
})
evidence_env={**previous.qualify_evidence.__globals__,**globals(),'__file__':__file__}
exec(compile(evidence_source,__file__+'::same-full-research-contract-exact-new-scope','exec'),evidence_env)
qualify_evidence=evidence_env['qualify_evidence']
source=checked_text(previous.source,{
    "'dk4-reviewed-hodram-b211-b230-release-v1'":"'dk4-reviewed-hodram-b231-b250-release-v1'",
    "len(styles['objects']) == 4":"len(styles['objects']) == 2",
})
env={**previous.env,'qualify_evidence':qualify_evidence,'__file__':__file__}
exec(compile(source,__file__+'::same-complete-SC1-transaction-preserved-inverses','exec'),env)
plan_release=env['plan_release']
