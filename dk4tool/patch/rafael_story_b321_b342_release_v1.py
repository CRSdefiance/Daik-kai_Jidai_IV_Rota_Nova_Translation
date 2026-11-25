"""Qualify the complete B321–B342 dialogue transaction over Rafael4347."""
from dk4tool.patch import rafael_story_b301_b320_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def menu_versions(proof, item):
    """Bind a grouped receipt to exactly one source-owned three-choice object."""
    if len(item['record_IDs']) == 2:
        return proof['versions']
    matches = [row for row in proof['menus']
               if (row['block'], row['source_command_offset'], row['record_IDs']) ==
               (item['block'], item['source_command_offset'], item['record_IDs'])]
    if len(matches) != 1:
        raise ValueError('Expected exactly one matching source-owned ternary menu')
    return matches[0]['versions']


evidence_source = checked_text(previous.evidence_source, {
    '(453, 397, 56)': '(556, 364, 192)',
    "len(names['records']) == 19": "len(names['records']) == 16",
    'all 19 public name and role decisions': 'all 16 public name and role decisions',
    "conf['native_pages'] == 444": "conf['native_pages'] == 552",
    "conf['relative_cases'] == 630": "conf['relative_cases'] == 650",
    "conf['speech_count'] == 442": "conf['speech_count'] == 540",
    "conf['style_count'] == 145": "conf['style_count'] == 298",
    "len(styles['objects']) == 19 and styles['native_target_slot_cases'] == 152":
        "len(styles['objects']) == 48 and styles['native_target_slot_cases'] == 384",
    "for row in styles['compiler_negatives']) == 171": "for row in styles['compiler_negatives']) == 432",
    "sum(row['kind']=='system-FE' for row in speech) == 16": "sum(row['kind']=='system-FE' for row in speech) == 20",
    '(343,40,646)': '(343,44,642)',
    "conf['menu_count'] == 5": "conf['menu_count'] == 7",
    "conf['typed_choice_count'] == 11": "conf['typed_choice_count'] == 16",
    '(17441,1,45,47,11,397)': '(24881,1,72,76,16,468)',
    "(proof['versions'] if count==2 else proof['menus'][0]['versions'])": 'menu_versions(proof, item)',
    """{(row['block'], row['source_command_offset']) for row in actual['menus']}
            == {(row['block'], row['offset']) for row in stored['typed_objects']}""":
        """{(row['block'], row['source_command_offset']) for row in actual['menus']}
            == {(row['block'], row['source_command_offset']) for row in menu['menus']}
            and {(row['block'], row['stored_command_offset']) for row in actual['menus']}
            == {(row['block'], row['offset']) for row in stored['typed_objects']}""",
    'seven_complete_style_commands_observed_under_unmodified_default_roles':
        'six_complete_style_commands_observed_under_unmodified_default_roles',
    'all_five_menu_instances_default_cursor_and_following_fixture_speech_observed':
        'all_seven_menu_instances_default_cursor_and_following_fixture_speech_observed',
})
evidence_env = {**previous.evidence_env, 'menu_versions': menu_versions, '__file__': __file__}
exec(compile(evidence_source, __file__ + '::exact-556-record-evidence', 'exec'), evidence_env)
qualify_evidence = evidence_env['qualify_evidence']
source = checked_text(previous.source, {"len(styles['objects']) == 19": "len(styles['objects']) == 48"})
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(source, __file__ + '::same-native-archive-transaction', 'exec'), env)
plan_release = env['plan_release']
