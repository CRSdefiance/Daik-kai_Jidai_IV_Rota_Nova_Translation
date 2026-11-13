"""Qualify the complete B301–B320 dialogue transaction over Rafael3894."""
from dk4tool.patch import rafael_story_b281_b300_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


evidence_source = checked_text(previous.evidence_source, {
    '(245, 202, 43)': '(453, 397, 56)',
    "len(names['records']) == 17": "len(names['records']) == 19",
    'all 17 public name and role decisions': 'all 19 public name and role decisions',
    "conf['native_pages'] == 248": "conf['native_pages'] == 444",
    "conf['relative_cases'] == 800": "conf['relative_cases'] == 630",
    "conf['speech_count'] == 240": "conf['speech_count'] == 442",
    "conf['style_count'] == 76": "conf['style_count'] == 145",
    "len(styles['objects']) == 11 and styles['native_target_slot_cases'] == 88":
        "len(styles['objects']) == 19 and styles['native_target_slot_cases'] == 152",
    "for row in styles['compiler_negatives']) == 99": "for row in styles['compiler_negatives']) == 171",
    "sum(row['kind']=='system-FE' for row in speech) == 17": "sum(row['kind']=='system-FE' for row in speech) == 16",
    "conf['menu_count'] == 2": "conf['menu_count'] == 5",
    "conf['typed_choice_count'] == 5": "conf['typed_choice_count'] == 11",
    '(12881,1,27,31,5,213)': '(17441,1,45,47,11,397)',
    'nine_complete_style_commands_observed_under_unmodified_default_roles':
        'seven_complete_style_commands_observed_under_unmodified_default_roles',
    'all_two_menu_instances_default_cursor_and_following_fixture_speech_observed':
        'all_five_menu_instances_default_cursor_and_following_fixture_speech_observed',
})
evidence_env = {**previous.evidence_env, '__file__': __file__}
exec(compile(evidence_source, __file__ + '::exact-453-record-evidence', 'exec'), evidence_env)
qualify_evidence = evidence_env['qualify_evidence']
source = checked_text(previous.source, {"len(styles['objects']) == 11": "len(styles['objects']) == 19"})
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(source, __file__ + '::same-native-archive-transaction', 'exec'), env)
plan_release = env['plan_release']
