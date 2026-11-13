"""Register the five speech-only Rafael blocks with their sealed native evidence."""
import inspect

from dk4tool.patch import rafael_story_b141_b160_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

original = inspect.getsource(previous.qualify_evidence)
menu_start = original.index("    require(stored['typed_labels_checked']")
menu_end = original.index("    require((actual['total_frames']", menu_start)
observed_menu_start = original.index("    require({(m['block']")
observed_menu_end = original.index("    renderer=", observed_menu_start)
qualification = checked_text(original, {
    "names['all20_individual_five_gates_pass_for_public_nameplanes'] and len(names['records'])==conf['scoped_name_count']==20":
        "names['all_individual_five_gates_pass_for_public_nameplanes'] and len(names['records'])==conf['scoped_name_count']==8",
    "conf['native_pages']==558 and visual['all558_body_pages_8_captions_20_public_names_approved']":
        "conf['native_pages']==68 and visual['all_body_and_name_planes_approved']",
    "visual['all193_final_observed_pages_andfour_menus_directly_viewed']": "visual['all_actual_pages_directly_viewed']",
    "stored['total_relocated_native_relative_cases']==conf['relative_cases']==1190":
        "stored['fresh_relocated_native_relative_cases']==conf['relative_cases']==100",
    "conf['speech_count']==549": "conf['speech_count']==67",
    "conf['FE_count']==6": "conf['FE_count']==1",
    "len(lookup['records'])==549": "len(lookup['records'])==67",
    "(343,2,684)": "(343,10,676)",
    original[menu_start:menu_end]: """    require(stored['typed_labels_checked']==conf['typed_choice_count']==0
        and len(stored['typed_objects'])==len(menu['menus'])==conf['menu_count']==0
        and not stored['style_records'] and not styles['objects']
        and menu['complete_clean_current_census_proves_no_choice_objects']
        and styles['complete_clean_current_census_proves_no4100_objects'], 'exact absence of menu and style objects')
""",
    """        and actual['other_cursor_states_VM_returns_branches_andcancellation_offline_only']
        and actual['all_four_menus_default_cursor_andfollowing_fixture_speech_observed'],'bounded emulator coverage')""":
        """        and actual['original_story_branches_and_event_outcomes_unvisited']
        and actual['no_typed_menus_in_scope'] and not actual['menus'],'bounded emulator coverage')""",
    "and len({(r['id'],r['page']) for r in actual['exact_observed_pages']})==193":
        """and len({(r['id'],r['page']) for r in actual['exact_observed_pages']})==56
        and actual['observed_public_name_actor_IDs']==sorted(r['actor_ID'] for r in names['records'])""",
    original[observed_menu_start:observed_menu_end]: "",
})
env = dict(previous.env)
exec(compile(qualification, __file__ + '::scoped-reviewed-speech-evidence', 'exec'), env)
exec(compile(previous.source, __file__ + '::source-bound-transaction', 'exec'), env)
plan_release = env['plan_release']
