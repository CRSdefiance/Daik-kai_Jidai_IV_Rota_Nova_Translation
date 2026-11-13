"""Registered tutorial transaction with the exact B177 legacy current menu binding."""
import inspect
from types import FunctionType

from dk4tool.patch import rafael_story_b141_b160_release_v1 as previous
from scripts.rebuild_rafael_B177_B180_reviewed_v1 import compile_bound_choices
from scripts.rebuild_rafael_B177_B180_reviewed_v2 import rebuild_bound_block
from scripts.source_locked_derivation_v5118 import checked_text

qualification = checked_text(inspect.getsource(previous.qualify_evidence), {
    "lookup['stored_sha256']==sha(Path(conf['stored_native']).read_bytes())":
        "lookup['stored_sha256']==stored['speech_proof_sha256']==sha(Path(stored['speech_proof']).read_bytes())",
    "names['all20_individual_five_gates_pass_for_public_nameplanes'] and len(names['records'])==conf['scoped_name_count']==20":
        "names['all_individual_five_gates_pass_for_public_nameplanes'] and len(names['records'])==conf['scoped_name_count']==9",
    "conf['native_pages']==558 and visual['all558_body_pages_8_captions_20_public_names_approved']":
        "conf['native_pages']==186 and visual['all_body_caption_andname_planes_approved']",
    "visual['all193_final_observed_pages_andfour_menus_directly_viewed']": "visual['all_actual_pages_andmenus_directly_viewed']",
    "stored['total_relocated_native_relative_cases']==conf['relative_cases']==1190":
        "stored['fresh_relocated_native_relative_cases']==conf['relative_cases']==290",
    "conf['speech_count']==549": "conf['speech_count']==175",
    "conf['FE_count']==6": "conf['FE_count']==1",
    "len(lookup['records'])==549": "len(lookup['records'])==175",
    "(343,2,684)": "(343,8,678)",
    """        require((proof['native_provider_alignments'],proof['bridged_modal_returns'],proof['complete_English_caption_style_planes'])==(6,18,8),
            'native menu alignments, styles and returns')""":
        """        require((proof['native_provider_alignments'],proof['bridged_modal_returns'])==(6,18),
            'native menu alignments and returns')
        require(sum(row['version']=='reviewed-English' for row in proof['records'])==4, 'all reviewed caption styles')
        expected_omissions=2 if obj['block']==178 else 0
        require(len(proof['omitted_corrupt_baseline_ASCII_planes'])==expected_omissions
            and proof['complete_English_caption_style_planes']==8-2*expected_omissions,'exact scope of corrupt current baseline exceptions')
        require(proof['exact_legacy_current_slot_exception']==(obj['block']==177), 'exact B177 legacy current slot only')""",
    "and len({(r['id'],r['page']) for r in actual['exact_observed_pages']})==193":
        """and len({(r['id'],r['page']) for r in actual['exact_observed_pages']})==115
        and actual['observed_public_name_actor_IDs']==sorted(r['actor_ID'] for r in names['records'])""",
})
env = dict(previous.env)
exec(compile(qualification,__file__+'::same-evidence-with-exact-tutorial-coverage','exec'),
    {**previous.qualify_evidence.__globals__}, env)
objects = env['compound_objects']
env['compound_objects'] = FunctionType(objects.__code__,{**objects.__globals__,'compile_choices':compile_bound_choices})
env['rebuild_block'] = rebuild_bound_block
exec(compile(previous.source,__file__+'::same-registered-transaction-and-scoped-legacy-input','exec'),env)
plan_release = env['plan_release']
